from spacy.lang.en import English


nlp = English()

nlp.add_pipe("relation_extractor")


