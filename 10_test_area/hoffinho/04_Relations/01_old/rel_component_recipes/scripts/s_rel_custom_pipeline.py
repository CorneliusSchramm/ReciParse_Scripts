import spacy
from rel_pipe import RelationExtractor
from rel_pipe import make_relation_extractor

nlp = spacy.load("en_core_web_sm")

print(nlp.pipeline)
print(nlp.pipe_names)

component = make_relation_extractor(nlp=nlp, name="test", model="/Users/jhoff/Desktop/ReciParse_Scripts/10 test_area/hoffinho/04_Relations/02_new/rel_component_recipes/training/model-best/relation_extractor/model", 
threshold=(0.6))
#print(component)
#RelationExtractor #(xx, xxx)  # initialise component
nlp.add_pipe(component, last=True) #alternativ: nlp.add_pipe(make_relation_extractor, )

print("--------")

#nlp.add_pipe("relation_extractor")

print("here")

print("Pipeline", nlp.pipe_names)  # pipeline contains component name

print("done")
#update model 
nlp._.update


