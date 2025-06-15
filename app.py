import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "bolag_data.json"

# Läs data från fil
def las_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                return []
    except json.JSONDecodeError:
        return []

# Spara data till fil
def spara_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Beräkna medelvärde med skydd mot division med noll
def medelvärde(lista):
    if not lista:
        return 0
    return sum(lista) / len(lista)

# Beräkna targetkurs P/E och P/S med säkerhetsmarginal 10%
def berakna_targetkurser(b):
    # Läs in P/E och P/S
    pe_values = [b.get(f"pe{i}", 0) for i in range(1,5) if b.get(f"pe{i}") is not None]
    ps_values = [b.get(f"ps{i}", 0) for i in range(1,5) if b.get(f"ps{i}") is not None]

    # Vinster och omsättningstillväxt
    vinst_i_år = b.get("vinst_i_år", 0)
    vinst_nästa_år = b.get("vinst_nästa_år", 0)
    oms_tillv_i_år = b.get("oms_tillv_i_år", 0) / 100  # omvandlas från % till decimal
    oms_tillv_nästa_år = b.get("oms_tillv_nästa_år", 0) / 100

    # Nuvarande kurs och nuvarande P/S
    kurs = b.get("nuvarande_kurs", 0)
    nuvarande_ps = b.get("nuvarande_ps", 1)  # undvik division med 0

    # Medelvärde P/E och P/S
    medel_pe = medelvärde(pe_values)
    medel_ps = medelvärde(ps_values)

    # Targetkurser med 10% säkerhetsmarginal (multiplicera med 0.9)
    target_pe_år = medel_pe * vinst_i_år * 0.9
    target_pe_nästa_år = medel_pe * vinst_nästa_år * 0.9

    # Target P/S beräknas som medelvärde av P/S * omsättningstillväxt * kurs / nuvarande_ps * 0.9
    target_ps_år = medel_ps * oms_tillv_i_år * kurs / max(nuvarande_ps, 0.0001) * 0.9
    target_ps_nästa_år = medel_ps * oms_tillv_i_år * oms_tillv_nästa_år * kurs / max(nuvarande_ps, 0.0001) * 0.9

    return target_pe_år, target_pe_nästa_år, target_ps_år, target_ps_nästa_år

# Beräkna undervärdering i % baserat på nuvarande kurs och targetkurs
def berakna_undervardering(nuvarande_kurs, targetkurs):
    if targetkurs == 0:
        return 0
    return (targetkurs - nuvarande_kurs) / targetkurs * 100

# Setup för session_state och initial data
if "bolag_list" not in st.session_state:
    st.session_state.bolag_list = las_data()

if "refresh" not in st.session_state:
    st.session_state.refresh = False

st.title("Enkel Riktkurs- & Aktieanalys")

# Uppdatera funktion som ersätter st.experimental_rerun
def refresh_app():
    st.session_state.refresh = True
    st.experimental_rerun()

if st.session_state.refresh:
    st.session_state.refresh = False
    st.experimental_rerun()

def lagg_till_bolag():
    with st.form(key="form_lagg_till"):
        namn = st.text_input("Bolagsnamn")
        nuv_kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
        vinst_ar = st.number_input("Vinst i år", format="%.2f")
        vinst_nastaar = st.number_input("Vinst nästa år", format="%.2f")
        oms_tillvaxt_ar = st.number_input("Omsättningstillväxt i år (%)", format="%.2f")
        oms_tillvaxt_nastaar = st.number_input("Omsättningstillväxt nästa år (%)", format="%.2f")
        pe1 = st.number_input("P/E år 1", format="%.2f")
        pe2 = st.number_input("P/E år 2", format="%.2f")
        ps1 = st.number_input("P/S år 1", format="%.2f")
        ps2 = st.number_input("P/S år 2", format="%.2f")
        insatt_datum = datetime.date.today().isoformat()

        submit = st.form_submit_button("Lägg till bolag")
        if submit:
            nytt_bolag = {
                "namn": namn,
                "nuvarande_kurs": nuv_kurs,
                "vinst_ar": vinst_ar,
                "vinst_nastaar": vinst_nastaar,
                "oms_tillvaxt_ar": oms_tillvaxt_ar,
                "oms_tillvaxt_nastaar": oms_tillvaxt_nastaar,
                "pe1": pe1,
                "pe2": pe2,
                "ps1": ps1,
                "ps2": ps2,
                "insatt_datum": insatt_datum,
                "senast_andrad": insatt_datum,
            }
            st.session_state.bolag_list.append(nytt_bolag)
            spara_data(st.session_state.bolag_list)
            st.success(f"{namn} har lagts till!")
            refresh_app()

