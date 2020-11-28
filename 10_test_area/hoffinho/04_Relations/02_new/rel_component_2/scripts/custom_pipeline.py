import spacy
"""from rel_pipe import RelationExtractor
from rel_pipe import make_relation_extractor
from rel_pipe import relation_extactor
from pathlib import Path
from spacy.util import load_model_from_path"""

from thinc.api import Config
"""from spacy.language import Language
from rel_model import create_relation_model, create_classification_layer, create_instances, create_tensors
from spacy.vocab import Vocab"""
from spacy.lang.en import English


#nlp = spacy.load("en_core_web_sm")

config = Config().from_disk("/Users/jhoff/Desktop/ReciParse_Scripts/10_test_area/hoffinho/04_Relations/02_new/rel_component_2/configs/rel_tok2vec.cfg")
nlp = English().from_config(config)

nlp.add_pipe("ner", first=True)


print(nlp.pipe_names)

confs = nlp.config