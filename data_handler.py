import json
import os

DATA_FILE = "data.json"

def load_data():
    """Läser in sparade bolag från JSON-filen."""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_data(data):
    """Sparar bolag till JSON-filen."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def ta_bort_bolag(namn):
    """Tar bort ett bolag med angivet namn."""
    data = load_data()
    if namn in data:
        del data[namn]
        save_data(data)
