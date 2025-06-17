import streamlit as st
from utils import berakna_targetkurser

def visa_bolag_ett_i_taget(data):
    st.header("Undervärderade bolag")

    if not data:
        st.info("Inga bolag tillgängliga.")
        return

    # Filtrera bolag med minst 30 % rabatt
    undervarderade = {}
    for namn, info in data.items():
        try:
            result = berakna_targetkurser(info)
            rabatt_pe_nasta = result["undervärdering_pe_nasta"]
            rabatt_ps_nasta = result["undervärdering_ps_nasta"]

            if rabatt_pe_nasta >= 30 or rabatt_ps_nasta >= 30:
                undervarderade[namn] = (info, result)
        except Exception:
            continue

    if not undervarderade:
        st.warning("Inga undervärderade bolag hittades.")
        return

    bolagslista = list(undervarderade.items())
    index = st.session_state.get("bolags_index", 0)

    if index >= len(bolagslista):
        index = 0
        st.session_state["bolags_index"] = 0

    namn, (info, result) = bolagslista[index]

    st.subheader(namn)

    st.markdown(f"**Nuvarande kurs:** {info.get('kurs', 0):.2f} kr")

    st.markdown("**🎯 Targetkurser (med 10% säkerhetsmarginal):**")
    st.markdown(f"- P/E i år: {result['target_pe_iaar']:.2f} kr")
    st.markdown(f"- P/E nästa år: {result['target_pe_nasta']:.2f} kr")
    st.markdown(f"- P/S i år: {result['target_ps_iaar']:.2f} kr")
    st.markdown(f"- P/S nästa år: {result['target_ps_nasta']:.2f} kr")

    st.markdown("**📉 Undervärdering:**")
    st.markdown(f"- P/E: {result['undervärdering_pe_nasta']:.1f}%")
    st.markdown(f"- P/S: {result['undervärdering_ps_nasta']:.1f}%")

    st.markdown("**🛒 Köpvärd vid:**")
    st.markdown(f"- P/E (30% rabatt): {result['target_pe_nasta'] * 0.7:.2f} kr")
    st.markdown(f"- P/S (30% rabatt): {result['target_ps_nasta'] * 0.7:.2f} kr")

    col1, col2 = st.columns(2)
    if col1.button("Föregående"):
        st.session_state["bolags_index"] = (index - 1) % len(bolagslista)
        st.experimental_rerun()
    if col2.button("Nästa"):
        st.session_state["bolags_index"] = (index + 1) % len(bolagslista)
        st.experimental_rerun()
