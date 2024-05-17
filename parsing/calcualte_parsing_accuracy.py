import argparse
import json
import os

parser = argparse.ArgumentParser()
parser.add_argument("strategy", type=str, default="guided_decoding", help="Available strategies: guided_decoding, "
                                                                          "multi_prompt, multi_prompt_plus")
args = parser.parse_args()

prefix = f"./{args.strategy}/results/"
files = [i for i in os.listdir(prefix) if i.endswith(".json")]

for file in files:
    f = open(f"./{prefix}/{file}")
    data = json.load(f)
    count = 0
    for i in data:
        if i["parsed_text"] == i["label"]:
            count += 1
    print(f"Parsing results for {file.split('.json')[0]}: {round(count/len(data), 4) * 100}%")
