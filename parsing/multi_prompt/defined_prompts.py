operation_type_prompt = "Choose one of the following operations: adversarial | augment | cfe | data | countdata| domain | editlabel | nlpattribute | function | influence | keywords | label | learn | likelihood | mistake | model | predict | qacfe | qafa | qada | qarationale | qasim | qaadv | qainflu | qaedit | qalearn | qaunlearn | rationalize | score | show | similar | unlearn\nExamples:\nInput: Provide an adversarial attack for sample 102. Output: adversarial\nInput: Augment id 46. Output: augment\nInput: Generate a counterfactual for id 45. Output: cfe\nInput: What is the counterfactual for this sample? Output: cfe\nInput: Show me a cfe for the sample with id 100. Output: cfe\nInput: How can I flip the prediction for id 1290? Output: cfe\nInput: How do the data look like? Output: data\nInput: What is the dataset? Output: data\nInput: What is the dataset size? Output: countdata\nInput: What is the total number of data samples? Output: countdata\nInput: How many items are present in the dataset? Output: countdata\nInput: What is precision or recall? Output: domain\nInput: What is the meaning of term input gradients? Output: domain\nInput: How does attention work? Output: domain\n Input: What is the definition of ROC score? Output: domain\nInput: Can you explain the meaning of LIME? Output: domain\nInput: Change the label of id 678 to the provided label Output: editlabel\nInput: What are the most important words in the sample 427? Output: nlpattribute\nInput: Show me the token attributions for id 74. Output: filter id 74 and nlpattribute all.\nInput: What are the most important tokens according to the attention scores for id 122? Output: filter id 122 and nlpattribute attention.\nInput: Can you explain this prediction for id 61 with input gradients? Output: filter id 61 and nlpattribute input_x_gradient\nInput: Explain sample 25 with the integrated gradients method. Output: filter id 25 and nlpattribute integrated_gradient\nInput: What can you do? Output: function\nInput: Show me 5 most influential important data instances for id 912. Output: influence\nInput: What are the top 10 keyword tokens? Output: keywords 10\nInput: What are 5 most frequent words in the dataset? Output: keywords 5\nInput: Which labels do we have? Output: label\nInput: What is the label distribution? Output: label\nInput: Train the model again with instance 1789. Output: learn\nInput: How likely is the predicted output for instance 355? Output: likelihood\nInput: Show me some mistakes. Output: mistake sample\nInput: Show me some misclassified points. Output: mistake sample\nInput: Count the number of wrongly predicted points. Output: mistake count\nInput: Show me some samples that were incorrectly predicted Output: mistake sample\nInput: Can you explain me the model? Output: model\nInput: What is the model prediction on id 82? Output: predict\nInput: What's counterfactual operation in NLP? Output: qacfe\nInput: How does counterfactual operation works (in general)? Output: qacfe\nInput: What role does feature attribution play in NLP? Output: qafa\nInput: How does feature attribution work? Output: qafa\nInput: Explain me the data augmentation process Output: qada\nInput: Can you provide an explanation for the data augmentation method in the context of NLP? Output: qada\nInput: What's rationalization in NLP? Output: qarationale\nInput: Explain the rationalization operation Output: qarationale\nInput: What's semantic similarity? Output: qasim\nInput: Definition of semantic similarity? Output: qasim\nInput: Definition of adversarial attack? Output: qaadv\nInput: What is an adversarial attack operation? Output: qaadv\nInput: Can you tell me what influential operation means? Output: qainflu\nInput: What does it mean to check influential samples? Output: qainflu\nInput: What is a label editing operation? Output: qaedit\nInput: Please explain to me how the editing operation works. Output: qaedit\nInput: What does the unlearn operation do? Output: qaunlearn\nInput: What's the meaning of unlearn? Output: qaunlearn\nInput: How does learn operation work? Output: qalearn, \nInput: Can you explain to me the learn operation? Output: qalearn\nInput: Please provide a rationale for id 25. Output: rationalize\nInput: Generate a reasoning chain (explanation) for id 44 in natural language. Output: rationalize\nInput: Please tell me about the accuracy scores. Output: score accuracy\nInput: What is the roc score for these data? Output: score roc\nInput: Compute f1 on the data Output: score f1\nInput: Show id 22 Output: showInput: Can you show me data with id 124? Output: show\nInput: Show me five more instances that are like id 28. Output: similar 5\nInput: Show me 3 samples that are similar to id 42. Output: similar 3\nInput: Please remove instance 30 from the model. Output: unlearn\nPlease choose only one operation from the list separated by bars, pay attention to similar operations (e.g., data vs countdata): adversarial | augment | cfe | data | countdata | domain | editlabel | nlpattribute | function | influence | keywords | label | learn | likelihood | mistake | model | predict | qacfe | qafa | qada | qarationale | qasim | qaadv | qainflu | qaedit | qalearn | qaunlearn | rationalize | score | show | similar | unlearn"  # Select one operation from this list for the user input

