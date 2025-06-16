import streamlit as st
from berakningar import berakna_targetkurs_pe, berakna_targetkurs_ps, berakna_undervardering

def visa_bolag_ett_i_taget():
    data = st.session_state.data
    bolag_lista = list(data.keys())
    if not bolag_lista:
        st.info("Inga bolag att visa.")
        return

    if "index" not in st.session_state:
        st.session_state.index = 0

    kol1, kol2, kol3 = st.columns([1, 6, 1])

    with kol1:
        if st.button("⬅️ Föregående"):
            st.session_state.index = (st.session_state.index - 1) % len(bolag_lista)
    with kol3:
        if st.button("Nästa ➡️"):
            st.session_state.index = (st.session_state.index + 1) % len(bolag_lista)

    valt_bolag = bolag_lista[st.session_state.index]
    bolag = data[valt_bolag]

    st.markdown(f"## {valt_bolag}")

    kurs = bolag.get("kurs", 0)
    vinst_1 = bolag.get("vinst_1", 0)
    vinst_2 = bolag.get("vinst_2", 0)
    oms_tillv_1 = bolag.get("oms_tillv_1", 0)
    oms_tillv_2 = bolag.get("oms_tillv_2", 0)
    pe1 = bolag.get("pe1", 0)
    pe2 = bolag.get("pe2", 0)
    pe3 = bolag.get("pe3", 0)
    pe4 = bolag.get("pe4", 0)
    ps1 = bolag.get("ps1", 0)
    ps2 = bolag.get("ps2", 0)
    ps3 = bolag.get("ps3", 0)
    ps4 = bolag.get("ps4", 0)

    target_pe_1, target_pe_2 = berakna_targetkurs_pe(vinst_1, vinst_2, pe1, pe2, pe3, pe4)
    target_ps_1, target_ps_2 = berakna_targetkurs_ps(kurs, oms_tillv_1, oms_tillv_2, ps1, ps2, ps3, ps4)

    underv_pe_1 = berakna_undervardering(kurs, target_pe_1)
    underv_pe_2 = berakna_undervardering(kurs, target_pe_2)
    underv_ps_1 = berakna_undervardering(kurs, target_ps_1)
    underv_ps_2 = berakna_undervardering(kurs, target_ps_2)

    st.write(f"**Nuvarande kurs:** {kurs:.2f} SEK")

    st.write("### Targetkurs P/E")
    st.write(f"I år: {target_pe_1:.2f} SEK ({underv_pe_1:+.1f} % undervärdering)")
    st.write(f"Nästa år: {target_pe_2:.2f} SEK ({underv_pe_2:+.1f} % undervärdering)")

    st.write("### Targetkurs P/S")
    st.write(f"I år: {target_ps_1:.2f} SEK ({underv_ps_1:+.1f} % undervärdering)")
    st.write(f"Nästa år: {target_ps_2:.2f} SEK ({underv_ps_2:+.1f} % undervärdering)")

    # Köpvärd nivå = targetkurs - 30%
    koper_pe_1 = target_pe_1 * 0.7
    koper_pe_2 = target_pe_2 * 0.7
    koper_ps_1 = target_ps_1 * 0.7
    koper_ps_2 = target_ps_2 * 0.7

    st.write("### Köpvärd nivå (30 % rabatt)")
    st.write(f"P/E i år: {koper_pe_1:.2f} SEK")
    st.write(f"P/E nästa år: {koper_pe_2:.2f} SEK")
    st.write(f"P/S i år: {koper_ps_1:.2f} SEK")
    st.write(f"P/S nästa år: {koper_ps_2:.2f} SEK")
