import streamlit as st
from utils import berakna_undervarderingar

def visa_bolag(data: dict):
    for namn, bolag in data.items():
        st.subheader(f"📊 {namn}")
        kurs = bolag.get("kurs", 0.0)
        st.write(f"Nuvarande kurs: {kurs:.2f} kr")

        pe_target_i_ar, pe_target_nasta_ar, ps_target_i_ar, ps_target_nasta_ar, undervardering = berakna_undervarderingar(bolag)

        st.write(f"🎯 Targetkurs P/E (i år): {pe_target_i_ar:.2f} kr")
        st.write(f"🎯 Targetkurs P/E (nästa år): {pe_target_nasta_ar:.2f} kr")
        st.write(f"🎯 Targetkurs P/S (i år): {ps_target_i_ar:.2f} kr")
        st.write(f"🎯 Targetkurs P/S (nästa år): {ps_target_nasta_ar:.2f} kr")
        st.write(f"📉 Undervärdering (max av P/E och P/S): {undervardering:.1f} %")

        st.markdown("---")
