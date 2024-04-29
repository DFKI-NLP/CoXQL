# Local Explanation
| File name       | Function                          | Grammar                  | Additional Attributes                                                  | Description     |
|-----------------|-----------------------------------|--------------------------|------------------------------------------------------------------------|-----------------| 
| attribute.txt   | attribute(instance, topk, method) | nlpattribute topk method | topk, default, attention, lime, input_x_gradient, integrated_gradients | Provide feature attribution scores |
| incluence.txt   | incluence(instance, topk)         | influence topk           | topk                                                                   | Provide the most influential training data instances |
| rationalize.txt | rationalize(instance)             | rationalize                    | -                                                                      | Explain the output/decision in natural language|
