import streamlit as st
from utils import berakna_targetkurser, filtrera_undervarderade
from data_handler import las_data, spara_data
from forms import nytt_bolag_form
from views import visa_lista

def main():
    st.title("Aktieanalys med Targetkurser och Undervärdering")

    # Läs in bolag från fil till session_state om inte redan gjort
    if "bolag_list" not in st.session_state:
        st.session_state["bolag_list"] = las_data()

    # Formulär för nytt bolag
    nytt = nytt_bolag_form("nytt_bolag_form")
    if nytt:
        berakna_targetkurser(nytt)
        st.session_state["bolag_list"].append(nytt)
        spara_data(st.session_state["bolag_list"])
        st.success(f"Bolag {nytt['namn']} tillagt!")

    # Uppdatera targetkurser för alla bolag (t.ex. om någon ändrat data)
    for bolag in st.session_state["bolag_list"]:
        berakna_targetkurser(bolag)

    # Checkbox för att filtrera undervärderade
    visa_undervarderade = st.checkbox("Visa endast undervärderade (>30%)", value=False)
    lista = st.session_state["bolag_list"]
    if visa_undervarderade:
        lista = filtrera_undervarderade(lista, procent_grans=30)

    # Visa bolagslista
    if lista:
        visa_lista(lista)
    else:
        st.info("Inga bolag att visa.")

if __name__ == "__main__":
    main()
