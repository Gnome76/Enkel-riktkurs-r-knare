import streamlit as st
from data_handler import save_data

def nytt_bolag_formular(data):
    st.subheader("Lägg till nytt bolag")

    with st.form("nytt_bolag_form"):
        namn = st.text_input("Bolagsnamn").strip()
        nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0)

        nuvarande_pe = st.number_input("Nuvarande P/E", min_value=0.0)
        pe = [st.number_input(f"P/E {i+1}", min_value=0.0) for i in range(4)]

        nuvarande_ps = st.number_input("Nuvarande P/S", min_value=0.0)
        ps = [st.number_input(f"P/S {i+1}", min_value=0.0) for i in range(4)]

        vinst_i_ar = st.number_input("Förväntad vinst i år", min_value=0.0)
        vinst_nasta_ar = st.number_input("Förväntad vinst nästa år", min_value=0.0)

        tillvaxt_i_ar = st.number_input("Omsättningstillväxt i år (%)", min_value=0.0) / 100
        tillvaxt_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", min_value=0.0) / 100

        submit = st.form_submit_button("Spara bolag")

        if submit and namn:
            data[namn] = {
                "nuvarande_kurs": nuvarande_kurs,
                "nuvarande_pe": nuvarande_pe,
                "pe": pe,
                "nuvarande_ps": nuvarande_ps,
                "ps": ps,
                "vinst_i_ar": vinst_i_ar,
                "vinst_nasta_ar": vinst_nasta_ar,
                "tillvaxt_i_ar": tillvaxt_i_ar,
                "tillvaxt_nasta_ar": tillvaxt_nasta_ar,
            }
            save_data(data)
            st.success(f"{namn} har sparats.")

def redigeringsformular(data):
    st.subheader("Redigera bolag")

    if not data:
        st.info("Inga bolag att redigera ännu.")
        return

    val = st.selectbox("Välj bolag att redigera", list(data.keys()))

    if not val:
        return

    bolag = data[val]

    with st.form(f"redigera_{val}"):
        nuvarande_kurs = st.number_input("Nuvarande kurs", value=bolag["nuvarande_kurs"], min_value=0.0)
        nuvarande_pe = st.number_input("Nuvarande P/E", value=bolag["nuvarande_pe"], min_value=0.0)
        pe = [st.number_input(f"P/E {i+1}", value=bolag["pe"][i], min_value=0.0) for i in range(4)]

        nuvarande_ps = st.number_input("Nuvarande P/S", value=bolag["nuvarande_ps"], min_value=0.0)
        ps = [st.number_input(f"P/S {i+1}", value=bolag["ps"][i], min_value=0.0) for i in range(4)]

        vinst_i_ar = st.number_input("Förväntad vinst i år", value=bolag["vinst_i_ar"], min_value=0.0)
        vinst_nasta_ar = st.number_input("Förväntad vinst nästa år", value=bolag["vinst_nasta_ar"], min_value=0.0)

        tillvaxt_i_ar = st.number_input("Omsättningstillväxt i år (%)", value=bolag["tillvaxt_i_ar"] * 100, min_value=0.0)
        tillvaxt_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", value=bolag["tillvaxt_nasta_ar"] * 100, min_value=0.0)

        submit = st.form_submit_button("Uppdatera bolag")

        if submit:
            data[val] = {
                "nuvarande_kurs": nuvarande_kurs,
                "nuvarande_pe": nuvarande_pe,
                "pe": pe,
                "nuvarande_ps": nuvarande_ps,
                "ps": ps,
                "vinst_i_ar": vinst_i_ar,
                "vinst_nasta_ar": vinst_nasta_ar,
                "tillvaxt_i_ar": tillvaxt_i_ar / 100,
                "tillvaxt_nasta_ar": tillvaxt_nasta_ar / 100,
            }
            save_data(data)
            st.success(f"{val} har uppdaterats.")
