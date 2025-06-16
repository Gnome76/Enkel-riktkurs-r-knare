import streamlit as st
from data_handler import load_data, save_data
from forms import nytt_bolag_formular, redigeringsformular
from view import visa_bolag_ett_i_taget

def main():
    st.title("Aktieanalysapp")

    data = load_data()

    # Huvudmeny: Lägg till eller redigera bolag
    val = st.radio("Vad vill du göra?", ("Visa bolag", "Lägg till nytt bolag", "Redigera befintligt bolag"))

    if val == "Visa bolag":
        visa_bolag_ett_i_taget()
    elif val == "Lägg till nytt bolag":
        if nytt_bolag_formular(data):
            save_data(data)
            st.success("Nytt bolag tillagt och sparat!")
    elif val == "Redigera befintligt bolag":
        if redigeringsformular(data):
            save_data(data)
            st.success("Bolagsdata uppdaterad och sparad!")

if __name__ == "__main__":
    main()
