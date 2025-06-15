import json
import os
from datetime import datetime

DATA_FILE = "bolag_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def add_or_update_company(company_data, editing=False):
    data = load_data()
    existing_index = next((i for i, d in enumerate(data) if d["namn"] == company_data["namn"]), None)

    company_data["senast_andrad"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    if editing and existing_index is not None:
        data[existing_index] = company_data
    elif existing_index is None:
        company_data["insatt_datum"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        data.append(company_data)
    else:
        # Overwrite anyway if editing is not set but company already exists
        data[existing_index] = company_data

    save_data(data)

def delete_company(company_name):
    data = load_data()
    data = [d for d in data if d["namn"] != company_name]
    save_data(data)
