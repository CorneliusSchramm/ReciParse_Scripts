import spacy

nlp = spacy.load("de_core_news_sm")

print(nlp.pipeline)
print(nlp.pipe_names)