valid_operation_names = [
    "adversarial",
    "augment",
    "cfe",
    "data",
    "countdata",
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
    "do an adversarial attack",
    "perform data augmentation",
    "generate counterfactual",
    "provide dataset details",
    "show number of data points in the dataset",
    "explain domain-related terminology",
    "edit label",
    "show feature importance and token attribution (e.g., with attention, lime or integrated gradients)",
    "what is functionality",
    "what are the most influential samples for a specific instance",
    "show keywords",
    "show labels",
    "train model again with a new sample",
    "show likelihood of the prediction",
    "count or show mistakes",
    "explain model",
    "show what model predicts for this sample",
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
    "provide natural language rationale",
    "show scores for evaluating model performance: accuracy, f1, precision, recall, roc",
    "show sample given the id",
    "show similar samples from the dataset",
    "remove sample, unlearn it",
]

valid_operation_prompt_samples = {
    "adversarial": [
        "Show me an adversarial example given id 14.",
        "What is the result of an adversarial attack on id 187?",
    ],
    "augment": [
        "Please augment id 25",
        "Please create a new instance based on id 50",
        "Starting from id 75, how would a new instance look like?",
    ],
    "cfe": [
        "What does instance with id 22 need to do to change the prediction?",
        "show me cfe's for the instance with id 22",
        "How would you flip the prediction for id 23?",
        "How do I change the prediction for the data point with id number 34?",
        "What is the way to change the prediction for the data point with the id number 422?",
        "Could you please tell me the predictions for id 5132 and what you have to do to flip the prediction?",
    ],
    "data": ["How does the dataset look like?", "What are the data?"],
    "countdata": [
        "How many data points are in the dataset?",
        "What is the number of instances in the dataset?",
    ],
    "domain": [
        "What is the meaning of LIME?",
        "How dos attention work?",
        "What is precision? How is it calculated?",
        "How do you calculate f1 score?",
        "What is the meaning of roc score?",
        "What are integrated gradients?",
    ],
    "editlabel": ["Please change the label for id 1999", "I want to modify the label for id 825"],
    "nlpattribute": [
        "show most important features for data point 1000",
        "explain id 15 using lime",
        "why do you predict instance with id 987 this way, can you explain it using the input gradients?",
        "10 most important features for id's 5 regarding attention",
        "Why does the model predict id 178 like this? How does the attention-based explanation look like? Show me the top 5 features",
        "what three features most influence the model's predictions for ids 1515 using lime",
        "Show me the key seven features for id 799 using attention for token attribution.",
        "What are the importance scores for id 42 using attention?",
        "what are the top 10 important features for id 20?",
        "I would like to see feature importances for id 121 with attention",
    ],
    "function": ["What is the functionality?", "Which functions do you support?"],
    "influence": [
        "Show me top 10 most influential sample in the dataset given id 68",
        "What is the most important training sample for id 62?",
        "Show me 5 most important instances for data point 42?",
    ],
    "keywords": [
        "What are the most frequent keywords in the data?",
        "Keywords",
        "What are the three most frequent keywords?",
        "Which five words occur most often in the data?",
        "Which word occur least in the data?",
    ],
    "label": ["What are the labels in the data?", "Show me the dataset labels."],
    "learn": [
        "Do the training again with instance id 90.",
        "Re-train the model with id 6223",
        "Finetune the model with id 144.",
    ],
    "likelihood": [
        "Show me the confidence score for id 1688.",
        "What is the likelihood of the models prediction for id 7?",
    ],
    "mistake": [
        "can you show me how much data the model predicts incorrectly?",
        "tell me the amount of data the model predicts incorrectly",
        "How many misclassified instances do we have?",
        "could you count incorrectly predicted points?",
        "How frequently does the model make mistakes?",
        "how many misclassified data points do we have?",
        "show me the number of data points the model predicts inaccurately?",
        "Give me some misclassified data points",
        "show me data the model gets wrong",
        "what are some instances that are classified in a wrong way?",
        "show me a few examples from the data that are misclassified",
        "show me some incorrectly classified examples",
    ],
    "model": ["What is the model?", "What model is used?"],
    "predict": [
        "What do you predict for 215?",
        "What is the prediction for data point number 9130?",
        "For id 776, please provide the prediction.",
        "predict 320",
        "return prediction id 13423",
        "please display the prediction of the instance with id 34",
    ],
    "qacfe": ["What is a counterfactual?"],
    "qafa": ["What is feature or token attribution?"],
    "qada": ["How does data augmentation work?"],
    "qarationale": ["What is rationalization?"],
    "qasim": ["What is a smiliarity operation?"],
    "qaadv": ["What is the meaning of adversarial attack?"],
    "qainflu": ["What does it mean to have influence operation?"],
    "qaedit": ["What does label editing do?"],
    "qalearn": ["What is the meaning of learn operation?"],
    "qaunlearn": ["What does unlearn operation do?"],
    "rationalize": [
        "explain id 150 in natural language",
        "explain id 6390 with rationale",
        "generate a natural language explanation for id 2222",
        "rationalize the prediction for id 9555",
    ],
    "score": [
        "give me the accuracy on the data",
        "could you give me the test accuracy on the training data?",
        "how often are you correct?",
        "what's the rate you do correct predictions?",
        "how accurate is the model on all the data?",
        "nice! could you give me the test f1?",
        "display score",
        "testing f1",
        "I meant what is the f1 score on the evaluation data",
        "What is the micro-F1 score?",
        "What is the macro-F1 score?",
        "What is the weighted F1 score?",
        "can you show me the precision on the data?",
        "What is the micro precision?",
        "What is the macro score for precision?",
        "Please compute the weighted precision.",
        "give the recall score",
        "What is the micro recall?",
        "What is the weighted recall?",
        "can you show me the roc score on the testing data?",
        "what's the roc score",
        "show me the roc score, please",
    ],
    "show": [
        "Can you display the instance with id 2451?",
        "For 3315, please show me the values of the features.",
        "Could you show me data point number 215?",
        "Show id 105111, please.",
        "What text does id 278 have?",
    ],
    "similar": [
        "Please retrieve four examples that are similar to ID 50",
        "Could you give me 10 analogous data points to ID 75.",
        "I'm looking for a case that is akin to id 14. Could you help me with that?",
        "Show 3 similar instances for ID 25.",
        "Can you bring up 6 instances that share similarities with ID 35?",
        "Could you locate 5 comparable data points to ID 75 for me?",
        "Show 5 similar instances for id 61",
        "Demonstrate the most similar datapoint for id 28.",
        "Show me 10 instances related to ID 2264",
        "Can you show me 7 data points most similar to ID 78",
    ],
    "unlearn": [
        "Remove sample 142 from the training set.",
        "Delete instance 7992 from the training data",
    ],
}

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
    "score": ["accuracy", "f1", "micro", "macro", "weighted", "precision", "recall", "roc"],
    "influence": ["topk"],
}

