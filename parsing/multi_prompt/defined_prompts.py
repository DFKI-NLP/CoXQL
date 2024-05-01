operation_type_prompt = "Choose one of the following operations: adversarial | augment | cfe | data | domain | editlabel | nlpattribute | function | influence | keywords | label | learn | likelihood | mistake | model | countdata | predict | qacfe | qafa | qada | qarationale | qasim | qaadv | qainflu | qaedit | qalearn | qaunlearn | rationalize | score | show | similar | unlearn\nExamples:\nInput: Provide an adversarial attack for sample 102. Output: adversarial\nInput: Augment id 46. Output: augment\nInput: Generate a counterfactual for id 45. Output: cfe\nInput: What is the counterfactual for this sample? Output: cfe\nInput: Show me a cfe for the sample with id 100. Output: cfe\nInput: How can I flip the prediction for id 1290? Output: cfe\nInput: What are the data? Output: data\nInput: Can you explain some terminology relevant for this domain? Output: domain\nInput: Change the label of id 678 to the provided label Output: editlabel\nInput: What are the most important words in the sample 427? Output: nlpattribute\nInput: Show me the token attributions for id 74. Output: filter id 74 and nlpattribute all.\nInput: What are the most important tokens according to the attention scores for id 122? Output: filter id 122 and nlpattribute attention.\nInput: Can you explain this prediction for id 61 with input gradients? Output: filter id 61 and nlpattribute input_x_gradient\nInput: Explain sample 25 with the integrated gradients method. Output: filter id 25 and nlpattribute integrated_gradient\nInput: What can you do? Output: function\nInput: Show the most influential important data instance for id 912. Output: influence\nInput: What are the top keyword tokens? Output: keywords\nInput: What are the most common keywords in the data? Output: keywords\nInput: Which labels do we have? Output: label\nInput: Train the model again with instance 1789. Output: learn\nInput: How likely is the predicted output for instance 355? Output: likelihood\nInput: Show me some mistakes. Output: mistake\nInput: Can you explain me the model? Output: model\nInput: How many data points are in the dataset? Output: countdata\nInput: What is the model prediction on id 82? Output: predict\nInput: What's counterfactual operation in NLP? Output: qacfe\nInput: How does counterfactual operation works (in general)? Output: qacfe\nInput: What role does feature attribution play in NLP? Output: qafa\nInput: How does feature attribution work? Output: qafa\nInput: Explain me the data augmentation process Output: qada\nInput: Can you provide an explanation for the data augmentation method in the context of NLP? Output: qada\nInput: What's rationalization in NLP? Output: qarationale\nInput: Explain the rationalization operation Output: qarationale\nInput: What's semantic similarity? Output: qasim\nInput: Definition of semantic similarity? Output: qasim\nInput: Definition of adversarial attack? Output: qaadv\nInput: What is an adversarial attack operation? Output: qaadv\nInput: Can you tell me what influential operation means? Output: qainflu\nInput: What does it mean to check influential samples? Output: qainflu\nInput: What is a label editing operation? Output: qaedit\nInput: Please explain to me how the editing operation works. Output: qaedit\nInput: What does the unlearn operation do? Output: qaunlearn\nInput: What's the meaning of unlearn? Output: qaunlearn\nInput: How does learn operation work? Output: qalearn, \nInput: Can you explain to me the learn operation? Output: qalearn\nInput: Please provide a rationale for id 25. Output: rationalize\nInput: Please tell me about the accuracy scores. Output: score\nInput: Show id 22 Output: show\nInput: Show me another instance that is similar to id 148. Output: similar\nInput: Please remove instance 30 from the model. Output: unlearn\nPlease choose only one operation from the list separated by bars: adversarial | augment | cfe | data | domain | editlabel | nlpattribute | function | influence | keywords | label | learn | likelihood | mistake | model | countdata | predict | qacfe | qafa | qada | qarationale | qasim | qaadv | qainflu | qaedit | qalearn | qaunlearn | rationalize | score | show | similar | unlearn"  # Select one operation from this list for the user input

