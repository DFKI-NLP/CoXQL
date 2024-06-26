import argparse
import json
import sys
from os.path import abspath, dirname
from string import punctuation
from typing import Any, List

import torch.cuda
from thefuzz import fuzz

parent = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(parent)

from parsing.multi_prompt.defined_prompts import (
    operation2attributes,
    operation2prompt,
    operation2template,
    operation2tutorial,
    operation2types,
    operation_needs_id,
    operation_type_prompt,
    operations_with_default,
    operations_with_number,
    operations_with_topk_number,
    operations_wo_attributes,
    topk_operations,
    tutorial2operation,
    tutorial_operations,
    valid_operation_meanings,
    valid_operation_names,
    valid_operation_prompt_samples,
)
from sentence_transformers import SentenceTransformer, util
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig, GPTQConfig
from word2number import w2n


class MultiPromptParser:
    def __init__(
        self,
        decoder_model: AutoModelForCausalLM,
        tokenizer: AutoTokenizer,
        st_model: SentenceTransformer,
        device: str,
    ):
        self.decoder_model = decoder_model
        self.tokenizer = tokenizer
        self.st_model = st_model
        self.device = device
        self.encoded_operations_st = self.st_model.encode(
            valid_operation_names, convert_to_tensor=True
        )

        self.valid_operation_names_with_id = [
            op for op in valid_operation_names if op in operation_needs_id
        ]
        self.valid_operation_names_wo_id = [
            op for op in valid_operation_names if op not in operation_needs_id
        ]
        valid_operation_meanings_with_id = [
            op
            for idx, op in enumerate(valid_operation_meanings)
            if valid_operation_names[idx] in operation_needs_id
        ]
        valid_operation_meanings_wo_id = [
            op
            for idx, op in enumerate(valid_operation_meanings)
            if valid_operation_names[idx] not in operation_needs_id
        ]

        if (
            "falcon" in self.decoder_model.name_or_path.lower()
            or "pythia" in self.decoder_model.name_or_path.lower()
        ):
            valid_operation_prompt_samples_concatenated = []
            for op_name in valid_operation_names:
                valid_operation_prompt_samples_concatenated.append(
                    " ".join(valid_operation_prompt_samples[op_name][:5])
                )
            valid_operation_prompt_samples_with_id_concatenated = []
            valid_operation_prompt_samples_wo_id_concatenated = []
            for op_name in valid_operation_names:
                if op_name in operation_needs_id:
                    valid_operation_prompt_samples_with_id_concatenated.append(
                        " ".join(valid_operation_prompt_samples[op_name][:5])
                    )
                else:
                    valid_operation_prompt_samples_wo_id_concatenated.append(
                        " ".join(valid_operation_prompt_samples[op_name][:5])
                    )

            self.encoded_op_meanings_st = self.st_model.encode(
                valid_operation_prompt_samples_concatenated, convert_to_tensor=True
            )
            self.encoded_op_meanings_with_id_st = self.st_model.encode(
                valid_operation_prompt_samples_with_id_concatenated, convert_to_tensor=True
            )
            self.encoded_op_meanings_wo_id_st = self.st_model.encode(
                valid_operation_prompt_samples_wo_id_concatenated, convert_to_tensor=True
            )
        else:
            self.encoded_op_meanings_st = self.st_model.encode(
                valid_operation_meanings, convert_to_tensor=True
            )
            self.encoded_op_meanings_with_id_st = self.st_model.encode(
                valid_operation_meanings_with_id, convert_to_tensor=True
            )
            self.encoded_op_meanings_wo_id_st = self.st_model.encode(
                valid_operation_meanings_wo_id, convert_to_tensor=True
            )

        self.attribute2st = dict()
        for operation in operation2attributes:
            for attribute in operation2attributes[operation]:
                self.attribute2st[attribute] = self.st_model.encode(
                    attribute, convert_to_tensor=True
                )
        # if "llama" in self.decoder_model.name_or_path.lower():
        #    max_new_tokens = 20
        # else:
        max_new_tokens = 10
        self.generation_config = GenerationConfig(
            penalty_alpha=0.6,
            do_sample=True,
            top_k=5,
            top_p=0.95,
            temperature=0.1,
            repetition_penalty=1.2,
            max_new_tokens=max_new_tokens,
            bos_token_id=1,
            eos_token_id=2,
            pad_token_id=2,
        )

    def in_vocabulary(self, operation: str):
        operation_words = operation.split()
        for op in valid_operation_names:
            if op in operation_words:
                return True
        return False

    def check_attribute(self, attribute: str, main_operation: str, user_input: str):
        """checks if the parsed attributes are valid tokens for the operation."""
        attribute = attribute.strip()
        for punct in [".", ",", ":"]:
            attribute = attribute.replace(punct, "")
        valid_attributes = []
        if main_operation in operation2attributes:
            valid_attributes += operation2attributes[main_operation]
        # number can always be a valid attribute and needs to be checked first
        try:
            number = w2n.word_to_num(attribute)
            number = str(number)
            if number in user_input:
                return number
        except Exception:
            pass
        if attribute in valid_attributes:
            return attribute
        else:
            # check the embedding similarity to the valid attributes
            if len(valid_attributes) > 0:
                valid_attributes_st = self.st_model.encode(
                    valid_attributes, convert_to_tensor=True
                )
                if attribute in self.attribute2st:
                    attribute_st = self.attribute2st[attribute]
                else:
                    attribute_st = self.st_model.encode(attribute, convert_to_tensor=True)
                attr_scores = util.cos_sim(attribute_st, valid_attributes_st)[0].tolist()
                if max(attr_scores) >= 0.5:
                    return valid_attributes[attr_scores.index(max(attr_scores))]
                else:
                    return ""
            else:
                return ""

    def generate_with_prompt(self, prompt: str, user_input: str):
        """generates the parse given a user input and a prompt."""
        inputs = self.tokenizer(
            prompt + "\nInput: " + user_input + " Output:", return_tensors="pt"
        ).to(self.device)

        outputs = self.decoder_model.generate(**inputs, generation_config=self.generation_config)

        parsed_operation = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        offset = len("Output:")
        parsed_operation = parsed_operation[parsed_operation.rindex("Output:") + offset :].strip()

        # for falcon and pythia only since they are not good at parsing ids
        # we check if we have id word in the user input and in case
        # "filter id" is missing in the parsed output we add it to the parse
        if (
            "falcon" in self.decoder_model.name_or_path.lower()
            or "pythia" in self.decoder_model.name_or_path.lower()
        ):
            op_id = self.find_id(user_input).strip()
            if len(op_id) > 0:
                parsed_operation = "filter id " + op_id + " and " + parsed_operation

        # each operation consists of:
        # - prefix ("filter id ...")
        # - main_operation (e.g., "cfe", "similar")
        # - attributes (e.g., "topk 5")
        op_prefix = ""
        main_operation = parsed_operation
        attributes = ""
        splitted_op = parsed_operation.split()
        if parsed_operation.startswith("filter id") and len(splitted_op) > 4:
            op_prefix = " ".join(splitted_op[:4]) + " and "
            main_operation = " ".join(splitted_op[4:])

        splitted_main_op = main_operation.split()
        if len(splitted_main_op) > 0:
            main_operation = splitted_main_op[0]

        if not (self.in_vocabulary(main_operation)):
            # find a similar operation with SBERT
            main_operation = self.find_similar_operation(
                user_input,
                valid_operation_names,
                self.encoded_op_meanings_st,
            )

        # check that the attributes are valid
        if len(splitted_main_op) > 1:
            attributes = " ".join(splitted_main_op[1:])
            if "[E]" in attributes:
                attributes = attributes[: attributes.rindex("[E]") + 3]
            checked_attributes: List[str] = []
            for attribute in attributes.split():
                attribute = self.check_attribute(attribute, main_operation, user_input)
                if attribute not in checked_attributes:
                    if len(checked_attributes) <= 2 and len(attribute) > 0:
                        checked_attributes.append(attribute)
                    else:
                        break
            if (
                len(checked_attributes) == 0
                and (main_operation in operation2attributes)
                and len(operation2attributes[main_operation]) > 0
            ):  # some operations can have numbers but no other fixed attributes
                attributes = operation2attributes[main_operation][0]
            else:
                attributes = " ".join(checked_attributes)

        parsed_operation = op_prefix + main_operation
        if len(attributes) > 0:
            parsed_operation += " " + attributes

        return parsed_operation

    def find_id(self, user_input: str):
        """fallback in case the id was not parsed correctly."""
        user_input = user_input.lower()
        correct_id = ""
        id_words = ["data point ", "data ", "id ", "instance ", "sample ", "item "]
        for id_word in id_words:
            if id_word in user_input:
                # if there is no id, e.g.: "counterfactual for this id"
                offset = user_input.rindex(id_word) + len(id_word)
                if offset == len(user_input):
                    continue
                for id_candidate in user_input[offset:].split():
                    if len(id_candidate) == 0:
                        continue
                    correct_id = id_candidate.replace("s", "")
                    try:
                        if (
                            correct_id != "point"
                        ):  # because w2n parses point as a number (it outputs 0)!
                            correct_id = w2n.word_to_num(correct_id)
                            correct_id = str(correct_id)
                            return correct_id
                        else:
                            correct_id = ""
                    except Exception:
                        correct_id = ""
        return correct_id

    def has_number(self, user_input: str):
        """check numerical attributes in the user input."""
        num_attr = None
        sample_id = self.find_id(user_input)
        for token in user_input.split():
            if token.isnumeric() and token != sample_id:
                return token
        return num_attr

    def fuzzy_match(self, attr: str, user_input: str):
        """check fuzzy string matching between the attribute and user input."""
        normalized_attr = " ".join(attr.split("_"))
        if fuzz.partial_ratio(normalized_attr, user_input) > 85:
            return True
        return False

    def find_similar_operation(self, user_input: str, operation_names: List[str], encoded_op: Any):
        """implements similarity check with SBERT between the user input and available
        operations."""
        encoded_user_input = self.st_model.encode(user_input, convert_to_tensor=True)
        op_scores = util.cos_sim(encoded_user_input, encoded_op)[0].tolist()
        best_match_op = operation_names[op_scores.index(max(op_scores))]
        return best_match_op

    def check_num_attribute(self, parsed_token, template_element):
        """checks whether there is a number in the user input."""
        if template_element == "num" and parsed_token.isnumeric():
            return parsed_token

    def check_operation_template(
        self,
        parsed_operation: str,
        user_input: str,
        main_operation: str,
        id_token: str,
        template: List[Any],
    ):
        """checks the correspondence of the parsed operation to its template, 'imitating' guided
        decoding."""
        final_operation = []
        user_input_tokens = user_input.split()
        parsed_operation_tokens = parsed_operation.split()
        allowed_tokens = []
        for element in template:
            if isinstance(element, list):
                allowed_tokens.extend(element)
            else:
                allowed_tokens.append(element)
        for token in parsed_operation_tokens:
            if token.isnumeric() and "num" in allowed_tokens:
                allowed_tokens += [token]
        j = 0
        skip_parsed_tokens = False
        for i in range(len(template)):
            template_token = template[i]
            if j < len(parsed_operation_tokens):
                parsed_token = parsed_operation_tokens[j].strip()
                while parsed_token not in allowed_tokens and j + 1 < len(parsed_operation_tokens):
                    j += 1
                    parsed_token = parsed_operation_tokens[j].strip()
            else:
                skip_parsed_tokens = True
            if isinstance(template_token, list):
                # several options available
                found_match = False
                if not skip_parsed_tokens:
                    for template_element in template_token:
                        has_num_attr = self.check_num_attribute(parsed_token, template_element)
                        if (
                            parsed_token != id_token
                            and template_element == parsed_token
                            or has_num_attr
                        ):
                            if (
                                has_num_attr
                                and main_operation in operations_with_topk_number
                                and "topk" not in final_operation
                            ):
                                final_operation.append("topk")
                            final_operation.append(parsed_token)
                            found_match = True
                            break
                if not found_match:
                    for tkn in parsed_operation_tokens + user_input_tokens:
                        if tkn in template_token or (tkn.isnumeric() and "num" in template_token):
                            if not (tkn in final_operation):
                                if (
                                    tkn.isnumeric()
                                    and main_operation in operations_with_topk_number
                                    and "topk" not in final_operation
                                ):
                                    final_operation.append("topk")
                                final_operation.append(tkn)
                                break
            else:
                found_match = False
                if not skip_parsed_tokens:
                    has_num_attr = self.check_num_attribute(parsed_token, template_token)
                    if template_token == parsed_token or has_num_attr:
                        if (
                            parsed_token != id_token
                            and has_num_attr
                            and main_operation in operations_with_topk_number
                            and "topk" not in final_operation
                        ):
                            final_operation.append("topk")
                        final_operation.append(parsed_token)
                        found_match = True
                if not found_match:
                    for tkn in parsed_operation_tokens + user_input_tokens:
                        if tkn == template_token or (tkn.isnumeric() and template_token == "num"):
                            if not (tkn in final_operation):
                                if (
                                    tkn.isnumeric()
                                    and main_operation in operations_with_topk_number
                                    and "topk" not in final_operation
                                ):
                                    final_operation.append("topk")
                                final_operation.append(tkn)
                                break
            j += 1

        return " ".join(final_operation)

    def parse_user_input(self, user_input: str):
        """performs multi-prompt parsing for operations and their attributes."""
        user_input = "".join([ch for ch in user_input if ch not in punctuation])
        parsed_operation = (
            self.generate_with_prompt(operation_type_prompt, user_input).replace("[E]", "").strip()
        )

        op_start = parsed_operation.split()[0]
        if not ((op_start in valid_operation_names) or (op_start == "filter")):
            parsed_operation = self.find_similar_operation(
                user_input, valid_operation_names, self.encoded_op_meanings_st
            )
        splitted_parsed_op = parsed_operation.split()

        if (
            splitted_parsed_op[0] not in operations_wo_attributes
            and parsed_operation in operation2prompt.keys()
        ):
            operation_prompt = operation2prompt[parsed_operation]
            parsed_operation = self.generate_with_prompt(operation_prompt, user_input)
        # if we have an id we cannot have a tutorial operation
        if parsed_operation in tutorial2operation:
            for input_token in user_input:
                if input_token in ["id", "sample", "instance", "item", "this", "it"]:
                    no_tutorial = True
                    operation = tutorial2operation[parsed_operation]
                    operation_prompt = operation2prompt[operation]
                    parsed_operation = self.generate_with_prompt(operation_prompt, user_input)
                    break
        non_repeated_tokens = set()
        splitted_parsed_op = parsed_operation.split()
        filtered_parsed_op_tokens = []
        # check that tokens other than numbers do not appear more than once in the parsed output
        for token in splitted_parsed_op:
            is_number_token = isinstance(token, int)
            if (not (is_number_token) and not (token in non_repeated_tokens)) or is_number_token:
                filtered_parsed_op_tokens.append(token)
                non_repeated_tokens.add(token)
            if token == "[E]":
                break

        found_id = self.find_id(user_input)

        for i, token in enumerate(filtered_parsed_op_tokens):
            if token == "id" and filtered_parsed_op_tokens[i + 1] != found_id:
                # replace hallucinated id
                if len(found_id) > 0:
                    filtered_parsed_op_tokens[i + 1] = found_id
                else:
                    filtered_parsed_op_tokens = filtered_parsed_op_tokens[i + 3 :]
                break
        parsed_operation = " ".join(filtered_parsed_op_tokens).strip()

        # check if we parsed a standard operation but there is no id
        splitted_op = parsed_operation.split()
        if parsed_operation.startswith("filter") and len(splitted_op) > 4:
            main_operation = splitted_op[4]
        else:
            main_operation = splitted_op[0]

        if len(found_id) > 0:
            if main_operation in operation_needs_id:
                # check if we have a number in the parsed text, use it as id
                parsed_operation = "filter id " + found_id + " and " + main_operation
            # if we have filter it's not the tutorial
            elif main_operation in tutorial2operation:
                main_operation = tutorial2operation[main_operation]
                parsed_operation = "filter id " + found_id + " and " + main_operation

        if not ("filter id " in parsed_operation) and (
            main_operation in operation2tutorial
        ):  # no filter for tutorial operations
            parsed_operation = operation2tutorial[main_operation]

        if not (parsed_operation.endswith(" [E]")):
            parsed_operation += " [E]"
        # remove invalid insertion of the filter (e.g., happens with the inputs like "counterfactual for this id")
        parsed_operation = parsed_operation.replace("filter id and", "")

        # check if operation needs default at the end of the parse
        if main_operation in operations_with_default:
            if parsed_operation.endswith(main_operation + " [E]"):
                parsed_operation = parsed_operation.replace(" [E]", " all default [E]")
            elif parsed_operation.endswith(main_operation + " all [E]"):
                parsed_operation = parsed_operation.replace(" [E]", " default [E]")
        # check if there is a number in the user input that is not an id and whether it should be added to the parse (e.g., as topk)
        if main_operation in (
            operations_with_number + operations_with_topk_number
        ) and parsed_operation.endswith(main_operation + " [E]"):
            num = self.has_number(user_input)
            topk_prefix = " topk" if main_operation in operations_with_topk_number else ""
            if num is not None:
                parsed_operation = parsed_operation.replace(
                    main_operation, main_operation + topk_prefix + " " + num
                )
            else:
                parsed_operation = parsed_operation.replace(
                    main_operation, main_operation + topk_prefix + " 1"
                )
        if " all " in parsed_operation:
            topk_num = self.has_number(user_input)
            if topk_num is not None:
                parsed_operation = parsed_operation.replace(" all ", " topk " + topk_num + " ")
        # check that if there is a number there should be also topk in front of it (for operations that require topk such as nlpattribute and influence)
        if main_operation in topk_operations and "topk" not in parsed_operation:
            num = self.has_number(parsed_operation)
            if num is not None:
                parsed_operation = parsed_operation.replace(" " + num + " ", " topk " + num + " ")
        # check if whether default can be replaced with the fuzzy matched attribute
        if main_operation in operations_with_default and "default" in parsed_operation:
            for attr in operation2types[main_operation]:
                if self.fuzzy_match(attr, user_input):
                    parsed_operation = parsed_operation.replace("default", attr)
                    break

        if parsed_operation.split()[0] in tutorial_operations:
            parsed_operation = "qatutorial " + parsed_operation
        else:
            # no id but parsed operation requires it
            if main_operation in operation_needs_id and len(found_id) == 0:
                # match ops w/o id
                main_operation = self.find_similar_operation(
                    user_input, self.valid_operation_names_wo_id, self.encoded_op_meanings_wo_id_st
                )
                parsed_operation = main_operation
            # has id but operation does not allow it
            elif main_operation not in operation_needs_id and len(found_id) > 0:
                # match ops with id
                main_operation = self.find_similar_operation(
                    user_input,
                    self.valid_operation_names_with_id,
                    self.encoded_op_meanings_with_id_st,
                )
                parsed_operation = "filter id " + found_id + " and " + main_operation
            # check if the final operation corresponds to the template, adjust if necessary
            parsed_operation = (
                self.check_operation_template(
                    parsed_operation,
                    user_input,
                    main_operation,
                    self.find_id(user_input),
                    operation2template[main_operation],
                )
                + " [E]"
            )

        return parsed_operation