operation2types = {
    "nlpattribute": [
        "input_x_gradient",
        "integrated_gradients",
        "lime",
        "attention",
    ]
}

operations_wo_attributes = ["data", "countdata", "domain", "function", "label", "model"]
topk_operations = ["nlpattribute", "influence"]

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

operations_with_default = ["nlpattribute"]
operations_with_number = ["similar"]
operations_with_topk_number = ["influence"]

# add "\nInput: input text Output:" at the end of each prompt
nlpattribute_prompt = "Please parse the input as shown in the examples:\nInput: show most important features for data point 1000 Output: filter id 1000 and nlpattribute all default [E]\nInput: explain id 15 using lime Output: filter id 15 and nlpattribute lime [E]\nInput: why do you predict instance with id 987 this way, can you explain it using the input gradients? Output: filter id 987 and nlpattribute input_x_gradient [E]\nInput: 10 most important features for id's 5 regarding attention Output: filter id 5 and nlpattribute topk 10 attention [E]\nInput: Why does the model predict id 178 like this? How does the attention-based explanation look like? Show me the top 5 features Output: filter id 178 and nlpattribute topk 5 attention [E]\nInput: what three features most influence the model's predictions for ids 1515 using lime Output: filter id 1515 and nlpattribute topk 3 lime [E]\nShow me the key seven features for id 799 using attention for token attribution. Output: filter id 799 and nlpattribute topk 7 attention [E]\nInput: What are the importance scores for id 42 using attention? Output: filter id 42 and nlpattribute all attention [E]\nInput: what are the top 10 important features for id 20?\nOutput: filter id 20 and nlpattribute topk 10 default [E]\nInput: I would like to see feature importances for id 121 with attention\nOutput: filter id 121 and nlpattribute all attention [E]"

