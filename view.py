import streamlit as st
from utils import berakna_targetkurser_och_undervardering

def visa_bolag(data):
    st.header("📈 Mina sparade bolag")
    st.markdown("##### Debug – inläst data från data.json")
    st.json(data)

    if not data:
        st.info("Ingen data sparad ännu.")
        return

    for namn, info in data.items():
        st.subheader(f"📊 {namn}")

        kurs = info.get("kurs", 0.0)
        st.write(f"**Nuvarande kurs:** {kurs:.2f} kr")

        try:
            resultat = berakna_targetkurser_och_undervardering(info)
        except Exception as e:
            st.error(f"Kunde inte beräkna för {namn}: {e}")
            continue

        st.write(f"🎯 **Targetkurs P/E (i år):** {resultat['target_pe_iar']:.2f} kr")
        st.write(f"🎯 **Targetkurs P/E (nästa år):** {resultat['target_pe_nasta_ar']:.2f} kr")
        st.write(f"🎯 **Targetkurs P/S (i år):** {resultat['target_ps_iar']:.2f} kr")
        st.write(f"🎯 **Targetkurs P/S (nästa år):** {resultat['target_ps_nasta_ar']:.2f} kr")

        undervardering = resultat["undervardering_procent"]
        undervardering_str = f"{undervardering:.1f} %"
        if undervardering >= 30:
            st.success(f"📉 **Undervärdering (max av P/E och P/S): {undervardering_str}**")
        elif undervardering > 0:
            st.warning(f"📉 **Undervärdering (max av P/E och P/S): {undervardering_str}**")
        else:
            st.error(f"📉 **Övervärdering: {undervardering_str}**")
