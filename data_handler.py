import json
import os
from datetime import datetime

DATAFIL = "bolag_data.json"

def las_bolag():
    if os.path.exists(DATAFIL):
        with open(DATAFIL, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def spara_bolag_lista(bolag_lista):
    with open(DATAFIL, "w", encoding="utf-8") as f:
        json.dump(bolag_lista, f, ensure_ascii=False, indent=2)

def lagg_till_eller_uppdatera_bolag(nytt_bolag):
    bolag_lista = las_bolag()
    nytt_bolag["senast_andrad"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Ersätt om bolaget redan finns
    uppdaterad = False
    for i, bolag in enumerate(bolag_lista):
        if bolag["namn"] == nytt_bolag["namn"]:
            bolag_lista[i] = nytt_bolag
            uppdaterad = True
            break

    if not uppdaterad:
        bolag_lista.append(nytt_bolag)

    spara_bolag_lista(bolag_lista)

def ta_bort_bolag(namn):
    bolag_lista = las_bolag()
    bolag_lista = [b for b in bolag_lista if b["namn"] != namn]
    spara_bolag_lista(bolag_lista)
