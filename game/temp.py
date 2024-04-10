import json

f = open('game/imageMetaData.json')

data = json.load(f)

print(data)
print("separator")
print(data["block"])
print("separator")
for key in data:
    print("key is:",key)