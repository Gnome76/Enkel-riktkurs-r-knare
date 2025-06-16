import streamlit as st

def nytt_bolag_formular(data):
    st.write("### Lägg till nytt bolag")
    with st.form(key="nytt_bolag_form"):
        namn = st.text_input("Bolagsnamn").strip()
        kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")

        vinst_i_ar = st.number_input("Förväntad vinst i år", format="%.2f")
        vinst_nasta_ar = st.number_input("Förväntad vinst nästa år", format="%.2f")

        oms_tillv_i_ar = st.number_input("Omsättningstillväxt i år (%)", format="%.2f")
        oms_tillv_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", format="%.2f")

        nuvarande_pe = st.number_input("Nuvarande P/E", min_value=0.0, format="%.2f")
        pe1 = st.number_input("P/E 1", min_value=0.0, format="%.2f")
        pe2 = st.number_input("P/E 2", min_value=0.0, format="%.2f")
        pe3 = st.number_input("P/E 3", min_value=0.0, format="%.2f")
        pe4 = st.number_input("P/E 4", min_value=0.0, format="%.2f")

        nuvarande_ps = st.number_input("Nuvarande P/S", min_value=0.0, format="%.2f")
        ps1 = st.number_input("P/S 1", min_value=0.0, format="%.2f")
        ps2 = st.number_input("P/S 2", min_value=0.0, format="%.2f")
        ps3 = st.number_input("P/S 3", min_value=0.0, format="%.2f")
        ps4 = st.number_input("P/S 4", min_value=0.0, format="%.2f")

        submit = st.form_submit_button("Lägg till bolag")

        if submit:
            if not namn:
                st.error("⚠️ Bolagsnamn krävs!")
                return

            data[namn] = {
                "kurs": kurs,
                "vinst_i_ar": vinst_i_ar,
                "vinst_nasta_ar": vinst_nasta_ar,
                "oms_tillv_i_ar": oms_tillv_i_ar,
                "oms_tillv_nasta_ar": oms_tillv_nasta_ar,
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
            }
            st.success(f"✅ Bolaget '{namn}' har lagts till.")