valid_operation_names = [
    "adversarial",
    "augment",
    "cfe",
    "data",
    "domain",
    "editlabel",
    "nlpattribute",
    "function",
    "influence",
    "keywords",
    "label",
    "learn",
    "likelihood",
    "mistake",
    "model",
    "countdata",
    "predict",
    "qacfe",
    "qafa",
    "qada",
    "qarationale",
    "qasim",
    "qaadv",
    "qainflu",
    "qaedit",
    "qalearn",
    "qaunlearn",
    "rationalize",
    "score",
    "show",
    "similar",
    "unlearn",
]

valid_operation_meanings = [
    "adversarial attack",
    "data augmentation",
    "counterfactual",
    "dataset",
    "domain terminology",
    "editing label",
    "feature importance, token attribution",
    "functionality",
    "influential samples",
    "keywords",
    "labels",
    "training with a new sample",
    "prediction likelihood",
    "count or show mistakes",
    "explain model",
    "number of data points",
    "model prediction",
    "explain how counterfactuals work",
    "explain how feature and token attribution works",
    "explain how data augmentation works",
    "explain how rationalization works",
    "explain how similarity operation works",
    "explain how adversarial attack works",
    "explain how influential operation works",
    "explain how label editing works",
    "explain how learn operation works",
    "explain how unlearn operation works",
    "rationalization",
    "accuracy, f1, precision, recall scores",
    "show sample",
    "show similar samples",
    "remove sample, unlearn it",
]

valid_operation_prompt_samples = [
    "Show me an adversarial attack",
    "Can you perform data augmentation for id 9555?",
    "Please find a counterfactual for id 110.",
    "Explain to me the dataset, please",
    "Could you tell me more about this domain and its terminology?",
    "Please modify this label",
    "What are the most attributed tokens for id 122?",
    "What is the function of this application?",
    "What are the most influential samples in the data?",
    "Top 10 keywords in the data.",
    "Which labels do we have?",
    "Please fine-tune the model with the new instance",
    "What is the likelihood of the prediction for id 57?",
    "What are the mistakes that the model makes?",
    "What is the underlying model?",
    "How many samples do we have in this dataset?",
    "Can you show me the prediction that the model makes on id 77?",
    "Can you explain me how exactly this operation works?",
    "How does counterfactual operation works (in general)?",
    "What role does feature attribution play in NLP?",
    "Explain me the data augmentation process",
    "Explain the rationalization operation",
    "What's semantic similarity?",
    "What is an adversarial attack operation?",
    "Can you tell me what influential operation means?",
    "What is a label editing operation?",
    "What does the unlearn operation do?",
    "Can you explain to me the learn operation?",
    "Can you provide a rationale for id 489?",
    "What are the scores?",
    "Please show sample number 15.",
    "What are other similar examples for id 92?",
    "Please exclude sample 72 from the model",
]

operation2attributes = {
    "nlpattribute": [
        "all",
        "topk",
        "input_x_gradient",
        "integrated_gradients",
        "lime",
        "attention",
    ],
    "keywords": ["all"],
    "mistake": ["count", "sample"],
    "score": ["accuracy", "f1", "micro", "macro", "weighted", "precision", "recall"],
    "influence": ["topk"],
}

operations_wo_attributes = ["data", "domain", "function", "label", "model", "countdata"]

tutorial_operations = [
    "qacfe",
    "qafa",
    "qada",
    "qarationale",
    "qasim",
    "qaadv",
    "qainflu",
    "qaedit",
    "qalearn",
    "qaunlearn",
]

tutorial2operation = {
    "qacfe": "cfe",
    "qafa": "nlpattribute",
    "qada": "augment",
    "qarationale": "rationalize",
    "qasim": "similar",
    "qaadv": "adversarial",
    "qainflu": "influence",
    "qaedit": "editlabel",
    "qalearn": "learn",
    "qaunlearn": "unlearn",
}

operation2tutorial = {v: k for k, v in tutorial2operation.items()}

