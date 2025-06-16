import streamlit as st
from test_save_load import test_save_load
from data_handler import load_data
from forms import nytt_bolag_formular, redigeringsformular
from view import visa_bolag_ett_i_taget

def main():
    st.title("Aktieanalysapp")

    meny = st.sidebar.radio("Välj vy", ["Visa bolag", "Lägg till nytt bolag", "Redigera bolag", "Testa spar/läs"])

    if meny == "Visa bolag":
        data = load_data()
        visa_bolag_ett_i_taget(data)
    elif meny == "Lägg till nytt bolag":
        data = load_data()
        nytt_bolag_formular(data)
    elif meny == "Redigera bolag":
        data = load_data()
        redigeringsformular(data)
    elif meny == "Testa spar/läs":
        test_data, loaded_data = test_save_load()
        st.write("Data som sparades:")
        st.json(test_data)
        st.write("Data som lästes in:")
        st.json(loaded_data)

if __name__ == "__main__":
    main()
