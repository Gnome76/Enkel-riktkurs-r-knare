import streamlit as st
from data_handler import load_data, save_data
from forms import visa_inmatningsform, visa_redigeringsform

import datetime

st.set_page_config(page_title="Aktieanalysapp", layout="wide")

# --- Hjälpfunktioner för beräkningar ---

def snittvärde(values):
    vals = [v for v in values if v > 0]
    return sum(vals) / len(vals) if vals else 0

def beräkna_targetkurser(bolag):
    säkerhetsmarginal = 0.9

    pe_values = [bolag.get(f"pe_{i}") for i in range(1,5)]
    snitt_pe = snittvärde(pe_values)
    ps_values = [bolag.get(f"ps_{i}") for i in range(1,5)]
    snitt_ps = snittvärde(ps_values)

    # Targetkurs P/E idag och nästa år
    target_pe_idag = snitt_pe * bolag.get("vinst_i_ar", 0) * säkerhetsmarginal
    target_pe_nasta = snitt_pe * bolag.get("vinst_nasta_ar", 0) * säkerhetsmarginal

    # Targetkurs P/S idag
    oms_tillvxt_i_ar = bolag.get("oms_tillvaxt_i_ar", 0)/100
    oms_tillvxt_nasta_ar = bolag.get("oms_tillvaxt_nasta_ar", 0)/100
    nuvarande_ps = bolag.get("nuvarande_ps", 1) or 1  # undvik division med 0

    target_ps_idag = snitt_ps * (oms_tillvxt_i_ar / nuvarande_ps) * bolag.get("nuvarande_kurs", 0) * säkerhetsmarginal
    target_ps_nasta = snitt_ps * ((oms_tillvxt_i_ar * oms_tillvxt_nasta_ar) / nuvarande_ps) * bolag.get("nuvarande_kurs", 0) * säkerhetsmarginal

    return {
        "target_pe_idag": target_pe_idag,
        "target_pe_nasta": target_pe_nasta,
        "target_ps_idag": target_ps_idag,
        "target_ps_nasta": target_ps_nasta
    }

def beräkna_undervardering(targetkurs, nuvarande_kurs):
    if nuvarande_kurs == 0:
        return 0
    return (targetkurs - nuvarande_kurs) / nuvarande_kurs * 100

def beräkna_kopvard_niva(targetkurs):
    return targetkurs * 0.7  # 30% rabatt

# --- Initiera eller ladda data ---

if "bolag_data" not in st.session_state:
    st.session_state.bolag_data = load_data()

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

st.title("Aktieanalysapp")

# --- Lägg till nytt bolag ---

st.header("Lägg till nytt bolag")
nytt_bolag = visa_inmatningsform()
if nytt_bolag:
    # Lägg till datumfält
    nytt_bolag["insatt_datum"] = datetime.datetime.now().isoformat()
    st.session_state.bolag_data.append(nytt_bolag)
    save_data(st.session_state.bolag_data)
    st.success(f"Bolag '{nytt_bolag['namn']}' tillagt!")

# --- Visa och bläddra undervärderade bolag ---

st.header("Undervärderade bolag (sorterade efter P/E nästa år)")

# Beräkna targetkurser och undervärdering för alla bolag
for b in st.session_state.bolag_data:
    targets = beräkna_targetkurser(b)
    b.update(targets)
    b["undervardering_pe_nasta"] = beräkna_undervardering(b["target_pe_nasta"], b["nuvarande_kurs"])
    b["undervardering_pe_idag"] = beräkna_undervardering(b["target_pe_idag"], b["nuvarande_kurs"])
    b["undervardering_ps_nasta"] = beräkna_undervardering(b["target_ps_nasta"], b["nuvarande_kurs"])
    b["undervardering_ps_idag"] = beräkna_undervardering(b["target_ps_idag"], b["nuvarande_kurs"])

# Filtrera undervärderade bolag (minst 0% undervärdering baserat på target_pe_nasta)
undervarderade = [b for b in st.session_state.bolag_data if b["undervardering_pe_nasta"] > 0]

# Sortera efter mest undervärderade baserat på P/E nästa år
undervarderade.sort(key=lambda x: x["undervardering_pe_nasta"], reverse=True)

if not undervarderade:
    st.info("Inga undervärderade bolag enligt P/E nästa år just nu.")
else:
    # Navigering
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("⬅️ Föregående"):
            st.session_state.current_index = max(0, st.session_state.current_index - 1)
    with col3:
        if st.button("Nästa ➡️"):
            st.session_state.current_index = min(len(undervarderade) - 1, st.session_state.current_index + 1)

    current_bolag = undervarderade[st.session_state.current_index]
    st.subheader(f"{current_bolag['namn']}")

    st.markdown(f"**Nuvarande kurs:** {current_bolag['nuvarande_kurs']:.2f} SEK")
    st.markdown(f"**Targetkurs P/E idag:** {current_bolag['target_pe_idag']:.2f} SEK")
    st.markdown(f"**Targetkurs P/E nästa år:** {current_bolag['target_pe_nasta']:.2f} SEK")
    st.markdown(f"**Targetkurs P/S idag:** {current_bolag['target_ps_idag']:.2f} SEK")
    st.markdown(f"**Targetkurs P/S nästa år:** {current_bolag['target_ps_nasta']:.2f} SEK")

    st.markdown(f"**Undervärdering P/E nästa år:** {current_bolag['undervardering_pe_nasta']:.2f} %")
    st.markdown(f"**Köpvärd nivå P/E nästa år:** {beräkna_kopvard_niva(current_bolag['target_pe_nasta']):.2f} SEK")

    # --- Redigera bolag ---
    st.subheader("Redigera bolag")
    uppdaterad = visa_redigeringsform(current_bolag)
    if uppdaterad:
        uppdaterad["insatt_datum"] = current_bolag.get("insatt_datum", datetime.datetime.now().isoformat())
        uppdaterad["senast_andrad"] = datetime.datetime.now().isoformat()
        # Uppdatera data i session_state
        idx = st.session_state.bolag_data.index(current_bolag)
        st.session_state.bolag_data[idx] = uppdaterad
        save_data(st.session_state.bolag_data)
        st.success("Bolaget uppdaterades!")

    # --- Ta bort bolag ---
    if st.button("Ta bort bolag"):
        idx = st.session_state.bolag_data.index(current_bolag)
        namn_bort = current_bolag['namn']
        st.session_state.bolag_data.pop(idx)
        save_data(st.session_state.bolag_data)
        st.success(f"Bolaget '{namn_bort}' togs bort!")
        # Justera index vid borttagning
        if st.session_state.current_index >= len(undervarderade) - 1:
            st.session_state.current_index = max(0, st.session_state.current_index - 1)
        st.experimental_rerun()