# add "\nInput: input text Output:" at the end of each prompt
nlpattribute_prompt = "Please parse the input as shown in the examples:\nInput: most important features for data point 1000 Output: filter id 1000 and nlpattribute all [E]\nInput: explain id 15 using lime Output: filter id 15 and nlpattribute lime [E]\nInput: why do you predict instance with id 987 this way, can you explain it using the input gradients? Output: filter id 987 and nlpattribute input_x_gradient [E]\nInput: 10 most important features for id's 5 regarding attention Output: filter id 5 and nlpattribute topk 10 attention [E]\nInput: Why does the model predict id 178 like this? How does the attention-based explanation look like? Show me the top 5 features Output: filter id 178 and nlpattribute topk 5 attention [E]\nInput: what three features most influence the model's predictions for ids 1515 using lime Output: filter id 1515 and nlpattribute topk 3 lime [E]\nShow me the key seven features for id 799 using attention for token attribution. Output: filter id 799 and nlpattribute topk 7 attention [E]"

rationalize_prompt = "Please parse the input as shown in the examples:\nInput: explain id 150 in natural language Output: filter id 150 and rationalize [E]\nInput: explain id 6390 with rationale Output: filter id 6390 and rationalize [E]\nInput: generate a natural language explanation for id 2222 Output: filter id 2222 and rationalize [E]\nInput: rationalize the prediction for id 9555 Output: filter id 9555 and rationalize [E]"

show_prompt = "Please parse the input as shown in the examples:\nInput: Can you display the instance with id 2451? Output: filter id 2451 and show [E]\nInput: For 3315, please show me the values of the features. Output: filter id 3315 and show [E]\nInput: Could you show me data point number 215? Output: filter id 215 and show [E]\nInput: Show id 105111, please. Output: filter id 105111 and show [E]"

keywords_prompt = "Please parse the input as shown in the examples:\nInput: What are the most frequent keywords in the data? Output: keywords all [E]\nInput: Keywords Output: keywords all most [E]\nInput: What are the three most frequent keywords? Output: keywords 3 [E]\nInput: Which five words occur the most in the data? Output: keywords 5 [E]\nInput: Which word occur least in the data? Output: keywords 1 least [E]"

similar_prompt = "Please parse the input as shown in the examples:\nInput: Please retrieve an example that is similar to ID 50 Output: filter id 50 and similar 1 [E]\nInput: Could you give me an analogous data point to ID 75. Output: filter id 75 and similar 1 [E]\nInput: I'm looking for a case that is akin to id 14. Could you help me with that? Output: filter id 14 and similar 1 [E]\nInput: Show 3 similar instances to ID 25. Output: filter id 25 and similar 3 [E]\nInput: Can you bring up 3 instances that shares similarities with ID 35? Output: filter id 35 and similar 3 [E]\nInput: Could you locate 6 comparable data point to ID 75 for me? Output: filter id 75 and similar 6 [E]"

augment_prompt = "Please parse the input as shown in the examples:\nInput: Please augment id 25 Output: filter id 25 and augment [E]\nInput: Please create a new instance based on id 50 Output: filter id 50 and augment [E]\nInput: Starting from id 75, how would a new instance look like? Output: filter id 75 and augment [E]"

cfe_prompt = "Please parse the input as shown in the examples:\nInput: What does instance with id 22 need to do to change the prediction? Output: filter id 22 and cfe [E]\nInput: show me cfe's for the instance with id 22 Output: filter id 22 and cfe [E]\nInput: How would you flip the prediction for id 23? Output: filter id 23 and cfe [E]\nInput: How do I change the prediction for the data point with id number 34? Output: filter id 34 and cfe [E]\nInput: What is the way to change the prediction for the data point with the id number 422? Output: filter id 422 and cfe [E]\nInput: Could you please tell me the predictions for id 5132 and what you have to do to flip the prediction? Output: filter id 54 and predict and cfe [E]"

mistake_prompt = "Please parse the input as shown in the examples:\nInput: can you show me how much data the model predicts incorrectly? Output: mistake count [E]\nInput: tell me the amount of data the model predicts falsely Output: mistake count [E]\nInput: How frequently does the model make mistakes? Output: mistake count [E]\nInput: show me the number of data points the model forecasts inaccurately? Output: mistake count [E]\nInput: show me data the model gets wrong Output: mistake sample [E]\nInput: what are some data points you get incorrect? Output: mistake sample [E]\nInput: could you show me a few examples of data that you get wrong? Output: mistake sample [E]"

