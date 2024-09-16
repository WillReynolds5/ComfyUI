import json
from urllib import request, parse
import random

#This is the ComfyUI api prompt format.

#If you want it for a specific workflow you can "enable dev mode options"
#in the settings of the UI (gear beside the "Queue Size: ") this will enable
#a button on the UI to save workflows in api format.

#keep in mind ComfyUI is pre alpha software so this format will change a bit.

#this is the one for the default workflow

def gen_prompt(pos_prompt, neg_prompt, seed=None):
    if seed is None:
        seed = random.randint(0, 1000000)

    prompt_text = """{
      "1": {
        "inputs": {
          "ckpt_name": "RealVisXL_V4.0.safetensors"
        },
        "class_type": "CheckpointLoaderSimple",
        "_meta": {
          "title": "Load Checkpoint"
        }
      },
      "3": {
        "inputs": {
          "ipadapter_file": "ip-adapter-plus-face_sdxl_vit-h.safetensors"
        },
        "class_type": "IPAdapterModelLoader",
        "_meta": {
          "title": "Load IPAdapter Model"
        }
      },
      "4": {
        "inputs": {
          "clip_name": "sd1.5/BEN_USE_THIS/model.safetensors"
        },
        "class_type": "CLIPVisionLoader",
        "_meta": {
          "title": "Load CLIP Vision"
        }
      },
      "5": {
        "inputs": {
          "weight": 0.8,
          "noise": 0,
          "weight_type": "original",
          "start_at": 0,
          "end_at": 1,
          "unfold_batch": false,
          "ipadapter": [
            "3",
            0
          ],
          "clip_vision": [
            "4",
            0
          ],
          "image": [
            "6",
            0
          ],
          "model": [
            "1",
            0
          ]
        },
        "class_type": "IPAdapterApply",
        "_meta": {
          "title": "Apply IPAdapter"
        }
      },
      "6": {
        "inputs": {
          "image": "ComfyUI_temp_aitqc_00001_ (1).png",
          "upload": "image"
        },
        "class_type": "LoadImage",
        "_meta": {
          "title": "Load Image"
        }
      },
      "7": {
        "inputs": {
          "text": "",
          "clip": [
            "1",
            1
          ]
        },
        "class_type": "CLIPTextEncode",
        "_meta": {
          "title": "CLIP Text Encode (Prompt)"
        }
      },
      "8": {
        "inputs": {
          "text": "",
          "clip": [
            "1",
            1
          ]
        },
        "class_type": "CLIPTextEncode",
        "_meta": {
          "title": "CLIP Text Encode (Prompt)"
        }
      },
      "9": {
        "inputs": {
          "seed": [
            "17",
            0
          ],
          "steps": 25,
          "cfg": 6,
          "sampler_name": "dpmpp_2m_sde_gpu",
          "scheduler": "karras",
          "denoise": 1,
          "model": [
            "5",
            0
          ],
          "positive": [
            "7",
            0
          ],
          "negative": [
            "8",
            0
          ],
          "latent_image": [
            "10",
            0
          ]
        },
        "class_type": "KSampler",
        "_meta": {
          "title": "KSampler"
        }
      },
      "10": {
        "inputs": {
          "width": 1024,
          "height": 1024,
          "batch_size": 1
        },
        "class_type": "EmptyLatentImage",
        "_meta": {
          "title": "Empty Latent Image"
        }
      },
      "11": {
        "inputs": {
          "samples": [
            "9",
            0
          ],
          "vae": [
            "1",
            2
          ]
        },
        "class_type": "VAEDecode",
        "_meta": {
          "title": "VAE Decode"
        }
      },
      "15": {
        "inputs": {
          "images": [
            "11",
            0
          ]
        },
        "class_type": "PreviewImage",
        "_meta": {
          "title": "Preview Image"
        }
      },
      "17": {
        "inputs": {
          "seed": 15
        },
        "class_type": "Seed (rgthree)",
        "_meta": {
          "title": "Seed (rgthree)"
        }
      },
      "18": {
        "inputs": {
          "enabled": true,
          "swap_model": "inswapper_128.onnx",
          "facedetection": "retinaface_resnet50",
          "face_restore_model": "GFPGANv1.4.pth",
          "face_restore_visibility": 1,
          "codeformer_weight": 1,
          "detect_gender_source": "female",
          "detect_gender_input": "female",
          "source_faces_index": "0",
          "input_faces_index": "0",
          "console_log_level": 1,
          "source_image": [
            "6",
            0
          ],
          "input_image": [
            "11",
            0
          ]
        },
        "class_type": "ReActorFaceSwap",
        "_meta": {
          "title": "ReActor - Fast Face Swap"
        }
      },
      "21": {
        "inputs": {
          "images": [
            "18",
            0
          ]
        },
        "class_type": "PreviewImage",
        "_meta": {
          "title": "Preview Image"
        }
      },
      "24": {
        "inputs": {
          "filename_prefix": "mia/mia",
          "images": [
            "18",
            0
          ]
        },
        "class_type": "SaveImage",
        "_meta": {
          "title": "Save Image"
        }
      }
    }
    """
    # load json and format dict
    parsed_prompt = json.loads(prompt_text)
    parsed_prompt["7"]["inputs"]["text"] = pos_prompt
    parsed_prompt["8"]["inputs"]["text"] = neg_prompt
    parsed_prompt["17"]["inputs"]["seed"] = seed
    return parsed_prompt

def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req = request.Request("http://127.0.0.1:8188/prompt", data=data)
    resp = request.urlopen(req)
    print(resp.read())

i

positive_prompt = "(hyper realistic animation), women standing on beach"
negative_prompt = "deformed face, disfigured eyes, deformed breasts"

prompt = gen_prompt(positive_prompt, negative_prompt)

queue_prompt(prompt)
