import gspread
from google.oauth2.service_account import Credentials

# Namnet på Google Sheet (det du ser högst upp i arket)
GOOGLE_SHEET_NAME = "Ditt Google Sheet namn här"

# Din JSON-nyckelfil från Google Cloud
SERVICE_ACCOUNT_FILE = "streamlit-api-463202-980e3b760531.json"

# Scopes som krävs för att läsa och skriva i Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_sheet():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open(GOOGLE_SHEET_NAME).sheet1  # Använder första arket
    return sheet

def load_data():
    sheet = get_sheet()
    records = sheet.get_all_records()  # Returnerar en lista av dicts

    data = {}
    for record in records:
        # Förutsätter att första kolumnen är bolagsnamn
        bolagsnamn = record.get("Bolagsnamn")
        if bolagsnamn:
            # Ta bort nyckeln 'Bolagsnamn' för att spara resten i dict
            bolag_data = {k: v for k, v in record.items() if k != "Bolagsnamn"}
            data[bolagsnamn] = bolag_data
    return data

def save_data(data):
    sheet = get_sheet()
    # För att skriva till Google Sheets behöver vi skriva om hela tabellen

    # Skapa lista med rubriker (kolumnnamn)
    headers = ["Bolagsnamn"]
    # Hitta alla unika nycklar i data (alla fält)
    keys = set()
    for bolag in data.values():
        keys.update(bolag.keys())
    headers.extend(sorted(keys))  # Sortera för konsekvens

    # Bygg rader: första rad = headers
    rows = [headers]

    # Lägg till data-rader
    for bolagsnamn, bolag_data in data.items():
        row = [bolagsnamn]
        for key in headers[1:]:
            row.append(bolag_data.get(key, ""))
        rows.append(row)

    # Rensa befintligt ark
    sheet.clear()

    # Skriv alla rader
    sheet.update(rows)
    print(f"Data sparad i Google Sheet '{GOOGLE_SHEET_NAME}'. Antal bolag: {len(data)}")
