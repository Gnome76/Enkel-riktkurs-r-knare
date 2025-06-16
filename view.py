import streamlit as st
from data_handler import load_data
from utils import beräkna_targetkurser, beräkna_undervärdering

def visa_bolag_ett_i_taget():
    data = load_data()

    if not data:
        st.info("Inga bolag har lagts till ännu.")
        return

    bolagslista = list(data.keys())
    if "index" not in st.session_state:
        st.session_state.index = 0

    # Navigeringsknappar
    kol1, kol2, kol3 = st.columns([1, 2, 1])
    with kol1:
        if st.button("⬅️ Föregående") and st.session_state.index > 0:
            st.session_state.index -= 1
    with kol3:
        if st.button("Nästa ➡️") and st.session_state.index < len(bolagslista) - 1:
            st.session_state.index += 1

    bolagsnamn = bolagslista[st.session_state.index]
    info = data[bolagsnamn]

    st.subheader(f"{bolagsnamn}")
    st.write(f"**Nuvarande kurs:** {info.get('nuvarande_kurs', '–')} kr")

    # Targetkurser
    target_pe_i_ar, target_pe_nasta = beräkna_targetkurser(info, metod="pe")
    target_ps_i_ar, target_ps_nasta = beräkna_targetkurser(info, metod="ps")

    if target_pe_i_ar and target_pe_nasta:
        st.write(f"**Targetkurs P/E:** {target_pe_i_ar:.1f} kr / {target_pe_nasta:.1f} kr")
    else:
        st.warning("⚠️ Kunde inte räkna ut targetkurs P/E.")

    if target_ps_i_ar and target_ps_nasta:
        st.write(f"**Targetkurs P/S:** {target_ps_i_ar:.1f} kr / {target_ps_nasta:.1f} kr")
    else:
        st.warning("⚠️ Kunde inte räkna ut targetkurs P/S.")

    # Undervärdering
    result_pe = beräkna_undervärdering(info, metod="pe")
if result_pe:
    underv_pe_i_ar, underv_pe_nasta = result_pe
    st.write(f"**Undervärdering P/E:** {underv_pe_i_ar:.0f}% / {underv_pe_nasta:.0f}%")
else:
    st.warning("⚠️ Kunde inte räkna ut undervärdering för P/E.")
    result_ps = beräkna_undervärdering(info, metod="ps")
if result_ps:
    underv_ps_i_ar, underv_ps_nasta = result_ps
    st.write(f"**Undervärdering P/S:** {underv_ps_i_ar:.0f}% / {underv_ps_nasta:.0f}%")
else:
    st.warning("⚠️ Kunde inte räkna ut undervärdering för P/S.")

    if underv_pe_i_ar is not None and underv_pe_nasta is not None:
        st.write(f"**Undervärdering P/E:** {underv_pe_i_ar:.0f}% / {underv_pe_nasta:.0f}%")
    else:
        st.warning("⚠️ Kunde inte räkna ut undervärdering för P/E.")

    if underv_ps_i_ar is not None and underv_ps_nasta is not None:
        st.write(f"**Undervärdering P/S:** {underv_ps_i_ar:.0f}% / {underv_ps_nasta:.0f}%")
    else:
        st.warning("⚠️ Kunde inte räkna ut undervärdering för P/S.")

    st.caption(f"Visar bolag {st.session_state.index + 1} av {len(bolagslista)}")
