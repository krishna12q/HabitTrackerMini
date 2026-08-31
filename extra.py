import json


import json

def pull_habit_ids():
    with open("info.json", "r") as file:
        data = json.load(file)
    
    # Extract only the specific fields needed into a list of dicts
    habits = []
    for habit in data["habits"]:
        habits.append({
            "id": habit["id"],
            "completed": habit["completed"],
            "icon": habit["icon"],
            "color": habit["color"]
        })
    
    return habits


data = pull_habit_ids()
print(data)
