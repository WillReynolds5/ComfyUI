import os
import shutil
import base64
import json
import random
import re
import asyncio
import aiohttp
from tqdm.asyncio import tqdm
import aiofiles
from PIL import Image


# Define the variants and prompt at the global scope
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

async def parse_answer(response_content):
    match = re.search(r'<answer>(.*?)</answer>', response_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return "No caption found"

async def process_image(session, source_directory, destination_directory, filename):
    try:
        image_path = os.path.join(source_directory, filename)
        caption_filename = os.path.splitext(filename)[0] + ".txt"
        caption_path = os.path.join(destination_directory, caption_filename)

        # Check if the caption file already exists
        if os.path.exists(caption_path):
            print(f"Skipping {filename} because caption already exists")
            return False

        # Check image dimensions
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                if width < 900 or height < 900:
                    print(f"Skipping {filename} due to small dimensions ({width}x{height})")
                    return False
        except Exception as e:
            print(f"Failed to check dimensions for {filename}: {str(e)}")
            return False

        # Open the image asynchronously
        try:
            async with aiofiles.open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(await image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Failed to read image {filename}: {str(e)}")
            return False

        variant = random.choice([variant_1, variant_2])
        caption_prompt = caption_prmopt_OG.format(filename=filename, variant=variant)

        # Send the request asynchronously
        try:
            async with session.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer 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",
                },
                json={
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
                }
            ) as response:
                if response.status == 200:
                    response_content = await response.json()
                    caption = await parse_answer(response_content.get('choices', [{}])[0].get('message', {}).get('content', ''))
                    
                    if caption == "No caption found":
                        print(f"Skipping {filename} because no caption was found")
                        return False
                    
                    shutil.copy(image_path, destination_directory)
                    
                    async with aiofiles.open(caption_path, "w") as caption_file:
                        await caption_file.write(caption)
                    
                    return True
                else:
                    print(f"Failed to get caption for {filename}. Status Code: {response.status}")
                    return False
        except Exception as e:
            print(f"API request failed for {filename}: {str(e)}")
            return False
            
    except Exception as e:
        print(f"Unexpected error processing {filename}: {str(e)}")
        return False

async def main():
    source_directory = "/home/mclean/Documents/GitHub/ComfyUI/images"
    destination_directory = "/home/mclean/Pictures/captioned_characters_elitebabe"
    os.makedirs(destination_directory, exist_ok=True)

    image_filenames = [filename for filename in os.listdir(source_directory) if filename.endswith(('.png', '.jpg', '.jpeg'))]
    random.shuffle(image_filenames)

    successful_count = 0
    async with aiohttp.ClientSession() as session:
        tasks = []
        for filename in image_filenames[:1000]:  # Limit to 1000 images
            tasks.append(process_image(session, source_directory, destination_directory, filename))
        
        # Use tqdm to display a progress bar for successful operations only
        pbar = tqdm(total=len(tasks), desc="Processing images")
        for f in asyncio.as_completed(tasks):
            result = await f
            if result:  # Only increment if processing was successful
                successful_count += 1
                pbar.update(1)
        pbar.close()
        
    print(f"Successfully processed {successful_count} images")

if __name__ == "__main__":
    asyncio.run(main())


