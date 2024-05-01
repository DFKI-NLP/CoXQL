import json
import os

from sklearn.model_selection import train_test_split


def save_dataset_as_json(X, y, split="train"):
    output = []
    for i in range(len(X)):
        output.append({
            "idx": i,
            "text": X[i],
            "sql": y[i]
        })

    jsonString = json.dumps(output)
    jsonFile = open(f"coxql_{split}.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()


def output_number_of_pairs_per_file(save=False, without_logic=True):
    """
    Merge all (user question, parsed text) pairs, calculate the total number of pairs and store them in jsonl file
    """
    prefix = "./"

    if without_logic:
        folder_names = [i for i in os.listdir() if
                        os.path.isdir(prefix + i) and i != "includes" and i != "filters"]
    else:
        folder_names = [i for i in os.listdir() if os.path.isdir(prefix + i)]

    user_question = []
    parsed_text = []

    for folder_name in folder_names:
        files = os.listdir(prefix + folder_name)

        for f in files:
            if f.endswith(".txt"):
                before = len(user_question)

                f_pointer = open(f"./{folder_name}/{f}", "r")
                lines = [line.strip() for line in f_pointer.readlines()]

                for l in lines:
                    if l.startswith("User"):
                        user_question.append(l.split("User: ")[1])
                    elif l.startswith("Parsed"):
                        parsed_text.append(l.split("Parsed: ")[1])

                after = len(user_question)

                print(f"{f}: {after - before}")

    print(f"In total: {len(user_question)}")

    if save:
        X_train, X_test, y_train, y_test = train_test_split(user_question, parsed_text, shuffle=True, random_state=42,
                                                            test_size=0.2)

        save_dataset_as_json(X_train, y_train, "train")
        save_dataset_as_json(X_test, y_test, "test")


output_number_of_pairs_per_file(without_logic=False)
