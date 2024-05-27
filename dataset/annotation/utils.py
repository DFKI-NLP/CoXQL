import json
import random
from nltk import agreement


def remove_labeled_annotations():
    f = open(f"../coxql_test.json")
    data = json.load(f)

    texts = []
    sqls = []

    for i in data:
        texts.append(i["text"])
        sqls.append(i["sql"])

    output = []
    for i in range(len(texts)):
        output.append({
            "idx": i,
            "text": texts[i],
            "sql": ""
        })

    random.shuffle(output)

    jsonFile = open("./coxql_test_annotation.json", "w")
    jsonString = json.dumps(output, indent=2)
    jsonFile.write(jsonString)
    jsonFile.close()


def get_annotation_with_order(data):
    label = []
    for i in range(len(data)):
        for j in data:
            if j["idx"] == i:
                label.append(j['sql'])
                break
    return label


def calculate_IAA():

    f = open("./coxql_test_annotation1.json.json")
    data = json.load(f)
    rater1 = [i["sql"] for i in data]

    f1 = open("./coxql_test_annotation2.json")
    data1 = json.load(f1)

    f2 = open("./coxql_test_annotation3.json")
    data2 = json.load(f2)

    rater2 = get_annotation_with_order(data1)
    rater3 = get_annotation_with_order(data2)

    task_data = ([[0, str(i), str(rater1[i])] for i in range(0, len(rater1))] +
                 [[1, str(i), str(rater2[i])] for i in range(0, len(rater2))] +
                 [[2, str(i), str(rater3[i])] for i in range(0, len(rater3))])

    rating_task = agreement.AnnotationTask(data=task_data)

    print("Kappa " + str(rating_task.kappa()))
    print("Fleiss " + str(rating_task.multi_kappa()))
    print("Alpha " + str(rating_task.alpha()))
    print("Scotts " + str(rating_task.pi()))
