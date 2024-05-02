import json
import pandas as pd
import requests
from openai import OpenAI
from tqdm import tqdm

skip_api_call = False
API_KEY = "sk-proj-r7YA96Q798RgILhW6Zc8T3BlbkFJKJCWE90s3dhVvoFNMDBM"
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"


class GPTresponses:
    def __init__(self, model: str, temperature: float = 1.0, max_tokens=None):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = OpenAI(
            api_key=API_KEY
        )

    # works with messages (incl. system role)
    def generate_chat_completion(self, messages):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        }

        data = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
        }

        if self.max_tokens is not None:
            data["max_tokens"] = self.max_tokens

        response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")

    # works with prompt
    def get_completion(self, prompt):  # gpt-3.5-turbo
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    gpt = GPTresponses(
        model="gpt-4-0125-preview",
        temperature=0.7
    )

    final_instances = []
    df = pd.read_csv("prompt_data.csv")

    system_prompt = ("In the following, you will read a dialogue between a self-explaining AI and a user who is "
                     "knowledgeable in AI. The self-explaining AI can be requested to talk about the training data, do "
                     "predictions on that data, perform perturbation, and explain the reasoning behind their "
                     "predictions either in natural language or using explainability methods such as feature "
                     "attributions.\n")

    dataset_prompt = {
        "boolq": ("The task at hand is BoolQ, a question answering dataset where, given a passage of text, the answer "
                  "to each question is either 'True' (Yes) or 'False' (No).)\n"),
        "daily_dialog": ("The task at hand is DailyDialog, a dialogue act classification dataset where a turn of a "
                         "dialogue is classified as 'Inform', 'Question', 'Directive', or 'Commissive'.\n"),
        "olid": ("The task at hand is OLID, a hate speech detection dataset where a tweet is classified as 'offensive' "
                 "or 'non-offensive'.\n")
    }

    text_styles = {
        "short_and_easy": "short and easy to understand for non-experts",
        "short_and_complex": "short and written for the AI expert user",
        "elaborate_and_easy": "elaborate and easy to understand for non-experts",
        "elaborate_and_complex": "elaborate and written for the AI expert user",
    }

    for i, instance in tqdm(df.iterrows(), total=len(df)):
        for style_id, style in text_styles.items():
            if not pd.isna(instance[style_id]):
                print(f"Already generated:\n\t{instance[style_id]}\n")
                continue

            instruction = (
                f"You are a rival AI who is tasked to come up with a better response for the last user question. "
                f"It should be based on the dialogue context, {style}.\n"
            )

            # Concatenation of final prompt
            prompt = (system_prompt
                      + dataset_prompt[instance["dataset"]]
                      + instruction + "\n"
                      + "User:\n> " + instance["user_context_1"] + "\n\n"
                      + "AI:\n> " + instance["system_context_1"].replace("\n", "\n> ") + "\n\n"
                      + "User:\n> " + instance["user_context_2"] + "\n\n"
                      + "AI:\n> " + instance["system_context_2"].replace("\n", "\n> ") + "\n\n"
                      + "User:\n> " + instance["user"] + "\n\n"
                      + "AI:\n> " + instance["system"].replace("\n", "\n> ") + "\n\n"
                      + "Rival AI's response:\n> "
                      )
            # Save prompt
            instance[f"prompt_{style_id}"] = prompt

            if not skip_api_call:
                # Inference
                output = gpt.get_completion(prompt)
                generation = output.replace(prompt, '')  # Removing the prompt
                print(f"{generation}")
                instance[style_id] = generation

            # Save output to list
            final_instances.append(instance)

    pd.DataFrame(final_instances).to_csv("results.csv", index=False)
