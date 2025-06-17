import streamlit as st
from utils import berakna_targetkurser_och_undervardering

def visa_alla_bolag(data):
    st.subheader("📊 Mina sparade bolag")

    if not data:
        st.info("Ingen data sparad ännu.")
        return

    st.markdown("#### Debug – inläst data från data.json")
    st.json(data)

    resultat = berakna_targetkurser_och_undervardering(data)

    for bolag, info in data.items():
        st.markdown(f"### 📊 {bolag}")
        kurs = info.get("kurs", 0.0)
        st.write(f"**Nuvarande kurs:** {kurs:.2f} kr")

        target = resultat.get(bolag, {})
        pe_ia = target.get("target_pe_i_ar", 0.0)
        pe_na = target.get("target_pe_nasta_ar", 0.0)
        ps_ia = target.get("target_ps_i_ar", 0.0)
        ps_na = target.get("target_ps_nasta_ar", 0.0)
        undervardering = target.get("undervardering_procent", 0.0)

        st.write(f"🎯 **Targetkurs P/E (i år):** {pe_ia:.2f} kr")
        st.write(f"🎯 **Targetkurs P/E (nästa år):** {pe_na:.2f} kr")
        st.write(f"🎯 **Targetkurs P/S (i år):** {ps_ia:.2f} kr")
        st.write(f"🎯 **Targetkurs P/S (nästa år):** {ps_na:.2f} kr")

        undervardering_text = (
            f"📉 **Undervärdering (max av P/E och P/S):** {undervardering:.1f} %"
            if undervardering >= 0
            else f"📈 **Övervärdering (max av P/E och P/S):** {undervardering:.1f} %"
        )
        st.write(undervardering_text)

        st.markdown("---")

def visa_ett_bolag(data, valt_bolag):
    if valt_bolag not in data:
        st.warning("Bolaget finns inte i datan.")
        return

    info = data[valt_bolag]
    resultat = berakna_targetkurser_och_undervardering({valt_bolag: info})[valt_bolag]

    st.markdown(f"## 📈 {valt_bolag}")
    st.write(f"**Nuvarande kurs:** {info.get('kurs', 0.0):.2f} kr")

    st.write(f"🎯 **Targetkurs P/E (i år):** {resultat['target_pe_i_ar']:.2f} kr")
    st.write(f"🎯 **Targetkurs P/E (nästa år):** {resultat['target_pe_nasta_ar']:.2f} kr")
    st.write(f"🎯 **Targetkurs P/S (i år):** {resultat['target_ps_i_ar']:.2f} kr")
    st.write(f"🎯 **Targetkurs P/S (nästa år):** {resultat['target_ps_nasta_ar']:.2f} kr")

    undervardering = resultat["undervardering_procent"]
    undervardering_text = (
        f"📉 **Undervärdering:** {undervardering:.1f} %"
        if undervardering >= 0
        else f"📈 **Övervärdering:** {undervardering:.1f} %"
    )
    st.write(undervardering_text)
