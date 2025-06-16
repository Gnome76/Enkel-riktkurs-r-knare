import streamlit as st

def nytt_bolag_form():
    with st.form(key="nytt_bolag_form", clear_on_submit=True):
        st.subheader("Lägg till nytt bolag")

        bolagsnamn = st.text_input("Bolagsnamn", max_chars=50)

        nuvarande_kurs = st.number_input("Nuvarande kurs (kr)", min_value=0.0, format="%.2f")
        
        # Vinst
        vinst_forra_aret = st.number_input("Vinst förra året (kr)", format="%.2f")
        vinst_i_ar = st.number_input("Förväntad vinst i år (kr)", format="%.2f")
        vinst_nasta_ar = st.number_input("Förväntad vinst nästa år (kr)", format="%.2f")

        # Omsättningstillväxt i procent (decimaltal, t.ex. 0.1 = 10%)
        omsattningstillvaxt_i_ar = st.number_input("Omsättningstillväxt i år (%)", format="%.2f") / 100
        omsattningstillvaxt_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", format="%.2f") / 100

        # P/E-tal (nuvarande och prognoser)
        pe_nuvarande = st.number_input("Nuvarande P/E", min_value=0.0, format="%.2f")
        pe_1 = st.number_input("P/E prognos år 1", min_value=0.0, format="%.2f")
        pe_2 = st.number_input("P/E prognos år 2", min_value=0.0, format="%.2f")
        pe_3 = st.number_input("P/E prognos år 3", min_value=0.0, format="%.2f")
        pe_4 = st.number_input("P/E prognos år 4", min_value=0.0, format="%.2f")

        # P/S-tal (nuvarande och prognoser)
        ps_nuvarande = st.number_input("Nuvarande P/S", min_value=0.0, format="%.2f")
        ps_1 = st.number_input("P/S prognos år 1", min_value=0.0, format="%.2f")
        ps_2 = st.number_input("P/S prognos år 2", min_value=0.0, format="%.2f")
        ps_3 = st.number_input("P/S prognos år 3", min_value=0.0, format="%.2f")
        ps_4 = st.number_input("P/S prognos år 4", min_value=0.0, format="%.2f")

        skickaknapp = st.form_submit_button("Spara bolag")

        if skickaknapp:
            if not bolagsnamn.strip():
                st.error("Bolagsnamn kan inte vara tomt.")
                return None
            data = {
                "nuvarande_kurs": nuvarande_kurs,
                "vinst_forra_aret": vinst_forra_aret,
                "vinst_i_ar": vinst_i_ar,
                "vinst_nasta_ar": vinst_nasta_ar,
                "omsattningstillvaxt_i_ar": omsattningstillvaxt_i_ar,
                "omsattningstillvaxt_nasta_ar": omsattningstillvaxt_nasta_ar,
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
            }
            return bolagsnamn.strip(), data
        return None
