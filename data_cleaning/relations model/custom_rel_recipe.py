import prodigy

@prodigy.recipe(
    "my-custom-recipe",
    dataset=("Dataset to save answers to", "positional", None, str),
    view_id=("Annotation interface", "option", "v", str)
)
def my_custom_recipe(dataset, view_id="text"):
    # Load your own streams from anywhere you want
    stream = load_my_custom_stream()

    def update(examples):
        # This function is triggered when Prodigy receives annotations
        print(f"Received {len(examples)} annotations!")

    return {
        "dataset": dataset,
        "view_id": view_id,
        "stream": stream,
        "update": update
    }



# Call with: prodigy my-custom-recipe my_dataset --view-id text -F custom-rel_recipe.py