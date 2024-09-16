import json
from urllib import request, parse
import random


# This is the ComfyUI api prompt format.

# If you want it for a specific workflow you can "enable dev mode options"
# in the settings of the UI (gear beside the "Queue Size: ") this will enable
# a button on the UI to save workflows in api format.

# keep in mind ComfyUI is pre alpha software so this format will change a bit.

# this is the one for the default workflow

def gen_prompt(pos_prompt, neg_prompt, seed=None):
    if seed is None:
        seed = random.randint(0, 1000000)

    # open json file called resposer.json
    with open("reposer.json", "r") as f:
        prompt_text = f.read()
    # load json and format dict
    parsed_prompt = json.loads(prompt_text)
    # parsed_prompt["7"]["inputs"]["text"] = pos_prompt
    # parsed_prompt["8"]["inputs"]["text"] = neg_prompt
    # parsed_prompt["17"]["inputs"]["seed"] = seed
    queue_prompt(prompt_text)

    return parsed_prompt


def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req = request.Request("http://127.0.0.1:8188/prompt", data=data)
    resp = request.urlopen(req)
    print(resp.read())


positive_prompt = "(hyper realistic animation), women standing on golf course in southern utah with bikini"
negative_prompt = "deformed face, disfigured eyes, deformed breasts"

prompt = gen_prompt(positive_prompt, negative_prompt)

queue_prompt(prompt)
