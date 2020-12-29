st = [(ent.start, ent.text) for ent in pred.ents if ent.label_ == "V" ]

# threshhold = 0.2
# steps_list = []
# for v_start, v in v_list:
#     step_tup = (v,{})
#     for rels_tup, probs in pred._.rel.items():
#         max_prob_rel = max(probs, key=probs.get)
#         if rels_tup[0] == v_start and (probs[max_prob_rel] > threshhold): #and rels_tup[1] not in list(zip(*v_list))[1]:
#             if probs[max_prob_rel] not in step_tup[1]:
#                 step_tup[1][max_prob_rel] = [pred[rels_tup[1]].text] # doc[ent_start_i]
#             else:
#                 step_tup[1][max_prob_rel].append(pred[rels_tup[1]].text)
#     steps_list.append(step_tup) 

# print(steps_list