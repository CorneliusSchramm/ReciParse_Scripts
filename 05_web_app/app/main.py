from flask import Flask, render_template, url_for, request

# Importing NLP Stuff
import spacy
nlp = spacy.load('en_core_web_sm')

test_sent = "Brad Pit lives in LA and works for Google. This is where our cooking instructions could be displayed."
doc = nlp(test_sent)

ents_list = [
    {
        "text": ent.text,
        "label": ent.label_,
        "start_char": ent.start_char, 
        "end_char": ent.end_char       
    }
    for ent in doc.ents  
]


# Word Info
tokens = doc.to_json()["tokens"]
print(tokens)

# Initialize App
app = Flask(__name__)

@app.route("/")#, methods=['GET','POST'])
def home():
    # if request.method == 'POST':
    #     rawtext = request.form['rawtext']
    #     doc = nlp(rawtext)
    #     ents_list = [
    #         {
    #             "text": ent.text,
    #             "label": ent.label_,
    #             "start_char": ent.start_char, 
    #             "end_char": ent.end_char       
    #         }
    #         for ent in doc.ents  
    #     ]
    return render_template("home.html", ents_list = ents_list, doc_text = doc.text)

# @app.route('/', methods=['POST'])
# def my_form_post():
#     text = request.form['text']
#     processed_text = text.upper()
#     return processed_text
    
@app.route("/about")
def about():
    return render_template("about.html", title = "About")
    
if __name__ == "__main__":
    app.run(debug=True)