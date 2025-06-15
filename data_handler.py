import json
import os

DATA_FIL = "bolag_data.json"

def load_data():
    """Ladda bolagsdata från JSON-fil. Returnerar lista av dicts."""
    if not os.path.exists(DATA_FIL):
        return []
    with open(DATA_FIL, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
    return data

def save_data(data):
    """Spara bolagsdata till JSON-fil."""
    with open(DATA_FIL, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def add_bolag(bolag_list, nytt_bolag):
    """Lägg till nytt bolag i listan och spara."""
    bolag_list.append(nytt_bolag)
    save_data(bolag_list)

def update_bolag(bolag_list, index, uppdaterat_bolag):
    """Uppdatera bolag på angiven index och spara."""
    if 0 <= index < len(bolag_list):
        bolag_list[index] = uppdaterat_bolag
        save_data(bolag_list)

def remove_bolag(bolag_list, index):
    """Ta bort bolag på angiven index och spara."""
    if 0 <= index < len(bolag_list):
        bolag_list.pop(index)
        save_data(bolag_list)
