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
      "filename_prefix": {id},
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
    pass

def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req = request.Request("http://127.0.0.1:8188/prompt", data=data)
    return request.urlopen(req)


if __name__ == "__main__":
    positive = "white women"
    negative = "deformed body and face"
    print(comfyui_inference(positive, negative))