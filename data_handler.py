import json
import os

DATAFIL = "bolag_data.json"

def load_data():
    if not os.path.exists(DATAFIL):
        return {}
    with open(DATAFIL, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATAFIL, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
