import streamlit as st
from data_handler import save_data

def nytt_bolag_formular(data):
    st.header("Lägg till nytt bolag")
    with st.form(key="nytt_bolag_form"):
        bolagsnamn = st.text_input("Bolagsnamn").strip()
        nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
        vinst_foregaende_ar = st.number_input("Vinst förra året", format="%.2f")
        vinst_i_ar = st.number_input("Vinst i år (förväntad)", format="%.2f")
        vinst_nasta_ar = st.number_input("Vinst nästa år (förväntad)", format="%.2f")
        omsattning_foregaende_ar = st.number_input("Omsättning förra året", format="%.2f")
        omsattningstillvaxt_i_ar = st.number_input("Omsättningstillväxt i år (%)", format="%.2f")
        omsattningstillvaxt_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", format="%.2f")

        # Nuvarande och P/E 1-4
        pe_nuvarande = st.number_input("Nuvarande P/E", format="%.2f")
        pe_1 = st.number_input("P/E 1", format="%.2f")
        pe_2 = st.number_input("P/E 2", format="%.2f")
        pe_3 = st.number_input("P/E 3", format="%.2f")
        pe_4 = st.number_input("P/E 4", format="%.2f")

        # Nuvarande och P/S 1-4
        ps_nuvarande = st.number_input("Nuvarande P/S", format="%.2f")
        ps_1 = st.number_input("P/S 1", format="%.2f")
        ps_2 = st.number_input("P/S 2", format="%.2f")
        ps_3 = st.number_input("P/S 3", format="%.2f")
        ps_4 = st.number_input("P/S 4", format="%.2f")

        knapp = st.form_submit_button("Spara nytt bolag")

    if knapp:
        if bolagsnamn == "":
            st.error("Ange bolagsnamn")
            return
        if bolagsnamn in data:
            st.error("Bolaget finns redan")
            return

        data[bolagsnamn] = {
            "nuvarande_kurs": nuvarande_kurs,
            "vinst_foregaende_ar": vinst_foregaende_ar,
            "vinst_i_ar": vinst_i_ar,
            "vinst_nasta_ar": vinst_nasta_ar,
            "omsattning_foregaende_ar": omsattning_foregaende_ar,
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
        save_data(data)
        st.success(f"Bolag '{bolagsnamn}' sparat.")

def redigeringsformular(data):
    st.header("Redigera bolag")
    bolagslista = list(data.keys())
    valt_bolag = st.selectbox("Välj bolag att redigera", bolagslista)

    if valt_bolag:
        info = data[valt_bolag]

        with st.form(key="redigerings_form"):
            nuvarande_kurs = st.number_input("Nuvarande kurs", value=info.get("nuvarande_kurs", 0.0), format="%.2f")
            vinst_foregaende_ar = st.number_input("Vinst förra året", value=info.get("vinst_foregaende_ar", 0.0), format="%.2f")
            vinst_i_ar = st.number_input("Vinst i år (förväntad)", value=info.get("vinst_i_ar", 0.0), format="%.2f")
            vinst_nasta_ar = st.number_input("Vinst nästa år (förväntad)", value=info.get("vinst_nasta_ar", 0.0), format="%.2f")
            omsattning_foregaende_ar = st.number_input("Omsättning förra året", value=info.get("omsattning_foregaende_ar", 0.0), format="%.2f")
            omsattningstillvaxt_i_ar = st.number_input("Omsättningstillväxt i år (%)", value=info.get("omsattningstillvaxt_i_ar", 0.0), format="%.2f")
            omsattningstillvaxt_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", value=info.get("omsattningstillvaxt_nasta_ar", 0.0), format="%.2f")

            pe_nuvarande = st.number_input("Nuvarande P/E", value=info.get("pe_nuvarande", 0.0), format="%.2f")
            pe_1 = st.number_input("P/E 1", value=info.get("pe_1", 0.0), format="%.2f")
            pe_2 = st.number_input("P/E 2", value=info.get("pe_2", 0.0), format="%.2f")
            pe_3 = st.number_input("P/E 3", value=info.get("pe_3", 0.0), format="%.2f")
            pe_4 = st.number_input("P/E 4", value=info.get("pe_4", 0.0), format="%.2f")

            ps_nuvarande = st.number_input("Nuvarande P/S", value=info.get("ps_nuvarande", 0.0), format="%.2f")
            ps_1 = st.number_input("P/S 1", value=info.get("ps_1", 0.0), format="%.2f")
            ps_2 = st.number_input("P/S 2", value=info.get("ps_2", 0.0), format="%.2f")
            ps_3 = st.number_input("P/S 3", value=info.get("ps_3", 0.0), format="%.2f")
            ps_4 = st.number_input("P/S 4", value=info.get("ps_4", 0.0), format="%.2f")

            knapp = st.form_submit_button("Uppdatera bolag")

        if knapp:
            data[valt_bolag] = {
                "nuvarande_kurs": nuvarande_kurs,
                "vinst_foregaende_ar": vinst_foregaende_ar,
                "vinst_i_ar": vinst_i_ar,
                "vinst_nasta_ar": vinst_nasta_ar,
                "omsattning_foregaende_ar": omsattning_foregaende_ar,
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
            save_data(data)
            st.success(f"Bolag '{valt_bolag}' uppdaterat.")
