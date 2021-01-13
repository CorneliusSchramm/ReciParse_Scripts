import jsonlines
import spacy
import spacy.language
from spacy.tokens import Doc
from spacy.scorer import Scorer
from spacy.vocab import Vocab

# global variables
vocab = Vocab()
scorer = Scorer()

rels_to_compare = ["ARG0", "ARG1", "ARG"]
# ["ARG0", "ARG1", "ARG"]

# path to jsonl overlap files
path_coco = r"/Users/jhoff/Universität St.Gallen/STUD-Capstoneproject Tell 6 - Dokumente/General/02-Coding/01-Data/20_overlap/overlap_total/overlap_coco.jsonl"
path_graf = r"/Users/jhoff/Universität St.Gallen/STUD-Capstoneproject Tell 6 - Dokumente/General/02-Coding/01-Data/20_overlap/overlap_total/overlap_leo.jsonl"
path_hoff = r"/Users/jhoff/Universität St.Gallen/STUD-Capstoneproject Tell 6 - Dokumente/General/02-Coding/01-Data/20_overlap/overlap_total/overlap_jona.jsonl"
path_jthn = r"/Users/jhoff/Universität St.Gallen/STUD-Capstoneproject Tell 6 - Dokumente/General/02-Coding/01-Data/20_overlap/overlap_total/overlap_jonathan.jsonl"

def jsonl_to_list(path):
    """takes path to jsonl file and returns list of dicts"""
    
    with jsonlines.open(path) as reader:
        list_of_dicts = list(reader)

    return list_of_dicts

def create_ent_set(rel_list, rels_to_comp):
    """for each example recipe it creates a set of annotations (label, start, end)"""
    rel_set = set()

    for relation in rel_list:
        try: 
            if relation["label"] in rels_to_comp:
                rel_set.add((relation["head_span"]["token_start"], relation["head_span"]["token_end"],
                 relation["child_span"]["token_start"], relation["child_span"]["token_end"], relation["label"]))   #start = start character, end = end character
            
            else: 
                pass
        except:
            #print("No start was found. (bad span)")
            pass
    
    return rel_set


ov_recipes_coco = jsonl_to_list(path_coco)

ov_dict_coco = {example["text"] : create_ent_set(example["relations"], rels_to_compare) for example in ov_recipes_coco}
print(ov_dict_coco)




