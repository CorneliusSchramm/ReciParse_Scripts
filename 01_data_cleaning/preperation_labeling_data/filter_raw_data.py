""" Create Datasaet with only not annotated recipes (data - batch1 - batch2) """


import pandas as pd
import json
import sys
import numpy


input_path = "/Users/jonathanebner/Universität St.Gallen/STUD-Capstoneproject Tell 6 - General/02-Coding/01-Data/00_raw_data/recipes_cleaned.json"
batches = "/Users/jonathanebner/Universität St.Gallen/STUD-Capstoneproject Tell 6 - General/02-Coding/01-Data/11_clean_batches"
output_path = "/Users/jonathanebner/Universität St.Gallen/STUD-Capstoneproject Tell 6 - General/02-Coding/01-Data/00_raw_data/recipes_no_batch1and2.json"


#with open(input_path, "r", encoding="utf8") as json_file:
#	recipes = [json.loads(line) for line in json_file]


recipes = json.loads(open(input_path,"r").read())

batch1_coco = json.loads(open(batches + "/batch1_coco.json","r").read())
batch1_leo = json.loads(open(batches + "/batch1_leo.json","r").read())
batch1_jona = json.loads(open(batches + "/batch1_jona.json","r").read())
batch1_jonathan = json.loads(open(batches + "/batch1_jonathan.json","r").read())

batch1 = batch1_jonathan + batch1_jona + batch1_leo + batch1_coco
print(len(batch1))

batch2_coco = json.loads(open(batches + "/batch2_coco.json","r").read())
batch2_leo = json.loads(open(batches + "/batch2_leo.json","r").read())
batch2_jona = json.loads(open(batches + "/batch2_jona.json","r").read())
batch2_jonathan = json.loads(open(batches + "/batch2_jonathan.json","r").read())

batch2 = batch2_jonathan + batch2_jona + batch2_leo + batch2_coco
print(len(batch2))

print(len(recipes))


recipe_list = []
for recipe in recipes:
	if recipe["text"] not in [i["text"] for i in batch1]:
		if recipe["text"] not in [j["text"] for j in batch2]:
			recipe_list.append(recipe)

print(len(recipe_list))


with open(output_path, 'w') as outfile:
	for entry in recipe_list:
		json.dump(entry, outfile)
		outfile.write('\n')