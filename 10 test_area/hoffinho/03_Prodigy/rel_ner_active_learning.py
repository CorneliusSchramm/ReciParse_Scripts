import prodigy
import spacy
import json

nlp = spacy.load("/Users/jhoff/Desktop/Capstone_local/03_Prodigy/02_Models/01_Leo_171120/ner_custom_all")

@prodigy.recipe(
    "ner_active_learning",
    dataset=("Dataset to save answers to", "positional", None, str),
    view_id=("Annotation interface", "option", "v", str)
)

def ner_active_learning(dataset, view_id="text"):
    # Load your own streams from anywhere you want
    #pre_stream = json.load("/Users/jhoff/Desktop/Capstone_local/03_Prodigy/01_Data/01_Test1/recipes-texts_test_jona.json")
    #prodigy.components.loaders.JSONL("/Users/jhoff/Desktop/Capstone_local/03_Prodigy/01_Data/01_Test1/recipes-texts_test_jona.json"))
    #print(pre_stream[0])
    stream = {"text":"Kürbisfleisch würfeln. Möhren schälen und würfeln. Zwiebel schälen und fein hacken. Petersilie waschen, trocken schütteln und grob hacken.Putenschnitzel in 8 Streifen schneiden, wellenförmig auf Holzspieße stecken und mit Salz, Pfeffer und Paprika würzen.1 EL Pflanzencreme in einem Topf erhitzen, Kürbis, Möhren und Zwiebel darin ca. 5 Minuten dünsten, Brühe dazugießen und im geschlossenen Topf ca. 25 Minuten kochen.Mit einem Kartoffelstampfer grob zerstampfen, Cremefine und Petersilie unterheben und mit Salz und Pfeffer abschmecken.Restliche Pflanzencreme in einer Pfanne erhitzen, Putenspieße darin knusprig braun braten.Energie- und Nährstoffgehalt:Pro Portion:Energie (kcal): 353Energie (kJ): 1469Eiweiß (g): 23Kohlenhydrate (g): 20Fett (g): 20"},{"text":"Den Seeteufel in 2-3 cm große Würfel, den Schnittlauch in feine Röllchen schneiden.Die Butter zerlassen und die Fischwürfel kurz anziehen lassen. Mit Weißwein ablöschen und zugedeckt 2-3 Minuten ziehen lassen. Die Fischwürfel aus der Pfanne nehmen, mit Salz und Pfeffer würzen und warm stellen.Wermut und Fischfond angießen, auf die Hälfte einkochen. Dann die Sahne zugeben und sämig einkochen. Die Sauce mit der kalten Butter montieren, abschmecken, eventuell eine Prise Zucker hinzufügen. Fischwürfel und Schnittlauchröllchen in die Sauce geben und vorsichtig erwärmen. Nicht mehr kochen."}

    def update(answers):
        texts = [eg["text"] for eg in answers]
        print(texts)
        #ents = [(span["start"], span["end"], span["label"]) for span in x["span"] for x in answers]
        ents = []
        for eg in answers: 
            for span in eg["span"]:
                ents.append((span["start"], span["end"], span["label"]))
        annots = [{"entities": ent} for ent in ents]
        losses = {}
        nlp.update(texts, annots, losses=losses)
        return losses["ner"]

    return {
        "dataset": dataset,
        "view_id": view_id,
        "stream": stream,
        "update": update
    }