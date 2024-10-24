import os
import shutil
import base64
import requests
from PIL import Image
import json
import random
import re
from tqdm import tqdm

def parse_answer(response_content):
    # Extract the answer from the <answer> tags using regular expressions
    match = re.search(r'<answer>(.*?)</answer>', response_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return "No caption found"

def main():
    # Define the source and destination directories
    source_directory = "/home/mclean/Documents/GitHub/ComfyUI/images"
    destination_directory = "/home/mclean/Pictures/captioned_characters_elitebabe"

    # Ensure the destination directory exists
    os.makedirs(destination_directory, exist_ok=True)


    variant_1 = """# Examples
Here are some great examples, separate each part of the description with a comma:
- “sitting on a park bench, wearing a white bra and nothing on the bottom, beautiful park background, vagina showing and breast cleavage, fingering vagina”
- “backside shot of butt sticking out, completely nude, plain grey background, showing butt and vulva, no face in shot”
- "Standing in front of a window, wearing a bikini top and high heels, modern cityscape background, breasts and legs showing"
- "Lying on a bed, wearing lace lingerie, dimly lit bedroom background, breasts and lower body showing."
- "Two women lying on a bed, wearing lace lingerie, dimly lit bedroom background, breasts and lower body showing, each licking the other's pussy."
- "Sitting on a yoga mat, wearing sports bra and shorts, outdoor beach background, upper body and legs showing, fingers rubbing vagina."
- "Standing in a bathroom, wearing a bathrobe, minimalist bathroom background, only lower legs and feet showing and lots of cleavage, seductive expression."
- "Close-up of a vagina, with fingers spreading the lips, no face in shot, vagina showing"
"""

    variant_2 = """# Examples
Here are some great examples, give an extremely detailed description of the image:
- "Sitting on a park bench, wearing a white bra and nothing on the bottom, with a beautiful park background. Vagina and breast cleavage are showing."
- "In a backside shot with butt sticking out, completely nude, against a plain grey background. Butt and vulva are showing, with no face in the shot."
- "Standing in front of a window, wearing a bikini top and high heels, with a modern cityscape background. Breasts and legs are showing."
- "Two women lying on a bed, wearing lace lingerie, in a dimly lit bedroom background. Breasts and lower body are showing, each is licking the other's pussy."
- "Kneeling on all fours, completely nude, against a plain white background. Buttocks and back are showing, with her fingers in her vagina."
- "Sitting on a yoga mat, wearing a sports bra and shorts, with an outdoor beach background. Upper body and legs are showing"
- "Close-up of a vagina, with fingers spreading the lips, no face in shot, vagina showing"
"""


    caption_prmopt_OG = """# Task
You are an expert AI image labeler that creates descriptions of NSFW images. Label the image using the following guidelines, examples, and filename. Examine the image carefully.
Focus carefully on the following attributes:
1. character pose
2. outfit
3. background setting
4. what private parts are showing (use words like vagina, pussy, breasts, cleavage, ass, butt, anus.)

{variant}

* Begin by enclosing all thoughts within <thinking> tags.

* Explore multiple solutions individually if possible, comparing approaches in reflections.

* Use thoughts as a scratchpad, writing out all ideas and reasoning explicitly.

* Synthesize the final answer within <answer> tags. Only output the description here, nothing else.

Here is an example output format:
<thinking>
... scratchpad here ...
</thinking>
<answer>
... description here ...
</answer>
"""

    # Initialize a counter for the number of images processed
    image_count = 0

    # Get a list of image filenames
    image_filenames = [filename for filename in os.listdir(source_directory) if filename.endswith(('.png', '.jpg', '.jpeg'))]

    # Shuffle the list of image filenames
    random.shuffle(image_filenames)

    # Iterate over each file in the shuffled list with a progress bar
    for filename in tqdm(image_filenames, total=1000, desc="Processing Images"):
        if filename.endswith(('.png', '.jpg', '.jpeg')):  # Check for image files
            # Increment the image counter
            image_count += 1

            # Break the loop if 1000 images have been processed
            if image_count > 1000:
                break

            image_path = os.path.join(source_directory, filename)
            
            # Open the image
            with open(image_path, "rb") as image_file:
                # Convert the image to base64
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')

            # Format the description prompt
            variant = random.choice([variant_1, variant_2])
            caption_prompt = caption_prmopt_OG.format(filename=filename, variant=variant)
            # Prepare the API request payload
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer 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",
                },
                data=json.dumps({
                    "model": "qwen/qwen-2-vl-72b-instruct",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": caption_prompt
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                                }
                            ]
                        },
                        {
                            "role": "assistant",
                            "content": {
                                "type": "text",
                                "text": "<thinking>"
                            }
                        }
                    ]
                })
            )
            
            # Parse the response to extract the caption
            if response.status_code == 200:
                response_content = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
                caption = parse_answer(response_content)
                
                # Skip the image if no caption is found
                if caption == "No caption found":
                    print(f"Skipping {filename} because no caption was found")
                    print(f"Response content: {response_content}")
                    continue
                
                # Copy the image to the destination directory
                shutil.copy(image_path, destination_directory)
                
                # Create a caption file with the same name as the image
                caption_filename = os.path.splitext(filename)[0] + ".txt"
                caption_path = os.path.join(destination_directory, caption_filename)
                
                # Write the caption to the caption file
                with open(caption_path, "w") as caption_file:
                    caption_file.write(caption)
                
                print(f"Processed {filename}: Caption saved to {caption_filename}")
            else:
                print(f"Failed to get caption for {filename}. Status Code: {response.status_code}")

if __name__ == "__main__":
    main()
