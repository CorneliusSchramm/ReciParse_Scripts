#!/usr/bin/env python
# coding: utf8
"""Example of training an additional entity type

This script shows how to add a new entity type to an existing pretrained NER
model. To keep the example short and simple, only four sentences are provided
as examples. In practice, you'll need many more — a few hundred would be a
good start. You will also likely need to mix in examples of other entity
types, which might be obtained by running the entity recognizer over unlabelled
sentences, and adding their annotations to the training set.

The actual training is performed by looping over the examples, and calling
`nlp.entity.update()`. The `update()` method steps through the words of the
input. At each word, it makes a prediction. It then consults the annotations
provided on the GoldParse instance, to see whether it was right. If it was
wrong, it adjusts its weights so that the correct action will score higher
next time.

After training your model, you can save it to a directory. We recommend
wrapping models as Python packages, for ease of deployment.

For more details, see the documentation:
* Training: https://spacy.io/usage/training
* NER: https://spacy.io/usage/linguistic-features#named-entities

Compatible with: spaCy v2.1.0+
Last tested with: v2.2.4
"""
from __future__ import unicode_literals, print_function

import plac
import random
import warnings
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding


# new entity label
# LABEL = "ANIMAL"

# training data
# Note: If you're using an existing model, make sure to mix in examples of
# other entity types that spaCy correctly recognized before. Otherwise, your
# model might learn the new type, but "forget" what it previously knew.
# https://explosion.ai/blog/pseudo-rehearsal-catastrophic-forgetting
TRAIN_DATA = [

(
    "Marinade:Das Öl mit den Kräutern, Salz, Pfeffer und Zitronensaft mischen.Die Fische säubern, salzen, pfeffern. Je Fisch 1 Scheibe Bacon und 1 Stk. Kräuterbutter in den Bauchraum legen, bevor die Fische mit Küchengarn gut verschnürt werden.Die Kräuterbutter kann auch im Bauchraum verrieben werden, sodass ihr Aroma während der Marinierzeit noch besser einziehen kann.Die Fische zwei Tage in die Marinade legen und dann in Alufolie grillen (oder im Ofen zubereiten).Wer mag, kann auch noch einen/zwei Rosmarinzweige mit den in Bauchraum legen.Dieses sehr simple Essen schmeckt sehr gut mit Kräuterbaguette oder Salat oder auch Brat- oder Salzkartoffeln.",
    {"entities":[
	    (13,15,"Z"),
	    (16,19,"PRÄP"),
	    (24,32,"Z"),
	    (34,38,"Z"),
	    (40,47,"Z"),
	    (52,64,"Z"),
	    (65,72,"V"),
	    (77,83,"Z"),
	    (84,91,"V"),
	    (93,99,"V"),
	    (101,109,"V"),
	    (111,119,"Z"),
	    (120,135,"Z"),
	    (140,160,"Z"),
	    (161,177,"Z"),
	    (178,183,"V"),
	    (185,238,"ZEITP"),
	    (371,377,"Z"),
	    (378,387,"DAUER"),
	    (388,390,"PRÄP"),
	    (395,403,"Z"),
	    (404,409,"V"),
	    (414,418,"ZEITP"),
	    (419,421,"PRÄP"),
	    (422,430,"TOOL"),
	    (431,438,"V")
    ]}),
]


@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    new_model_name=("New model name for model meta.", "option", "nm", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int),
)
def main(model=None, new_model_name="ner_recipe_instructions", output_dir=None, n_iter=30):
    """Set up the pipeline and entity recognizer, and train the new entity."""
    random.seed(0)
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("de")  # create blank Language class
        print("Created blank 'de' model")
    # Add entity recognizer to model if it's not in the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner)
    # otherwise, get it, so we can add labels to it
    else:
        ner = nlp.get_pipe("ner")

    new_labels = ["V","Z","TOOL","PRÄP","ZEITP","DAUER","ATTR","TEMP"]
    for label in new_labels:
        ner.add_label(label)  # add new entity label to entity recognizer
  
    # Adding extraneous labels shouldn't mess anything up
    # ner.add_label("VEGETABLE")
    if model is None:
        optimizer = nlp.begin_training()
    else:
        optimizer = nlp.resume_training()
    move_names = list(ner.move_names)
    # get names of other pipes to disable them during training
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
    # only train NER
    with nlp.disable_pipes(*other_pipes), warnings.catch_warnings():
        # show warnings for misaligned entity spans once
        warnings.filterwarnings("once", category=UserWarning, module='spacy')

        sizes = compounding(1.0, 4.0, 1.001)
        # batch up the examples using spaCy's minibatch
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            batches = minibatch(TRAIN_DATA, size=sizes)
            losses = {}
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)
            print("Losses", losses)

    # test the trained model
    test_text = "20g Zucker mit der Butter vermischen und in den Topf geben."
    doc = nlp(test_text)
    print("Entities in '%s'" % test_text)
    for ent in doc.ents:
        print(ent.label_, ent.text)

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.meta["name"] = new_model_name  # rename model
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        # Check the classes have loaded back consistently
        assert nlp2.get_pipe("ner").move_names == move_names
        doc2 = nlp2(test_text)
        for ent in doc2.ents:
            print(ent.label_, ent.text)


if __name__ == "__main__":
    plac.call(main)