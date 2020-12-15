from flask import Flask, render_template, url_for, request
from flaskext.markdown import Markdown

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
ner_nlp = spacy.load(r"C:\Users\CocoL\Universität St.Gallen\STUD-Capstoneproject Tell 6 - General\02-Coding\03-Models\NER trained on nightly\ner-cb1-159-15-12")
rel_nlp = spacy.load(r"C:\Users\CocoL\Universität St.Gallen\STUD-Capstoneproject Tell 6 - General\02-Coding\03-Models\Relations\1-trained-on-cpu\cb1-180-15-12")

# Initialize App
app = Flask(__name__)
Markdown(app)

@app.route("/")#, methods=['GET','POST'])
def home():
    # demo_text = "Die Pinienkerne in der trockenen Pfanne goldgelb rösten und dann auf einem Teller abkühlen lassen.Die Zucchini waschen, putzen und in Scheiben schneiden. Die Champignons säubern und in mundgerechte Stücke schneiden. Die Zwiebel schälen und in kleine Würfel schneiden, den Schinken in Streifen schneiden und noch zweimal quer durchschneiden.Die Bandnudeln in reichlich Salzwasser bissfest kochen, abgießen und abtropfen lassen.Etwas Pflanzenöl in einer großen beschichteten Pfanne erhitzen und die Zwiebeln darin glasig werden lassen. Schinken und Rosmarin dazugeben und ca. 2 Minuten mit anbraten. Champignons und Zucchini in die Pfanne geben und kurz mit anbraten. Mit der Gemüsebrühe ablöschen und alles zugedeckt bei mittlerer Hitze ca. 10 Minuten dünsten. Die Sahne einrühren und die Sauce mit Salz und Pfeffer abschmecken.Die Nudeln unterheben, kurz durchschwenken, dann alles auf zwei tiefe Teller verteilen und mit Pinienkernen bestreut servieren. Dazu kann man noch frisch geriebenen Parmesan reichen."
    # docx = nlp(demo_text)

    # demo_html = displacy.render(docx, style= "ent")
    # demo_result = demo_html

    # # Just Display regular text
    # plain_text = docx.text
    return render_template("home.html")#, demo_result = demo_result, demo_text = plain_text)

# @app.route("/analyse")
# def analyse():
#     return render_template("analyse.html", title = "Analyze")

# @app.route("/extract", methods= ["GET", "POST"])
# def extract():
#     if request.method == "POST":

#         # Get the text from the input form
#         rawtext = request.form["rawtext"]
#         doc = ner_nlp(rawtext)

#         # Create HTML Respresentation
#         colors = {"V": "F16F55"}
#         options = {"ents": ["V"], "colors": colors}

#         html = displacy.render(doc, style= "ent", options=options)
#         result = html

#         # Just Display regular text
#         plain_text = doc.text
#     return render_template("result.html", rawtext = rawtext, result = result , plain_text = plain_text)

@app.route("/output", methods= ["GET", "POST"])
def columns():
    if request.method == "POST":
        # demo_text = "Die Pinienkerne in der trockenen Pfanne goldgelb rösten und dann auf einem Teller abkühlen lassen.Die Zucchini waschen, putzen und in Scheiben schneiden. Die Champignons säubern und in mundgerechte Stücke schneiden. Die Zwiebel schälen und in kleine Würfel schneiden, den Schinken in Streifen schneiden und noch zweimal quer durchschneiden.Die Bandnudeln in reichlich Salzwasser bissfest kochen, abgießen und abtropfen lassen.Etwas Pflanzenöl in einer großen beschichteten Pfanne erhitzen und die Zwiebeln darin glasig werden lassen. Schinken und Rosmarin dazugeben und ca. 2 Minuten mit anbraten. Champignons und Zucchini in die Pfanne geben und kurz mit anbraten. Mit der Gemüsebrühe ablöschen und alles zugedeckt bei mittlerer Hitze ca. 10 Minuten dünsten. Die Sahne einrühren und die Sauce mit Salz und Pfeffer abschmecken.Die Nudeln unterheben, kurz durchschwenken, dann alles auf zwei tiefe Teller verteilen und mit Pinienkernen bestreut servieren. Dazu kann man noch frisch geriebenen Parmesan reichen."
        
        rawtext = request.form["rawtext"]
        doc = ner_nlp(rawtext)

        # --- Spacy 3 with rel ---

        # Get NE predictions
        pred = ner_nlp(rawtext)
        # Get Relation predictions
        for name, proc in rel_nlp.pipeline:
            pred = proc(pred)

        v_list = [(ent.start, ent.text) for ent in pred.ents if ent.label_ == "V" ]

        threshhold = 0.2
        steps_list = []
        for v_start, v in v_list:
            step_tup = (v,{})
            for rels_tup, probs in pred._.rel.items():
                max_prob_rel = max(probs, key=probs.get)
                if rels_tup[0] == v_start and probs[max_prob_rel] > threshhold:
                    if probs[max_prob_rel] not in step_tup[1]:
                        step_tup[1][max_prob_rel] = [pred[rels_tup[1]].text] # doc[ent_start_i]
                    else:
                        step_tup[1][max_prob_rel].append(pred[rels_tup[1]].text)
            steps_list.append(step_tup) 
        print(steps_list)

        # --- Spacy 3 with rel ---
        colors = {
            "V": "#F4927E", 
            "Z":"#739DBF", 
            "TOOL": "#C7D7E5", 
            "TEMP": "#00F5AF" , 
            "ATTR": "#00F5AF",
            "ZEITP": "#00F5AF",
            "DAUER": "#00F5AF", 
            "PRÄP":  "#00F5AF"}
            
        my_options = {"ents": ["V","Z", "TOOL", "TEMP", "ATTR","ZEITP","DAUER", "PRÄP" ], "colors": colors}
        demo_html = displacy.render(doc, style= "ent", options=my_options)
        demo_result = demo_html

        # Just Display regular text
        plain_text = doc.text
        # print(plain_text)
        verbs = [ent.text for ent in doc.ents if ent.label_== "V"]
        # print(verbs)
    return render_template(
        "output.html", 
        title="Output",  
        demo_result = demo_result, 
        demo_text = plain_text, 
        verbs = verbs, 
        steps_list = steps_list
        )

if __name__ == "__main__":
    app.run(debug=True)