rationalize_prompt = "Please parse the input as shown in the examples:\nInput: explain id 150 in natural language Output: filter id 150 and rationalize [E]\nInput: explain id 6390 with rationale Output: filter id 6390 and rationalize [E]\nInput: generate a natural language explanation for id 2222 Output: filter id 2222 and rationalize [E]\nInput: rationalize the prediction for id 9555 Output: filter id 9555 and rationalize [E]"

show_prompt = "Please parse the input as shown in the examples:\nInput: Can you display the instance with id 2451? Output: filter id 2451 and show [E]\nInput: For 3315, please show me the values of the features. Output: filter id 3315 and show [E]\nInput: Could you show me data point number 215? Output: filter id 215 and show [E]\nInput: Show id 105111, please. Output: filter id 105111 and show [E]\nInput: What text does id 278 have? Output: filter id 278 and show [E]"

keywords_prompt = "Please parse the input as shown in the examples:\nInput: What are the most frequent keywords in the data? Output: keywords all [E]\nInput: Keywords Output: keywords all most [E]\nInput: What are the three most frequent keywords? Output: keywords 3 [E]\nInput: Which five words occur most often in the data? Output: keywords 5 [E]\nInput: Which word occur least in the data? Output: keywords 1 least [E]"

similar_prompt = "Please parse the input as shown in the examples:\nInput: Please retrieve four examples that are similar to ID 50 Output: filter id 50 and similar 4 [E]\nInput: Could you give me 10 analogous data points to ID 75. Output: filter id 75 and similar 10 [E]\nInput: I'm looking for a case that is akin to id 14. Could you help me with that? Output: filter id 14 and similar 1 [E]\nInput: Show 3 similar instances for ID 25. Output: filter id 25 and similar 3 [E]\nInput: Can you bring up 6 instances that share similarities with ID 35? Output: filter id 35 and similar 6 [E]\nInput: Could you locate 5 comparable data points to ID 75 for me? Output: filter id 75 and similar 5 [E]\nInput: Show 5 similar instances for id 61 Output: filter id 61 and similar 5 [E]\nInput: Demonstrate the most similar datapoint for id 28. Output: filter id 28 and similar 1 [E]\nInput: Show me 10 instances related to ID 2264 Output: filter id 2264 and similar 10 [E]\nInput: Can you show me 7 data points most similar to ID 78 Output: filter id 78 and similar 7 [E]"

augment_prompt = "Please parse the input as shown in the examples:\nInput: Please augment id 25 Output: filter id 25 and augment [E]\nInput: Please create a new instance based on id 50 Output: filter id 50 and augment [E]\nInput: Starting from id 75, how would a new instance look like? Output: filter id 75 and augment [E]"

cfe_prompt = "Please parse the input as shown in the examples:\nInput: What does instance with id 22 need to do to change the prediction? Output: filter id 22 and cfe [E]\nInput: show me cfe's for the instance with id 22 Output: filter id 22 and cfe [E]\nInput: How would you flip the prediction for id 23? Output: filter id 23 and cfe [E]\nInput: How do I change the prediction for the data point with id number 34? Output: filter id 34 and cfe [E]\nInput: What is the way to change the prediction for the data point with the id number 422? Output: filter id 422 and cfe [E]\nInput: Could you please tell me the predictions for id 5132 and what you have to do to flip the prediction? Output: filter id 54 and predict and cfe [E]"

mistake_prompt = "There are two labels: 'mistake count' and 'mistake sample'. Note that mistake count corresponds to questions about the amount of misclassified instances and mistake sample corresponds to questions about the specific examples of misclassified samples. Please parse the input as shown in the examples:\nInput: can you show me how much data the model predicts incorrectly? Output: mistake count [E]\nInput: tell me the amount of data the model predicts incorrectly Output: mistake count [E]\nInput: How many misclassified instances do we have? Output: mistake count [E]\nInput: could you count incorrectly predicted points? Output: mistake count [E]\nInput: How frequently does the model make mistakes? Output: mistake count [E]\nInput: how many misclassified data points do we have? Output: mistake count [E]\nInput: show me the number of data points the model predicts inaccurately? Output: mistake count [E]\nInput: Give me some misclassified data points Output: mistake sample [E]\nInput: show me data the model gets wrong Output: mistake sample [E]\nInput: what are some instances that are classified in a wrong way? Output: mistake sample [E]\nInput: show me a few examples from the data that are misclassified Output: mistake sample [E]\nInput: show me some incorrectly classified examples Output: mistake sample [E]"

