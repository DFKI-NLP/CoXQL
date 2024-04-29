GRAMMAR = r"""
?start: action
action: operation done | operation join action | followup done

join: and | or
and: " and"
or: " or"
followup: " followup"
done: " [e]"

operation: adversarial | augment | cfe | data | domain | editlabel | featureattribution | filter | function | influence | keywords | label | learn | likelihood | mistakes | modeldescription | ndatapoints  | predictions | qatutorial | rationalize | score | show | similarity | unlearn

adversarial: " adversarial"

augment: " augment"

cfe: " cfe"

data: dataop
dataop: " data"

domain: " domain"

editlabel: " editlabel"

featureattribution: featureattributionword (allfeaturesword | topk) ( methodflag )
featureattributionword: " nlpattribute"
allfeaturesword: " all"
topk: topkword ( {topkvalues} )
topkword: " topk"
methodflag: " default" | " integrated_gradients" | " attention" | " lime" | " input_x_gradient"

filter: filterword featuretype
filterword: " filter id" | " filter" 
featuretype: {availablefeaturetypes}

function: " function"

keywords: kwword ( {topkvalues} | allfeaturesword )
kwword: " keywords"

influence: influenceword topk
influenceword: " influence"

label: " label"

learn: " learn"

likelihood: " likelihood"

mistakes: mistakesword mistakestypes
mistakesword: " mistake"
mistakestypes: " count" | " sample"

modeldescription: model
model: " model"

ndatapoints: " countdata"

predictions: " predict"

qatutorial : tutorial qaops
tutorial: " qatutorial"
qaops: " qacfe" | " qafa" | " qada" | " qarationale" | " qasim" | " qaadv" | " qainflu" | " qaedit" | " qalearn" | " qaunlearn" 

rationalize: " rationalize"

score: scoreword metricword
scoreword: " score"
metricword: " accuracy" | " f1" | " roc" | " precision" | " recall" 

show: " show"

similarity: similarword ( {topkvalues} )
similarword: " similar"

unlearn: "unlearn"

%import common.WS
%ignore WS
%ignore /\#.*/

"""