""" Create batch3 to batch6 """

import pandas as pd
import json
import sys
import numpy as np

np.random.seed(42)

input_path = "/Users/jonathanebner/Universität St.Gallen/STUD-Capstoneproject Tell 6 - General/02-Coding/01-Data/00_raw_data/recipes_no_batch1and2.json"
output_path = "/Users/jonathanebner/Universität St.Gallen/STUD-Capstoneproject Tell 6 - General/02-Coding/01-Data/11_clean_batches/"

with open(input_path, "r", encoding="utf8") as json_file:
    recipes = [json.loads(line) for line in json_file]

print(len(recipes))
print(type(recipes))
print(recipes[0])

recipes_text = [i["text"] for i in recipes]
print(type(recipes_text[0]))

recipes_text_df = pd.DataFrame(recipes_text, columns = ["text"]).sample(frac=1).reset_index(drop=True).iloc[:,0].to_frame()

amount_recipes_batch = 60

batches = ["batch3", "batch4", "batch5", "batch6"]
names = ["jona", "leo", "coco", "jonathan"]


for name in names:
	for batch in batches:
		a = recipes_text_df.sample(amount_recipes_batch)
		recipes_text_df.drop(list(a.index))
		a.to_json(output_path+batch+"_"+name+".json",orient='records',force_ascii=False)













