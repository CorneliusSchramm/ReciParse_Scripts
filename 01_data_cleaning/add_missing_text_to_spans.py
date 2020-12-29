import pandas as pd
import json


# Pfad to json/jsonl, dass ausgebessert werden soll
input_path = "/Users/jonathanebner/Universität St.Gallen/STUD-Capstoneproject Tell 6 - General/02-Coding/01-Data/12_annotated_batches/batch2/batch2_all_f.jsonl"

#Pfad für output json
output_path = "/Users/jonathanebner/Universität St.Gallen/STUD-Capstoneproject Tell 6 - General/02-Coding/01-Data/12_annotated_batches/batch2/batch2_all_fi.jsonl"

with open(input_path, "r", encoding="utf8") as json_file:
    annotated_recipes = [json.loads(line) for line in json_file]


data = pd.DataFrame(annotated_recipes)


for index, row in data.iterrows():
    for span in row["spans"]:
        if "text" not in span.keys():
            try:
                span["text"] = row["text"][span["start"]:span["end"]]
                span["type"] = "ent"
            except KeyError:
                pass


data.to_json(output_path, orient = "records", force_ascii=False, lines = True)

#with open(output_path, 'w') as outfile:
#	for entry in data:
#		json.dump(entry, outfile)
#		outfile.write('\n')