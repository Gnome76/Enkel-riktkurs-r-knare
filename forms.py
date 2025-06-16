import streamlit as st
from data_handler import load_data, save_data

def nytt_bolag_formular(data):
    st.header("Lägg till nytt bolag")

    with st.form(key="nytt_bolag_form"):
        bolagsnamn = st.text_input("Bolagsnamn").strip()
        kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")

        # Exempel på fler fält, lägg till alla du behöver enligt din specifikation
        pe_1 = st.number_input("P/E 1", min_value=0.0, format="%.2f")
        pe_2 = st.number_input("P/E 2", min_value=0.0, format="%.2f")
        ps_1 = st.number_input("P/S 1", min_value=0.0, format="%.2f")
        ps_2 = st.number_input("P/S 2", min_value=0.0, format="%.2f")

        skickaknapp = st.form_submit_button("Lägg till bolag")

        if skickaknapp:
            if bolagsnamn == "":
                st.error("Ange ett bolagsnamn.")
                return

            if bolagsnamn in data:
                st.error("Bolaget finns redan. Använd redigera istället.")
                return

            # Lägg till i data dict
            data[bolagsnamn] = {
                "kurs": kurs,
                "pe_1": pe_1,
                "pe_2": pe_2,
                "ps_1": ps_1,
                "ps_2": ps_2,
                # Lägg till fler fält här...
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
            pe_1 = st.number_input("P/E 1", min_value=0.0, format="%.2f", value=bolag.get("pe_1", 0.0))
            pe_2 = st.number_input("P/E 2", min_value=0.0, format="%.2f", value=bolag.get("pe_2", 0.0))
            ps_1 = st.number_input("P/S 1", min_value=0.0, format="%.2f", value=bolag.get("ps_1", 0.0))
            ps_2 = st.number_input("P/S 2", min_value=0.0, format="%.2f", value=bolag.get("ps_2", 0.0))

            skickaknapp = st.form_submit_button("Uppdatera bolag")

            if skickaknapp:
                data[bolagsnamn] = {
                    "kurs": kurs,
                    "pe_1": pe_1,
                    "pe_2": pe_2,
                    "ps_1": ps_1,
                    "ps_2": ps_2,
                    # Lägg till fler fält här...
                }
                save_data(data)
                st.success(f"Bolaget '{bolagsnamn}' har uppdaterats.")