predict_prompt = "Please parse the input as shown in the examples:\nInput: What do you predict for 215? Output: filter id 215 and predict [E]\nInput: What is the prediction for data point number 9130? Output: filter id 9130 and predict [E]\nInput: For id 776, please provide the prediction. Output: filter id 776 and predict [E]\nInput: predict 320 Output: filter id 320 and predict [E]\nInput: return prediction id 13423 Output: filter id 13423 and predict [E]\nInput: please display the prediction of the instance with id 34 Output: filter id 34 and predict [E]"

score_prompt = "Please parse the input as shown in the examples:\nInput: testing accuracy Output: score accuracy [E]\nInput: give me the accuracy on the data Output: score accuracy [E]\nInput: could you give me the test accuracy on the training data? Output: score accuracy [E]\nInput: how often are you correct? Output: score accuracy [E]\nInput: what's the rate you do correct predictions? Output: score accuracy [E]\nInput: how accurate is the model on all the data? Output: score accuracy [E]\nInput: nice! could you give me the test f1? Output: score accuracy f1 [E]\nInput: display score Output: score default [E]\nInput: testing f1 Output: score f1 [E]\nInput: I meant what is the f1 score on the evaluation data Output: score f1 [E]\nInput: What is the micro-F1 score? Output: score f1 micro [E]\nInput: What is the macro-F1 score? Output: score f1 macro [E]\nInput: What is the weighted F1 score? Output: score f1 weighted [E]\nInput: can you show me the precision on the data? Output: score precision [E]\nInput: What is the micro precision? Output: score precision micro [E]\nInput: What is the macro score for precision? Output: score precision macro [E]\nInput: Please compute the weighted precision. Output: score precision weighted [E]\nInput: give the recall score Output: score recall [E]\nInput: What is the micro recall? Output: score recall micro [E]\nInput: What is the macro recall? Output: score recall macro [E]\nInput: What is the weighted recall? Output: score recall weighted [E]\nInput: can you show me the roc score on the testing data? Output: score roc [E]\nInput: what's the roc score Output: score roc [E]"

adversarial_prompt = "Please parse the input as shown in the examples:\nInput: Show me an adversarial example given id 14. Output: filter id 14 and adversarial [E]\nInput: What is the result of an adversarial attack on id 187? Output: filter id 14 and adversarial 187 [E]"

editlabel_prompt = "Please change the label for id 1999 Output: filter id 1999 and editlabel [E]\nInput: I want to modify the label for id 825 Output: filter id 825 and editlabel [E]"

influence_prompt = "Show me top 10 most influential sample in the dataset given id 68 Output: filter id 68 and influence topk 10 [E]\nInput: What is the most important training sample for id 62? Output: filter id 62 and influence topk 1 [E]"

likelihood_prompt = "Show me the confidence score for id 1688. Output: filter id 1688 and likelihood [E]\nInput: What is the likelihood of the models prediction for id 7? Output: filter id 7 and likelihood [E]"

learn_prompt = "Do the training again with instance id 90. Output: filter id 90 and learn [E]\nInput: Re-train the model with id 6223 Output: filter id 6223 and learn [E]"

unlearn_prompt = "Remove sample 142 from the training set. Output: filter id 142 and unlearn [E]\nInput: Delete instance 7992 from the training data Output: filter id 7992 and unlearn [E]"

operation2prompt = {
    "nlpattribute": nlpattribute_prompt,
    "rationalize": rationalize_prompt,
    "show": show_prompt,
    "keywords": keywords_prompt,
    "similar": similar_prompt,
    "augment": augment_prompt,
    "cfe": cfe_prompt,
    "mistake": mistake_prompt,
    "predict": predict_prompt,
    "score": score_prompt,
    "adversarial": adversarial_prompt,
    "editlabel": editlabel_prompt,
    "influence": influence_prompt,
    "likelihood": likelihood_prompt,
    "learn": learn_prompt,
    "unlearn": unlearn_prompt,
}

operation_needs_id = [
    "nlpattribute",
    "rationalize",
    "show",
    "similar",
    "augment",
    "cfe",
    "predict",
    "adversarial",
    "editlabel",
    "influence",
    "likelihood",
    "learn",
    "unlearn",
]
