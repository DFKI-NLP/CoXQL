import json
import os


def output_number_of_pairs_per_file():
    """
    Merge all (user question, parsed text) pairs, calculate the total number of pairs and store them in jsonl file
    """
    prefix = "./"
    folder_names = [i for i in os.listdir() if os.path.isdir(prefix + i) and i != "filter" and i != "talktomodel" and i != "work_in_progress"]

    output = []
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

                print(f"{f}: {after-before}")

    print(f"In total: {len(user_question)}")

    for i in range(len(user_question)):
        output.append({
            "idx": i,
            "text": user_question[i],
            "sql": parsed_text[i]
        })

    jsonString = json.dumps(output)
    jsonFile = open(f"final_coxql.jsonl", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

output_number_of_pairs_per_file()