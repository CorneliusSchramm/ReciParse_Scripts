t = {1:"hallo", 2: "bitch"}
for key, value in t.items():
    print(key, "---", value)

test = ("hallo", {})

test[1]["key"] = 5

print(test)
