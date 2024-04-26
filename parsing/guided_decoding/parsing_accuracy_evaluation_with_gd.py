import json

import torch
from sentence_transformers import SentenceTransformer, util
from transformers import MaxLengthCriteria, AutoModelForCausalLM, AutoTokenizer

from parsing.guided_decoding.gd_logits_processor import GuidedParser, GuidedDecodingLogitsProcessor
from parsing.guided_decoding.grammar import GRAMMAR


def add_terminal_or(name: str, cur_terminals: str) -> str:
    """Adds a terminal or to a string of terminals."""

    if len(cur_terminals) == 0:
        cur_terminals = " " + "\" " + name + "\""
    else:
        cur_terminals += " | " + "\" " + name + "\""
    return cur_terminals


def get_topk_grammar_text(num=50):
    """Gets text for the available top k features."""
    grammar_text = ""
    for num in range(1, num):
        grammar_text = add_terminal_or(str(num), grammar_text)
    return grammar_text.strip()


def predict_f(text: str, grammar: str, model, tokenizer, use_guided_decoding):
    """The function to get guided decoding."""
    input_ids = tokenizer(text, return_tensors="pt").input_ids.to(model.device.type)

    if use_guided_decoding:
        parser = GuidedParser(grammar, tokenizer, model="gpt")
        guided_preprocessor = GuidedDecodingLogitsProcessor(parser, input_ids.shape[1])
        with torch.no_grad():
            generation = model.greedy_search(input_ids,
                                             logits_processor=guided_preprocessor,
                                             eos_token_id=parser.eos_token,
                                             pad_token_id=model.config.pad_token_id,
                                             device=model.device.type)
    else:
        stopping_criteria = MaxLengthCriteria(max_length=200)
        generation = model.greedy_search(input_ids,
                                         stopping_criteria=stopping_criteria,
                                         device=model.device.type)

    decoded_generation = tokenizer.decode(generation[0])
    return decoded_generation


def load_config():
    f = open("./config.json")
    data = json.load(f)

    use_guided_decoding = data["use_guided_decoding"]
    num_shots = data["num_shots"]

    model = AutoModelForCausalLM.from_pretrained(data["model"])
    tokenizer = AutoTokenizer.from_pretrained(data["tokenizer"])

    print(f"[UPDATE] loading model - {data['model']}")

    sentence_transformer = SentenceTransformer(data["sentence_transformer"])

    print(f"[UPDATE] loading sentence transformer - {data['sentence_transformer']}")

    model.config.pad_token_id = model.config.eos_token_id

    return model, tokenizer, sentence_transformer, use_guided_decoding, num_shots


def load_evaluation_pairs():
    f = open("../../dataset/final_coxql.json")
    data = json.load(f)

    texts = []
    sqls = []

    for i in data:
        texts.append(i["text"])
        sqls.append(i["sql"])

    return texts, sqls


def prepare_prompt_template(idx, embeddings, texts, sqls, num_shots, current_text):
    cosine_scores = util.cos_sim(embeddings[idx], embeddings)
    _, indices = torch.sort(cosine_scores[0], descending=True)

    prompt_template = ""

    for i in indices[1:num_shots+1]:
        prompt_template += f"User: {texts[i]}\n"
        prompt_template += f"Parsed: {sqls[i]}\n\n"
    prompt_template += f"User: {current_text}\n"
    prompt_template += "Parsed: "

    return prompt_template


def few_shot_prompting():
    model, tokenizer, sentence_transformer, use_guided_decoding, num_shots = load_config()

    # load evaluation pairs
    texts, sqls = load_evaluation_pairs()

    embeddings = sentence_transformer.encode(texts, convert_to_tensor=True)

    # predictions = []

    grammar = GRAMMAR.format(topkvalues=get_topk_grammar_text(), availablefeaturetypes=get_topk_grammar_text(10000))

    counter = 0

    for i, text in enumerate(texts[:5]):
        prompt_template = prepare_prompt_template(i, embeddings, texts, sqls, num_shots, text)

        generation = predict_f(prompt_template, grammar, model, tokenizer, use_guided_decoding)
        parsed_text = generation.split(prompt_template)[1].replace("[e]", "[E]").strip()
        # predictions.append(parsed_text)
        print(f"{sqls[i]} >>> {parsed_text} >> {sqls[i] == parsed_text}")

        if sqls[i] == parsed_text:
            counter += 1

    print(f"Matched: {counter}; Total: {len(texts)}; Accuracy: {round(counter/len(texts)*100, 2)}%")


few_shot_prompting()