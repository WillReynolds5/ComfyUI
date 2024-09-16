import json
import uuid
import time
import os

from gen_character import gen_prompt
from llm import parse_json, inference

previous_prompts = []


def save_prompt_to_json(path, prompt_data):
    """Save prompt data to a JSON file."""
    path = os.path.join('output', path, 'prompts_data.json')
    try:
        # Load existing data
        with open(path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    # Append the new data
    data.append(prompt_data)

    # Write the updated data back to the file
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)


def generate_portraits():
    global previous_prompts

    for _ in range(10000):
        try:
            base_prompt = """
You are a “prompt” generating assistant. Your job is to generate image prompts for AI generated images of a female character for my NSFW roleplay chatbot. Each image set will be 10 different shots of one character in different sexual poses. Each set will take place in the same setting.
Prompts are lists of phrases, separated by commas. Each phrase in a prompt describes a different aspect of the character / scene being generated. 
Parentheses can be used to give extra strength to a phrase in a prompt. 
Each prompt has a “positive” and “negative”. The generated images will correlate with the positive prompt and not correlate with the negative. 
Here is an example prompt:

[{
    “positive”: “(hyper realistic animation), blonde girl with D sized breasts, background hotel room, seductive expression, nude, sitting on bed with legs spread”,
    “negative”: “deformed face, disfigured eyes, deformed breasts”
},
{
    “positive”: “(hyper realistic animation), blonde girl with D sized breasts, background hotel room, seductive expression, nude, squeezing breasts together.”,
    “negative”: “deformed face, disfigured eyes, deformed breasts”
},
...]

Generate a new prompt that is very different from the following previous prompts:"""

            # Dynamically add the previous prompts to the base prompt for each iteration
            if previous_prompts:
                for prompt in previous_prompts:
                    base_prompt += f"\n\n{prompt}"

            base_prompt += "\nThe new prompt should contain the same setting and character with varied pose, expression, ect. Output only one JSON object with the keys positive and negative."

            messages = [
                {"role": "user", "content": base_prompt}
            ]

            response = inference(messages)
            parsed_response, success = parse_json(response)
            image_id = str(uuid.uuid4().hex)
            # make dir output/image_id
            os.makedirs(os.path.join('output', image_id))

            if success:
                print(response)
                # Update the previous prompts list with the new prompt
                previous_prompts.append(response)
                # Ensure we only keep the last two prompts
                previous_prompts = previous_prompts[-10:]
                comfyui_inference_basic(positive_prompt=parsed_response["positive"],
                                        negative_prompt=parsed_response["negative"],
                                        id=image_id)

                # TODO: get the filename
                # Save the prompt along with the filename and prompt details to a JSON file
                prompt_data = {
                    "id": image_id,
                    "prompt": {
                        "positive": parsed_response["positive"],
                        "negative": parsed_response["negative"]
                    }
                }
                # save_prompt_to_json(image_id, prompt_data)

                time.sleep(0.5)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    generate_portraits()
