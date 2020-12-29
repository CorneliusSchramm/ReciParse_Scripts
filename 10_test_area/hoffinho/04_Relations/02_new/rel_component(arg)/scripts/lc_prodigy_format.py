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

# input verändern: Ein oder mehrere Rezepte
# nlp pipeline component die tokenized und ner macht

def main(ner_pipeline: Path, trained_pipeline: Path, input_data: Path, threshold: float = 0.99):
    
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
		# for item in pred._.rel.items():
		# 	if item[0][0] in v_list:
		# 		if max(item[1].values()) > threshold:
		# 			print(item[0],max(item[1], key=item[1].get),max(item[1].values()))
		# 		else: 
		# 			print("No probable relation.")

		# Append predicted doc to list of preds_list
		preds_list.append(pred)

		print("Recipe predicted")

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
	for item in preds_list[0]._.rel.items():
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

	return preds_list

if __name__ == "__main__":
    typer.run(main)