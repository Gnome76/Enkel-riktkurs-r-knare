import streamlit as st
import json
from utils import berakna_targetkurser_och_undervardering
from view import visa_alla_bolag, visa_ett_bolag

DATA_FIL = "data.json"

def las_in_data():
    try:
        with open(DATA_FIL, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def spara_data(data):
    with open(DATA_FIL, "w") as f:
        json.dump(data, f, indent=2)

def main():
    st.title("Enkel aktieanalysapp")

    data = las_in_data()

    # Visa alla bolag med beräkningar
    if data:
        beraknat = berakna_targetkurser_och_undervardering(data)
        visa_alla_bolag(beraknat)
    else:
        st.info("Inga bolag sparade ännu.")

    # Form för att lägga till nytt bolag
    with st.form(key="nytt_bolag_form"):
        st.header("Lägg till nytt bolag")
        namn = st.text_input("Bolagsnamn").strip()
        kurs = st.number_input("Nuvarande kurs (kr)", min_value=0.0, format="%.2f")
        vinst_i_ar = st.number_input("Vinst i år", format="%.2f")
        vinst_nasta_ar = st.number_input("Vinst nästa år", format="%.2f")
        oms_tillv_i_ar = st.number_input("Omsättningstillväxt i år", format="%.2f")
        oms_tillv_nasta_ar = st.number_input("Omsättningstillväxt nästa år", format="%.2f")
        pe_1 = st.number_input("P/E 1", format="%.2f")
        pe_2 = st.number_input("P/E 2", format="%.2f")
        pe_3 = st.number_input("P/E 3", format="%.2f")
        pe_4 = st.number_input("P/E 4", format="%.2f")
        ps_1 = st.number_input("P/S 1", format="%.2f")
        ps_2 = st.number_input("P/S 2", format="%.2f")
        ps_3 = st.number_input("P/S 3", format="%.2f")
        ps_4 = st.number_input("P/S 4", format="%.2f")
        ps_nuvarande = st.number_input("Nuvarande P/S", format="%.2f")

        knapp = st.form_submit_button("Spara bolag")

        if knapp:
            if namn == "":
                st.error("Ange ett bolagsnamn!")
            elif namn in data:
                st.error("Bolaget finns redan!")
            else:
                data[namn] = {
                    "kurs": kurs,
                    "vinst_i_ar": vinst_i_ar,
                    "vinst_nasta_ar": vinst_nasta_ar,
                    "oms_tillv_i_ar": oms_tillv_i_ar,
                    "oms_tillv_nasta_ar": oms_tillv_nasta_ar,
                    "pe_1": pe_1,
                    "pe_2": pe_2,
                    "pe_3": pe_3,
                    "pe_4": pe_4,
                    "ps_1": ps_1,
                    "ps_2": ps_2,
                    "ps_3": ps_3,
                    "ps_4": ps_4,
                    "ps_nuvarande": ps_nuvarande
                }
                spara_data(data)
                st.success(f"Bolaget '{namn}' sparades!")
                st.experimental_rerun()

if __name__ == "__main__":
    main()