def main(model_id: str, test_file_path: str, verbose: bool):
    """parsing accuracy evaluation (exact matches)"""
    # loading model and tokenizer
    # model ids: "EleutherAI/pythia-2.8b-v0" #"TheBloke/Llama-2-7b-Chat-GPTQ" #"TheBloke/Mistral-7B-v0.1-GPTQ" #"tiiuae/falcon-rw-1b"

    if "GPTQ" in model_id:
        quantization_config = GPTQConfig(bits=4, disable_exllama=True)
        decoder_model = AutoModelForCausalLM.from_pretrained(
            model_id,
            low_cpu_mem_usage=True,
            device_map="auto",
            quantization_config=quantization_config,
        )
    else:
        decoder_model = AutoModelForCausalLM.from_pretrained(
            model_id, low_cpu_mem_usage=True, device_map="auto"
        )

    decoder_model.eval()

    decoder_model.config.pad_token_id = decoder_model.config.eos_token_id

    tokenizer = AutoTokenizer.from_pretrained(model_id)

    # loading SBERT
    st_model = SentenceTransformer("BAAI/bge-base-en-v1.5")

    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"

    # initializing the multi-prompt parsing model
    parser = MultiPromptParser(decoder_model, tokenizer, st_model, device)

    f = open(test_file_path)
    gold_data = json.load(f)

    # evaluation
    correct_parses = []
    user_inputs = []
    for sample in gold_data:
        correct_parses.append(sample["sql"])
        user_inputs.append(sample["text"])
    sys_parses = []
    for ui, user_input in enumerate(user_inputs):
        parsed_operation = parser.parse_user_input(user_input)
        if verbose:
            print(
                "parsed: "
                + parsed_operation
                + " vs gold: "
                + correct_parses[ui]
                + " >>> "
                + user_input
            )
        sys_parses.append(parsed_operation)
    matched = 0

    assert len(sys_parses) == len(correct_parses)

    for i in range(len(sys_parses)):
        if sys_parses[i] == correct_parses[i]:
            matched += 1

    # save results
    output = []
    for i in range(len(sys_parses)):
       output.append({
           "idx": i,
           "parsed_text": sys_parses[i],
           "label": correct_parses[i]
       })
    jsonFile = open(f"../multi_prompt/results/{model_id.split('/')[1]}.json", "w")
    jsonString = json.dumps(output, indent=2)
    jsonFile.write(jsonString)
    jsonFile.close()

    print(
        f"Matched: {matched}; total: {len(correct_parses)}; acc: {round(matched / len(correct_parses), 4) * 100}%"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_id",
        type=str,
        required=True,
        help="Parsing model name or path, e.g., `tiiuae/falcon-rw-1b`.",
    )
    parser.add_argument(
        "--test_file_path",
        type=str,
        required=True,
        help="Path to the test file.",
    )
    parser.add_argument(
        "--silent",
        dest="verbose",
        action="store_false",
        help="Whether to show verbose output.",
    )
    args = vars(parser.parse_args())
    main(**args)
