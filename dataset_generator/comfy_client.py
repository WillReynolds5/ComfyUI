import random
import json
from urllib import request

def comfyui_inference_basic(positive_prompt, negative_prompt, id):

    random_seed = random.randint(0, 1000000000)
    prompt = """
{{
  "3": {{
    "inputs": {{
      "seed": {random_seed},
      "steps": 20,
      "cfg": 8,
      "sampler_name": "euler",
      "scheduler": "normal",
      "denoise": 1,
      "model": [
        "4",
        0
      ],
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "5",
        0
      ]
    }},
    "class_type": "KSampler",
    "_meta": {{
      "title": "KSampler"
    }}
  }},
  "4": {{
    "inputs": {{
      "ckpt_name": "BEN_USE_THIS/sd_xl_base_1.0.safetensors"
    }},
    "class_type": "CheckpointLoaderSimple",
    "_meta": {{
      "title": "Load Checkpoint"
    }}
  }},
  "5": {{
    "inputs": {{
      "width": 1024,
      "height": 1024,
      "batch_size": 1
    }},
    "class_type": "EmptyLatentImage",
    "_meta": {{
      "title": "Empty Latent Image"
    }}
  }},
  "6": {{
    "inputs": {{
      "text": "{positive}",
      "clip": [
        "4",
        1
      ]
    }},
    "class_type": "CLIPTextEncode",
    "_meta": {{
      "title": "CLIP Text Encode (Prompt)"
    }}
  }},
  "7": {{
    "inputs": {{
      "text": "{negative}",
      "clip": [
        "4",
        1
      ]
    }},
    "class_type": "CLIPTextEncode",
    "_meta": {{
      "title": "CLIP Text Encode (Prompt)"
    }}
  }},
  "8": {{
    "inputs": {{
      "samples": [
        "3",
        0
      ],
      "vae": [
        "4",
        2
      ]
    }},
    "class_type": "VAEDecode",
    "_meta": {{
      "title": "VAE Decode"
    }}
  }},
  "9": {{
    "inputs": {{
      "filename_prefix": "{id}",
      "images": [
        "8",
        0
      ]
    }},
    "class_type": "SaveImage",
    "_meta": {{
      "title": "Save Image",
    }}
  }}
}}""".format(positive=positive_prompt, negative=negative_prompt, random_seed=random_seed, id=id)
    json_prompt = json.loads(prompt)
    return queue_prompt(json_prompt)


def comfyui_inference_ipadpater():

    prompt = """
{
  "1": {
    "inputs": {
      "ckpt_name": "RealVisXL_V3.0.safetensors"
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
      "image": "0c33596bc55c4f4ea4e973ab4f8071a3_00001_.png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "7": {
    "inputs": {
      "text": "standing in the kitchen with back on a fridge",
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
      "seed": -1
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
      "face_restore_model": "codeformer.pth",
      "face_restore_visibility": 1,
      "codeformer_weight": 1,
      "detect_gender_source": "no",
      "detect_gender_input": "no",
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
  "22": {
    "inputs": {
      "facedetection": "retinaface_resnet50",
      "codeformer_fidelity": 1,
      "facerestore_model": [
        "23",
        0
      ],
      "image": [
        "18",
        0
      ]
    },
    "class_type": "FaceRestoreCFWithModel",
    "_meta": {
      "title": "FaceRestoreCFWithModel"
    }
  },
  "23": {
    "inputs": {
      "model_name": "codeformer.pth"
    },
    "class_type": "FaceRestoreModelLoader",
    "_meta": {
      "title": "FaceRestoreModelLoader"
    }
  },
  "24": {
    "inputs": {
      "filename_prefix": "2024-02-11/faceswapped",
      "images": [
        "22",
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

def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req = request.Request("http://127.0.0.1:8188/prompt", data=data)
    return request.urlopen(req)


if __name__ == "__main__":
    positive = "white women"
    negative = "deformed body and face"
    print(comfyui_inference(positive, negative))