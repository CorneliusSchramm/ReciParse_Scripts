import spacy

@spacy.registry.callbacks("customize_language_data")
def create_callback():
    def customize_language_data(lang_cls):
        lang_cls.Defaults.infixes = lang_cls.Defaults.infixes + [r'[!&:,\(\)\.]']
        return lang_cls
    return customize_language_data

nlp = spacy.load(r"models\model-best")

doc = nlp("Ein Ei, 70 ml.Wasser, etwas Mehl und 100gr.Zucker(braun) mischen und zu einem Teig kneten. Den Teig ausrollen und im Ofen bei 700 Grad Celsius 1 Stunde backen.")

print(doc)

for ent in doc.ents: 
    print(ent, ent.label_)

print([tok for tok in doc])