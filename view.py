import streamlit as st
from utils import berakna_targetkurser_och_undervardering

def visa_alla_bolag(data):
    st.header("Mina sparade bolag")
    st.markdown("### Debug – inläst data från data.json")
    st.json(data)

    if not data:
        st.info("Ingen data sparad ännu.")
        return

    st.markdown("### Sparade bolag:")
    for namn, info in data.items():
        st.markdown(f"#### 📊 {namn}")
        st.write(f"Nuvarande kurs: {info['kurs']:.2f} kr")

        resultat = berakna_targetkurser_och_undervardering(info)
        st.write(f"🎯 Targetkurs P/E (i år): {resultat['target_pe_i_ar']:.2f} kr")
        st.write(f"🎯 Targetkurs P/E (nästa år): {resultat['target_pe_nasta_ar']:.2f} kr")
        st.write(f"🎯 Targetkurs P/S (i år): {resultat['target_ps_i_ar']:.2f} kr")
        st.write(f"🎯 Targetkurs P/S (nästa år): {resultat['target_ps_nasta_ar']:.2f} kr")
        st.write(f"📉 Undervärdering (max av P/E och P/S): {resultat['undervardering_procent']:.1f} %")

def visa_ett_bolag(data, bolagsnamn):
    info = data.get(bolagsnamn)
    if not info:
        st.warning("Det gick inte att hitta bolaget.")
        return

    st.markdown(f"## 📌 {bolagsnamn}")
    st.write(f"Nuvarande kurs: {info['kurs']:.2f} kr")

    resultat = berakna_targetkurser_och_undervardering(info)
    st.write(f"🎯 Targetkurs P/E (i år): {resultat['target_pe_i_ar']:.2f} kr")
    st.write(f"🎯 Targetkurs P/E (nästa år): {resultat['target_pe_nasta_ar']:.2f} kr")
    st.write(f"🎯 Targetkurs P/S (i år): {resultat['target_ps_i_ar']:.2f} kr")
    st.write(f"🎯 Targetkurs P/S (nästa år): {resultat['target_ps_nasta_ar']:.2f} kr")
    st.write(f"📉 Undervärdering (max av P/E och P/S): {resultat['undervardering_procent']:.1f} %")
