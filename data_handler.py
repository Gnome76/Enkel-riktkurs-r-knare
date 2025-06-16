import json
import os
from datetime import datetime

DATA_FILE = "bolag_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def add_or_update_company(data, namn, bolag_data):
    today = datetime.today().strftime("%Y-%m-%d")
    bolag_data["senast_andrad"] = today
    data[namn] = bolag_data
    save_data(data)

def delete_company(data, namn):
    if namn in data:
        del data[namn]
        save_data(data)

def get_sorted_companies(data, undervardering_filter=False):
    def sort_key(item):
        v = item[1]
        return max(v.get("undervardering_pe_i_ar", 0), v.get("undervardering_ps_i_ar", 0))

    if undervardering_filter:
        filtered = {
            namn: v for namn, v in data.items()
            if v.get("undervardering_pe_i_ar", 0) >= 30 or v.get("undervardering_ps_i_ar", 0) >= 30
        }
        return dict(sorted(filtered.items(), key=sort_key, reverse=True))
    return dict(sorted(data.items(), key=sort_key, reverse=True))
