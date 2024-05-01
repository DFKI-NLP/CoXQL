import json

import torch
from sentence_transformers import SentenceTransformer, util
from transformers import MaxLengthCriteria, AutoModelForCausalLM, AutoTokenizer, GPTQConfig

from parsing.guided_decoding.gd_logits_processor import GuidedParser, GuidedDecodingLogitsProcessor
from parsing.guided_decoding.grammar import GRAMMAR


def add_terminal_or(name: str, cur_terminals: str) -> str:
    """Adds a terminal or to a string of terminals."""

    if len(cur_terminals) == 0:
        cur_terminals = " " + "\" " + name + "\""
    else:
        cur_terminals += " | " + "\" " + name + "\""
    return cur_terminals


def get_num_grammar_text(num=20):
    """Gets text for the available num features."""
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
    """load configuration, model and sentence transformer"""
    f = open("./config.json")
    data = json.load(f)

    use_guided_decoding = data["use_guided_decoding"]
    num_shots = data["num_shots"]
    use_cuda = data["use_cuda"]

    if use_cuda and torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"

    print(f"[UPDATE] loading model - {data['model']}")

    if data["model"] != "NN":
        # quantization_config = GPTQConfig(bits=8, disable_exllama=True)
        # model = AutoModelForCausalLM.from_pretrained(data["model"], low_cpu_mem_usage=True, device_map="auto", quantization_config=quantization_config)
        model = AutoModelForCausalLM.from_pretrained(data["model"], device_map="auto", load_in_8bit=True)
        tokenizer = AutoTokenizer.from_pretrained(data["tokenizer"])

        model.config.pad_token_id = model.config.eos_token_id

        sentence_transformer = SentenceTransformer(data["sentence_transformer"]).to(device)
    else:
        tokenizer = None
        model = SentenceTransformer(data["sentence_transformer"]).to(device)
        sentence_transformer = model
        num_shots = None

    print(f"[UPDATE] loading sentence transformer - {data['sentence_transformer']}")
    return model, tokenizer, sentence_transformer, use_guided_decoding, num_shots, device


def load_evaluation_pairs(filename):
    f = open(f"../../dataset/{filename}")
    data = json.load(f)

    texts = []
    sqls = []

    for i in data:
        texts.append(i["text"])
        sqls.append(i["sql"])

    return texts, sqls


def prepare_prompt_template(test_embedding, train_embeddings, texts, sqls, num_shots, current_text):
    """selection of top k demonstrations and fill them into prompt template"""
    cosine_scores = util.cos_sim(test_embedding, train_embeddings)
    _, indices = torch.sort(cosine_scores[0], descending=True)

    prompt_template = ""

    for i in indices[:num_shots]:
        prompt_template += f"User: {texts[i]}\n"
        prompt_template += f"Parsed: {sqls[i]}\n\n"
    prompt_template += f"User: {current_text}\n"
    prompt_template += "Parsed: "

    return prompt_template


def post_process(parsed_text):
    """required for mistral and llama model (<s> contained in the generation)"""
    ls = parsed_text.split(" ")
    for (idx, i) in enumerate(ls):
        if "<s>" in i:
            ls[idx] = i.split("<s>")[0]
    ls = [i for i in ls if i != '']
    parsed_text = " ".join(ls)

    return parsed_text


def few_shot_prompting():
    model, tokenizer, sentence_transformer, use_guided_decoding, num_shots, device = load_config()

    # load train/test sets
    train_texts, train_sqls = load_evaluation_pairs("coxql_train.json")
    test_texts, test_sqls = load_evaluation_pairs("coxql_test.json")

    train_embeddings = sentence_transformer.encode(train_texts, convert_to_tensor=True)
    test_embeddings = sentence_transformer.encode(test_texts, convert_to_tensor=True)

    counter = 0

    if num_shots:
        """few-shot prompting"""
        grammar = GRAMMAR.format(topkvalues=get_num_grammar_text(), availablefeaturetypes=get_num_grammar_text(9999))

        for i, text in enumerate(test_texts):
            prompt_template = prepare_prompt_template(test_embeddings[i], train_embeddings, train_texts, train_sqls, num_shots, text)

            generation = predict_f(prompt_template, grammar, model, tokenizer, use_guided_decoding)
            parsed_text = generation.split(prompt_template)[1].replace("[e]", "[E]").strip()

            # post-process the parsed text
            parsed_text = post_process(parsed_text)

            print(f"Index: {i}; {test_sqls[i]} >>> {parsed_text} >> {test_sqls[i] == parsed_text}")

            if test_sqls[i] == parsed_text:
                counter += 1
    else:
        """baseline - nearest neighbor"""
        for i, text in enumerate(test_texts):
            # get the most similar one
            cosine_scores = util.cos_sim(test_embeddings[i], train_embeddings)
            _, indices = torch.sort(cosine_scores[0], descending=True)

            parsed_text = train_sqls[indices[0]]

            print(f"Index {i}: {test_sqls[i]} >>> {parsed_text} >> {test_sqls[i] == parsed_text}")

            if test_sqls[i] == parsed_text:
                counter += 1

    print(f"Matched: {counter}; Total: {len(test_sqls)}; Accuracy: {round(counter/len(test_sqls)*100, 2)}%")


# few_shot_prompting()