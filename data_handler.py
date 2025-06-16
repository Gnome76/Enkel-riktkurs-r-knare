import json
import os

DATA_FILE = "bolag_data.json"

def load_data(filename=DATA_FILE):
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            else:
                # Om datatypen inte är dict, returnera tom dict
                return {}
    except json.JSONDecodeError:
        # Om filen är tom eller innehåller ogiltig JSON
        return {}

def save_data(data, filename=DATA_FILE):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Data sparad i {filename}. Antal bolag: {len(data)}")
