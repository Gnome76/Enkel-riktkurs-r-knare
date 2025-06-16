import streamlit as st
from data_handler import load_data, save_data
from forms import nytt_bolag_formular, redigeringsformular
from view import visa_bolag_ett_i_taget

def main():
    st.title("Enkel Riktkurs-Räknare")

    menyval = st.sidebar.radio("Meny", ["Visa bolag", "Lägg till bolag", "Redigera bolag"])

    if menyval == "Visa bolag":
        visa_bolag_ett_i_taget()

    elif menyval == "Lägg till bolag":
        data = load_data()
        nytt_bolag_formular(data)
        save_data(data)

    elif menyval == "Redigera bolag":
        data = load_data()
        redigeringsformular(data)
        save_data(data)

if __name__ == "__main__":
    main()
