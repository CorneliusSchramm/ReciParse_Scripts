import random
import typer
from pathlib import Path
import spacy
from spacy.tokens import DocBin, Doc
from spacy.training.example import Example
from spacy.vocab import Vocab
import pickle

# make the factory work
from rel_pipe import make_relation_extractor, score_relations

# make the config work
from rel_model import create_relation_model, create_classification_layer, create_instances, create_tensors


with open('MYDOC.pickle', 'rb') as handle:
    MYDOC = pickle.load(handle)

# print(MYDOC.ents)
nlp = spacy.load(r"C:\Users\CocoL\OneDrive - Universitaet St.Gallen\2-Academics\Bachelor\7-Semester\Capstone\ReciParse_Scripts\10 test_area\Coco\rel_component_2\training\model-best")
# nlp.add_pipe("ner")

# doc1 = nlp("Gemüse in der Pfanne anbraten.")
print(f"Piplines are: {nlp.pipe_names}")
print("ok")

pred = Doc(
            nlp.vocab,
            words=[t.text for t in MYDOC],
            spaces=[t.whitespace_ for t in MYDOC],
        )
pred.ents = MYDOC.ents

for name, proc in nlp.pipeline:
    # print(name,proc)
    pred = proc(pred)

print(pred.ents)
print([t for t in pred])
print([t for t in pred])
i = 0
for value, rel_dict in pred._.rel.items():
    print(value,rel_dict)
    i +=1
    if i == 3:
        break