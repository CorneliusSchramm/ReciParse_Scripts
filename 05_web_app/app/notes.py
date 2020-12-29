# Importing NLP Stuff
import spacy
from spacy import displacy

# import 
# New Tokenizer



# For Rel Model
import rel_pipe
import rel_model
import custom_functions

# Load Models           
# ner_nlp = spacy.load(r"C:\Users\CocoL\Universität St.Gallen\STUD-Capstoneproject Tell 6 - General\02-Coding\03-Models\NER trained on nightly\ner-cb1-159-15-12")
ner_nlp = spacy.load(r"C:\Users\CocoL\Universität St.Gallen\STUD-Capstoneproject Tell 6 - General\02-Coding\03-Models\NER trained on nightly\ner-trf_12-16_coco\model-best")
# rel_nlp = spacy.load(r"C:\Users\CocoL\Universität St.Gallen\STUD-Capstoneproject Tell 6 - General\02-Coding\03-Models\Relations\0-trained-on-djx\model-best")
rel_nlp = spacy.load(r"C:\Users\CocoL\Universität St.Gallen\STUD-Capstoneproject Tell 6 - General\02-Coding\03-Models\Relations\16-12_relations_tok2vec")

rawtext = """ 
            Die Pinienkerne in der trockenen Pfanne goldgelb rösten und dann auf einem Teller abkühlen lassen.Die Zucchini waschen, 
            putzen und in Scheiben schneiden. Die Champignons säubern und in mundgerechte Stücke schneiden. Die Zwiebel schälen und 
            in kleine Würfel schneiden, den Schinken in Streifen schneiden und noch zweimal quer durchschneiden.Die Bandnudeln in 
            reichlich Salzwasser bissfest kochen, abgießen und abtropfen lassen.Etwas Pflanzenöl in einer großen beschichteten Pfanne 
            erhitzen und die Zwiebeln darin glasig werden lassen. Schinken und Rosmarin dazugeben und ca. 2 Minuten mit anbraten. Champignons 
            und Zucchini in die Pfanne geben und kurz mit anbraten. Mit der Gemüsebrühe ablöschen und alles zugedeckt bei mittlerer 
            Hitze ca. 10 Minuten dünsten. Die Sahne einrühren und die Sauce mit Salz und Pfeffer abschmecken.Die Nudeln unterheben, kurz 
            durchschwenken, dann alles auf zwei tiefe Teller verteilen und mit Pinienkernen bestreut servieren. Dazu kann man noch frisch geriebenen Parmesan reichen.
            """

# Get NE predictions
pred = ner_nlp(rawtext)
ents_ref = {ent.start: ent.text for ent in pred.ents}

# Get Relation predictions
for name, proc in rel_nlp.pipeline:
    pred = proc(pred)

i = 0
for rels_tup, probs in pred._.rel.items():
    # print(f"Combination: {rels_tup}, predictions: {probs}")
    i += 1
    if i == 20:
        break
v_list = [(ent.start, ent.text) for ent in pred.ents if ent.label_ == "V" ]

threshhold = 0.05
steps_list = [] 
for v_start, v in v_list:
    step_tup = (v,{})
    for rels_tup, probs in pred._.rel.items():
        max_prob_rel = max(probs, key=probs.get)
        if rels_tup[0] == v_start and (probs[max_prob_rel] > threshhold) and max_prob_rel != "ArgNone": #and (v_start - rels_tup[1] > -5):
            if probs[max_prob_rel] not in step_tup[1]:
                step_tup[1][max_prob_rel] = [ents_ref[rels_tup[1]]] # doc[ent_start_i]
            else:
                step_tup[1][max_prob_rel].append(ents_ref[rels_tup[1]])
    steps_list.append(step_tup) 
for step in steps_list:
    print(step)