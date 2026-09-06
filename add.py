import json

info = { 
    "ceeericsssket": {
        "created": "2026-09-02T12:00:00",
        "completions": [
            "2026-09-01T12:00:00",
            "2026-09-03T12:00:00"
        ]
    },
}

# 1. Open the old file, or start with an empty DICTIONARY if it doesn't exist
try:
    with open("data.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}  # Changed from [] to {}

# 2. Merge the new data into the existing dictionary
data.update(info)

# 3. Save everything back
with open("data.json", "w") as f:
    json.dump(data, f, indent=4)