predict_prompt = "Please parse the input as shown in the examples:\nInput: What do you predict for 215? Output: filter id 215 and predict [E]\nInput: What is the prediction for data point number 9130? Output: filter id 9130 and predict [E]\nInput: For id 776, please provide the prediction. Output: filter id 776 and predict [E]\nInput: predict 320 Output: filter id 320 and predict [E]\nInput: return prediction id 13423 Output: filter id 13423 and predict [E]\nInput: please display the prediction of the instance with id 34 Output: filter id 34 and predict [E]"

score_prompt = "Note that score corresponds to accuracy, f1, precision, recall or roc. Please parse the input as shown in the examples:\nInput: testing accuracy Output: score accuracy [E]\nInput: give me the accuracy on the data Output: score accuracy [E]\nInput: could you give me the test accuracy on the training data? Output: score accuracy [E]\nInput: how often are you correct? Output: score accuracy [E]\nInput: what's the rate you do correct predictions? Output: score accuracy [E]\nInput: how accurate is the model on all the data? Output: score accuracy [E]\nInput: nice! could you give me the test f1? Output: score accuracy f1 [E]\nInput: display score Output: score default [E]\nInput: testing f1 Output: score f1 [E]\nInput: I meant what is the f1 score on the evaluation data Output: score f1 [E]\nInput: What is the micro-F1 score? Output: score f1 micro [E]\nInput: What is the macro-F1 score? Output: score f1 macro [E]\nInput: What is the weighted F1 score? Output: score f1 weighted [E]\nInput: can you show me the precision on the data? Output: score precision [E]\nInput: What is the micro precision? Output: score precision micro [E]\nInput: What is the macro score for precision? Output: score precision macro [E]\nInput: Please compute the weighted precision. Output: score precision weighted [E]\nInput: give the recall score Output: score recall [E]\nInput: What is the micro recall? Output: score recall micro [E]\nInput: What is the macro recall? Output: score recall macro [E]\nInput: What is the weighted recall? Output: score recall weighted [E]\nInput: can you show me the roc score on the testing data? Output: score roc [E]\nInput: what's the roc score Output: score roc [E]\nInput: show me the roc score, please Output: score roc [E]"

adversarial_prompt = "Please parse the input as shown in the examples:\nInput: Show me an adversarial example given id 14. Output: filter id 14 and adversarial [E]\nInput: What is the result of an adversarial attack on id 187? Output: filter id 14 and adversarial 187 [E]"

editlabel_prompt = "Please parse the input as shown in the examples:\nInput: Please change the label for id 1999 Output: filter id 1999 and editlabel [E]\nInput: I want to modify the label for id 825 Output: filter id 825 and editlabel [E]"

influence_prompt = "Please parse the input as shown in the examples:\nInput: Show me top 10 most influential sample in the dataset given id 68 Output: filter id 68 and influence topk 10 [E]\nInput: What is the most important training sample for id 62? Output: filter id 62 and influence topk 1 [E]\nInput: Show me 5 most important instances for data point 42? Output: filter id 42 and influence topk 5 [E]"

likelihood_prompt = "Please parse the input as shown in the examples:\nInput: Show me the confidence score for id 1688. Output: filter id 1688 and likelihood [E]\nInput: What is the likelihood of the models prediction for id 7? Output: filter id 7 and likelihood [E]"

learn_prompt = "Please parse the input as shown in the examples:\nInput: Do the training again with instance id 90. Output: filter id 90 and learn [E]\nInput: Re-train the model with id 6223 Output: filter id 6223 and learn [E]\nInput: Finetune the model with id 144. Output: filter id 144 and learn [E]"

unlearn_prompt = "Please parse the input as shown in the examples:\nInput: Remove sample 142 from the training set. Output: filter id 142 and unlearn [E]\nInput: Delete instance 7992 from the training data Output: filter id 7992 and unlearn [E]"

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
