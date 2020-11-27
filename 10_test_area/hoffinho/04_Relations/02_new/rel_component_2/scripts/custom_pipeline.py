import spacy
from rel_pipe import RelationExtractor
from rel_pipe import make_relation_extractor
from rel_pipe import relation_extactor

nlp = spacy.load("en_core_web_sm")

print(nlp.pipeline)
print(nlp.pipe_names)

nlp.add_pipe("relation_extactor")