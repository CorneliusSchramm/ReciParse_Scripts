import spacy
from rel_pipe import RelationExtractor
from rel_pipe import make_relation_extractor

nlp = spacy.load("en_core_web_sm")

print(nlp.pipeline)
print(nlp.pipe_names)

print("----")

nlp.add_pipe("relation_extractor")

