import json
import os

# Namnet på JSON-filen där data ska sparas/läsas
DATA_FILE = "bolag_data.json"

def load_data(filename=DATA_FILE):
    """Läser in bolagsdata från JSON-fil."""
    if not os.path.exists(filename):
        print(f"[load_data] Filen finns inte: {filename}")
        return {}

    try:
        with open(filename, "r") as f:
            data = json.load(f)
            if isinstance(data, dict):
                print(f"[load_data] Laddade {len(data)} bolag från {filename}")
                return data
            else:
                print("[load_data] Fel format, inte dict – återgår till tom dict.")
                return {}
    except json.JSONDecodeError:
        print("[load_data] JSONDecodeError – ogiltig JSON eller tom fil.")
        return {}

def save_data(data, filename=DATA_FILE):
    """Sparar bolagsdata till JSON-fil."""
    full_path = os.path.abspath(filename)
    print(f"[save_data] Försöker spara data till: {full_path}")
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[save_data] Sparade {len(data)} bolag till {full_path}")
    except Exception as e:
        print(f"[save_data] FEL vid sparning: {e}")
