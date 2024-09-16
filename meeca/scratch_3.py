import json
import requests
import random

def gen_prompt(pos_prompt, neg_prompt, background_prompt, face_image, pose_image, seed=None):
    if seed is None:
        seed = random.randint(0, 1_000_000)

    # Load the character generation JSON file
    with open('meeca/charactergen.json', 'r') as file:
        character_gen_data = json.load(file)

    # Modify the positive, negative, and background prompts
    character_gen_data["17"]["inputs"]["text"] = pos_prompt
    character_gen_data["18"]["inputs"]["text"] = neg_prompt
    character_gen_data["86"]["inputs"]["text"] = background_prompt  # Added background prompt

    # Set the seed
    character_gen_data["19"]["inputs"]["seed"] = seed

    # Set the grounding dino prompt to 'women'
    character_gen_data["14"]["inputs"]["prompt"] = "women"

    # Set the image paths for face and pose images
    character_gen_data["11"]["inputs"]["image"] = pose_image
    character_gen_data["29"]["inputs"]["image"] = face_image

    return character_gen_data

def queue_prompt(prompt):
    payload = {"prompt": prompt}
    data = json.dumps(payload)
    headers = {'Content-Type': 'application/json'}
    response = requests.post("http://174.52.227.249:8188/prompt", data=data, headers=headers)
    print(response.text)

if __name__ == "__main__":
    # Set default positive and negative prompts
    positive_prompt = "((masterpiece, best quality)), award winning, 4k, 8k, gorgeous women, super model"
    negative_prompt = "text, watermark, underexposed, ugly, jpeg"

    # Paths to the face and pose images
    face_image = "path/to/face_image.jpg"
    pose_image = "path/to/pose_image.jpg"

    # Generate the prompt with default values
    prompt = gen_prompt(positive_prompt, negative_prompt, face_image, pose_image)

    # Send the workflow to the API
    queue_prompt(prompt)
