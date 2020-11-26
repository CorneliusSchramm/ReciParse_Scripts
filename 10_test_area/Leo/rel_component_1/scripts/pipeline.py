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

# input verändern: Ein oder mehrere Rezepte
# nlp pipeline component die tokenized und ner macht


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

        break


        # ANSWER KEY

   

if __name__ == "__main__":
    typer.run(main)