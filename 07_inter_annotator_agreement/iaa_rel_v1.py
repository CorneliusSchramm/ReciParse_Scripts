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
ov_dict_coco = {example["text"] : create_ent_set(example["relations"]) for example in ov_recipes_coco}
ov_dict_graf = {example["text"] : create_ent_set(example["relations"]) for example in ov_recipes_graf}
ov_dict_hoff = {example["text"] : create_ent_set(example["relations"]) for example in ov_recipes_hoff}
ov_dict_jthn = {example["text"] : create_ent_set(example["relations"]) for example in ov_recipes_jthn}

ov_all_dicts = [ov_dict_coco, ov_dict_graf, ov_dict_hoff, ov_dict_jthn]
annot_names = ["Coco", "Graf", "Hoff", "Giov"]

# dict with all relevant information for about comparison
inf_per_comparison = {}

count = 1
for i in range(len(ov_all_dicts)-1):
    main = ov_all_dicts[i]                      #first annotator dictionary

    for j in range(i+1, len(ov_all_dicts)):
        comp = ov_all_dicts[j]                  #second annotator dictionary

        temp_dict = {}                          #temp dict filled with information for each compared recipe

        count2 = 1

        tp_count = 0                            #total amount tp for comparison between two annotators
        fp_count = 0
        fn_count = 0

        for key in ov_all_dicts[i].keys():      #loop through all recipes
            tp, fp, fn = score_set(ov_all_dicts[i][key], ov_all_dicts[j][key])  #compare each recipe for both annotators
            k = "SetComp" + str(count2)
            temp_dict[k] = {}

            temp_dict[k]["tp"] = tp
            temp_dict[k]["fp"] = fp
            temp_dict[k]["fn"] = fn

            tp_count += tp
            fp_count += fp
            fn_count += fn
            
            count2 += 1
        
        

        ann_comp_precis = precision(tp_count, fp_count)
        ann_comp_recall = recall(tp_count, fn_count)
        ann_comp_fscore = fscore(ann_comp_precis, ann_comp_recall)


        inf_per_comparison["AnnComp"+str(count)] = {}
        inf_per_comparison["AnnComp"+str(count)]["Ann info"] = (annot_names[i], annot_names[j])
        inf_per_comparison["AnnComp"+str(count)]["Precision"] = ann_comp_precis
        inf_per_comparison["AnnComp"+str(count)]["Recall"] = ann_comp_recall
        inf_per_comparison["AnnComp"+str(count)]["F-Score"] = ann_comp_fscore
        inf_per_comparison["AnnComp"+str(count)]["Set info"] = temp_dict

        count += 1

print("")
print("####   Individual comparison   ####")

for key in inf_per_comparison.keys():
    k1 = "Ann info"
    k2 = "Precision"
    k3 = "Recall"
    k4 = "F-Score"

    print(f"{inf_per_comparison[key][k1][0]} & {inf_per_comparison[key][k1][1]} --> P: {round(inf_per_comparison[key][k2], 3)}, R: {round(inf_per_comparison[key][k3], 3)}, F: {round(inf_per_comparison[key][k4], 3)}")


average_p = sum([inf_per_comparison[key]["Precision"] for key in inf_per_comparison.keys()]) / len(inf_per_comparison)
average_r = sum([inf_per_comparison[key]["Recall"] for key in inf_per_comparison.keys()]) / len(inf_per_comparison)
average_f = sum([inf_per_comparison[key]["F-Score"] for key in inf_per_comparison.keys()]) / len(inf_per_comparison)

print("")
print("####   Overall statistics   ####")
print(f"Average Precision: {round(average_p, 3)}")
print(f"Average Recall   : {round(average_r, 3)}")
print(f"Average F-score  : {round(average_f, 3)}")