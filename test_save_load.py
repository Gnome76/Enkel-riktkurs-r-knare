import os
import json
from data_handler import save_data, load_data

def test_save_load():
    test_filename = "test_bolag_data.json"

    # Testdata att spara
    test_data = {
        "Testbolag": {
            "kurs": 100.0,
            "pe_1": 10.0,
            "pe_2": 12.0,
            "ps_1": 1.5,
            "ps_2": 1.7
        }
    }

    # Spara testdata
    save_data(test_data, filename=test_filename)

    # Läs in data igen
    data_loaded = load_data(filename=test_filename)

    # Rensa upp: ta bort testfilen efter test
    if os.path.exists(test_filename):
        os.remove(test_filename)

    return test_data, data_loaded
