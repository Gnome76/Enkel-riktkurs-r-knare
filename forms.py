import streamlit as st
from data_handler import save_data

def bolagsform(data):
    st.subheader("➕ Lägg till eller uppdatera bolag")
    with st.form("bolagsform"):
        namn = st.text_input("Bolagsnamn").strip()

        kurs = st.number_input("Nuvarande kurs", min_value=0.0, step=1.0)
        pe_nuvarande = st.number_input("Nuvarande P/E", min_value=0.0, step=1.0)
        ps_nuvarande = st.number_input("Nuvarande P/S", min_value=0.0, step=0.1)

        vinst_i_ar = st.number_input("Förväntad vinst i år", min_value=0.0, step=0.1)
        vinst_nasta_ar = st.number_input("Förväntad vinst nästa år", min_value=0.0, step=0.1)

        oms_tillv_i_ar = st.number_input("Omsättningstillväxt i år (%)", min_value=0.0, step=0.1) / 100 + 1
        oms_tillv_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", min_value=0.0, step=0.1) / 100 + 1

        pe_1 = st.number_input("P/E år 1", min_value=0.0, step=1.0)
        pe_2 = st.number_input("P/E år 2", min_value=0.0, step=1.0)
        pe_3 = st.number_input("P/E år 3", min_value=0.0, step=1.0)
        pe_4 = st.number_input("P/E år 4", min_value=0.0, step=1.0)

        ps_1 = st.number_input("P/S år 1", min_value=0.0, step=0.1)
        ps_2 = st.number_input("P/S år 2", min_value=0.0, step=0.1)
        ps_3 = st.number_input("P/S år 3", min_value=0.0, step=0.1)
        ps_4 = st.number_input("P/S år 4", min_value=0.0, step=0.1)

        submitted = st.form_submit_button("💾 Spara bolag")

        if submitted and namn:
            data[namn] = {
                "kurs": kurs,
                "pe_nuvarande": pe_nuvarande,
                "pe_1": pe_1,
                "pe_2": pe_2,
                "pe_3": pe_3,
                "pe_4": pe_4,
                "ps_nuvarande": ps_nuvarande,
                "ps_1": ps_1,
                "ps_2": ps_2,
                "ps_3": ps_3,
                "ps_4": ps_4,
                "vinst_i_ar": vinst_i_ar,
                "vinst_nasta_ar": vinst_nasta_ar,
                "oms_tillv_i_ar": oms_tillv_i_ar,
                "oms_tillv_nasta_ar": oms_tillv_nasta_ar
            }
            save_data(data)
            st.success(f"{namn} sparades.")
            st.experimental_rerun()
