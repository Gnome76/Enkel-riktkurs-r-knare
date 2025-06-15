import streamlit as st
from datetime import datetime
from utils import berakna_targetkurser

def input_form():
    with st.form("input_form", clear_on_submit=True):
        st.subheader("➕ Lägg till nytt bolag")

        namn = st.text_input("Bolagsnamn")
        nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0)

        nuvarande_pe = st.number_input("Nuvarande P/E", min_value=0.0)
        pe1 = st.number_input("P/E 1", min_value=0.0)
        pe2 = st.number_input("P/E 2", min_value=0.0)
        pe3 = st.number_input("P/E 3", min_value=0.0)
        pe4 = st.number_input("P/E 4", min_value=0.0)

        nuvarande_ps = st.number_input("Nuvarande P/S", min_value=0.0)
        ps1 = st.number_input("P/S 1", min_value=0.0)
        ps2 = st.number_input("P/S 2", min_value=0.0)
        ps3 = st.number_input("P/S 3", min_value=0.0)
        ps4 = st.number_input("P/S 4", min_value=0.0)

        vinst_i_ar = st.number_input("Förväntad vinst i år", min_value=0.0)
        vinst_nastaar = st.number_input("Förväntad vinst nästa år", min_value=0.0)
        tillvaxt_i_ar = st.number_input("Omsättningstillväxt i år (%)", min_value=0.0)
        tillvaxt_nastaar = st.number_input("Omsättningstillväxt nästa år (%)", min_value=0.0)

        submitted = st.form_submit_button("Spara bolag")

        if submitted and namn:
            bolag = {
                "namn": namn,
                "nuvarande_kurs": nuvarande_kurs,
                "nuvarande_pe": nuvarande_pe,
                "pe1": pe1, "pe2": pe2, "pe3": pe3, "pe4": pe4,
                "nuvarande_ps": nuvarande_ps,
                "ps1": ps1, "ps2": ps2, "ps3": ps3, "ps4": ps4,
                "vinst_i_ar": vinst_i_ar,
                "vinst_nastaar": vinst_nastaar,
                "tillvaxt_i_ar": tillvaxt_i_ar,
                "tillvaxt_nastaar": tillvaxt_nastaar,
                "insatt_datum": datetime.now().strftime("%Y-%m-%d"),
            }

            # Beräkna targetkurser
            bolag.update(berakna_targetkurser(bolag))
            return bolag
    return None

def edit_form(bolag):
    with st.form("edit_form_" + bolag["namn"]):
        st.subheader(f"✏️ Redigera {bolag['namn']}")

        nuvarande_kurs = st.number_input("Nuvarande kurs", value=bolag.get("nuvarande_kurs", 0.0))
        nuvarande_pe = st.number_input("Nuvarande P/E", value=bolag.get("nuvarande_pe", 0.0))
        pe1 = st.number_input("P/E 1", value=bolag.get("pe1", 0.0))
        pe2 = st.number_input("P/E 2", value=bolag.get("pe2", 0.0))
        pe3 = st.number_input("P/E 3", value=bolag.get("pe3", 0.0))
        pe4 = st.number_input("P/E 4", value=bolag.get("pe4", 0.0))

        nuvarande_ps = st.number_input("Nuvarande P/S", value=bolag.get("nuvarande_ps", 0.0))
        ps1 = st.number_input("P/S 1", value=bolag.get("ps1", 0.0))
        ps2 = st.number_input("P/S 2", value=bolag.get("ps2", 0.0))
        ps3 = st.number_input("P/S 3", value=bolag.get("ps3", 0.0))
        ps4 = st.number_input("P/S 4", value=bolag.get("ps4", 0.0))

        vinst_i_ar = st.number_input("Förväntad vinst i år", value=bolag.get("vinst_i_ar", 0.0))
        vinst_nastaar = st.number_input("Förväntad vinst nästa år", value=bolag.get("vinst_nastaar", 0.0))
        tillvaxt_i_ar = st.number_input("Omsättningstillväxt i år (%)", value=bolag.get("tillvaxt_i_ar", 0.0))
        tillvaxt_nastaar = st.number_input("Omsättningstillväxt nästa år (%)", value=bolag.get("tillvaxt_nastaar", 0.0))

        uppdatera = st.form_submit_button("Uppdatera")
        if uppdatera:
            nytt = {
                "namn": bolag["namn"],
                "nuvarande_kurs": nuvarande_kurs,
                "nuvarande_pe": nuvarande_pe,
                "pe1": pe1, "pe2": pe2, "pe3": pe3, "pe4": pe4,
                "nuvarande_ps": nuvarande_ps,
                "ps1": ps1, "ps2": ps2, "ps3": ps3, "ps4": ps4,
                "vinst_i_ar": vinst_i_ar,
                "vinst_nastaar": vinst_nastaar,
                "tillvaxt_i_ar": tillvaxt_i_ar,
                "tillvaxt_nastaar": tillvaxt_nastaar,
                "insatt_datum": bolag["insatt_datum"],
                "senast_andrad": datetime.now().strftime("%Y-%m-%d"),
            }
            nytt.update(berakna_targetkurser(nytt))
            return nytt
    return None
