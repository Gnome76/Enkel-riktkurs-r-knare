import streamlit as st
from data_handler import load_data, save_data
from forms import nytt_bolag_formular, redigeringsformular
from view import visa_bolag_ett_i_taget
from utils import beräkna_targetkurser, beräkna_undervärdering

st.set_page_config(page_title="Enkel riktkursräknare", layout="centered")

st.title("📈 Enkel riktkursräknare")

# Ladda data
data = load_data()

# Om datan är None eller inte en dict, återställ till tom
if not isinstance(data, dict):
    st.warning("❗ Databasen kunde inte läsas korrekt. Startar med tom databas.")
    data = {}

# Välj läge
läge = st.radio("Vad vill du göra?", ["➕ Lägg till nytt bolag", "✏️ Redigera befintligt bolag"])

if läge == "➕ Lägg till nytt bolag":
    nytt_bolag_formular(data)
elif läge == "✏️ Redigera befintligt bolag":
    redigeringsformular(data)

# Spara data om något ändrats (uppdateringar hanteras i formulären)
save_data(data)

# Visa bolag en i taget
st.markdown("---")
visa_bolag_ett_i_taget()
