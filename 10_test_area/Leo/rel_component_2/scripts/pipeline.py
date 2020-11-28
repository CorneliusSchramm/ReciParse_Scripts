# import random
import pandas as pd
import typer
from pathlib import Path
import spacy
# from spacy.tokens import DocBin, Doc
# from spacy.training.example import Example

# make the factory work
from rel_pipe import make_relation_extractor, score_relations

# make the config work
from rel_model import create_relation_model, create_classification_layer, create_instances, create_tensors



def main(ner_pipeline: Path, trained_pipeline: Path, input_data: Path, threshold: float = 0.8):

    # Load input data into a pandas dataframe and convert to list
    data = pd.read_json(input_data)["text"].to_list()
    
    # Load pipelines
    ner_nlp = spacy.load(ner_pipeline)
    rel_nlp = spacy.load(trained_pipeline)

    # Objekt, das alle Docs inklusive Predictions speichert
    preds_list = []

    # Iterate over recipes
    for recipe in data:

        # Get NE predictions
        pred = ner_nlp(recipe)
        # print([(ent, ent.label_, ent.start) for ent in pred.ents])

        # Get Relation predictions
        for name, proc in rel_nlp.pipeline:
            pred = proc(pred)

        # List of start tokens of "V"-entities
        v_list = [ent.start for ent in pred.ents if ent.label_ == "V" ]
        
        # Printing relevant relations
        for item in pred._.rel.items():
            if item[0][0] in v_list:
                if max(item[1].values()) > threshold:
                    print(item[0],max(item[1], key=item[1].get),max(item[1].values()))
                else: 
                    print("No probable relation.")

        # Append predicted doc to list of preds_list
        preds_list.append(pred)

        print("Recipe predicted")

    return preds_list

   

if __name__ == "__main__":
    typer.run(main)