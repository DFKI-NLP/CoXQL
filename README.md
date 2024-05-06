
# CoXQL: A Dataset for Explanation Request Parsing in Conversational XAI Systems

**Co**nversational E**x**planation **Q**uery **L**anguage (CoXQL): A text-to-SQL-like benchmark.

## 🚀 Setup
![Static Badge](https://img.shields.io/badge/python-3.8-blue)
![Static Badge](https://img.shields.io/badge/python-3.9-blue)
![Static Badge](https://img.shields.io/badge/python-3.10-blue)
![Static Badge](https://img.shields.io/badge/python-3.11-blue)

We recommand to use Python 3.8+

##  ⚙️ Install the requirements
```shell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 💥 CoXQL Dataset
`dataset` folder's structure is listed below:
```
dataset
    |- data
    |- filters
    |- global_prediction
    |- includes
    |- local_explanation
    |- local_predicrion
    |- meta
    |- modification
    |- perturbation
```
In `dataset` folder, you can find the dataset in `json` format: `coxql_train.json` and `coxql_test.json`.

## 🔍 Evaluation
Parsing accuracy results can be found in `parsing/guided_decoding/results` and `parsing/multi_prompt/results`