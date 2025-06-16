import json
import os

FILNAMN = "bolag_data.json"

def load_data():
    """
    Ladda bolagsdata från JSON-fil.
    Returnerar en dict med bolagsdata.
    Om filen inte finns, returneras en tom dict.
    """
    if not os.path.exists(FILNAMN):
        return {}

    try:
        with open(FILNAMN, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        # Vid fel, returnera tom dict men skriv ut fel i konsolen (kan bytas till logg)
        print(f"Fel vid inläsning av {FILNAMN}: {e}")
        return {}

def save_data(data):
    """
    Spara bolagsdata till JSON-fil.
    Tar en dict som input.
    """
    try:
        with open(FILNAMN, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Fel vid sparning av {FILNAMN}: {e}")
