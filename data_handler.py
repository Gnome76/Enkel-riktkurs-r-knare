import json
import os
from datetime import datetime

DATAFIL = "bolag_data.json"

def load_data():
    if not os.path.exists(DATAFIL):
        return {}
    with open(DATAFIL, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATAFIL, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def lägg_till_bolag(namn, info):
    data = load_data()
    info["insatt_datum"] = datetime.today().strftime("%Y-%m-%d")
    data[namn] = info
    save_data(data)

def uppdatera_bolag(namn, info):
    data = load_data()
    info["insatt_datum"] = datetime.today().strftime("%Y-%m-%d")
    data[namn] = info
    save_data(data)

def radera_bolag(namn):
    data = load_data()
    if namn in data:
        del data[namn]
        save_data(data)
