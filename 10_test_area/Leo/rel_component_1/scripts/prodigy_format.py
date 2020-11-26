

# PRODIGY OUTPUT -------------------------------------------------------------------------------

 		# # Create main output dict for prodigy
   #  	main_dict = {}

   #  	# TEXT KEY
   #      main_dict["text"] = pred.text

        # INPUT HASH KEY
        # TASK HASH KEY
        # SPANS KEY
        # TOKENS KEY
        # SESSION ID KEY
        # VIEW ID KEY

        # RELATIONS KEY
        relations = []
        ents_dict = { ent.start: (ent.text, ent.start, ent.end, ent.label_) for ent in pred.ents }
        tokens = { token.i: (token.text, token.idx, token.idx+len(token.text)) for token in pred }

        for item in pred._.rel.items():
        	if max(item[1].values()) > threshold:

        		# What is the most probable label and how high is the probability
        		print("Maximum Probability:", max(item[1].values()), "for", max(item[1], key=item[1].get))

        		# Build relations dict

	        	relation = dict()
	        	relation["head"] = item[0][0]
	        	relation["child"] = item[0][1]
	        	relation["head_span"] = dict()
	        	relation["child_span"] = dict()
	        	relation["color"] = colors_dict[max(item[1], key=item[1].get)]
	        	relation["label"] = max(item[1], key=item[1].get)

	        	relation["head_span"]["start"] = tokens[item[0][0]][1]
	        	relation["head_span"]["end"] = tokens[item[0][0]][2]
	        	relation["head_span"]["token_start"] = item[0][0]
	        	relation["head_span"]["token_end"] = ents_dict[item[0][0]][2]-1
	        	relation["head_span"]["label"] = ents_dict[item[0][0]][3]

	        	relation["child_span"]["start"] = tokens[item[0][1]][1]
	        	relation["child_span"]["end"] = tokens[item[0][1]][2]
	        	relation["child_span"]["token_start"] = item[0][1]
	        	relation["child_span"]["token_end"] = ents_dict[item[0][1]][2]-1
	        	relation["child_span"]["label"] = ents_dict[item[0][1]][3]

	        	print(relation)
	        	relations.append(relation)
        
        	break