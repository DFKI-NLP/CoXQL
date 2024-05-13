import json
import os

from sklearn.metrics import f1_score

category_2_idx = {
    "data": [0, 23],
    "global_prediction": [24, 38],
    "local_explanation": [29, 54],
    "local_prediction": [55, 63],
    "meta": [64, 91],
    "modification": [92, 102],
    "perturbation": [103, 112]
}

path = "./multi_prompt/results"
files = os.listdir(path)
os.chdir(path)

for file in files:
    if file.endswith(".json"):
        f = open(file)
        data = json.load(f)

        print(f"**********{file.split('.json')[0]}**********")

        for i, j in zip(category_2_idx.keys(), category_2_idx.values()):
            temp = data[j[0]:j[1]+1]

            prediction = []
            label = []

            for t in temp:
                prediction.append(t["parsed_text"])
                label.append(t["label"])

            print(f"{i}: f1: {f1_score(label, prediction, average='weighted')}")

        print()
