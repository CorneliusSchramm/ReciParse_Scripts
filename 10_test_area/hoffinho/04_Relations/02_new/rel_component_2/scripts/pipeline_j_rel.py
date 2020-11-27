import spacy

nlp = spacy.load("/Users/jhoff/Desktop/ReciParse_Scripts/10_test_area/hoffinho/04_Relations/02_new/rel_component_2/training/model-best")

print(nlp.pipeline)
