import streamlit as st

def nytt_bolag_formular(data):
    st.subheader("Lägg till nytt bolag")

    with st.form(key="nytt_bolag_form"):
        namn = st.text_input("Bolagsnamn")
        kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")

        # Nuvarande P/E och P/S
        pe_nuvarande = st.number_input("Nuvarande P/E", min_value=0.0, format="%.2f")
        ps_nuvarande = st.number_input("Nuvarande P/S", min_value=0.0, format="%.2f")

        # P/E 1–4
        pe1 = st.number_input("P/E år 1", min_value=0.0, format="%.2f")
        pe2 = st.number_input("P/E år 2", min_value=0.0, format="%.2f")
        pe3 = st.number_input("P/E år 3", min_value=0.0, format="%.2f")
        pe4 = st.number_input("P/E år 4", min_value=0.0, format="%.2f")

        # P/S 1–4
        ps1 = st.number_input("P/S år 1", min_value=0.0, format="%.2f")
        ps2 = st.number_input("P/S år 2", min_value=0.0, format="%.2f")
        ps3 = st.number_input("P/S år 3", min_value=0.0, format="%.2f")
        ps4 = st.number_input("P/S år 4", min_value=0.0, format="%.2f")

        submit = st.form_submit_button("Lägg till")

        if submit:
            if namn.strip() == "":
                st.error("Bolagsnamn får inte vara tomt.")
                return

            data[namn] = {
                "namn": namn,
                "nuvarande_kurs": kurs,
                "pe_nuvarande": pe_nuvarande,
                "ps_nuvarande": ps_nuvarande,
                "pe1": pe1,
                "pe2": pe2,
                "pe3": pe3,
                "pe4": pe4,
                "ps1": ps1,
                "ps2": ps2,
                "ps3": ps3,
                "ps4": ps4,
            }

            st.success(f"Bolag {namn} tillagt!")

def redigeringsformular(data):
    st.write("Här kommer redigeringsformuläret snart.")
