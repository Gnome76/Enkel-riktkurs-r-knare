import streamlit as st
from data_handler import load_data, save_data

def nytt_bolag_formular():
    st.header("Lägg till nytt bolag")

    with st.form(key="nytt_bolag_form"):
        namn = st.text_input("Bolagsnamn", max_chars=50)
        nuvarande_kurs = st.number_input("Nuvarande kurs (kr)", min_value=0.0, format="%.2f")
        vinst_fjol = st.number_input("Vinst förra året (kr)", format="%.2f")
        vinst_i_ar = st.number_input("Förväntad vinst i år (kr)", format="%.2f")
        vinst_nasta_ar = st.number_input("Förväntad vinst nästa år (kr)", format="%.2f")
        omsattning_fjol = st.number_input("Omsättning förra året (kr)", format="%.2f")
        omsattningstillvxt_i_ar = st.number_input("Omsättningstillväxt i år (%)", format="%.2f")
        omsattningstillvxt_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", format="%.2f")

        pe_aktuell = st.number_input("Nuvarande P/E", min_value=0.0, format="%.2f")
        pe1 = st.number_input("P/E år 1", min_value=0.0, format="%.2f")
        pe2 = st.number_input("P/E år 2", min_value=0.0, format="%.2f")
        pe3 = st.number_input("P/E år 3", min_value=0.0, format="%.2f")
        pe4 = st.number_input("P/E år 4", min_value=0.0, format="%.2f")

        ps_aktuell = st.number_input("Nuvarande P/S", min_value=0.0, format="%.2f")
        ps1 = st.number_input("P/S år 1", min_value=0.0, format="%.2f")
        ps2 = st.number_input("P/S år 2", min_value=0.0, format="%.2f")
        ps3 = st.number_input("P/S år 3", min_value=0.0, format="%.2f")
        ps4 = st.number_input("P/S år 4", min_value=0.0, format="%.2f")

        skickaknapp = st.form_submit_button("Lägg till bolag")

    if skickaknapp:
        if namn.strip() == "":
            st.warning("Bolagsnamn kan inte vara tomt.")
            return

        data = load_data()
        if namn in data:
            st.warning(f"Bolaget '{namn}' finns redan.")
            return

        data[namn] = {
            "nuvarande_kurs": nuvarande_kurs,
            "vinst_fjol": vinst_fjol,
            "vinst_i_ar": vinst_i_ar,
            "vinst_nasta_ar": vinst_nasta_ar,
            "omsattning_fjol": omsattning_fjol,
            "omsattningstillvxt_i_ar": omsattningstillvxt_i_ar,
            "omsattningstillvxt_nasta_ar": omsattningstillvxt_nasta_ar,
            "pe_aktuell": pe_aktuell,
            "pe1": pe1,
            "pe2": pe2,
            "pe3": pe3,
            "pe4": pe4,
            "ps_aktuell": ps_aktuell,
            "ps1": ps1,
            "ps2": ps2,
            "ps3": ps3,
            "ps4": ps4
        }
        save_data(data)
        st.success(f"Bolaget '{namn}' har lagts till.")

def redigeringsformular():
    st.header("Redigera bolag")

    data = load_data()
    if not data:
        st.info("Inga bolag att redigera.")
        return

    bolagslista = list(data.keys())
    valt_bolag = st.selectbox("Välj bolag att redigera", bolagslista)

    if valt_bolag:
        info = data[valt_bolag]

        with st.form(key="redigera_bolag_form"):
            nuvarande_kurs = st.number_input("Nuvarande kurs (kr)", min_value=0.0, format="%.2f", value=info.get("nuvarande_kurs", 0.0))
            vinst_fjol = st.number_input("Vinst förra året (kr)", format="%.2f", value=info.get("vinst_fjol", 0.0))
            vinst_i_ar = st.number_input("Förväntad vinst i år (kr)", format="%.2f", value=info.get("vinst_i_ar", 0.0))
            vinst_nasta_ar = st.number_input("Förväntad vinst nästa år (kr)", format="%.2f", value=info.get("vinst_nasta_ar", 0.0))
            omsattning_fjol = st.number_input("Omsättning förra året (kr)", format="%.2f", value=info.get("omsattning_fjol", 0.0))
            omsattningstillvxt_i_ar = st.number_input("Omsättningstillväxt i år (%)", format="%.2f", value=info.get("omsattningstillvxt_i_ar", 0.0))
            omsattningstillvxt_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", format="%.2f", value=info.get("omsattningstillvxt_nasta_ar", 0.0))

            pe_aktuell = st.number_input("Nuvarande P/E", min_value=0.0, format="%.2f", value=info.get("pe_aktuell", 0.0))
            pe1 = st.number_input("P/E år 1", min_value=0.0, format="%.2f", value=info.get("pe1", 0.0))
            pe2 = st.number_input("P/E år 2", min_value=0.0, format="%.2f", value=info.get("pe2", 0.0))
            pe3 = st.number_input("P/E år 3", min_value=0.0, format="%.2f", value=info.get("pe3", 0.0))
            pe4 = st.number_input("P/E år 4", min_value=0.0, format="%.2f", value=info.get("pe4", 0.0))

            ps_aktuell = st.number_input("Nuvarande P/S", min_value=0.0, format="%.2f", value=info.get("ps_aktuell", 0.0))
            ps1 = st.number_input("P/S år 1", min_value=0.0, format="%.2f", value=info.get("ps1", 0.0))
            ps2 = st.number_input("P/S år 2", min_value=0.0, format="%.2f", value=info.get("ps2", 0.0))
            ps3 = st.number_input("P/S år 3", min_value=0.0, format="%.2f", value=info.get("ps3", 0.0))
            ps4 = st.number_input("P/S år 4", min_value=0.0, format="%.2f", value=info.get("ps4", 0.0))

            knapp = st.form_submit_button("Uppdatera bolag")

        if knapp:
            data[valt_bolag] = {
                "nuvarande_kurs": nuvarande_kurs,
                "vinst_fjol": vinst_fjol,
                "vinst_i_ar": vinst_i_ar,
                "vinst_nasta_ar": vinst_nasta_ar,
                "omsattning_fjol": omsattning_fjol,
                "omsattningstillvxt_i_ar": omsattningstillvxt_i_ar,
                "omsattningstillvxt_nasta_ar": omsattningstillvxt_nasta_ar,
                "pe_aktuell": pe_aktuell,
                "pe1": pe1,
                "pe2": pe2,
                "pe3": pe3,
                "pe4": pe4,
                "ps_aktuell": ps_aktuell,
                "ps1": ps1,
                "ps2": ps2,
                "ps3": ps3,
                "ps4": ps4
            }
            save_data(data)
            st.success(f"Bolaget '{valt_bolag}' har uppdaterats.")
