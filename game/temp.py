import json

f = open('game/projectCostData.json')

data = json.load(f)

print(data)
print("separator")
lst = data["projectLists"]
print("type of lst",type(lst))
print(lst)
print("separator")
projToCostMap = data["projectToCostMap"]
print("type of map",type(projToCostMap))
print(projToCostMap)
print("separator")