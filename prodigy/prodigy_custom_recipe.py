# Sources
# https://prodi.gy/docs/custom-recipes


import prodigy
@prodigy.recipe("kitchen_relations")

def kitchen_relations(dataset, data_path):
    stream = data_path # ???

# return a dictionairy of components that define the settings for the annotation server
    return {
        "dataset": dataset,
        "stream": stream,
        "view_id": "relations"
        
    }