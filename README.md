
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
In `dataset` folder, you can find the dataset in `json` format: `coxql_train.json` and `coxql_test.json`. More details about the number of pairs in each operation category can be found in `dataset/README.md`.

Both `json` files have the same structure as follows:
```json
{
  "idx": ...,
  "text": ...,
  "sql": ...
}
```

## 🔍 Evaluation
Parsing accuracy results can be found in `parsing/guided_decoding/results` and `parsing/multi_prompt/results`

You can run `calculate_parsing_accuracy.py` to get an overview of parsing accuracy.
```bash
python calcualte_parsing_accuracy.py {guided_decoding, multi_prompt}
```

🤗We evaluate in total seven state-of-the-art LMs:

| Model  | Size | Huggingface Link |
|--------|------| ------------- |
| **Falcon** | 1B   | https://huggingface.co/tiiuae/falcon-rw-1b|
| **Pythia** | 2.8B |https://huggingface.co/EleutherAI/pythia-2.8b-v0|
|**Mistral** | 7B | https://huggingface.co/mistralai/Mistral-7B-v0.1|
| **CodeQWen1.5** | 7B | https://huggingface.co/Qwen/CodeQwen1.5-7B-Chat|
| **sqlcoder** | 7B | https://huggingface.co/defog/sqlcoder-7b-2|
| **Llama3** | 8B | https://huggingface.co/meta-llama/Meta-Llama-3-8B|
| **Llama3** | 70B | https://huggingface.co/meta-llama/Meta-Llama-3-70B|