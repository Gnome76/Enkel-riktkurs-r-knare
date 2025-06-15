import streamlit as st
import json
import os
from datetime import datetime

DATAFIL = "bolag_data.json"

def las_data():
    if not os.path.exists(DATAFIL):
        return []
    try:
        with open(DATAFIL, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def spara_data(data):
    with open(DATAFIL, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

st.set_page_config(page_title="Enkel riktkurs-räknare", layout="centered")
st.title("Enkel riktkurs-räknare")

# Ladda bolagsdata in i session_state en gång
if "bolag_list" not in st.session_state:
    st.session_state.bolag_list = las_data()

def berakna_targetkurser(bolag):
    pe_varden = [bolag.get(f"pe{i}", 0) or 0 for i in range(1, 5)]
    ps_varden = [bolag.get(f"ps{i}", 0) or 0 for i in range(1, 5)]

    pe_varden = [v for v in pe_varden if v > 0]
    ps_varden = [v for v in ps_varden if v > 0]

    pe_snitt = sum(pe_varden) / len(pe_varden) if pe_varden else None
    ps_snitt = sum(ps_varden) / len(ps_varden) if ps_varden else None

    vinst_ar = bolag.get("vinst_i_ar")
    vinst_nasta_ar = bolag.get("vinst_nasta_ar")
    oms_tillvxt_ar = bolag.get("omsattningstillvaxt_i_ar")
    oms_tillvxt_nasta_ar = bolag.get("omsattningstillvaxt_nasta_ar")
    nuvarande_kurs = bolag.get("nuvarande_kurs")
    nuvarande_ps = bolag.get("nuvarande_ps")

    target_pe_i_ar = pe_snitt * vinst_ar * 0.9 if pe_snitt and vinst_ar else None
    target_pe_nasta_ar = pe_snitt * vinst_nasta_ar * 0.9 if pe_snitt and vinst_nasta_ar else None

    if ps_snitt and oms_tillvxt_ar is not None and nuvarande_kurs and nuvarande_ps:
        target_ps_i_ar = ps_snitt * (1 + oms_tillvxt_ar / 100) * nuvarande_kurs * 0.9
    else:
        target_ps_i_ar = None

    if ps_snitt and oms_tillvxt_ar is not None and oms_tillvxt_nasta_ar is not None and nuvarande_kurs and nuvarande_ps:
        target_ps_nasta_ar = ps_snitt * (1 + oms_tillvxt_ar / 100) * (1 + oms_tillvxt_nasta_ar / 100) * nuvarande_kurs * 0.9
    else:
        target_ps_nasta_ar = None

    return target_pe_i_ar, target_pe_nasta_ar, target_ps_i_ar, target_ps_nasta_ar

def safe_undervardering(kurs, target):
    if kurs and target and target != 0:
        return (1 - kurs / target) * 100
    else:
        return None

with st.form(key="lagg_till_bolag_form"):
    st.subheader("Lägg till / uppdatera bolag")
    namn = st.text_input("Bolagsnamn").strip()
    nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
    vinst_i_ar = st.number_input("Vinst i år", format="%.2f")
    vinst_nasta_ar = st.number_input("Vinst nästa år", format="%.2f")
    omsattningstillvaxt_i_ar = st.number_input("Omsättningstillväxt i år (%)", format="%.2f")
    omsattningstillvaxt_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", format="%.2f")

    nuvarande_pe = st.number_input("Nuvarande P/E", min_value=0.0, format="%.2f")
    pe1 = st.number_input("P/E 1", min_value=0.0, format="%.2f")
    pe2 = st.number_input("P/E 2", min_value=0.0, format="%.2f")
    pe3 = st.number_input("P/E 3", min_value=0.0, format="%.2f")
    pe4 = st.number_input("P/E 4", min_value=0.0, format="%.2f")

    nuvarande_ps = st.number_input("Nuvarande P/S", min_value=0.0, format="%.2f")
    ps1 = st.number_input("P/S 1", min_value=0.0, format="%.2f")
    ps2 = st.number_input("P/S 2", min_value=0.0, format="%.2f")
    ps3 = st.number_input("P/S 3", min_value=0.0, format="%.2f")
    ps4 = st.number_input("P/S 4", min_value=0.0, format="%.2f")

    submit = st.form_submit_button("Spara bolag")

    if submit:
        if namn == "":
            st.warning("Ange bolagsnamn.")
        else:
            nytt_bolag = {
                "namn": namn,
                "nuvarande_kurs": nuvarande_kurs,
                "vinst_i_ar": vinst_i_ar,
                "vinst_nasta_ar": vinst_nasta_ar,
                "omsattningstillvaxt_i_ar": omsattningstillvaxt_i_ar,
                "omsattningstillvaxt_nasta_ar": omsattningstillvaxt_nasta_ar,
                "nuvarande_pe": nuvarande_pe,
                "pe1": pe1,
                "pe2": pe2,
                "pe3": pe3,
                "pe4": pe4,
                "nuvarande_ps": nuvarande_ps,
                "ps1": ps1,
                "ps2": ps2,
                "ps3": ps3,
                "ps4": ps4,
                "insatt_datum": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "senast_andrad": None
            }

            idx = next((i for i, b in enumerate(st.session_state.bolag_list) if b["namn"].lower() == namn.lower()), None)
            if idx is not None:
                nytt_bolag["insatt_datum"] = st.session_state.bolag_list[idx]["insatt_datum"]
                nytt_bolag["senast_andrad"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.bolag_list[idx] = nytt_bolag
                st.success(f"Bolaget '{namn}' uppdaterades.")
            else:
                st.session_state.bolag_list.append(nytt_bolag)
                st.success(f"Bolaget '{namn}' tillagt.")

            spara_data(st.session_state.bolag_list)
            st.experimental_rerun()  # OBS! Kan bytas ut om du får fel i din miljö

st.header("Sparade bolag")

if not st.session_state.bolag_list:
    st.info("Inga bolag sparade ännu.")
else:
    valt_bolag_namn = st.selectbox("Välj bolag att visa/redigera", options=[b["namn"] for b in st.session_state.bolag_list])
    bolag = next((b for b in st.session_state.bolag_list if b["namn"] == valt_bolag_namn), None)
    if bolag:
        target_pe_i_ar, target_pe_nasta_ar, target_ps_i_ar, target_ps_nasta_ar = berakna_targetkurser(bolag)

        undervar_pe_i_ar = safe_undervardering(bolag["nuvarande_kurs"], target_pe_i_ar)
        undervar_pe_nasta_ar = safe_undervardering(bolag["nuvarande_kurs"], target_pe_nasta_ar)
        undervar_ps_i_ar = safe_undervardering(bolag["nuvarande_kurs"], target_ps_i_ar)
        undervar_ps_nasta_ar = safe_undervardering(bolag["nuvarande_kurs"], target_ps_nasta_ar)

        st.write(f"**{bolag['namn']}**")
        st.write(f"Nuvarande kurs: {bolag['nuvarande_kurs']:.2f} SEK")
        if target_pe_i_ar:
            st.write(f"Targetkurs P/E i år: {target_pe_i_ar:.2f} SEK (Undervärdering: {undervar_pe_i_ar:.1f} %)")
        if target_pe_nasta_ar:
            st.write(f"Targetkurs P/E nästa år: {target_pe_nasta_ar:.2f} SEK (Undervärdering: {undervar_pe_nasta_ar:.1f} %)")
        if target_ps_i_ar:
            st.write(f"Targetkurs P/S i år: {target_ps_i_ar:.2f} SEK (Undervärdering: {undervar_ps_i_ar:.1f} %)")
        if target_ps_nasta_ar:
            st.write(f"Targetkurs P/S nästa år: {target_ps_nasta_ar:.2f} SEK (Undervärdering: {undervar_ps_nasta_ar:.1f} %)")

        # Visa övriga data också
        st.write(f"Insatt datum: {bolag.get('insatt_datum')}")
        st.write(f"Senast ändrad: {bolag.get('senast_andrad') or 'Ej ändrad'}")
