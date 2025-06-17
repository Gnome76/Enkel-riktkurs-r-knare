import streamlit as st
from utils import berakna_targetkurser_och_undervardering

def visa_alla_bolag(data):
    st.header("📋 Mina sparade bolag")
    st.text("Debug – inläst data från data.json")
    st.json(data)

def visa_ett_bolag(data, valt_bolag):
    if not data:
        st.info("Ingen data sparad ännu.")
        return
    if not valt_bolag or valt_bolag not in data:
        st.info("Inget bolag valt.")
        return

    bolag = data[valt_bolag]
    st.subheader(f"📊 {valt_bolag}")

    st.write(f"**Nuvarande kurs:** {bolag['kurs']:.2f} kr")
    result = berakna_targetkurser_och_undervardering(bolag)
    st.write(f"🎯 **Targetkurs P/E (i år):** {result['target_pe_i_ar']:.2f} kr")
    st.write(f"🎯 **Targetkurs P/E (nästa år):** {result['target_pe_nasta_ar']:.2f} kr")
    st.write(f"🎯 **Targetkurs P/S (i år):** {result['target_ps_i_ar']:.2f} kr")
    st.write(f"🎯 **Targetkurs P/S (nästa år):** {result['target_ps_nasta_ar']:.2f} kr")

    undervardering = result["undervardering_procent"]
    st.write(f"📉 **Undervärdering (max av P/E och P/S):** {undervardering:.1f} %")