def visa_bolag_lista():
    st.subheader("Sparade bolag")
    for idx, bolag in enumerate(st.session_state.bolag_list):
        st.write(f"{idx+1}. {bolag['namn']} — Kurs: {bolag['nuvarande_kurs']}")

def ta_bort_bolag():
    st.subheader("Ta bort bolag")
    namn_lista = [b["namn"] for b in st.session_state.bolag_list]
    valt = st.selectbox("Välj bolag att ta bort", namn_lista)
    if st.button("Ta bort"):
        st.session_state.bolag_list = [b for b in st.session_state.bolag_list if b["namn"] != valt]
        spara_data(st.session_state.bolag_list)
        st.success(f"{valt} har tagits bort!")
        refresh_app()

def redigera_bolag():
    st.subheader("Redigera bolag")
    namn_lista = [b["namn"] for b in st.session_state.bolag_list]
    valt = st.selectbox("Välj bolag att redigera", namn_lista)
    if valt:
        bolag = next(b for b in st.session_state.bolag_list if b["namn"] == valt)
        with st.form(key="form_redigera"):
            bolag["nuvarande_kurs"] = st.number_input("Nuvarande kurs", value=bolag["nuvarande_kurs"], format="%.2f")
            bolag["vinst_ar"] = st.number_input("Vinst i år", value=bolag["vinst_ar"], format="%.2f")
            bolag["vinst_nastaar"] = st.number_input("Vinst nästa år", value=bolag["vinst_nastaar"], format="%.2f")
            bolag["oms_tillvaxt_ar"] = st.number_input("Omsättningstillväxt i år (%)", value=bolag["oms_tillvaxt_ar"], format="%.2f")
            bolag["oms_tillvaxt_nastaar"] = st.number_input("Omsättningstillväxt nästa år (%)", value=bolag["oms_tillvaxt_nastaar"], format="%.2f")
            bolag["pe1"] = st.number_input("P/E år 1", value=bolag["pe1"], format="%.2f")
            bolag["pe2"] = st.number_input("P/E år 2", value=bolag["pe2"], format="%.2f")
            bolag["ps1"] = st.number_input("P/S år 1", value=bolag["ps1"], format="%.2f")
            bolag["ps2"] = st.number_input("P/S år 2", value=bolag["ps2"], format="%.2f")
            submit = st.form_submit_button("Uppdatera bolag")
            if submit:
                bolag["senast_andrad"] = datetime.date.today().isoformat()
                # Uppdatera listan med nya värden
                for i, b in enumerate(st.session_state.bolag_list):
                    if b["namn"] == valt:
                        st.session_state.bolag_list[i] = bolag
                        break
                spara_data(st.session_state.bolag_list)
                st.success(f"{valt} har uppdaterats!")
                refresh_app()

if __name__ == "__main__":
    st.title("Enkel Riktkurs-Räknare")

    # Initiera session state om det inte finns
    if "bolag_list" not in st.session_state:
        st.session_state.bolag_list = las_data()

    st.sidebar.header("Navigering")
    val = st.sidebar.radio("Välj funktion", ("Lägg till bolag", "Visa bolag", "Redigera bolag", "Ta bort bolag"))

    if val == "Lägg till bolag":
        lagg_till_bolag()
    elif val == "Visa bolag":
        visa_bolag_lista()
    elif val == "Redigera bolag":
        redigera_bolag()
    elif val == "Ta bort bolag":
        ta_bort_bolag()
