import gspread
from google.oauth2.service_account import Credentials

SERVICE_ACCOUNT_FILE = "streamlit-api-463202-e98fcb55f8df.json"  # Ditt filnamn
GOOGLE_SHEET_NAME = "BolagData"  # Ditt Google Sheet namn

def test_gsheets():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
    client = gspread.authorize(creds)

    # Öppna dokumentet
    sheet = client.open(GOOGLE_SHEET_NAME)

    # Skriv ut arkens namn
    worksheets = sheet.worksheets()
    print("Följande ark finns i dokumentet:")
    for ws in worksheets:
        print("-", ws.title)

if __name__ == "__main__":
    test_gsheets()
