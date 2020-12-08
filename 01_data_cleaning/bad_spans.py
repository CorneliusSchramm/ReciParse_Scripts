from prodigy.components.db import connect
db = connect()
examples = db.get_dataset("batch1coco30")
filtered_examples = []
for eg in examples:
    if "spans" in eg:
        new_spans = []
        for span in eg["spans"]:
            if "start" not in span or "end" not in span:
                print("Found bad span:", span)
            else:
                new_spans.append(span)
        eg["spans"] = new_spans
    filtered_examples.append(eg)

# Add filtered examples to new dataset
db.add_dataset("myDataset2_filtered")
db.add_examples(filtered_examples, ["batch1coco30_f"])