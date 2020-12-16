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

def create_ent_set(rel_list):
    """for each example recipe it creates a set of annotations (label, start, end)"""
    ent_set = set()

    for entity in rel_list:
        try: 
            ent_set.add((entity["head"], entity["child"], entity["label"]))   #start = start character, end = end character
        
        except:
            #print("No start was found. (bad span)")
            pass
    
    return ent_set

x = jsonl_to_list(path_coco)

print(x[0]["relations"][0].keys())