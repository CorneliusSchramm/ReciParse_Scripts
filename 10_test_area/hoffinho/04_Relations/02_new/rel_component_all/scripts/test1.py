import spacy

"""
nlp = spacy.load("de_core_news_sm")

doc = nlp("Die Eier im heißen Wasser kochen, anschließend schneiden und zur Seite legen. Dann wieder kochen lassen.")

def children_getter(token, dict):       #dict = {}
    #Creating a nested dictionary with multiple levels of children.
    
    dict[token]= {}                     #dict = {token: {} }
    
    try: 
        for child in token.children:
            children_getter(child, dict[token])     #dict = {token: {child{}}}

    except:
        return 
    
    return 

"""


"""
verb_to_string = {}

text = ""
for token in doc:
    if token.pos_ == "VERB": 
        verb_to_string[token] = text

    elif token.pos == "PUNCT":
        pass

    else: 
        it = token.text + " "
        text += it
    
    print(f"{token}: POS = {token.pos_}; DEP = {token.dep_}; DEP_HEAD = {token.head.text}")

print(verb_to_string)

final_dict = {}

for key in verb_to_string.keys():
    text = verb_to_string[key] + key.text
    doc = nlp(text)

    for token in doc: 
        if token.pos_ == "VERB":

            children_getter(token, final_dict)
        
        else: 
            pass

"""


"""
for key in verb_to_string.keys():
    text = verb_to_string[key] + key.text
    doc = nlp(text)

    for token in doc: 
        if token.pos_ == "VERB":
            child1_lst = [child for child in token.children]
            print(child1_lst)

            temp_dict = {}

            for child1 in child1_lst:
                temp_dict[child1] = {}
                try: 
                    #print(child1)
                    for child2 in child1.children: 
                        temp_dict[child1][child2] = {}    #every 

                    try: 
                        for child2 in temp_dict[child1].keys():
                            child3_lst = [child3 for child3 in child2.children]
                            temp_dict[child1][child2] = child3_lst
                    
                    
                    except:
                        print("No third level child.")
                
                except: 
                    print("No second level child.")
                    #.temp_list.append(child1)
            
            final_dict[token] = temp_dict


           # print(f"{token.text} --> {[child for child in token.children]}")
        
        else: 
            print(f"{token}: POS = {token.pos_}; DEP = {token.dep_}; DEP_HEAD = {token.head.text}")
    print("--------------")
"""

#print(final_dict)


                    