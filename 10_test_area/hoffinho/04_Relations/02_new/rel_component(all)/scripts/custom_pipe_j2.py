import random
import pandas as pd
import typer
from pathlib import Path
import spacy
from spacy.tokens import DocBin, Doc
#from spacy.training.example import Example
import json

# make the factory work
from rel_pipe import make_relation_extractor, score_relations

# make the config work
from rel_model import create_relation_model, create_classification_layer, create_instances, create_tensors

def main(ner_pipeline="/Users/jhoff/Desktop/model-best-ner", t_p_arg="/Users/jhoff/Desktop/ReciParse_Scripts/10_test_area/hoffinho/04_Relations/02_new/rel_component (arg)/training/model-last", 
t_p_arg0="/Users/jhoff/Desktop/ReciParse_Scripts/10_test_area/hoffinho/04_Relations/02_new/rel_component (arg0)/training/model-last",t_p_arg1="/Users/jhoff/Desktop/ReciParse_Scripts/10_test_area/hoffinho/04_Relations/02_new/rel_component (arg1)/training/model-last", input_data="/Users/jhoff/Desktop/ReciParse_Scripts/10_test_area/hoffinho/04_Relations/02_new/rel_component (all)/assets/input1.json", threshold=0.02):
    
    data = pd.read_json(input_data)["text"].to_list()

    # Load pipelines
    ner_nlp = spacy.load(ner_pipeline)
    rel_a_nlp = spacy.load(t_p_arg)
    rel_a0_nlp = spacy.load(t_p_arg0)
    rel_a1_nlp = spacy.load(t_p_arg1)
    
    ner_docs = []
    for recipe in data:
        print(recipe)
        pred = ner_nlp(recipe)
        ner_docs.append(pred)
    
    ent_dict = {ent.start : {"label": ent.label_, "text": ent} for ent in ner_docs[0].ents}

    for name, proc in rel_a_nlp.pipeline:
        doc_rel_a = proc(ner_docs[0])
    
    for name, proc in rel_a0_nlp.pipeline:
        doc_rel_a0 = proc(ner_docs[0])

    for name, proc in rel_a1_nlp.pipeline:
        doc_rel_a1 = proc(ner_docs[0])

    rel_dict = {ent.start : {"verb": ent, "assigned": []} for ent in ner_docs[0].ents if ent.label_ == "V"}

    for item in doc_rel_a._.rel.items():
        
        #pull rel information
        start_token_head, start_token_child, arg_dict = [item[0][0], item[0][1], item[1]]

        #combine rel information mit entity information
        text_head, labl_head, text_child, labl_child   = [ent_dict[start_token_head]["text"], ent_dict[start_token_head]["label"], ent_dict[start_token_child]["text"], ent_dict[start_token_child]["label"]]

        max_key = max(arg_dict, key=arg_dict.get)
        prob = arg_dict[max_key]

        if max_key == "Arg":
            if prob >= 0.4:
                rel_dict[start_token_head]["assigned"].append((text_child, labl_child, max_key, prob))
        else:
            if prob >= 0.000002:
                rel_dict[start_token_head]["assigned"].append((text_child, labl_child, max_key, prob))
    
    for item in doc_rel_a0._.rel.items():
        
        #pull rel information
        start_token_head, start_token_child, arg_dict = [item[0][0], item[0][1], item[1]]

        #combine rel information mit entity information
        text_head, labl_head, text_child, labl_child   = [ent_dict[start_token_head]["text"], ent_dict[start_token_head]["label"], ent_dict[start_token_child]["text"], ent_dict[start_token_child]["label"]]

        max_key = max(arg_dict, key=arg_dict.get)
        prob = arg_dict[max_key]

        if max_key == "Arg0":
            if prob >= 0.05:
                rel_dict[start_token_head]["assigned"].append((text_child, labl_child, max_key, prob))
        else:
            if prob >= 0.000002:
                rel_dict[start_token_head]["assigned"].append((text_child, labl_child, max_key, prob))

    for item in doc_rel_a1._.rel.items():
        
        #pull rel information
        start_token_head, start_token_child, arg_dict = [item[0][0], item[0][1], item[1]]

        #combine rel information mit entity information
        text_head, labl_head, text_child, labl_child   = [ent_dict[start_token_head]["text"], ent_dict[start_token_head]["label"], ent_dict[start_token_child]["text"], ent_dict[start_token_child]["label"]]

        max_key = max(arg_dict, key=arg_dict.get)
        prob = arg_dict[max_key]

        if max_key == "Arg1":
            if prob >= 0.9:
                rel_dict[start_token_head]["assigned"].append((text_child, labl_child, max_key, prob))
        else:
            if prob >= 0.000002:
                rel_dict[start_token_head]["assigned"].append((text_child, labl_child, max_key, prob))
    
    
    # print(rel_dict)

    for key in rel_dict.keys():
        print(rel_dict[key])

    return


if __name__ == "__main__":
    typer.run(main)