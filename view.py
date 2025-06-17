import streamlit as st
from utils import berakna_targetkurser_och_undervardering

def visa_alla_bolag(data):
    st.subheader("📊 Alla bolag")
    for namn, info in data.items():
        kurs = info.get("kurs", 0)
        resultat = berakna_targetkurser_och_undervardering(info)

        st.markdown(f"### 📌 {namn}")
        st.markdown(f"- Nuvarande kurs: **{kurs:.2f} kr**")
        st.markdown(f"- 🎯 Targetkurs P/E (i år): **{resultat['target_pe_i_ar']:.2f} kr**")
        st.markdown(f"- 🎯 Targetkurs P/E (nästa år): **{resultat['target_pe_nasta_ar']:.2f} kr**")
        st.markdown(f"- 🎯 Targetkurs P/S (i år): **{resultat['target_ps_i_ar']:.2f} kr**")
        st.markdown(f"- 🎯 Targetkurs P/S (nästa år): **{resultat['target_ps_nasta_ar']:.2f} kr**")
        st.markdown(f"- 📉 Undervärdering (max av P/E och P/S): **{resultat['max_undervardering']:.1f} %**")
        st.markdown("---")

def visa_ett_bolag(data):
    if not data:
        st.info("Ingen data att visa.")
        return

    bolagsnamn = list(data.keys())
    valt_bolag = st.selectbox("Välj bolag att visa", bolagsnamn)

    if valt_bolag:
        info = data[valt_bolag]
        kurs = info.get("kurs", 0)
        resultat = berakna_targetkurser_och_undervardering(info)

        st.subheader(f"📊 {valt_bolag}")
        st.markdown(f"- Nuvarande kurs: **{kurs:.2f} kr**")
        st.markdown(f"- 🎯 Targetkurs P/E (i år): **{resultat['target_pe_i_ar']:.2f} kr**")
        st.markdown(f"- 🎯 Targetkurs P/E (nästa år): **{resultat['target_pe_nasta_ar']:.2f} kr**")
        st.markdown(f"- 🎯 Targetkurs P/S (i år): **{resultat['target_ps_i_ar']:.2f} kr**")
        st.markdown(f"- 🎯 Targetkurs P/S (nästa år): **{resultat['target_ps_nasta_ar']:.2f} kr**")
        st.markdown(f"- 📉 Undervärdering (max av P/E och P/S): **{resultat['max_undervardering']:.1f} %**")
