import random
import pandas as pd
import typer
from pathlib import Path
import spacy
from spacy.tokens import DocBin, Doc
from spacy.training.example import Example
import json

# make the factory work
from rel_pipe import make_relation_extractor, score_relations

# make the config work
from rel_model import create_relation_model, create_classification_layer, create_instances, create_tensors

colors_dict = {
	"Arg0": "#c5bdf4",
	"Arg1": "#ffd882",
	"Arg": "#d9fbad",
}


def main(ner_pipeline="/Users/jhoff/Desktop/model-best-ner", trained_pipeline="/Users/jhoff/Desktop/ReciParse_Scripts/10_test_area/hoffinho/04_Relations/02_new/rel_component_all/training/model-best", input_data = "/Users/jhoff/Desktop/ReciParse_Scripts/10_test_area/hoffinho/04_Relations/02_new/rel_component_all/assets/input1.json", threshold=0.02):
    
    data = pd.read_json(input_data)["text"].to_list()
    # Load pipelines
    ner_nlp = spacy.load(ner_pipeline)
    rel_nlp = spacy.load(trained_pipeline)
    
    ner_docs = []
    for recipe in data:
        print(recipe)
        pred = ner_nlp(recipe)
        ner_docs.append(pred)
    
    ent_dict = {ent.start : {"label": ent.label_, "text": ent} for ent in ner_docs[0].ents}
    print(ent_dict)

    for name, proc in rel_nlp.pipeline:
        doc_rel = proc(ner_docs[0])

    rel_dict = {ent.start : {"verb": ent, "assigned": []} for ent in ner_docs[0].ents if ent.label_ == "V"}

    for item in doc_rel._.rel.items():
        
        #pull rel information
        start_token_head, start_token_child, arg_dict = [item[0][0], item[0][1], item[1]]

        #combine rel information mit entity information
        text_head, labl_head, text_child, labl_child   = [ent_dict[start_token_head]["text"], ent_dict[start_token_head]["label"], ent_dict[start_token_child]["text"], ent_dict[start_token_child]["label"]]
        print(item)
        print(text_head)
        max_key = max(arg_dict, key=arg_dict.get)
        prob = arg_dict[max_key]

        if max_key == "Arg0":
            if prob >= 0.02:
                rel_dict[start_token_head]["assigned"].append((text_child, labl_child, max_key, prob))
        elif max_key == "Arg1":
            if prob >= 0.02:
                rel_dict[start_token_head]["assigned"].append((text_child, labl_child, max_key, prob)) 
        else:
            if prob >= 0.000002:
                rel_dict[start_token_head]["assigned"].append((text_child, labl_child, max_key, prob))
    
    # print(rel_dict)

    for key in rel_dict.keys():
        print(rel_dict[key])

    pred = doc_rel

    # PRODIGY OUTPUT -------------------------------------------------------------------------------

	# # Create main output dict for prodigy
    main_dict = {}

	# TEXT KEY
    print("### TEXT ###")
	# print(pred.text)
    main_dict["text"] = pred.text

	# INPUT HASH KEY
    print("### INPUT HASH ###")
	# TASK HASH KEY
    print("### TASK HASH ###")
	# SPANS KEY
    print("### SPANS ###")
    spans = [ {"text": ent.text, 
			   "token_start": ent.start, 
			   "token_end": ent.end-1, 
			   "start": pred[ent.start].idx, 
			   "end": pred[ent.start].idx + len(ent.text), 
			   "label": ent.label_, 
			   "type":"span"} for ent in pred.ents ]
	# print(spans)
    main_dict["spans"] = spans
	
	# TOKENS KEY
    print("### TOKENS  ###")
    tokens = [ {"text": token.text, 
				"start": token.idx, 
				"end": token.idx + len(token.text), 
				"id": token.i, 
				"ws": token.whitespace_, 
				"disabled": None} for token in pred ] # TODO
    for token in tokens:
        if token["ws"] == " ":
            token["ws"] = True
        elif token["ws"] == "":
            token["ws"] = False
	# print(tokens)
    main_dict["tokens"] = tokens
	
	# SESSION ID KEY
    print("### SESSION ID ###")
	# VIEW ID KEY
    print("### VIEW ID ###")
    main_dict["_view_id"] = "relations"

	# RELATIONS KEY
    print("### RELATIONS ###")
    relations = []
    ents_dict = { ent.start: (ent.text, ent.start, ent.end-1, ent.label_) for ent in pred.ents }
    tokens_dict = { token.i: (token.text, token.idx, token.idx+len(token.text)) for token in pred }
	# print([(type(ent.start),ent.start) for ent in pred.ents ])
    print(ents_dict)
    count = 0
    for item in doc_rel._.rel.items():
        if max(item[1].values()) > threshold:
			# print(item)
            count += 1
            print(count)
            
            try:

				# What is the most probable label and how high is the probability
				# print("Maximum Probability:", max(item[1].values()), "for", max(item[1], key=item[1].get))

				# Build relations dict
                relation = dict()
                relation["head"] = item[0][0]
                relation["child"] = item[0][1]
                relation["head_span"] = dict()
                relation["child_span"] = dict()
                relation["color"] = colors_dict[max(item[1], key=item[1].get)]
                relation["label"] = max(item[1], key=item[1].get)
                
                relation["head_span"]["start"] = tokens_dict[item[0][0]][1]
                relation["head_span"]["end"] = tokens_dict[item[0][0]][2]
                relation["head_span"]["token_start"] = item[0][0]
                
                if item[0][0] in ents_dict:
                    relation["head_span"]["token_end"] = ents_dict[item[0][0]][2]
                    relation["head_span"]["label"] = ents_dict[item[0][0]][3]
                else:
                    relation["head_span"]["token_end"] = item[0][0] # Gedanke: Wenn der Token nicht im ents dict ist, ist er nicht markiert, kann also kein span sein und deshalb ist der end token gleich dem start token. Richtig? IDK
                    relation["head_span"]["label"] = None # Weg damit einfach?
                    
                relation["child_span"]["start"] = tokens_dict[item[0][1]][1]
                relation["child_span"]["end"] = tokens_dict[item[0][1]][2]
                relation["child_span"]["token_start"] = item[0][1]
                
                if item[0][1] in ents_dict:
                    relation["child_span"]["token_end"] = ents_dict[item[0][1]][2]
                    relation["child_span"]["label"] = ents_dict[item[0][1]][3]
                else: 
                    relation["child_span"]["token_end"] = item[0][1]
                    relation["child_span"]["label"] = None # Weg damit einfach?

				# print(relation)
                relations.append(relation)
            except(KeyError):
                print("KeyError")
		# break
    main_dict["relations"] = relations
    print(main_dict)
	# with open('/Users/Leonidas/Desktop/rel_component_2/data.json', 'w', encoding='utf-8') as f:
	# 	json.dump(main_dict, f, ensure_ascii=False, indent=4)
    with open('/Users/jhoff/Desktop/Capstone_local/03_Prodigy/03_Review/data.jsonl', 'w', encoding='utf-8') as f:
        json.dump(main_dict, f, ensure_ascii=False)
    
    return doc_rel


if __name__ == "__main__":
    typer.run(main)