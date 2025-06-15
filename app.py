import streamlit as st
from data_handler import load_data, save_data
from forms import visa_inmatningsform, visa_redigeringsform
import datetime

st.set_page_config(page_title="Aktieanalysapp", layout="wide")

def snittvärde(values):
    vals = [v for v in values if v and v > 0]
    return sum(vals) / len(vals) if vals else 0

def beräkna_targetkurser(bolag):
    säkerhetsmarginal = 0.9
    pe_values = [bolag.get(f"pe_{i}", 0) or 0 for i in range(1,5)]
    ps_values = [bolag.get(f"ps_{i}", 0) or 0 for i in range(1,5)]
    snitt_pe = snittvärde(pe_values)
    snitt_ps = snittvärde(ps_values)

    vinst_i_ar = bolag.get("vinst_i_ar", 0) or 0
    vinst_nasta_ar = bolag.get("vinst_nasta_ar", 0) or 0
    oms_tillvaxt_i_ar = (bolag.get("oms_tillvaxt_i_ar", 0) or 0) / 100
    oms_tillvaxt_nasta_ar = (bolag.get("oms_tillvaxt_nasta_ar", 0) or 0) / 100
    nuvarande_kurs = bolag.get("nuvarande_kurs", 0) or 0
    nuvarande_ps = bolag.get("nuvarande_ps", 1) or 1
    if nuvarande_ps <= 0:
        nuvarande_ps = 1

    return {
        "target_pe_idag": snitt_pe * vinst_i_ar * säkerhetsmarginal,
        "target_pe_nasta": snitt_pe * vinst_nasta_ar * säkerhetsmarginal,
        "target_ps_idag": snitt_ps * (oms_tillvaxt_i_ar / nuvarande_ps) * nuvarande_kurs * säkerhetsmarginal,
        "target_ps_nasta": snitt_ps * ((oms_tillvaxt_i_ar * oms_tillvaxt_nasta_ar) / nuvarande_ps) * nuvarande_kurs * säkerhetsmarginal
    }

def beräkna_undervardering(targetkurs, nuvarande_kurs):
    return (targetkurs - nuvarande_kurs) / nuvarande_kurs * 100 if nuvarande_kurs else 0

def beräkna_kopvard_niva(targetkurs):
    return targetkurs * 0.7

if "bolag_data" not in st.session_state:
    st.session_state.bolag_data = load_data()

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "refresh" not in st.session_state:
    st.session_state["refresh"] = False

if st.session_state["refresh"]:
    st.session_state["refresh"] = False
    st.experimental_rerun()

st.title("Aktieanalysapp")
st.header("Lägg till nytt bolag")

nytt_bolag = visa_inmatningsform()
if nytt_bolag:
    nytt_bolag["insatt_datum"] = datetime.datetime.now().isoformat()
    st.session_state.bolag_data.append(nytt_bolag)
    save_data(st.session_state.bolag_data)
    st.success(f"Bolag '{nytt_bolag['namn']}' tillagt!")
    st.session_state.current_index = len(st.session_state.bolag_data) - 1

st.header("Bolagsöversikt")

visa_alla = st.checkbox("Visa alla bolag (inte bara undervärderade)", value=False)

for b in st.session_state.bolag_data:
    targets = beräkna_targetkurser(b)
    b.update(targets)
    b["undervardering_pe_idag"] = beräkna_undervardering(b["target_pe_idag"], b.get("nuvarande_kurs", 0))
    b["undervardering_pe_nasta"] = beräkna_undervardering(b["target_pe_nasta"], b.get("nuvarande_kurs", 0))
    b["undervardering_ps_idag"] = beräkna_undervardering(b["target_ps_idag"], b.get("nuvarande_kurs", 0))
    b["undervardering_ps_nasta"] = beräkna_undervardering(b["target_ps_nasta"], b.get("nuvarande_kurs", 0))

visade_bolag = st.session_state.bolag_data if visa_alla else [b for b in st.session_state.bolag_data if b["undervardering_pe_nasta"] > 0]
visade_bolag.sort(key=lambda x: x["undervardering_pe_nasta"], reverse=True)

if not visade_bolag:
    st.info("Inga bolag att visa enligt vald filter.")
else:
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("⬅️ Föregående", key="prev"):
            st.session_state.current_index = max(0, st.session_state.current_index - 1)
    with col3:
        if st.button("Nästa ➡️", key="next"):
            st.session_state.current_index = min(len(visade_bolag) - 1, st.session_state.current_index + 1)

    st.session_state.current_index = max(0, min(st.session_state.current_index, len(visade_bolag) - 1))
    current_bolag = visade_bolag[st.session_state.current_index]

    st.subheader(current_bolag['namn'])
    st.markdown(f"**Nuvarande kurs:** {current_bolag['nuvarande_kurs']:.2f} SEK")
    st.markdown(f"**Targetkurs P/E idag:** {current_bolag['target_pe_idag']:.2f}")
    st.markdown(f"**Targetkurs P/E nästa år:** {current_bolag['target_pe_nasta']:.2f}")
    st.markdown(f"**Targetkurs P/S idag:** {current_bolag['target_ps_idag']:.2f}")
    st.markdown(f"**Targetkurs P/S nästa år:** {current_bolag['target_ps_nasta']:.2f}")
    st.markdown(f"**Undervärdering P/E nästa år:** {current_bolag['undervardering_pe_nasta']:.2f}%")
    st.markdown(f"**Köpvärd nivå (30% rabatt):** {beräkna_kopvard_niva(current_bolag['target_pe_nasta']):.2f} SEK")

    st.subheader("Redigera bolag")
    uppdaterad = visa_redigeringsform(current_bolag)
    if uppdaterad:
        uppdaterad["insatt_datum"] = current_bolag.get("insatt_datum")
        uppdaterad["senast_andrad"] = datetime.datetime.now().isoformat()
        idx = st.session_state.bolag_data.index(current_bolag)
        st.session_state.bolag_data[idx] = uppdaterad
        save_data(st.session_state.bolag_data)
        st.success("Bolaget uppdaterades!")
        st.session_state["refresh"] = True
        st.stop()

    if st.button("Ta bort bolag", key=f"ta_bort_{current_bolag['namn']}"):
        idx = st.session_state.bolag_data.index(current_bolag)
        st.session_state.bolag_data.pop(idx)
        save_data(st.session_state.bolag_data)
        st.success("Bolaget togs bort!")
        st.session_state.current_index = max(0, st.session_state.current_index - 1)
        st.session_state["refresh"] = True
        st.stop()
