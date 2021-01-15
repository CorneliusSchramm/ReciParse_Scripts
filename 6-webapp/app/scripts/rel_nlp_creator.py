import random
import pandas as pd
import typer
from pathlib import Path
import spacy
from spacy.tokens import DocBin, Doc
from spacy.training.example import Example
import json
import pickle

# make the factory work
from rel_pipe import make_relation_extractor, score_relations

# make the config work
from rel_model import create_relation_model, create_classification_layer, create_instances, create_tensors

def main(trained_pipeline="/Users/jhoff/Universität St.Gallen/STUD-Capstoneproject Tell 6 - Dokumente/General/02-Coding/03-Models/Relations/0-trained-on-djx/model-best"):
    #data = pd.read_json(input_data)["text"].to_list()
    # Load pipelines

    rel_nlp = spacy.load(trained_pipeline)

    with open('rel_nlp.pkl', 'wb') as output:
        pickle.dump(rel_nlp, output, pickle.HIGHEST_PROTOCOL)

    return 

if __name__ == "__main__":
    typer.run(main)