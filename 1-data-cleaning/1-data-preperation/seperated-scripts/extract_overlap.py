import pandas as pd
import json
import sys
import numpy


# Pfäde über Terminal Input 
input_path = sys.argv[1] #JSON aus dem Overlap extrahiert werden soll
output_path = sys.argv[2] #Pfad wohin neues JSON gespeichert werden soll
overlap_path = sys.argv[3] #Pfad zum overlap.json

#input_path = "/Users/jonathanebner/Universität St.Gallen/STUD-Capstoneproject Tell 6 - General/02-Coding/01-Data/12_annotated_batches/batch1_jonathan.jsonl"
#output_path = "/Users/jonathanebner/Universität St.Gallen/STUD-Capstoneproject Tell 6 - General/02-Coding/01-Data/20_overlap/test.jsonl"
#overlap_path = "/Users/jonathanebner/Universität St.Gallen/STUD-Capstoneproject Tell 6 - General/02-Coding/01-Data/20_overlap/overlap.json"


# load overlap into df
overlap = pd.read_json(overlap_path)


with open(input_path, "r", encoding="utf8") as json_file:
	annotated_recipes = [json.loads(line) for line in json_file if json.loads(line)["answer"]=="accept"]


recipe_list = []
for recipe in annotated_recipes:
	for index,row in overlap.iterrows():
		if row["text"] == recipe["text"]:
			recipe_list.append(recipe)


# with open(output_path, 'w') as w:
#     json.dump(recipe_list , w)

with open(output_path, 'w') as outfile:
	for entry in recipe_list:
		json.dump(entry, outfile)
		outfile.write('\n')
