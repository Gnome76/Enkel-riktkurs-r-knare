import streamlit as st
from data_handler import load_data
from forms import nytt_bolag_formular, redigeringsformular
from view import visa_bolag_ett_i_taget

def main():
    data = load_data()

    st.title("Aktieanalysapp")

    meny = st.sidebar.radio("Välj vy", ["Visa bolag", "Lägg till nytt bolag", "Redigera bolag"])

    if meny == "Visa bolag":
        visa_bolag_ett_i_taget()
    elif meny == "Lägg till nytt bolag":
        nytt_bolag_formular(data)
    elif meny == "Redigera bolag":
        redigeringsformular(data)

if __name__ == "__main__":
    main()
