import streamlit as st
from data_handler import load_data, save_data

def nytt_bolag_formular(data):
    st.header("Lägg till nytt bolag")

    with st.form(key="nytt_bolag_form"):
        bolagsnamn = st.text_input("Bolagsnamn").strip()
        kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")

        # Nuvarande P/E och P/E 1-4
        pe_nuvarande = st.number_input("Nuvarande P/E", min_value=0.0, format="%.2f")
        pe_1 = st.number_input("P/E 1", min_value=0.0, format="%.2f")
        pe_2 = st.number_input("P/E 2", min_value=0.0, format="%.2f")
        pe_3 = st.number_input("P/E 3", min_value=0.0, format="%.2f")
        pe_4 = st.number_input("P/E 4", min_value=0.0, format="%.2f")

        # Nuvarande P/S och P/S 1-4
        ps_nuvarande = st.number_input("Nuvarande P/S", min_value=0.0, format="%.2f")
        ps_1 = st.number_input("P/S 1", min_value=0.0, format="%.2f")
        ps_2 = st.number_input("P/S 2", min_value=0.0, format="%.2f")
        ps_3 = st.number_input("P/S 3", min_value=0.0, format="%.2f")
        ps_4 = st.number_input("P/S 4", min_value=0.0, format="%.2f")

        # Vinst i år och nästa år
        vinst_i_ar = st.number_input("Vinst i år", min_value=0.0, format="%.2f")
        vinst_nasta_ar = st.number_input("Vinst nästa år", min_value=0.0, format="%.2f")

        # Omsättningstillväxt i år och nästa år (i procent)
        oms_tillv_i_ar = st.number_input("Omsättningstillväxt i år (%)", min_value=0.0, format="%.2f")
        oms_tillv_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", min_value=0.0, format="%.2f")

        skickaknapp = st.form_submit_button("Lägg till bolag")

        if skickaknapp:
            if bolagsnamn == "":
                st.error("Ange ett bolagsnamn.")
                return

            if bolagsnamn in data:
                st.error("Bolaget finns redan. Använd redigera istället.")
                return

            data[bolagsnamn] = {
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
                "oms_tillv_nasta_ar": oms_tillv_nasta_ar,
            }

            save_data(data)
            st.success(f"Bolaget '{bolagsnamn}' har lagts till.")

def redigeringsformular(data):
    st.header("Redigera bolag")

    if not data:
        st.info("Inga bolag finns att redigera.")
        return

    bolagsnamn = st.selectbox("Välj bolag att redigera", list(data.keys()))

    if bolagsnamn:
        bolag = data[bolagsnamn]

        with st.form(key="redigera_bolag_form"):
            kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f", value=bolag.get("kurs", 0.0))
            pe_nuvarande = st.number_input("Nuvarande P/E", min_value=0.0, format="%.2f", value=bolag.get("pe_nuvarande", 0.0))
            pe_1 = st.number_input("P/E 1", min_value=0.0, format="%.2f", value=bolag.get("pe_1", 0.0))
            pe_2 = st.number_input("P/E 2", min_value=0.0, format="%.2f", value=bolag.get("pe_2", 0.0))
            pe_3 = st.number_input("P/E 3", min_value=0.0, format="%.2f", value=bolag.get("pe_3", 0.0))
            pe_4 = st.number_input("P/E 4", min_value=0.0, format="%.2f", value=bolag.get("pe_4", 0.0))

            ps_nuvarande = st.number_input("Nuvarande P/S", min_value=0.0, format="%.2f", value=bolag.get("ps_nuvarande", 0.0))
            ps_1 = st.number_input("P/S 1", min_value=0.0, format="%.2f", value=bolag.get("ps_1", 0.0))
            ps_2 = st.number_input("P/S 2", min_value=0.0, format="%.2f", value=bolag.get("ps_2", 0.0))
            ps_3 = st.number_input("P/S 3", min_value=0.0, format="%.2f", value=bolag.get("ps_3", 0.0))
            ps_4 = st.number_input("P/S 4", min_value=0.0, format="%.2f", value=bolag.get("ps_4", 0.0))

            vinst_i_ar = st.number_input("Vinst i år", min_value=0.0, format="%.2f", value=bolag.get("vinst_i_ar", 0.0))
            vinst_nasta_ar = st.number_input("Vinst nästa år", min_value=0.0, format="%.2f", value=bolag.get("vinst_nasta_ar", 0.0))

            oms_tillv_i_ar = st.number_input("Omsättningstillväxt i år (%)", min_value=0.0, format="%.2f", value=bolag.get("oms_tillv_i_ar", 0.0))
            oms_tillv_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", min_value=0.0, format="%.2f", value=bolag.get("oms_tillv_nasta_ar", 0.0))

            skickaknapp = st.form_submit_button("Uppdatera bolag")

            if skickaknapp:
                data[bolagsnamn] = {
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
                    "oms_tillv_nasta_ar": oms_tillv_nasta_ar,
                }
                save_data(data)
                st.success(f"Bolaget '{bolagsnamn}' har uppdaterats.")
