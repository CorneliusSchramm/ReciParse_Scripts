import spacy

nlp = spacy.load(r"models\model-best")

doc = nlp("Ein Ei, 70 ml Wasser, etwas Mehl und 100g Zucker mischen und zu einem Teig kneten. Den Teig ausrollen und im Ofen bei 700 Grad Celsius 1 Stunde backen.")

print(doc)

for ent in doc.ents: 
    print(ent, ent.label_)