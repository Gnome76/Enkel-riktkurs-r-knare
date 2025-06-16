def visa_bolag_ett_i_taget():
    data = load_data()
    
    if not data:
        st.info("Inga bolag tillgängliga att visa ännu.")
        return

    bolagslista = list(data.keys())

    if "val_index" not in st.session_state:
        st.session_state["val_index"] = 0

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("⬅️ Föregående", use_container_width=True):
            st.session_state["val_index"] = (st.session_state["val_index"] - 1) % len(bolagslista)
    with col2:
        if st.button("Nästa ➡️", use_container_width=True):
            st.session_state["val_index"] = (st.session_state["val_index"] + 1) % len(bolagslista)

    valt_bolag = bolagslista[st.session_state["val_index"]]
    info = data[valt_bolag]

    st.subheader(valt_bolag)
    st.write(f"**Nuvarande kurs:** {info.get('nuvarande_kurs', 'saknas')} kr")

    st.write("DEBUG: Data till beräkna_targetkurser med metod='pe':", info)
    result_pe = beräkna_targetkurser(info, metod="pe")
    st.write("DEBUG: Resultat från beräkna_targetkurser (pe):", result_pe)
    if result_pe:
        target_pe_i_ar, target_pe_nasta = result_pe
        st.write(f"**Targetkurs P/E:** {target_pe_i_ar:.1f} kr / {target_pe_nasta:.1f} kr")
    else:
        target_pe_i_ar = target_pe_nasta = None
        st.warning("⚠️ Kunde inte räkna ut targetkurs för P/E.")

    st.write("DEBUG: Data till beräkna_targetkurser med metod='ps':", info)
    result_ps = beräkna_targetkurser(info, metod="ps")
    st.write("DEBUG: Resultat från beräkna_targetkurser (ps):", result_ps)
    if result_ps:
        target_ps_i_ar, target_ps_nasta = result_ps
        st.write(f"**Targetkurs P/S:** {target_ps_i_ar:.1f} kr / {target_ps_nasta:.1f} kr")
    else:
        target_ps_i_ar = target_ps_nasta = None
        st.warning("⚠️ Kunde inte räkna ut targetkurs för P/S.")

    st.write("DEBUG: Data till beräkna_undervärdering med metod='pe':", info)
    result_pe_underv = beräkna_undervärdering(info, metod="pe")
    st.write("DEBUG: Resultat från beräkna_undervärdering (pe):", result_pe_underv)
    if result_pe_underv:
        underv_pe_i_ar, underv_pe_nasta = result_pe_underv
        st.write(f"**Undervärdering P/E:** {underv_pe_i_ar:.0f}% / {underv_pe_nasta:.0f}%")
    else:
        st.warning("⚠️ Kunde inte räkna ut undervärdering för P/E.")

    st.write("DEBUG: Data till beräkna_undervärdering med metod='ps':", info)
    result_ps_underv = beräkna_undervärdering(info, metod="ps")
    st.write("DEBUG: Resultat från beräkna_undervärdering (ps):", result_ps_underv)
    if result_ps_underv:
        underv_ps_i_ar, underv_ps_nasta = result_ps_underv
        st.write(f"**Undervärdering P/S:** {underv_ps_i_ar:.0f}% / {underv_ps_nasta:.0f}%")
    else:
        st.warning("⚠️ Kunde inte räkna ut undervärdering för P/S.")

    # Köpvärda nivåer med säkerhetsmarginal (-30%)
    st.markdown("### 💰 Köpvärd nivå (-30%)")
    if target_pe_i_ar:
        st.write(f"- P/E i år: {target_pe_i_ar * 0.7:.1f} kr")
    if target_pe_nasta:
        st.write(f"- P/E nästa år: {target_pe_nasta * 0.7:.1f} kr")
    if target_ps_i_ar:
        st.write(f"- P/S i år: {target_ps_i_ar * 0.7:.1f} kr")
    if target_ps_nasta:
        st.write(f"- P/S nästa år: {target_ps_nasta * 0.7:.1f} kr")
