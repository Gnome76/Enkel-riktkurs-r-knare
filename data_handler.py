import json
import os

DATAFIL = "bolag_data.json"


def las_bolag():
    """Läser in bolagsdata från JSON-fil."""
    if os.path.exists(DATAFIL):
        with open(DATAFIL, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def spara_bolag(bolag_lista):
    """Sparar bolagsdata till JSON-fil."""
    with open(DATAFIL, "w", encoding="utf-8") as f:
        json.dump(bolag_lista, f, indent=2, ensure_ascii=False)
