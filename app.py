import streamlit as st
from data_handler import load_data
from forms import nytt_bolag_formular, redigeringsformular
from view import visa_bolag_ett_i_taget

def main():
    st.set_page_config(page_title="Aktieanalys", layout="centered")
    st.title("📈 Aktieanalysapp")

    # Läs in data
    data = load_data()

    # Meny
    menyval = st.sidebar.radio("Välj vy", ["Visa bolag", "Lägg till nytt bolag", "Redigera bolag"])

    if menyval == "Visa bolag":
        visa_bolag_ett_i_taget(data)
    elif menyval == "Lägg till nytt bolag":
        nytt_bolag_formular(data)
    elif menyval == "Redigera bolag":
        redigeringsformular(data)

if __name__ == "__main__":
    main()
