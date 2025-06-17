import json
import os

def load_data(filepath="data.json"):
    if not os.path.exists(filepath):
        return {}  # Om filen inte finns, returnera tom dict
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            # Om JSON är fel eller filen är tom, returnera tom dict
            return {}
    return data
