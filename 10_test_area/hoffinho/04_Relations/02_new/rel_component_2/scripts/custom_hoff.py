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


#def main(trained_pipeline: Path, test_data: Path, print_details: bool):
    
    
nlp = spacy.load(Path)
print(f"Trained pipeline path: {trained_pipeline}")
print(f"Trained pipeline comps: {nlp.pipeline}")

if __name__ == "__main__":
    typer.run(main)