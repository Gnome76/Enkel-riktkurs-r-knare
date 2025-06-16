import json
import os

FILNAMN = "bolag_data.json"

def load_data():
    if not os.path.exists(FILNAMN):
        print("DEBUG: Filen finns inte, returnerar tom dict.")
        return {}

    try:
        with open(FILNAMN, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            print(f"DEBUG: Filen lästes in men innehåller inte en dict: {type(data)}")
            return {}
        print(f"DEBUG: Data laddad, antal bolag: {len(data)}")
        return data
    except Exception as e:
        print(f"DEBUG: Fel vid inläsning av JSON: {e}")
        return {}
