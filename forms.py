import streamlit as st

def form_lagg_till_bolag():
    with st.form(key="form_lagg_till_bolag"):
        st.header("Lägg till nytt bolag")

        namn = st.text_input("Bolagsnamn")
        kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f", step=0.01)

        pe_nuvarande = st.number_input("P/E nuvarande", min_value=0.0, format="%.2f", step=0.01)
        pe_1 = st.number_input("P/E år 1", min_value=0.0, format="%.2f", step=0.01)
        pe_2 = st.number_input("P/E år 2", min_value=0.0, format="%.2f", step=0.01)
        pe_3 = st.number_input("P/E år 3", min_value=0.0, format="%.2f", step=0.01)
        pe_4 = st.number_input("P/E år 4", min_value=0.0, format="%.2f", step=0.01)

        ps_nuvarande = st.number_input("P/S nuvarande", min_value=0.0, format="%.2f", step=0.01)
        ps_1 = st.number_input("P/S år 1", min_value=0.0, format="%.2f", step=0.01)
        ps_2 = st.number_input("P/S år 2", min_value=0.0, format="%.2f", step=0.01)
        ps_3 = st.number_input("P/S år 3", min_value=0.0, format="%.2f", step=0.01)
        ps_4 = st.number_input("P/S år 4", min_value=0.0, format="%.2f", step=0.01)

        vinst_i_ar = st.number_input("Vinst i år", min_value=0.0, format="%.2f", step=0.01)
        vinst_nasta_ar = st.number_input("Vinst nästa år", min_value=0.0, format="%.2f", step=0.01)

        oms_tillv_i_ar = st.number_input("Omsättningstillväxt i år (decimaltal, t.ex. 1.05 för 5%)", min_value=0.0, format="%.4f", step=0.001)
        oms_tillv_nasta_ar = st.number_input("Omsättningstillväxt nästa år (decimaltal)", min_value=0.0, format="%.4f", step=0.001)

        submit = st.form_submit_button("Lägg till bolag")

        if submit:
            if namn.strip() == "":
                st.error("Bolagsnamn måste anges.")
                return None
            data = {
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
            return namn, data
    return None
