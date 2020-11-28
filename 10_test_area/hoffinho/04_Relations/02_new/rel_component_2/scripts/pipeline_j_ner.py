import spacy
from spacy import Language

print(type(Language.factory))

test_sentence = "Den Seeteufel in 2-3 cm große Würfel, den Schnittlauch in feine Röllchen schneiden.Die Butter zerlassen und die Fischwürfel kurz anziehen lassen. Mit Weißwein ablöschen und zugedeckt 2-3 Minuten ziehen lassen."

# load existing spacy model 
nlp = spacy.load("de_core_news_sm")

print(nlp.pipeline)
print(nlp.pipe_names)



