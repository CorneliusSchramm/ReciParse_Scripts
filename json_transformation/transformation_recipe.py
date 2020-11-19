# Copied Code from Website
import prodigy

@prodigy.recipe(
    "transform_rel2ner",
    dataset=("Dataset to save answers to", "positional", None, str),
)
def transform_rel2ner(dataset, input_dataset):
    # Load your own streams from anywhere you want
    stream = load_my_custom_stream()


    # Giovannis Code
    input_name = input_dataset
    data_input = []
    with open(path + '/' + input_name) as f:    
        for i in f:
            data = json.loads(i)
            data_input.append(data)


    def update(examples):
        # This function is triggered when Prodigy receives annotations
        print(f"Received {len(examples)} annotations!")

    return {
        "dataset": dataset,
        "view_id": view_id,
        "stream": stream,
        "update": update
    }


# --------

# load input JSON into dict data_input



# Keys in output json
output_keys = ["text", "_input_hash", "_task_hash", "tokens", "_session_id", "_view_id", "spans", "answer"]

# create output JSON from input JSON
output = []
for i in range(len(data_input)):
    output_ = {}
    for key in output_keys:
        output_[key] = data_input[i][key]
    output.append(output_)

# convert dict output into string
output_string = json.dumps(output)

# write JSON string into JSON file
output_name = "test2.jsonl"
with open(path + "/" + output_name,"w") as f:
  for json_ in output:
    json_string = json.dumps(json_)
    f.write(json_string + "\n")