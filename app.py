import streamlit as st
from data_handler import load_data
from forms import lagg_till_bolag_form, redigera_bolag_form, tabort_bolag_form
from view import visa_bolag_ett_i_taget

st.set_page_config(page_title="Aktieanalys", layout="centered")

if "data" not in st.session_state:
    st.session_state.data = load_data()

st.title("Aktieanalysapp")

meny = st.sidebar.radio("Navigering", ["Visa bolag", "Lägg till bolag", "Redigera bolag", "Ta bort bolag"])

if meny == "Visa bolag":
    visa_bolag_ett_i_taget()

elif meny == "Lägg till bolag":
    lagg_till_bolag_form()

elif meny == "Redigera bolag":
    redigera_bolag_form()

elif meny == "Ta bort bolag":
    tabort_bolag_form()
