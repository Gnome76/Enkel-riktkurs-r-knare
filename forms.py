import streamlit as st
from data_handler import load_data, save_data

fält = [
    "kurs", "pe_nuvarande", "pe_1", "pe_2", "pe_3", "pe_4",
    "ps_nuvarande", "ps_1", "ps_2", "ps_3", "ps_4",
    "vinst_i_ar", "vinst_nasta_ar", "oms_tillv_i_ar", "oms_tillv_nasta_ar"
]

def nytt_bolag_form():
    st.header("➕ Lägg till nytt bolag")
    data = load_data()

    with st.form("nytt_bolag_form"):
        namn = st.text_input("Bolagsnamn")
        values = {}
        for f in fält:
            values[f] = st.number_input(f"{f.replace('_', ' ').capitalize()}", value=0.0)
        submitted = st.form_submit_button("Spara")
        if submitted and namn:
            data[namn] = values
            save_data(data)
            st.success(f"{namn} har sparats.")

def redigera_bolag_form():
    st.header("✏️ Redigera bolag")
    data = load_data()
    if not data:
        st.info("Inga bolag att redigera.")
        return

    val = st.selectbox("Välj bolag att redigera", list(data.keys()))
    if not val:
        return

    meddata = data[val]

    with st.form("redigera_form"):
        nya_värden = {}
        for f in fält:
            nya_värden[f] = st.number_input(f"{f.replace('_', ' ').capitalize()}", value=meddata.get(f, 0.0))
        if st.form_submit_button("Uppdatera"):
            data[val] = nya_värden
            save_data(data)
            st.success(f"{val} har uppdaterats.")

def ta_bort_bolag_form():
    st.header("🗑️ Ta bort bolag")
    data = load_data()
    if not data:
        st.info("Inga bolag att ta bort.")
        return

    val = st.selectbox("Välj bolag att ta bort", list(data.keys()))
    if val and st.button("Bekräfta borttagning"):
        del data[val]
        save_data(data)
        st.success(f"{val} har tagits bort.")
