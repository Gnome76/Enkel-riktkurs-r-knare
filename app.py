import streamlit as st
from data_handler import load_data, save_data
from utils import beräkna_targetkurser, beräkna_undervärdering
from forms import nytt_bolag_formular

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

    # Targetkurser P/E
    result_pe = beräkna_targetkurser(info, metod="pe")
    if result_pe:
        target_pe_i_ar, target_pe_nasta = result_pe
        st.write(f"**Targetkurs P/E:** {target_pe_i_ar:.1f} kr / {target_pe_nasta:.1f} kr")
    else:
        target_pe_i_ar = target_pe_nasta = None
        st.warning("⚠️ Kunde inte räkna ut targetkurs för P/E.")

    # Targetkurser P/S
    result_ps = beräkna_targetkurser(info, metod="ps")
    if result_ps:
        target_ps_i_ar, target_ps_nasta = result_ps
        st.write(f"**Targetkurs P/S:** {target_ps_i_ar:.1f} kr / {target_ps_nasta:.1f} kr")
    else:
        target_ps_i_ar = target_ps_nasta = None
        st.warning("⚠️ Kunde inte räkna ut targetkurs för P/S.")

    # Undervärdering P/E
    result_pe_underv = beräkna_undervärdering(info, metod="pe")
    if result_pe_underv:
        underv_pe_i_ar, underv_pe_nasta = result_pe_underv
        st.write(f"**Undervärdering P/E:** {underv_pe_i_ar:.0f}% / {underv_pe_nasta:.0f}%")
    else:
        st.warning("⚠️ Kunde inte räkna ut undervärdering för P/E.")

    # Undervärdering P/S
    result_ps_underv = beräkna_undervärdering(info, metod="ps")
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

def main():
    st.title("Enkel Aktieanalys - Lägg till och Visa Bolag")

    st.header("Lägg till nytt bolag")
    data = load_data()
    nytt_bolag = nytt_bolag_formular(data)

    if nytt_bolag is not None:
        # Spara det nya bolaget i data
        data[nytt_bolag["bolagsnamn"]] = nytt_bolag
        save_data(data)
        st.success(f"Bolaget '{nytt_bolag['bolagsnamn']}' har lagts till.")
        # Sätt index till det nya bolaget så det visas direkt
        st.session_state["val_index"] = list(data.keys()).index(nytt_bolag["bolagsnamn"])

    st.header("Visa bolag ett i taget")
    visa_bolag_ett_i_taget()

if __name__ == "__main__":
    main()
