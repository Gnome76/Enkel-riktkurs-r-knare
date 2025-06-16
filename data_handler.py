import json
import os

DATAFIL = "bolag_data.json"

def load_data():
    if not os.path.exists(DATAFIL):
        print("DEBUG: Filen finns inte – skapar ny tom data.")
        return {}

    try:
        with open(DATAFIL, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                print("DEBUG: Data i filen är inte en dict – återgår till tom.")
                return {}
            print(f"DEBUG: Data korrekt inläst. Antal bolag: {len(data)}")
            return data
    except Exception as e:
        print(f"DEBUG: Fel vid inläsning av JSON: {e}")
        return {}

def save_data(data):
    try:
        with open(DATAFIL, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("DEBUG: Data sparad.")
    except Exception as e:
        print(f"DEBUG: Fel vid sparande av data: {e}")
