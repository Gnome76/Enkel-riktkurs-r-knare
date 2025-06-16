import streamlit as st
from data_handler import save_data, load_data
from datetime import datetime

def nytt_bolag_formular(data):
    st.header("📈 Lägg till nytt bolag")

    with st.form("nytt_bolag_form"):
        bolagsnamn = st.text_input("Bolagsnamn")
        nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, step=0.1)
        vinst_i_ar = st.number_input("Förväntad vinst i år", step=0.1)
        vinst_nasta_ar = st.number_input("Förväntad vinst nästa år", step=0.1)
        oms_tillv_i_ar = st.number_input("Omsättningstillväxt i år (%)", step=0.1)
        oms_tillv_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", step=0.1)

        pe_nu = st.number_input("Nuvarande P/E", min_value=0.0, step=0.1)
        pe_1 = st.number_input("P/E 1", min_value=0.0, step=0.1)
        pe_2 = st.number_input("P/E 2", min_value=0.0, step=0.1)
        pe_3 = st.number_input("P/E 3", min_value=0.0, step=0.1)
        pe_4 = st.number_input("P/E 4", min_value=0.0, step=0.1)

        ps_nu = st.number_input("Nuvarande P/S", min_value=0.0, step=0.1)
        ps_1 = st.number_input("P/S 1", min_value=0.0, step=0.1)
        ps_2 = st.number_input("P/S 2", min_value=0.0, step=0.1)
        ps_3 = st.number_input("P/S 3", min_value=0.0, step=0.1)
        ps_4 = st.number_input("P/S 4", min_value=0.0, step=0.1)

        insatt_datum = datetime.today().strftime("%Y-%m-%d")

        if st.form_submit_button("Spara bolag"):
            if not bolagsnamn:
                st.warning("⚠️ Du måste fylla i bolagsnamn för att spara.")
                return

            data[bolagsnamn] = {
                "nuvarande_kurs": nuvarande_kurs,
                "vinst_i_ar": vinst_i_ar,
                "vinst_nasta_ar": vinst_nasta_ar,
                "oms_tillv_i_ar": oms_tillv_i_ar,
                "oms_tillv_nasta_ar": oms_tillv_nasta_ar,
                "pe_nu": pe_nu,
                "pe_1": pe_1,
                "pe_2": pe_2,
                "pe_3": pe_3,
                "pe_4": pe_4,
                "ps_nu": ps_nu,
                "ps_1": ps_1,
                "ps_2": ps_2,
                "ps_3": ps_3,
                "ps_4": ps_4,
                "insatt_datum": insatt_datum,
                "senast_andrad": insatt_datum
            }
            save_data(data)
            st.success(f"{bolagsnamn} har sparats.")
