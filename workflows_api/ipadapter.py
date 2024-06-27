workflow = {
  "1": {
    "inputs": {
      "text": [
        "34",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "SDXL -ve Prompt"
    }
  },
  "2": {
    "inputs": {
      "width": [
        "19",
        0
      ],
      "height": [
        "19",
        1
      ],
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Empty Latent Image"
    }
  },
  "5": {
    "inputs": {
      "image": "Mia_face2 (16).png",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Face Image"
    }
  },
  "8": {
    "inputs": {
      "ckpt_name": "RealVisXL_V3.0.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load SDXL Checkpoint"
    }
  },
  "10": {
    "inputs": {
      "clip_name": "sd1.5/BEN_USE_THIS/model.safetensors"
    },
    "class_type": "CLIPVisionLoader",
    "_meta": {
      "title": "Load CLIP Vision (SD 1.5!)"
    }
  },
  "18": {
    "inputs": {
      "upscale_method": "nearest-exact",
      "megapixels": 1,
      "image": [
        "62",
        0
      ]
    },
    "class_type": "ImageScaleToTotalPixels",
    "_meta": {
      "title": "ImageScaleToTotalPixels"
    }
  },
  "19": {
    "inputs": {
      "image": [
        "18",
        0
      ]
    },
    "class_type": "GetImageSize",
    "_meta": {
      "title": "GetImageSize"
    }
  },
  "34": {
    "inputs": {
      "text_positive": "leads spread showing off vagina, lying on hotel bed, (completely naked), perfect body, perfect legs, perfect vagina",
      "text_negative": "deformed body, deformed legs, deformed vagina",
      "style": "base",
      "log_prompt": "No",
      "style_positive": True,
      "style_negative": True
    },
    "class_type": "SDXLPromptStyler",
    "_meta": {
      "title": "SDXL Prompt Styler"
    }
  },
  "35": {
    "inputs": {
      "width": 1024,
      "height": 1024,
      "crop_w": 0,
      "crop_h": 0,
      "target_width": 1024,
      "target_height": 1024,
      "text_g": [
        "34",
        0
      ],
      "text_l": "leads spread showing off vagina, lying on hotel bed"
    },
    "class_type": "CLIPTextEncodeSDXL",
    "_meta": {
      "title": "SDXL Encode +ve Prompt"
    }
  },
  "43": {
    "inputs": {
      "stop_at_clip_layer": -2,
      "clip": [
        "8",
        1
      ]
    },
    "class_type": "CLIPSetLastLayer",
    "_meta": {
      "title": "CLIP Set Last Layer"
    }
  },
  "44": {
    "inputs": {
      "b1": 1.39,
      "b2": 1.22,
      "s1": 1.05,
      "s2": 0.25,
      "model": [
        "87",
        0
      ]
    },
    "class_type": "FreeU_V2",
    "_meta": {
      "title": "FreeU_V2 (IPA)"
    }
  },
  "45": {
    "inputs": {
      "add_noise": "disable",
      "steps": 25,
      "cfg": 7.5,
      "sampler_name": "euler_ancestral",
      "scheduler": "normal",
      "start_at_step": 0,
      "end_at_step": 10000,
      "return_with_leftover_noise": "enable",
      "latent_image": [
        "2",
        0
      ]
    },
    "class_type": "KSamplerAdvanced",
    "_meta": {
      "title": "KSampler (IPA)"
    }
  },
  "46": {
    "inputs": {
      "samples": [
        "45",
        0
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "47": {
    "inputs": {
      "images": [
        "46",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "55": {
    "inputs": {
      "steps": 20,
      "cfg": 8,
      "sampler_name": "euler_ancestral",
      "scheduler": "normal",
      "denoise": 0.54,
      "latent_image": [
        "91",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "56": {
    "inputs": {
      "samples": [
        "55",
        0
      ],
      "vae": [
        "8",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "62": {
    "inputs": {
      "image": "0016-12_w400 (4).jpg",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Pose Image"
    }
  },
  "64": {
    "inputs": {
      "detect_hand": "enable",
      "detect_body": "enable",
      "detect_face": "enable",
      "resolution": 1024,
      "bbox_detector": "yolox_l.onnx",
      "pose_estimator": "dw-ll_ucoco_384.onnx"
    },
    "class_type": "DWPreprocessor",
    "_meta": {
      "title": "DWPose Estimator"
    }
  },
  "65": {
    "inputs": {
      "crop_padding_factor": 0.2,
      "cascade_xml": "haarcascade_profileface.xml",
      "image": [
        "5",
        0
      ]
    },
    "class_type": "Image Crop Face",
    "_meta": {
      "title": "Image Crop Face"
    }
  },
  "66": {
    "inputs": {
      "upscale_method": "nearest-exact",
      "megapixels": 1,
      "image": [
        "62",
        0
      ]
    },
    "class_type": "ImageScaleToTotalPixels",
    "_meta": {
      "title": "Scale Pose"
    }
  },
  "67": {
    "inputs": {
      "strength": 1,
      "start_percent": 0,
      "end_percent": 1,
      "positive": [
        "35",
        0
      ],
      "negative": [
        "1",
        0
      ],
      "control_net": [
        "71",
        0
      ],
      "image": [
        "64",
        0
      ]
    },
    "class_type": "ControlNetApplyAdvanced",
    "_meta": {
      "title": "Apply ControlNet (Advanced)"
    }
  },
  "71": {
    "inputs": {
      "control_net_name": "sd1.5/thibaud_xl_openpose_256lora.safetensors"
    },
    "class_type": "ControlNetLoader",
    "_meta": {
      "title": "Load SDXL Pose ControlNet"
    }
  },
  "72": {
    "inputs": {
      "images": [
        "64",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "73": {
    "inputs": {
      "seed": 787952265469233
    },
    "class_type": "Seed Everywhere",
    "_meta": {
      "title": "Seed Everywhere"
    }
  },
  "74": {
    "inputs": {
      "VAE": [
        "8",
        2
      ]
    },
    "class_type": "Anything Everywhere",
    "_meta": {
      "title": "Anything Everywhere - VAE"
    }
  },
  "75": {
    "inputs": {
      "images": [
        "65",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "76": {
    "inputs": {},
    "class_type": "Prompts Everywhere",
    "_meta": {
      "title": "Prompts Everywhere"
    }
  },
  "77": {
    "inputs": {
      "control_net_name": "sd1.5/control-lora-depth-rank128.safetensors"
    },
    "class_type": "ControlNetLoader",
    "_meta": {
      "title": "Load SDXL Depth ControlNet"
    }
  },
  "80": {
    "inputs": {
      "images": [
        "84",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "82": {
    "inputs": {
      "MODEL": [
        "44",
        0
      ]
    },
    "class_type": "Anything Everywhere",
    "_meta": {
      "title": "Anything Everywhere - IPA Model"
    }
  },
  "84": {
    "inputs": {
      "resolution": 1024
    },
    "class_type": "Zoe-DepthMapPreprocessor",
    "_meta": {
      "title": "Zoe Depth Map"
    }
  },
  "85": {
    "inputs": {
      "IMAGE": [
        "66",
        0
      ]
    },
    "class_type": "Anything Everywhere",
    "_meta": {
      "title": "Anything Everywhere"
    }
  },
  "87": {
    "inputs": {
      "weight": 0.75,
      "noise": 0.99,
      "weight_type": "original",
      "start_at": 0,
      "end_at": 1,
      "unfold_batch": False,
      "ipadapter": [
        "88",
        0
      ],
      "clip_vision": [
        "10",
        0
      ],
      "image": [
        "90",
        0
      ],
      "model": [
        "8",
        0
      ]
    },
    "class_type": "IPAdapterApply",
    "_meta": {
      "title": "Apply IPAdapter"
    }
  },
  "88": {
    "inputs": {
      "ipadapter_file": "ip-adapter-plus-face_sdxl_vit-h.safetensors"
    },
    "class_type": "IPAdapterModelLoader",
    "_meta": {
      "title": "Load IPAdapter Model"
    }
  },
  "90": {
    "inputs": {
      "interpolation": "LANCZOS",
      "crop_position": "center",
      "sharpening": 0,
      "image": [
        "65",
        0
      ]
    },
    "class_type": "PrepImageForClipVision",
    "_meta": {
      "title": "Prepare Image For Clip Vision"
    }
  },
  "91": {
    "inputs": {
      "version": "SDXL",
      "upscale": 1.5,
      "latent": [
        "45",
        0
      ]
    },
    "class_type": "NNLatentUpscale",
    "_meta": {
      "title": "NNLatentUpscale"
    }
  },
  "92": {
    "inputs": {
      "CLIP": [
        "43",
        0
      ]
    },
    "class_type": "Anything Everywhere",
    "_meta": {
      "title": "Anything Everywhere"
    }
  },
  "94": {
    "inputs": {
      "enabled": True,
      "swap_model": "inswapper_128.onnx",
      "facedetection": "retinaface_resnet50",
      "face_restore_model": "codeformer.pth",
      "face_restore_visibility": 0.1,
      "codeformer_weight": 0,
      "detect_gender_source": "female",
      "detect_gender_input": "female",
      "source_faces_index": "0",
      "input_faces_index": "0",
      "console_log_level": 1,
      "source_image": [
        "5",
        0
      ],
      "input_image": [
        "56",
        0
      ]
    },
    "class_type": "ReActorFaceSwap",
    "_meta": {
      "title": "ReActor - Fast Face Swap"
    }
  },
  "96": {
    "inputs": {
      "images": [
        "94",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "97": {
    "inputs": {
      "facedetection": "retinaface_resnet50",
      "codeformer_fidelity": 1,
      "facerestore_model": [
        "98",
        0
      ],
      "image": [
        "94",
        0
      ]
    },
    "class_type": "FaceRestoreCFWithModel",
    "_meta": {
      "title": "FaceRestoreCFWithModel"
    }
  },
  "98": {
    "inputs": {
      "model_name": "codeformer.pth"
    },
    "class_type": "FaceRestoreModelLoader",
    "_meta": {
      "title": "FaceRestoreModelLoader"
    }
  },
  "99": {
    "inputs": {
      "filename_prefix": "2024-02-26/faceswapped",
      "images": [
        "97",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  },
  "100": {
    "inputs": {
      "images": [
        "56",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  }
}