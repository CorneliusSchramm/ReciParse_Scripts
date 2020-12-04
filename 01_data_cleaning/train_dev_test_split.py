# ---Shuffeling---
import json
from pathlib import Path
import random

def train_dev_test_split(input_file: Path, output_dir: Path, train_split = 0.6):
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
        data = [rec for rec in json.load(json_file) if rec["answer"]== "accept"]
        
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
    ourput_path = Path(output_dir)
    train_path = ourput_path / "train.json"
    dev_path = ourput_path / "dev.json"
    test_path = ourput_path / "test.json"

    for data, data_path in [(train_data, train_path), (dev_data, dev_path), (test_data, test_path)]:
        with open(data_path, 'w') as f:
            json.dump(data, f)

train_dev_test_split (
    input_file = r"C:\Users\CocoL\Universität St.Gallen\STUD-Capstoneproject Tell 6 - General\02-Coding\01-Data\recipes_labeling\batch1_annotated\batch1all120.jsonl,
    output_dir= r"C:\Users\CocoL\Universität St.Gallen\STUD-Capstoneproject Tell 6 - General\02-Coding\01-Data\recipes_labeling\batch1_annotated"
    )
