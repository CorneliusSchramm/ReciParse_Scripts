#imports

import pandas as pd
import os
import numpy as np
import json
from prodigy.components.db import connect
from pathlib import Path
import random


#path = "/Users/jonathanebner/Universität St.Gallen/STUD-Capstoneproject Tell 6 - General/02-Coding/01-Data/all_in_one"
path = "/Users/jonathanebner/Universität St.Gallen/STUD-Capstoneproject Tell 6 - General/02-Coding/01-Data/12_annotated_batches/batch2all/"
batch = "batch2all"
names = ["coco", "leo", "jona"]
json_names = [f"{batch}_{name}" for name in names]


#2. unique_extractor

overlap_path = "/Users/jonathanebner/Universität St.Gallen/STUD-Capstoneproject Tell 6 - General/02-Coding/01-Data/20_overlap/overlap_batch2.json"

overlap = pd.read_json(overlap_path)

in_sets = []

for i in range(len(names)):
	input_path = path + json_names[i] + ".jsonl"
	with open(input_path, "r", encoding="utf8") as json_file:
		batch1_unique = [json.loads(line) for line in json_file if json.loads(line)["answer"]=="accept"]

	# looped über alle annotierten Rezepte in "batch1_unique" und checkt ob "text" in overlap enthalten, wenn nicht, dann wird das Rezept in recipe_list gespeichert
	recipe_list = []
	for recipe in batch1_unique:
		if recipe["text"] not in overlap["text"].to_list():
			recipe_list.append(recipe)

	print("Anzahl unique:", len(recipe_list))

	output_path = path + json_names[i] + "_unique.jsonl"
	with open(output_path, 'w') as outfile:
		for entry in recipe_list:
			json.dump(entry, outfile)
			outfile.write('\n')


	#3. db-in unique annotations

	dataset_name = json_names[i] + "_unique"
	os.system(f"prodigy db-in {dataset_name} '{output_path}'")
	in_sets.append(dataset_name)


#4. db-merge
# Befehl: db-merge in_sets out_set
out_set = f"{batch}_all"
in_sets_ = ",".join(in_sets)
batch_name_jonathan = "batch2_jonathan" #wie heißt der batch in meiner database
os.system(f"prodigy db-merge {in_sets_},{batch_name_jonathan} {out_set}")


#5. run bad spans script + 6. run impute script

db = connect()
examples = db.get_dataset(out_set)
filtered_examples = []
for eg in examples:
	if "spans" in eg:
		new_spans = []
		for span in eg["spans"]:
			if "start" not in span or "end" not in span:
				print("Found bad span:", span)
			else:
				#### Leos Input: Giovannis Code ####
				#print("---START---")
				#print(span)
				#v = span
				if "text" not in span.keys():
					try:
						span["text"] = eg["text"][span["start"]:span["end"]]
						span["type"] = "ent"
					except KeyError:
						print("KeyError:", span)

				#print(span)
				#n = span
				#print("----END----")
				#### End of Input ####
				new_spans.append(span)
		eg["spans"] = new_spans
	filtered_examples.append(eg)

# Add filtered examples to new dataset
db.add_dataset("myDataset2_filtered")
out_set_filtered = out_set + "_f"
db.add_examples(filtered_examples, [out_set_filtered])


#7. data-to-spacy
path_outputfile = path + out_set + "_dts.json"
os.system(f'prodigy data-to-spacy "{path_outputfile}" -l "de" -n {out_set_filtered}')


#8. shuffle and split

def train_dev_test_split(output_dir: Path, input_file=path_outputfile, train_split = 0.6):
    """
    Takes a JSON file specified in input_file, splits it into train, test, dev based on given distribution,
    and saves the three data sets into the specified output dir
    """

    dev_split = (1-train_split)/2
    test_split = dev_split

    file_path = Path(input_file)
    print(f"Input file at {file_path}")

    # Load JSON into list
    with open(file_path, "r", encoding="utf8") as json_file:
        # data = [json.loads(line) for line in json_file if json.loads(line)["answer"]=="accept"]
        # data = [rec for rec in json.load(json_file) if rec["answer"]== "accept"]
        data = [ rec for rec in json.load(json_file) ]
    # Checking Length
    data_len = len(data)
    print(f"Number of accepted recipes: {len(data)}")

    # Shuffle - Uncomment print statement to Confirm that shuffle worked
    # print(data[0]["text"]+"\n")
    random.shuffle(data)
    # print(data[0]["text"]+"\n")

    # Splitting into train, test, dev
    train_i = round(train_split * data_len)
    dev_i = round((train_split + dev_split) * data_len)

    train_data = data[:train_i]
    dev_data = data[train_i:dev_i]
    test_data = data[dev_i:]

    print(
        f"Training Data Length: {len(train_data)}", 
        f"\nDev Data Length: {len(dev_data)}", 
        f"\nTest Data Length: {len(test_data)}", 
        f"\nTotal Data Length: {sum([len(train_data),len(dev_data),len(test_data)])}\n")

    # Saving the three data sets to seperate jsons
    # output_path = Path(output_dir)
    train_path = output_dir + f"/{batch}_train.json"
    dev_path = output_dir + f"/{batch}_dev.json"
    test_path = output_dir + f"/{batch}_test.json"

    for data, data_path in [(train_data, train_path), (dev_data, dev_path), (test_data, test_path)]:
        with open(f"{data_path}", 'w') as f:
            json.dump(data, f)

train_dev_test_split (
        output_dir= path + "split"
    )










