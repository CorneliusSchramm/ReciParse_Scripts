import random
import typer
from pathlib import Path
import spacy
from spacy.tokens import DocBin, Doc
from spacy.training.example import Example

# make the factory work
from rel_pipe import make_relation_extractor, score_relations

# make the config work
from rel_model import create_relation_model, create_classification_layer, create_instances, create_tensors

print("Hi")

colors_dict = {
	"Arg0": "#c5bdf4",
	"Arg1": "#ffd882",
	"Arg": "#d9fbad",
}


def main(trained_pipeline: Path, test_data: Path, threshold: float = 0.8):
    nlp = spacy.load(trained_pipeline)

    doc_bin = DocBin(store_user_data=True).from_disk(test_data)
    docs = doc_bin.get_docs(nlp.vocab)

    # Iterate through annotated test recipes
    for gold in docs:
        # Create predictions with our trained pipeline and save them under var "pred"
        pred = Doc(
            nlp.vocab,
            words=[t.text for t in gold],
            spaces=[t.whitespace_ for t in gold],
        )

        # Set the entities of the "pred" object equal to the annotated ones
        pred.ents = gold.ents

        # Print out the label for each entity
        for ent in pred.ents:
        	print((ent.text, ent.label_, "start:",ent.start,"end:",ent.start ))
        	break

        # nlp.add_pipe("ner", first=True)
        print(nlp.pipeline)

        # Ich glaube, hier werden die pipeline components andgewandt
       	for name, proc in nlp.pipeline:
            pred = proc(pred)
            print(name)

        for item in pred._.rel.items():
        	print(item)
        	break

        # PRODIGY OUTPUT -------------------------------------------------------------------------------

 		# # Create main output dict for prodigy
   #  	main_dict = {}

   #  	# TEXT KEY
   #      main_dict["text"] = pred.text

        # INPUT HASH KEY
        # TASK HASH KEY
        # SPANS KEY
        # TOKENS KEY
        # SESSION ID KEY
        # VIEW ID KEY

        # RELATIONS KEY
        relations = []
        ents_dict = { ent.start: (ent.text, ent.start, ent.end, ent.label_) for ent in pred.ents }
        tokens = { token.i: (token.text, token.idx, token.idx+len(token.text)) for token in pred }

        for item in pred._.rel.items():
        	if max(item[1].values()) > threshold:

        		# What is the most probable label and how high is the probability
        		print("Maximum Probability:", max(item[1].values()), "for", max(item[1], key=item[1].get))

        		# Build relations dict

	        	relation = dict()
	        	relation["head"] = item[0][0]
	        	relation["child"] = item[0][1]
	        	relation["head_span"] = dict()
	        	relation["child_span"] = dict()
	        	relation["color"] = colors_dict[max(item[1], key=item[1].get)]
	        	relation["label"] = max(item[1], key=item[1].get)

	        	relation["head_span"]["start"] = tokens[item[0][0]][1]
	        	relation["head_span"]["end"] = tokens[item[0][0]][2]
	        	relation["head_span"]["token_start"] = item[0][0]
	        	relation["head_span"]["token_end"] = ents_dict[item[0][0]][2]-1
	        	relation["head_span"]["label"] = ents_dict[item[0][0]][3]

	        	relation["child_span"]["start"] = tokens[item[0][1]][1]
	        	relation["child_span"]["end"] = tokens[item[0][1]][2]
	        	relation["child_span"]["token_start"] = item[0][1]
	        	relation["child_span"]["token_end"] = ents_dict[item[0][1]][2]-1
	        	relation["child_span"]["label"] = ents_dict[item[0][1]][3]

	        	print(relation)
	        	relations.append(relation)
        
        	break
        break


        # ANSWER KEY

   

if __name__ == "__main__":
    typer.run(main)