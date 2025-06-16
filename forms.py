import streamlit as st
from data_handler import save_data

def lagg_till_bolag_form():
    with st.form(key="lagg_till_form"):
        namn = st.text_input("Bolagsnamn").strip()
        kurs = st.number_input("Nuvarande kurs (SEK)", min_value=0.0, format="%.2f")
        vinst_1 = st.number_input("Förväntad vinst i år", min_value=0.0, format="%.2f")
        vinst_2 = st.number_input("Förväntad vinst nästa år", min_value=0.0, format="%.2f")
        oms_tillv_1 = st.number_input("Omsättningstillväxt i år (%)", format="%.2f")
        oms_tillv_2 = st.number_input("Omsättningstillväxt nästa år (%)", format="%.2f")
        pe1 = st.number_input("P/E år 1", min_value=0.0, format="%.2f")
        pe2 = st.number_input("P/E år 2", min_value=0.0, format="%.2f")
        pe3 = st.number_input("P/E år 3", min_value=0.0, format="%.2f")
        pe4 = st.number_input("P/E år 4", min_value=0.0, format="%.2f")
        ps1 = st.number_input("P/S år 1", min_value=0.0, format="%.2f")
        ps2 = st.number_input("P/S år 2", min_value=0.0, format="%.2f")
        ps3 = st.number_input("P/S år 3", min_value=0.0, format="%.2f")
        ps4 = st.number_input("P/S år 4", min_value=0.0, format="%.2f")

        submit = st.form_submit_button("Lägg till bolag")

    if submit:
        if not namn:
            st.error("Ange bolagsnamn.")
            return
        if namn in st.session_state.data:
            st.error("Bolaget finns redan.")
            return
        st.session_state.data[namn] = {
            "kurs": kurs,
            "vinst_1": vinst_1,
            "vinst_2": vinst_2,
            "oms_tillv_1": oms_tillv_1,
            "oms_tillv_2": oms_tillv_2,
            "pe1": pe1,
            "pe2": pe2,
            "pe3": pe3,
            "pe4": pe4,
            "ps1": ps1,
            "ps2": ps2,
            "ps3": ps3,
            "ps4": ps4,
        }
        save_data(st.session_state.data)
        st.success(f"Bolag '{namn}' tillagt.")
        st.experimental_rerun()


def redigera_bolag_form():
    data = st.session_state.data
    namn_lista = list(data.keys())
    if not namn_lista:
        st.info("Inga bolag att redigera.")
        return

    valt_namn = st.selectbox("Välj bolag att redigera", namn_lista)
    bolag = data.get(valt_namn, {})

    with st.form(key="redigera_form"):
        kurs = st.number_input("Nuvarande kurs (SEK)", value=bolag.get("kurs", 0.0), format="%.2f")
        vinst_1 = st.number_input("Förväntad vinst i år", value=bolag.get("vinst_1", 0.0), format="%.2f")
        vinst_2 = st.number_input("Förväntad vinst nästa år", value=bolag.get("vinst_2", 0.0), format="%.2f")
        oms_tillv_1 = st.number_input("Omsättningstillväxt i år (%)", value=bolag.get("oms_tillv_1", 0.0), format="%.2f")
        oms_tillv_2 = st.number_input("Omsättningstillväxt nästa år (%)", value=bolag.get("oms_tillv_2", 0.0), format="%.2f")
        pe1 = st.number_input("P/E år 1", value=bolag.get("pe1", 0.0), format="%.2f")
        pe2 = st.number_input("P/E år 2", value=bolag.get("pe2", 0.0), format="%.2f")
        pe3 = st.number_input("P/E år 3", value=bolag.get("pe3", 0.0), format="%.2f")
        pe4 = st.number_input("P/E år 4", value=bolag.get("pe4", 0.0), format="%.2f")
        ps1 = st.number_input("P/S år 1", value=bolag.get("ps1", 0.0), format="%.2f")
        ps2 = st.number_input("P/S år 2", value=bolag.get("ps2", 0.0), format="%.2f")
        ps3 = st.number_input("P/S år 3", value=bolag.get("ps3", 0.0), format="%.2f")
        ps4 = st.number_input("P/S år 4", value=bolag.get("ps4", 0.0), format="%.2f")

        submit = st.form_submit_button("Uppdatera bolag")

    if submit:
        st.session_state.data[valt_namn] = {
            "kurs": kurs,
            "vinst_1": vinst_1,
            "vinst_2": vinst_2,
            "oms_tillv_1": oms_tillv_1,
            "oms_tillv_2": oms_tillv_2,
            "pe1": pe1,
            "pe2": pe2,
            "pe3": pe3,
            "pe4": pe4,
            "ps1": ps1,
            "ps2": ps2,
            "ps3": ps3,
            "ps4": ps4,
        }
        save_data(st.session_state.data)
        st.success(f"Bolag '{valt_namn}' uppdaterat.")
        st.experimental_rerun()


def tabort_bolag_form():
    data = st.session_state.data
    namn_lista = list(data.keys())
    if not namn_lista:
        st.info("Inga bolag att ta bort.")
        return

    valt_namn = st.selectbox("Välj bolag att ta bort", namn_lista)

    if st.button("Ta bort bolag"):
        data.pop(valt_namn, None)
        save_data(data)
        st.success(f"Bolag '{valt_namn}' borttaget.")
        st.experimental_rerun()
