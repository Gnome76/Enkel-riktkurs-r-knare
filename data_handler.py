import json
import os
from datetime import datetime
from utils import berakna_targetkurser

DATAFIL = "bolag_data.json"

def las_data():
    if os.path.exists(DATAFIL):
        with open(DATAFIL, "r") as f:
            return json.load(f)
    return {}

def spara_data(data):
    with open(DATAFIL, "w") as f:
        json.dump(data, f, indent=4)

def lagg_till_eller_uppdatera_bolag(bolagsdata):
    data = las_data()
    namn = bolagsdata["namn"]

    # Lägg till datum
    bolagsdata["senast_andrad"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Räkna ut targetkurser och undervärdering
    resultat = berakna_targetkurser(bolagsdata)
    bolagsdata.update(resultat)

    # Spara
    data[namn] = bolagsdata
    spara_data(data)

def hamta_bolag(namn):
    data = las_data()
    return data.get(namn)

def hamta_alla_bolag():
    return las_data()

def ta_bort_bolag(namn):
    data = las_data()
    if namn in data:
        del data[namn]
        spara_data(data)
