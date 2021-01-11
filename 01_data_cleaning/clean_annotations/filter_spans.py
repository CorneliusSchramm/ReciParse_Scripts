from prodigy.components.db import connect
db = connect()
examples = db.get_dataset("test354564")
filtered_examples = []
for eg in examples:
	if "spans" in eg:
		new_spans = []
		for span in eg["spans"]:
			if "start" not in span or "end" not in span:
				print("Found bad span:", span)
			else:
				#### Leos Input: Giovannis Code ####
				print("---START---")
				print(span)
				v = span
				if "text" not in span.keys():
					try:
						span["text"] = eg["text"][span["start"]:span["end"]]
						span["type"] = "ent"
					except KeyError:
						print("KeyError")
				print(span)
				n = span
				print("----END----")
				#### End of Input ####
				new_spans.append(span)
		eg["spans"] = new_spans
	filtered_examples.append(eg)

# Add filtered examples to new dataset
db.add_dataset("myDataset2_filtered")
db.add_examples(filtered_examples, ["overlap_coco_f"])
