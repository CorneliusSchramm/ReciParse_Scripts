import jsonlines
import spacy
import spacy.language
from spacy.tokens import Doc
from spacy.scorer import Scorer
from spacy.vocab import Vocab

# global variables
vocab = Vocab()
scorer = Scorer()

# path to jsonl overlap files
path_coco = "/Users/jhoff/Universität St.Gallen/STUD-Capstoneproject Tell 6 - Dokumente/General/02-Coding/01-Data/20_overlap/batch1_coco_overlap.jsonl"
path_graf = "/Users/jhoff/Universität St.Gallen/STUD-Capstoneproject Tell 6 - Dokumente/General/02-Coding/01-Data/20_overlap/batch1_leo_overlap.jsonl"
path_hoff = "/Users/jhoff/Universität St.Gallen/STUD-Capstoneproject Tell 6 - Dokumente/General/02-Coding/01-Data/20_overlap/batch1_jona_overlap.jsonl"
path_jthn = "/Users/jhoff/Universität St.Gallen/STUD-Capstoneproject Tell 6 - Dokumente/General/02-Coding/01-Data/20_overlap/batch1_jonathan_overlap.jsonl"


# functions
def jsonl_to_list(path):
    """takes path to jsonl file and returns list of dicts"""
    
    with jsonlines.open(path) as reader:
        list_of_dicts = list(reader)[0]

    return list_of_dicts

def create_ent_set(span_list):
    """for each example recipe it creates a set of annotations (label, start, end)"""
    ent_set = set()

    for entity in span_list:
        try: 
            ent_set.add((entity["label"], entity["start"], entity["end"]))   #start = start character, end = end character
        
        except:
            print("No start was found. (bad span)")
    
    return ent_set

def score_set(cand, gold):
    
    tp = len(cand.intersection(gold))
    fp = len(cand - gold)
    fn = len(gold - cand)
    
    return (tp, fp, fn)

def precision(tp, fp):
    return tp / (tp + fp + 1e-100)

def recall(tp, fn):
    return tp / (tp + fn + 1e-100)

def fscore(precision, recall):
    p = precision
    r = recall
    return 2 * ((p * r) / (p + r + 1e-100))


# list of individual overlap dicts
ov_recipes_coco = jsonl_to_list(path_coco)
ov_recipes_graf = jsonl_to_list(path_graf)
ov_recipes_hoff = jsonl_to_list(path_hoff)
ov_recipes_jthn = jsonl_to_list(path_jthn)

ov_all_list = [ov_recipes_coco, ov_recipes_graf, ov_recipes_hoff, ov_recipes_jthn] 

# create dict for each annotator: key=text of recipe, value = ent_set
ov_dict_coco = {example["text"] : create_ent_set(example["spans"]) for example in ov_recipes_coco}
ov_dict_graf = {example["text"] : create_ent_set(example["spans"]) for example in ov_recipes_graf}
ov_dict_hoff = {example["text"] : create_ent_set(example["spans"]) for example in ov_recipes_hoff}
ov_dict_jthn = {example["text"] : create_ent_set(example["spans"]) for example in ov_recipes_jthn}

ov_all_dicts = [ov_dict_coco, ov_dict_graf, ov_dict_hoff, ov_dict_jthn]


# comparison hoff-jthn
for key in ov_dict_jthn.keys():
    tp, fp, fn = score_set(ov_dict_jthn[key], ov_dict_hoff[key])

    print(f"True positive: {tp}")
    print(f"False positive: {fp}")
    print(f"False negative: {fn}")
    print(f"Precision: {precision(tp, fp)}")
    print(f"Recall: {recall(tp, fn)}")
    print(f"F-Score: {fscore(precision(tp, fp), recall(tp, fn))}")
    print("-----------")
