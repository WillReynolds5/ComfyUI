import json
import time
import openai

from comfy_client import comfyui_inference_basic
from llm import parse_json, inference

previous_prompts = []


def save_prompt_to_json(filename, prompt_data):
    """Save prompt data to a JSON file."""
    try:
        # Load existing data
        with open('prompts_data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        # If the file does not exist, start with an empty list
        data = []

    # Append the new data
    data.append(prompt_data)

    # Write the updated data back to the file
    with open('prompts_data.json', 'w') as file:
        json.dump(data, file, indent=4)


def generate_portraits():
    global previous_prompts

    for _ in range(10000):
        try:
            base_prompt = """
You are a “prompt” generating assistant. Your job is to generate image prompts for AI generated images of human characters faces. Each image will be a head shot.
Prompts are lists of phrases, separated by commas. Each phrase in a prompt describes a different aspect of the character / scene being generated. 
Parentheses can be used to give extra strength to a phrase in a prompt. 
Each prompt has a “positive” and “negative”. The generated images will correlate with the positive prompt and not correlate with the negative. 
Here is an example prompt:

{
    “positive”: “head shot, (hyper realistic animation), blonde city girl,  seductive expression”,
    “negative”: “deformed face, disfigured eyes”
}

Generate a new prompt that is very different from the following previous prompts:"""

            # Dynamically add the previous prompts to the base prompt for each iteration
            if previous_prompts:
                for prompt in previous_prompts:
                    base_prompt += f"\n\n{prompt}"

            base_prompt += "\nThe new prompt should describe and vary in style, gender, ethnicity, age, pose, expression. Output only one JSON object with the keys positive and negative."

            messages = [
                {"role": "user", "content": base_prompt}
            ]

            response = inference(messages)
            parsed_response, success = parse_json(response)
            prefix = str(uuid.uuid4().hex)
            if success:
                print(response)
                # Update the previous prompts list with the new prompt
                previous_prompts.append(response)
                # Ensure we only keep the last two prompts
                previous_prompts = previous_prompts[-10:]
                comfyui_inference_basic(positive_prompt=parsed_response["positive"],
                                        negative_prompt=parsed_response["negative"],
                                        id=prefix)

                # TODO: get the filename
                # Save the prompt along with the filename and prompt details to a JSON file
                prompt_data = {
                    "id": prefix,
                    "prompt": {
                        "positive": parsed_response["positive"],
                        "negative": parsed_response["negative"]
                    }
                }
                save_prompt_to_json('prompts_data.json', prompt_data)

                time.sleep(0.5)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    generate_portraits()
