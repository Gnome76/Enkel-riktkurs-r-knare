import streamlit as st
from utils import berakna_targetkurser
from data_handler import save_data

def visa_inmatningsform(data):
    st.header("📋 Hantera bolag")

    bolagsnamn_lista = [b["namn"] for b in data]
    valt_bolag = st.selectbox("Välj bolag att redigera eller ta bort", options=[""] + bolagsnamn_lista)

    if valt_bolag and valt_bolag in bolagsnamn_lista:
        befintligt = next(b for b in data if b["namn"] == valt_bolag)
    else:
        befintligt = {}

    with st.form(key="inmatning_form"):
        namn = st.text_input("Bolagsnamn", value=befintligt.get("namn", ""))
        nuvarande_kurs = st.number_input("Nuvarande kurs", value=befintligt.get("nuvarande_kurs", 0.0))
        nuvarande_pe = st.number_input("Nuvarande P/E", value=befintligt.get("nuvarande_pe", 0.0))
        pe1 = st.number_input("P/E 1", value=befintligt.get("pe1", 0.0))
        pe2 = st.number_input("P/E 2", value=befintligt.get("pe2", 0.0))
        pe3 = st.number_input("P/E 3", value=befintligt.get("pe3", 0.0))
        pe4 = st.number_input("P/E 4", value=befintligt.get("pe4", 0.0))

        nuvarande_ps = st.number_input("Nuvarande P/S", value=befintligt.get("nuvarande_ps", 0.0))
        ps1 = st.number_input("P/S 1", value=befintligt.get("ps1", 0.0))
        ps2 = st.number_input("P/S 2", value=befintligt.get("ps2", 0.0))
        ps3 = st.number_input("P/S 3", value=befintligt.get("ps3", 0.0))
        ps4 = st.number_input("P/S 4", value=befintligt.get("ps4", 0.0))

        vinst_iar = st.number_input("Förväntad vinst i år", value=befintligt.get("vinst_iar", 0.0))
        vinst_nastaar = st.number_input("Förväntad vinst nästa år", value=befintligt.get("vinst_nastaar", 0.0))
        oms_tillv_iar = st.number_input("Omsättningstillväxt i år (%)", value=befintligt.get("oms_tillv_iar", 0.0))
        oms_tillv_nastaar = st.number_input("Omsättningstillväxt nästa år (%)", value=befintligt.get("oms_tillv_nastaar", 0.0))

        submit = st.form_submit_button("💾 Spara bolag")

    if submit:
        nytt_bolag = {
            "namn": namn,
            "nuvarande_kurs": nuvarande_kurs,
            "nuvarande_pe": nuvarande_pe,
            "pe1": pe1,
            "pe2": pe2,
            "pe3": pe3,
            "pe4": pe4,
            "nuvarande_ps": nuvarande_ps,
            "ps1": ps1,
            "ps2": ps2,
            "ps3": ps3,
            "ps4": ps4,
            "vinst_iar": vinst_iar,
            "vinst_nastaar": vinst_nastaar,
            "oms_tillv_iar": oms_tillv_iar,
            "oms_tillv_nastaar": oms_tillv_nastaar
        }

        nytt_bolag.update(berakna_targetkurser(nytt_bolag))

        # Uppdatera eller lägg till
        data = [b for b in data if b["namn"] != namn]
        data.append(nytt_bolag)
        save_data(data)

        st.success(f"{namn} har sparats.")
        st.experimental_rerun()

    # Funktion för att ta bort bolag
    if valt_bolag and valt_bolag in bolagsnamn_lista:
        if st.button(f"🗑️ Ta bort '{valt_bolag}' permanent"):
            data = [b for b in data if b["namn"] != valt_bolag]
            save_data(data)
            st.success(f"{valt_bolag} har tagits bort.")
            st.experimental_rerun()
