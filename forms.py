import streamlit as st
from datetime import datetime

def nytt_bolag_formular(data):
    """
    Formulär för att lägga till ett nytt bolag.
    Tar emot den befintliga data-ordboken och uppdaterar den vid submit.
    Returnerar True om data ändrats och sparas, annars False.
    """
    with st.form(key="nytt_bolag_form"):
        bolagsnamn = st.text_input("Bolagsnamn").strip()

        nuvarande_kurs = st.number_input("Nuvarande kurs (kr)", min_value=0.0, format="%.2f")
        vinst_i_ar = st.number_input("Förväntad vinst i år", format="%.2f")
        vinst_nasta_ar = st.number_input("Förväntad vinst nästa år", format="%.2f")

        omsättningstillväxt_i_ar = st.number_input("Omsättningstillväxt i år (%)", format="%.2f")
        omsättningstillväxt_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", format="%.2f")

        pe_1 = st.number_input("P/E 1", min_value=0.0, format="%.2f")
        pe_2 = st.number_input("P/E 2", min_value=0.0, format="%.2f")
        pe_3 = st.number_input("P/E 3", min_value=0.0, format="%.2f")
        pe_4 = st.number_input("P/E 4", min_value=0.0, format="%.2f")

        ps_1 = st.number_input("P/S 1", min_value=0.0, format="%.2f")
        ps_2 = st.number_input("P/S 2", min_value=0.0, format="%.2f")
        ps_3 = st.number_input("P/S 3", min_value=0.0, format="%.2f")
        ps_4 = st.number_input("P/S 4", min_value=0.0, format="%.2f")

        submit = st.form_submit_button("Lägg till bolag")

    if submit:
        if not bolagsnamn:
            st.error("Ange ett bolagsnamn.")
            return False

        if bolagsnamn in data:
            st.error("Detta bolag finns redan. Välj 'Redigera befintligt bolag' för att ändra data.")
            return False

        data[bolagsnamn] = {
            "nuvarande_kurs": nuvarande_kurs,
            "vinst_i_ar": vinst_i_ar,
            "vinst_nasta_ar": vinst_nasta_ar,
            "omsättningstillväxt_i_ar": omsättningstillväxt_i_ar,
            "omsättningstillväxt_nasta_ar": omsättningstillväxt_nasta_ar,
            "pe_1": pe_1,
            "pe_2": pe_2,
            "pe_3": pe_3,
            "pe_4": pe_4,
            "ps_1": ps_1,
            "ps_2": ps_2,
            "ps_3": ps_3,
            "ps_4": ps_4,
            "insatt_datum": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "senast_andrad": None
        }
        return True

    return False


def redigeringsformular(data):
    """
    Formulär för att redigera befintligt bolag.
    Returnerar True om data ändrats och sparas, annars False.
    """
    if not data:
        st.info("Inga bolag att redigera.")
        return False

    valt_bolag = st.selectbox("Välj bolag att redigera", options=list(data.keys()))

    bolag = data[valt_bolag]

    with st.form(key="redigera_bolag_form"):
        nuvarande_kurs = st.number_input("Nuvarande kurs (kr)", value=bolag.get("nuvarande_kurs", 0.0), format="%.2f")
        vinst_i_ar = st.number_input("Förväntad vinst i år", value=bolag.get("vinst_i_ar", 0.0), format="%.2f")
        vinst_nasta_ar = st.number_input("Förväntad vinst nästa år", value=bolag.get("vinst_nasta_ar", 0.0), format="%.2f")

        omsättningstillväxt_i_ar = st.number_input("Omsättningstillväxt i år (%)", value=bolag.get("omsättningstillväxt_i_ar", 0.0), format="%.2f")
        omsättningstillväxt_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", value=bolag.get("omsättningstillväxt_nasta_ar", 0.0), format="%.2f")

        pe_1 = st.number_input("P/E 1", value=bolag.get("pe_1", 0.0), format="%.2f")
        pe_2 = st.number_input("P/E 2", value=bolag.get("pe_2", 0.0), format="%.2f")
        pe_3 = st.number_input("P/E 3", value=bolag.get("pe_3", 0.0), format="%.2f")
        pe_4 = st.number_input("P/E 4", value=bolag.get("pe_4", 0.0), format="%.2f")

        ps_1 = st.number_input("P/S 1", value=bolag.get("ps_1", 0.0), format="%.2f")
        ps_2 = st.number_input("P/S 2", value=bolag.get("ps_2", 0.0), format="%.2f")
        ps_3 = st.number_input("P/S 3", value=bolag.get("ps_3", 0.0), format="%.2f")
        ps_4 = st.number_input("P/S 4", value=bolag.get("ps_4", 0.0), format="%.2f")

        submit = st.form_submit_button("Uppdatera bolag")

    if submit:
        bolag.update({
            "nuvarande_kurs": nuvarande_kurs,
            "vinst_i_ar": vinst_i_ar,
            "vinst_nasta_ar": vinst_nasta_ar,
            "omsättningstillväxt_i_ar": omsättningstillväxt_i_ar,
            "omsättningstillväxt_nasta_ar": omsättningstillväxt_nasta_ar,
            "pe_1": pe_1,
            "pe_2": pe_2,
            "pe_3": pe_3,
            "pe_4": pe_4,
            "ps_1": ps_1,
            "ps_2": ps_2,
            "ps_3": ps_3,
            "ps_4": ps_4,
            "senast_andrad": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return True

    return False
