import streamlit as st
from data_handler import load_data
from utils import beräkna_targetkurser, beräkna_undervärdering

def visa_bolag_ett_i_taget():
    data = load_data()

    if not data:
        st.info("Inga bolag sparade ännu.")
        return

    bolag_lista = list(data.keys())
    if "bolag_index" not in st.session_state:
        st.session_state["bolag_index"] = 0

    if st.button("⬅️ Föregående"):
        st.session_state["bolag_index"] = max(0, st.session_state["bolag_index"] - 1)
    if st.button("➡️ Nästa"):
        st.session_state["bolag_index"] = min(len(bolag_lista) - 1, st.session_state["bolag_index"] + 1)

    valt_bolag = bolag_lista[st.session_state["bolag_index"]]
    info = data[valt_bolag]

    target_pe_i_ar, target_pe_nasta = beräkna_targetkurser(info, metod="pe")
    target_ps_i_ar, target_ps_nasta = beräkna_targetkurser(info, metod="ps")
    underv_pe_i_ar = beräkna_undervärdering(info["nuvarande_kurs"], target_pe_i_ar)
    underv_pe_nasta = beräkna_undervärdering(info["nuvarande_kurs"], target_pe_nasta)
    underv_ps_i_ar = beräkna_undervärdering(info["nuvarande_kurs"], target_ps_i_ar)
    underv_ps_nasta = beräkna_undervärdering(info["nuvarande_kurs"], target_ps_nasta)

    st.subheader(f"📊 {valt_bolag}")
    st.write(f"**Nuvarande kurs:** {info['nuvarande_kurs']:.2f} kr")
    st.write(f"**Targetkurs P/E (i år / nästa år):** {target_pe_i_ar:.2f} / {target_pe_nasta:.2f} kr")
    st.write(f"**Targetkurs P/S (i år / nästa år):** {target_ps_i_ar:.2f} / {target_ps_nasta:.2f} kr")
    st.write(f"**Undervärdering P/E:** {underv_pe_i_ar:.0f}% / {underv_pe_nasta:.0f}%")
    st.write(f"**Undervärdering P/S:** {underv_ps_i_ar:.0f}% / {underv_ps_nasta:.0f}%")
    st.write(f"**Köpvärd nivå (30% rabatt):** {target_pe_nasta * 0.7:.2f} kr")
