import gspread
from google.oauth2.service_account import Credentials

SERVICE_ACCOUNT_FILE = "streamlit-api-463202-e98fcb55f8df.json"
GOOGLE_SHEET_NAME = "BolagData"

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
client = gspread.authorize(creds)

def load_data():
    sheet = client.open(GOOGLE_SHEET_NAME).sheet1
    data = sheet.get_all_records()  # Lista av dict
    return sheet, data

def save_data(sheet, data):
    sheet.clear()
    if not data:
        return
    headers = list(data[0].keys())
    sheet.append_row(headers)
    for row in data:
        values = [row.get(h, "") for h in headers]
        sheet.append_row(values)
