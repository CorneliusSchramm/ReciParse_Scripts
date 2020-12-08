import spacy
from thinc.api import Config
from spacy.lang.en import English

# make the factory work
from rel_pipe import make_relation_extractor, score_relations

# make the config work
from rel_model import create_relation_model, create_classification_layer, create_instances, create_tensors

nlp = spacy.load("/Users/jhoff/Desktop/ReciParse_Scripts/10_test_area/hoffinho/04_Relations/02_new/rel_component_2/trainig/model-best")

print(nlp.pipe_names)

doc = nlp("Hallo das ist ein test")

print(doc._.rel)

confs = nlp.config

print(confs)