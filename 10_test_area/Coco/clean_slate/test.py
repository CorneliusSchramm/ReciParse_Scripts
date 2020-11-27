import spacy

nlp = spacy.load("/Users/jhoff/Desktop/ReciParse_Scripts/10_test_area/Coco/clean_slate/model-best")

doc = nlp("Hallo, das ist ein Test, um zu sehen wie das funktioniert. Zwiebeln")

print(doc)

for ent in doc.ents: 
    print(ent)