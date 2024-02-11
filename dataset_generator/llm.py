import json

import openai

openai_client = openai.Client(
    api_key="fd4c8cd310d4bdfa853e55f3d4233438d991e4cdfe26db702b88a3a5b1f7253b",
    base_url="https://api.together.xyz/v1",
)


def parse_json(json_string):
    try:
        return json.loads(json_string), True
    except json.JSONDecodeError:
        return json_string, False

def inference(messages, model_kwargs={"temperature": 1}):
    response = openai_client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=messages,
        max_tokens=256,
        **model_kwargs,
    )
    return response.choices[0].message.content

