import streamlit as st
from data_handler import load_data
from view import visa_alla_bolag, visa_ett_bolag
from forms import nytt_bolag_form, redigera_bolag_form, ta_bort_bolag_form

def main():
    st.set_page_config(page_title="Enkel riktkursräknare", layout="centered")
    st.title("📈 Mina sparade bolag")

    data = load_data()
    st.caption("Debug – inläst data från data.json")
    st.json(data)

    vy = st.sidebar.radio("Välj vy", ["Visa alla", "Visa ett bolag i taget", "Lägg till bolag", "Redigera bolag", "Ta bort bolag"])

    if vy == "Visa alla":
        visa_alla_bolag(data)
    elif vy == "Visa ett bolag i taget":
        visa_ett_bolag(data)
    elif vy == "Lägg till bolag":
        nytt_bolag_form()
    elif vy == "Redigera bolag":
        redigera_bolag_form()
    elif vy == "Ta bort bolag":
        ta_bort_bolag_form()

if __name__ == "__main__":
    main()
