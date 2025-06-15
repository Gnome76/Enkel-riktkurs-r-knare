import json
import os
from utils import berakna_targetkurser

DATAFIL = "bolag_data.json"

def ladda_data():
    if not os.path.exists(DATAFIL):
        return []

    with open(DATAFIL, "r") as f:
        data = json.load(f)

    # Uppdatera varje bolag med nya beräkningar
    for bolag in data:
        result = berakna_targetkurser(bolag)
        bolag.update(result)

    return data

def spara_data(data):
    # Uppdatera varje bolag med nya beräkningar innan det sparas
    for bolag in data:
        result = berakna_targetkurser(bolag)
        bolag.update(result)

    with open(DATAFIL, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
