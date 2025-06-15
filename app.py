import streamlit as st
import json
from datetime import datetime

DATA_FILE = "bolag_data.json"

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def init_session_state():
    if "bolag_data" not in st.session_state:
        st.session_state.bolag_data = load_data()
    if "refresh" not in st.session_state:
        st.session_state.refresh = False

def calc_targetkurs_pe(vinst_ar, vinst_nastaar, pe1, pe2):
    if not (vinst_ar and vinst_nastaar and pe1 and pe2):
        return None, None
    snitt_pe = (pe1 + pe2) / 2
    target_pe_ar = vinst_ar * snitt_pe
    target_pe_nastaar = vinst_nastaar * snitt_pe
    return target_pe_ar, target_pe_nastaar

def calc_targetkurs_ps(ps1, ps2, oms_tillvaxt_ar, oms_tillvaxt_nastaar, kurs):
    if not (ps1 and ps2 and oms_tillvaxt_ar and oms_tillvaxt_nastaar and kurs):
        return None, None
    snitt_ps = (ps1 + ps2) / 2
    # Förenklad formel (kan justeras)
    target_ps_ar = snitt_ps * oms_tillvaxt_ar * kurs
    target_ps_nastaar = snitt_ps * oms_tillvaxt_ar * oms_tillvaxt_nastaar * kurs
    return target_ps_ar, target_ps_nastaar

def calc_undervardering(kurs, targetkurs):
    if kurs and targetkurs:
        return round((targetkurs - kurs) / kurs * 100, 1)
    return None

def visa_bolag_info(bolag):
    st.write(f"### {bolag['namn']}")
    kurs = bolag.get("nuvarande_kurs")
    vinst_ar = bolag.get("vinst_ar")
    vinst_nastaar = bolag.get("vinst_nastaar")
    pe1 = bolag.get("pe1")
    pe2 = bolag.get("pe2")
    ps1 = bolag.get("ps1")
    ps2 = bolag.get("ps2")
    oms_tillvaxt_ar = bolag.get("oms_tillvaxt_ar")
    oms_tillvaxt_nastaar = bolag.get("oms_tillvaxt_nastaar")

    target_pe_ar, target_pe_nastaar = calc_targetkurs_pe(vinst_ar, vinst_nastaar, pe1, pe2)
    target_ps_ar, target_ps_nastaar = calc_targetkurs_ps(ps1, ps2, oms_tillvaxt_ar, oms_tillvaxt_nastaar, kurs)

    st.write(f"Nuvarande kurs: {kurs}")
    if target_pe_ar and target_pe_nastaar:
        underv_pe_ar = calc_undervardering(kurs, target_pe_ar)
        underv_pe_nastaar = calc_undervardering(kurs, target_pe_nastaar)
        st.write(f"Targetkurs P/E (i år): {target_pe_ar:.2f} ({underv_pe_ar}% undervärderad)")
        st.write(f"Targetkurs P/E (nästa år): {target_pe_nastaar:.2f} ({underv_pe_nastaar}% undervärderad)")
    if target_ps_ar and target_ps_nastaar:
        underv_ps_ar = calc_undervardering(kurs, target_ps_ar)
        underv_ps_nastaar = calc_undervardering(kurs, target_ps_nastaar)
        st.write(f"Targetkurs P/S (i år): {target_ps_ar:.2f} ({underv_ps_ar}% undervärderad)")
        st.write(f"Targetkurs P/S (nästa år): {target_ps_nastaar:.2f} ({underv_ps_nastaar}% undervärderad)")

def nytt_bolag_form():
    with st.form(key="nytt_bolag_form"):
        namn = st.text_input("Bolagsnamn")
        kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
        vinst_ar = st.number_input("Vinst i år", format="%.2f")
        vinst_nastaar = st.number_input("Vinst nästa år", format="%.2f")
        pe1 = st.number_input("P/E 1", format="%.2f")
        pe2 = st.number_input("P/E 2", format="%.2f")
        ps1 = st.number_input("P/S 1", format="%.2f")
        ps2 = st.number_input("P/S 2", format="%.2f")
        oms_tillvaxt_ar = st.number_input("Omsättningstillväxt i år (decimaltal, t.ex. 1.05 för 5%)", format="%.2f", value=1.0)
        oms_tillvaxt_nastaar = st.number_input("Omsättningstillväxt nästa år", format="%.2f", value=1.0)

        submit = st.form_submit_button("Spara nytt bolag")
        if submit:
            if namn.strip() == "":
                st.error("Bolagsnamn måste fyllas i!")
                return
            nytt_bolag = {
                "namn": namn.strip(),
                "nuvarande_kurs": kurs,
                "vinst_ar": vinst_ar,
                "vinst_nastaar": vinst_nastaar,
                "pe1": pe1,
                "pe2": pe2,
                "ps1": ps1,
                "ps2": ps2,
                "oms_tillvaxt_ar": oms_tillvaxt_ar,
                "oms_tillvaxt_nastaar": oms_tillvaxt_nastaar,
                "insatt_datum": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "senast_andrad": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            st.session_state.bolag_data[namn] = nytt_bolag
            save_data(st.session_state.bolag_data)
            st.success(f"Bolag {namn} sparat!")
            st.session_state.refresh = True
            st.stop()

def radera_bolag():
    bolag_namn = st.selectbox("Välj bolag att ta bort", options=list(st.session_state.bolag_data.keys()))
    if st.button("Ta bort valt bolag"):
        if bolag_namn in st.session_state.bolag_data:
            del st.session_state.bolag_data[bolag_namn]
            save_data(st.session_state.bolag_data)
            st.success(f"Bolag {bolag_namn} borttaget!")
            st.session_state.refresh = True
            st.stop()

def main():
    st.title("Aktieanalysapp")

    init_session_state()

    menu = st.sidebar.selectbox("Meny", ["Visa bolag", "Lägg till nytt bolag", "Radera bolag"])

    if menu == "Visa bolag":
        if not st.session_state.bolag_data:
            st.info("Inga bolag sparade än.")
            return
        valt_bolag = st.selectbox("Välj bolag att visa", options=list(st.session_state.bolag_data.keys()))
        if valt_bolag:
            visa_bolag_info(st.session_state.bolag_data[valt_bolag])

    elif menu == "Lägg till nytt bolag":
        nytt_bolag_form()

    elif menu == "Radera bolag":
        if not st.session_state.bolag_data:
            st.info("Inga bolag att ta bort.")
            return
        radera_bolag()

if __name__ == "__main__":
    main()
