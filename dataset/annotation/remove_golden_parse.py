import json
import random

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
