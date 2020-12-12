import json

import typer
from pathlib import Path

from spacy.tokens import Span, DocBin, Doc
from spacy.vocab import Vocab
from wasabi import Printer

msg = Printer()

MAP_LABELS = {
    "ARG0a": "Arg0Z",
    "ARG0b": "Arg0Tool",
    "ARG1a": "Arg1Z",
    "ARG1b": "Arg1Tool",
    "ARGa": "ArgAttr",
    "ARGb": "ArgTemp",
    "ARGc": "ArgDauer",
    "ARGd": "ArgZeitp",
    "ARGe": "ArgPräp"
}


def main(json_loc: Path, train_file: Path, dev_file: Path, test_file: Path, dev_split=0.2, test_split=0.1, train_split=0.7):
    """Creating the corpus from the Prodigy annotations."""
    Doc.set_extension("rel", default={})
    vocab = Vocab()

    docs = {"train": [], "dev": [], "test": []}
    ids = {"train": set(), "dev": set(), "test": set()}
    count_all = {"train": 0, "dev": 0, "test": 0}
    count_pos = {"train": 0, "dev": 0, "test": 0}

    long_rel_count = 0

    with json_loc.open("r", encoding="utf8") as jsonfile:
        length_training_data = len([True for line in jsonfile if json.loads(line)["answer"]=="accept"])
        msg.info(f"Number of accepted recipes: {length_training_data}")
        
    with json_loc.open("r", encoding="utf8") as jsonfile:
        for line in jsonfile:
            example = json.loads(line) #one recipe
            span_starts = set()

            if example["answer"] == "accept":
                neg = 0
                pos = 0
                try:
                    # Parse the tokens -> example["tokens"] = list of dicts
                    words = [t["text"] for t in example["tokens"]]  #list containing all words
                    spaces = [t["ws"] for t in example["tokens"]]   #list containing ws is behind word (ws = True/False)
                    doc = Doc(vocab, words=words, spaces=spaces)

                    # Parse the entities
                    spans = example["spans"]    #list of dicts containing entities
                    entities = []
                    span_end_to_start = {}
                    ents_dict = {}
                    for span in spans:          #every detected span
                        entity = doc.char_span(
                            span["start"], span["end"], label=span["label"]
                        ) #"start" = wievielter character ist start character des spans im doc
                        span_end_to_start[span["token_end"]] = span["token_start"] #end_token of span as key for start_token (start token = wievielter token in doc)
                        entities.append(entity)                 #appended to list
                        span_starts.add(span["token_start"])    #added to set
                        ents_dict[span["token_start"]] = (span["label"], span["token_start"])
                    doc.ents = entities                         #entity list assigned as doc entites

                    # Parse the relations
                    rels = {}

                    for x1 in span_starts:
                        if ents_dict[x1][0] == "V":             #filter entity type
                            for x2 in span_starts:
                                if ents_dict[x2][0] in ["Z","TOOL","ATTR","TEMP","DAUER","ZEITP","PRÄP"]:      #filter entity type
                                    if abs(ents_dict[x1][1] - ents_dict[x2][1]) <= 30:  #filter token distance (match with config?)
                                        rels[(x1, x2)] = {}         #every possible span combination becomes key for individual dict (1,1), (1,2) ...
        
                    relations = example["relations"]    #relations is list of dicts
                    count = 0
                    for relation in relations:
                        # the 'head' and 'child' annotations refer to the end token in the span
                        # but we want the first token
                        start = span_end_to_start[relation["head"]]     #wievielter token ist head token
                        end = span_end_to_start[relation["child"]]      #wievielter token ist child token
                        label = relation["label"]
                        
                        if label == "ARG":
                            if ents_dict[end][0] == "ATTR":
                                label = "ArgAttr"
                            elif ents_dict[end][0] == "TEMP":
                                label = "ArgTemp"
                            elif ents_dict[end][0] == "DAUER":
                                label = "ArgDauer"
                            elif ents_dict[end][0] == "ZEITP":
                                label = "ArgZeitp" 
                            elif ents_dict[end][0] == "PRÄP":
                                label = "ArgPräp"      #    "ARG": "ArgTemp", "ARG": "ArgDauer", "ARG": "ArgZeitp","ARG": "ArgPräp"

                        elif label == "ARG0":
                            if ents_dict[end][0] == "Z":
                                label = "Arg0Z"
                            elif ents_dict[end][0] == "TOOL":
                                label = "Arg0Tool"

                        elif label == "ARG1":
                            if ents_dict[end][0] == "Z":
                                label = "Arg1Z"
                            elif ents_dict[end][0] == "TOOL":
                                label = "Arg1Tool"

                        #label = MAP_LABELS[label]                       #MAP_LABELS = dict containing label as key 
                        try: 
                            if label not in rels[(start, end)]:             #check if label already exists for token combination
                                rels[(start, end)][label] = 1.0             #initialize label as new key with value 1.0
                                pos += 1                                    #positive case
                        except:                                     
                            long_rel_count +=1
                            pass


                    # The annotation is complete, so fill in zero's where the data is missing
                    for x1 in span_starts:
                        if ents_dict[x1][0] == "V":             #filter entity type
                            for x2 in span_starts:
                                if ents_dict[x2][0] in ["Z","TOOL","ATTR","TEMP","DAUER","ZEITP","PRÄP"]:      #filter entity type
                                    if abs(ents_dict[x1][1] - ents_dict[x2][1]) <= 30:      #filter token distance (match with config?)
                                        for label in MAP_LABELS.values():           #for every label
                                            if label not in rels[(x1, x2)]:         #if label isn't assigned to span combination
                                                neg += 1                            
                                                rels[(x1, x2)][label] = 0.0         #span combination with label as key gets 0 as value
                    print(rels)
                    doc._.rel = rels                                    # rels = {(1,1): {Arg0 : 1, Arg1 : 0, Arg : 0}, (1,2): {Arg0 : 0, ...}}

                    # only keeping documents with at least 1 positive case (if doc isn't annotated relations = empty list)
                    if pos > 0:

                        recipe_id = example["_input_hash"]

                        if len(docs["train"]) < round(train_split*length_training_data):
                            ids["train"].add(recipe_id)
                            docs["train"].append(doc)
                            count_pos["train"] += pos
                            count_all["train"] += pos + neg
                        elif len(docs["test"]) < round(test_split*length_training_data):
                            ids["test"].add(recipe_id)
                            docs["test"].append(doc)
                            count_pos["test"] += pos
                            count_all["test"] += pos + neg
                        else: 
                            ids["dev"].add(recipe_id)
                            docs["dev"].append(doc)
                            count_pos["dev"] += pos
                            count_all["dev"] += pos + neg                 

                except KeyError as e:
                    msg.fail(f"Skipping doc because of key error: {e} in {example['_input_hash']}")

    
    msg.info(f"{long_rel_count} relations have been cut because tokens are too far apart.")

    docbin = DocBin(docs=docs["train"], store_user_data=True)
    docbin.to_disk(train_file)
    msg.info(
        f"{len(docs['train'])} training recipes from {len(ids['train'])} unique recipes, "
        f"{count_pos['train']}/{count_all['train']} pos instances."
    )

    docbin = DocBin(docs=docs["dev"], store_user_data=True)
    docbin.to_disk(dev_file)
    msg.info(
        f"{len(docs['dev'])} dev recipes from {len(ids['dev'])} unique recipes, "
        f"{count_pos['dev']}/{count_all['dev']} pos instances."
    )

    docbin = DocBin(docs=docs["test"], store_user_data=True)
    docbin.to_disk(test_file)
    msg.info(
        f"{len(docs['test'])} test recipes from {len(ids['test'])} unique recipes, "
        f"{count_pos['test']}/{count_all['test']} pos instances."
    )


if __name__ == "__main__":
    typer.run(main)
