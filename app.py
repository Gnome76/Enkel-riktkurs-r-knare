import streamlit as st
from data_handler import load_data, save_data
from utils import berakna_targetkurser
from forms import visa_inmatningsform

st.set_page_config(page_title="Aktieanalys", layout="centered")
st.title("📈 Aktieanalys – Bläddra bland undervärderade bolag")

# Ladda sparad data
data = load_data()

# Uppdatera beräkningar för alla bolag
for bolag in data:
    beräkningar = berakna_targetkurser(bolag)
    bolag.update(beräkningar)

# Spara igen för att behålla uppdaterade värden
save_data(data)

# Filtrera undervärderade bolag (positiv undervärdering)
undervarderade = [b for b in data if b["undervardering_pct"] > 0]

# Sortera efter target P/E nästa år i förhållande till nuvarande kurs
undervarderade.sort(key=lambda b: ((b["target_pe_nastaar"] - b["nuvarande_kurs"]) / b["nuvarande_kurs"]), reverse=True)

# Sidvisning
if "index" not in st.session_state:
    st.session_state.index = 0

if undervarderade:
    bolag = undervarderade[st.session_state.index]

    st.subheader(f"🔍 {bolag['namn']}")
    st.write(f"**Nuvarande kurs:** {bolag['nuvarande_kurs']} kr")
    st.write(f"**Targetkurs P/E nästa år:** {bolag['target_pe_nastaar']} kr")
    st.write(f"**Undervärdering:** {bolag['undervardering_pct']} %")
    st.write(f"**Köpvärd nivå (30 % rabatt):** {bolag['kopvarde_niva']} kr")

    # Bläddringsknappar
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Föregående") and st.session_state.index > 0:
            st.session_state.index -= 1
    with col2:
        st.write(f"{st.session_state.index + 1} / {len(undervarderade)}")
    with col3:
        if st.button("Nästa ➡️") and st.session_state.index < len(undervarderade) - 1:
            st.session_state.index += 1
else:
    st.warning("Inga undervärderade bolag hittades.")

st.markdown("---")
visa_inmatningsform(data)
