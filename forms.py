import streamlit as st
from datetime import datetime
from utils import berakna_targetkurser
from data_handler import save_data, load_data

def visa_inmatningsform():
    st.header("Lägg till eller uppdatera bolag")

    data = load_data()
    bolagsnamn = st.selectbox("Välj bolag att uppdatera eller skriv nytt", options=[""] + sorted([b["namn"] for b in data]))
    nytt_bolag = bolagsnamn == ""

    with st.form(key="inmatningsform"):
        namn = st.text_input("Bolagsnamn", value=bolagsnamn if bolagsnamn else "")
        nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, value=0.0)
        nuvarande_pe = st.number_input("Nuvarande P/E", min_value=0.0, value=0.0)
        pe_1 = st.number_input("P/E 1", min_value=0.0, value=0.0)
        pe_2 = st.number_input("P/E 2", min_value=0.0, value=0.0)
        pe_3 = st.number_input("P/E 3", min_value=0.0, value=0.0)
        pe_4 = st.number_input("P/E 4", min_value=0.0, value=0.0)

        nuvarande_ps = st.number_input("Nuvarande P/S", min_value=0.0, value=0.0)
        ps_1 = st.number_input("P/S 1", min_value=0.0, value=0.0)
        ps_2 = st.number_input("P/S 2", min_value=0.0, value=0.0)
        ps_3 = st.number_input("P/S 3", min_value=0.0, value=0.0)
        ps_4 = st.number_input("P/S 4", min_value=0.0, value=0.0)

        vinst_år = st.number_input("Förväntad vinst i år", value=0.0)
        vinst_nästa_år = st.number_input("Förväntad vinst nästa år", value=0.0)
        tillväxt_iår = st.number_input("Omsättningstillväxt i år (%)", value=0.0)
        tillväxt_nästa_år = st.number_input("Omsättningstillväxt nästa år (%)", value=0.0)

        submitted = st.form_submit_button("Spara bolag")

    if submitted and namn:
        nytt_bolag_data = {
            "namn": namn,
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
            "vinst_år": vinst_år,
            "vinst_nästa_år": vinst_nästa_år,
            "tillväxt_iår": tillväxt_iår,
            "tillväxt_nästa_år": tillväxt_nästa_år,
            "senast_andrad": datetime.now().isoformat()
        }

        # Beräkna targetkurser och undervärdering
        nytt_bolag_data.update(berakna_targetkurser(nytt_bolag_data))

        # Uppdatera eller lägg till bolaget i datan
        data = [b for b in data if b["namn"] != namn]
        data.append(nytt_bolag_data)
        save_data(data)

        st.success(f"{namn} har sparats.")
