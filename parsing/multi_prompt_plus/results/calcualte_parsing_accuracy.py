import json
import os

files = [i for i in os.listdir("/") if i.endswith(".json")]

for file in files:
    f = open(f"./{file}")
    data = json.load(f)
    count = 0
    for i in data:
        if i["parsed_text"] == i["label"]:
            count += 1
    print(f"Parsing results for {file.split('.json')[0]}: {round(count/len(data), 4) * 100}%")
