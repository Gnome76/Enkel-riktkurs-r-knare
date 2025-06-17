import gspread
from google.oauth2.service_account import Credentials

GOOGLE_SHEET_NAME = "BolagData"
SERVICE_ACCOUNT_FILE = "streamlit-api-463202-e98fcb55f8df.json"  # Din JSON-nyckelfil

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Autentisering
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
client = gspread.authorize(creds)

def load_sheet():
    sheet = client.open(GOOGLE_SHEET_NAME).sheet1
    data = sheet.get_all_records()
    return sheet, data

def save_data(sheet, data):
    sheet.clear()  # Rensa arket helt
    if data:
        headers = list(data[0].keys())
        sheet.append_row(headers)
        for row in data:
            values = [row.get(h, "") for h in headers]
            sheet.append_row(values)
    else:
        print("Ingen data att spara.")

def main():
    sheet, data = load_sheet()
    print("Data från Google Sheet:")
    print(data)

    nytt_bolag = {
        "Bolagsnamn": "TestAB",
        "kurs": 10.0,
        "pe_nuvarande": 15.0,
        "pe_1": 14.5,
        "pe_2": 14.0,
        "pe_3": 13.5,
        "pe_4": 13.0,
        "ps_nuvarande": 2.5,
        "ps_1": 2.4,
        "ps_2": 2.3,
        "ps_3": 2.2,
        "ps_4": 2.1,
        "vinst_i_ar": 5.0,
        "vinst_nasta_ar": 5.5,
        "oms_tillv_i_ar": 10.0,
        "oms_tillv_nasta_ar": 12.0,
    }
    data.append(nytt_bolag)

    save_data(sheet, data)

    print("Data efter tillägg sparad:")
    data_uppdaterad = sheet.get_all_records()
    print(data_uppdaterad)

if __name__ == "__main__":
    main()
