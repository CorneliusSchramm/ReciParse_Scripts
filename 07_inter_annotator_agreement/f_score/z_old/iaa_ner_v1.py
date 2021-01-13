import jsonlines
import spacy
import spacy.language
from spacy.tokens import Doc
from spacy.scorer import Scorer

# path to jsonl overlap files
path_coco = "/Users/jhoff/Universität St.Gallen/STUD-Capstoneproject Tell 6 - Dokumente/General/02-Coding/01-Data/20_overlap/batch1_coco_overlap.jsonl"
path_graf = "/Users/jhoff/Universität St.Gallen/STUD-Capstoneproject Tell 6 - Dokumente/General/02-Coding/01-Data/20_overlap/batch1_leo_overlap.jsonl"
path_hoff = "/Users/jhoff/Universität St.Gallen/STUD-Capstoneproject Tell 6 - Dokumente/General/02-Coding/01-Data/20_overlap/batch1_jona_overlap.jsonl"
path_jthn = "/Users/jhoff/Universität St.Gallen/STUD-Capstoneproject Tell 6 - Dokumente/General/02-Coding/01-Data/20_overlap/batch1_jonathan_overlap.jsonl"

def jsonl_to_list(path):
    """takes path to jsonl file and returns list of dicts"""
    
    with jsonlines.open(path) as reader:
        list_of_dicts = list(reader)[0]

    return list_of_dicts

# list of individual overlap dicts
ov_recipes_coco = jsonl_to_list(path_coco)
ov_recipes_graf = jsonl_to_list(path_graf)
ov_recipes_hoff = jsonl_to_list(path_hoff)
ov_recipes_jthn = jsonl_to_list(path_jthn)

ov_all_list = [ov_recipes_coco, ov_recipes_graf, ov_recipes_hoff, ov_recipes_jthn] 

# print(ov_recipes_jthn[0].keys())

gold_standard = ov_recipes_jthn[0]["spans"] #list of spans
predicted_ann = ov_recipes_hoff[0]["spans"]

print(gold_standard)

# create GoldParse


# create Doc

scorer = Scorer()
scorer.score(predicted_ann, gold_standard)






# # docs_golds = ()


# # create nlp object
# nlp = spacy.load("de_core_news_sm")

# scorer = nlp.evaluate(docs_golds, verbose=True)
# print(scorer.scores)

