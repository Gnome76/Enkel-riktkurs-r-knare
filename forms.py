# forms.py
import streamlit as st

def visa_inmatningsform():
    """Visa formulär för att lägga till nytt bolag och returnera bolagsdata eller None."""
    with st.form(key="nytt_bolag_form"):
        namn = st.text_input("Bolagsnamn")
        nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
        nuvarande_pe = st.number_input("Nuvarande P/E", min_value=0.0, format="%.2f")
        pe_1 = st.number_input("P/E 1", min_value=0.0, format="%.2f")
        pe_2 = st.number_input("P/E 2", min_value=0.0, format="%.2f")
        pe_3 = st.number_input("P/E 3", min_value=0.0, format="%.2f")
        pe_4 = st.number_input("P/E 4", min_value=0.0, format="%.2f")
        nuvarande_ps = st.number_input("Nuvarande P/S", min_value=0.0, format="%.2f")
        ps_1 = st.number_input("P/S 1", min_value=0.0, format="%.2f")
        ps_2 = st.number_input("P/S 2", min_value=0.0, format="%.2f")
        ps_3 = st.number_input("P/S 3", min_value=0.0, format="%.2f")
        ps_4 = st.number_input("P/S 4", min_value=0.0, format="%.2f")
        vinst_i_ar = st.number_input("Förväntad vinst i år", format="%.2f")
        vinst_nasta_ar = st.number_input("Förväntad vinst nästa år", format="%.2f")
        oms_tillvaxt_i_ar = st.number_input("Omsättningstillväxt i år (%)", format="%.2f")
        oms_tillvaxt_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", format="%.2f")

        knapp = st.form_submit_button("Lägg till bolag")

    if knapp:
        if namn.strip() == "":
            st.error("Ange ett bolagsnamn.")
            return None
        return {
            "namn": namn.strip(),
            "nuvarande_kurs": nuvarande_kurs,
            "nuvarande_pe": nuvarande_pe,
            "pe_1": pe_1,
            "pe_2": pe_2,
            "pe_3": pe_3,
            "pe_4": pe_4,
            "nuvarande_ps": nuvarande_ps,
            "ps_1": ps_1,
            "ps_2": ps_2,
            "ps_3": ps_3,
            "ps_4": ps_4,
            "vinst_i_ar": vinst_i_ar,
            "vinst_nasta_ar": vinst_nasta_ar,
            "oms_tillvaxt_i_ar": oms_tillvaxt_i_ar,
            "oms_tillvaxt_nasta_ar": oms_tillvaxt_nasta_ar,
        }

    return None
