import json
import os

FILNAMN = "bolag_data.json"

def load_data():
    if os.path.exists(FILNAMN):
        with open(FILNAMN, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def save_data(data):
    with open(FILNAMN, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
