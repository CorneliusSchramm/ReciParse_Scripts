import spacy

def children_getter(token, dict):       #dict = {}
    """Creating a nested dictionary with multiple levels of children."""
    
    dict[token]= {}                     #dict = {token: {} }
    
    try: 
        for child in token.children:
            children_getter(child, dict[token])     #dict = {token: {child{}}}

    except:
        return 
    
    return 

def sentence_for_verb(doc):
    """Takes doc and creates text for each VERB in doc."""
    
    verb_to_string = {}

    text = ""
    for token in doc:
        if token.pos_ == "VERB": 
            verb_to_string[token] = text

        elif token.pos_ == "PUNCT":
            pass

        else: 
            it = token.text + " "
            text += it
        
        #print(f"{token}: POS = {token.pos_}; DEP = {token.dep_}; DEP_HEAD = {token.head.text}")

    return verb_to_string

def all_el_getter(key, dict, list):
    """Help function to get all elements from dictionary."""

    try: 
        for el in dict[key].keys():
            list.append(el)
            all_el_getter(el, dict[key], list)

    except:
        return list

def list_creator(dict, key):
    """Create list with all Elements assigned to a certain key in dictionary."""

    el_assigned_key = []

    all_el_getter(key, dict, el_assigned_key)

    return el_assigned_key


nlp = spacy.load("de_core_news_sm")

doc = nlp("Die Eier hart kochen. Dann pellen und mit einem Eierschneider in Scheiben schneiden. Den Reis halbgar kochen und zur Seite stellen. Die Wurst (Kolbász) in dünne Scheiben schneiden.Den Knoblauch abziehen und fein würfeln. Die Zwiebel schälen, fein hacken und in etwas Fett glasig braten. Knoblauch und Hackfleisch dazu geben und so lange braten, bis das Hackfleisch schön krümelig wird. Den eigenen Saft nicht ganz verkochen lassen. Die Fleischmasse mit Salz, Pfeffer und Paprikapulver würzen.Das Sauerkraut kurz durchspülen, ausdrücken und abtropfen lassen (damit es nicht zu sauer wird). Das Sauerkraut in einen Topf geben und mit dem Kümmel und den Lorbeerblättern vermischen. Ca. 30 Minuten unter Zugabe von wenig Wasser bei niedriger Stufe dünsten.Eine feuerfeste Form mit etwas Öl einfetten und den Boden dünn mit Sauerkraut belegen. Darauf Kolbász und die Hälfte der in Scheiben geschnittene Eier verteilen, dann eine weitere dünne Schicht Sauerkraut drüber legen. Mit 1 Becher Schmand bedecken. Nun das Hackfleisch mit dem Reis mischen und auf der Sauerkrautschicht gleichmäßig verteilen. Mit der zweiten Hälfte der Eier belegen und die dritte Schicht Sauerkraut oben drauf verteilen. Wenn noch Zutaten (Hackfleisch-Reis-Masse und Sauerkraut) übrig sind, kann man diese Schichten weiter so legen. Ganz oben kommt eine Schicht Sauerkraut. Auf diese letzte Schicht verteilt man noch den Rest vom Schmand (sollte reichlich sein). Den Speck in dünne Scheiben schneiden und damit alles abdecken. Mit etwas Öl besprenkeln. Die Form mit einem Deckel verschließend.Im vorgeheizten Backofen bei 175°C ober-\/Unterhitze gut 1 Std. garen.Ganz frische Baguettebrötchen oder Weißbrot schmeckt am allerbesten dazu. Man kann aber auch Kartoffel- oder Semmelknödel dazu reichen. Etwas aufwendig, aber die Mühe lohnt sich... es ist einfach mega-ober-lecker.Anmerkung: Für viele sind Eier in Verbindung mit Sauerkraut ein No-Go, man kann sie also auch weglassen.")

# Create dic with sentences to predict dependencies
verb_to_string = sentence_for_verb(doc)

final_dict = {}

for key in verb_to_string.keys():
    text = verb_to_string[key] + key.text
    doc = nlp(text)

    for token in doc: 
        if token.pos_ == "VERB":
            
            children_getter(token, final_dict)
        
        else: 
            pass


for key in final_dict.keys():
    print(f"{key} --> {list_creator(final_dict, key)}\n")


"""
doc2 = nlp("Die Eier hart Dann pellen ")

for token in doc2:
    print(f"{token}: POS = {token.pos_}; DEP = {token.dep_}; DEP_HEAD = {token.head.text}")"""

#spacy.load()

for name, proc in rel_nlp.pipeline:
    doc_rel = proc("Die Eier hart kochen. Dann pellen und mit einem Eierschneider in Scheiben schneiden. Den Reis halbgar kochen und zur Seite stellen. Die Wurst (Kolbász) in dünne Scheiben schneiden.Den Knoblauch abziehen und fein würfeln. Die Zwiebel schälen, fein hacken und in etwas Fett glasig braten. Knoblauch und Hackfleisch dazu geben und so lange braten, bis das Hackfleisch schön krümelig wird. Den eigenen Saft nicht ganz verkochen lassen. Die Fleischmasse mit Salz, Pfeffer und Paprikapulver würzen.Das Sauerkraut kurz durchspülen, ausdrücken und abtropfen lassen (damit es nicht zu sauer wird). Das Sauerkraut in einen Topf geben und mit dem Kümmel und den Lorbeerblättern vermischen. Ca. 30 Minuten unter Zugabe von wenig Wasser bei niedriger Stufe dünsten.Eine feuerfeste Form mit etwas Öl einfetten und den Boden dünn mit Sauerkraut belegen. Darauf Kolbász und die Hälfte der in Scheiben geschnittene Eier verteilen, dann eine weitere dünne Schicht Sauerkraut drüber legen. Mit 1 Becher Schmand bedecken. Nun das Hackfleisch mit dem Reis mischen und auf der Sauerkrautschicht gleichmäßig verteilen. Mit der zweiten Hälfte der Eier belegen und die dritte Schicht Sauerkraut oben drauf verteilen. Wenn noch Zutaten (Hackfleisch-Reis-Masse und Sauerkraut) übrig sind, kann man diese Schichten weiter so legen. Ganz oben kommt eine Schicht Sauerkraut. Auf diese letzte Schicht verteilt man noch den Rest vom Schmand (sollte reichlich sein). Den Speck in dünne Scheiben schneiden und damit alles abdecken. Mit etwas Öl besprenkeln. Die Form mit einem Deckel verschließend.Im vorgeheizten Backofen bei 175°C ober-\/Unterhitze gut 1 Std. garen.Ganz frische Baguettebrötchen oder Weißbrot schmeckt am allerbesten dazu. Man kann aber auch Kartoffel- oder Semmelknödel dazu reichen. Etwas aufwendig, aber die Mühe lohnt sich... es ist einfach mega-ober-lecker.Anmerkung: Für viele sind Eier in Verbindung mit Sauerkraut ein No-Go, man kann sie also auch weglassen.")

rel_dict = {ent.start : {"verb": ent, "assigned": []} for ent in ner_docs[0].ents if ent.label_ == "V"}

for item in doc_rel._.rel.items():

    print(item)