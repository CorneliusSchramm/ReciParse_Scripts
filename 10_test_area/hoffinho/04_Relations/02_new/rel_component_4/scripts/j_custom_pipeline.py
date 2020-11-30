import spacy import 
from thinc.api import Config
from spacy.lang.en import English

# make the factory work
from rel_pipe import make_relation_extractor, score_relations

# make the config work
from rel_model import create_relation_model, create_classification_layer, create_instances, create_tensors

nlp = spacy.load("/Users/jhoff/Desktop/ReciParse_Scripts/10_test_area/hoffinho/04_Relations/02_new/rel_component_4/training/model-best")

print(nlp.pipe_names)

doc = nlp("Zwiebeln mit dem scharfen Messer schneiden und zum Curry hinzugeben.")

nlp.update()

for rel in doc._.rel: 
    print(rel)

print(doc.ents)

confs = nlp.config

print(confs)