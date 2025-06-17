import streamlit as st
from data_handler import load_data, save_data
from forms import nytt_bolag_formular, redigeringsformular
from view import visa_bolag_ett_i_taget
import os
import time

def visa_debug_info():
    st.header("🔍 Debug – Sparad data")

    data = load_data()
    st.subheader("📦 Data i bolag_data.json")
    st.json(data)

    try:
        mod_time = os.path.getmtime("bolag_data.json")
        readable_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mod_time))
        st.write(f"🕒 Senast uppdaterad: {readable_time}")
    except Exception as e:
        st.warning("Kunde inte läsa filens ändringstid.")
        st.error(str(e))

    st.write(f"📊 Antal bolag: {len(data)}")

def main():
    data = load_data()

    st.title("📈 Aktieanalysapp")

    meny = st.sidebar.radio("Välj vy", [
        "Visa bolag",
        "Lägg till nytt bolag",
        "Redigera bolag",
        "Debug – Visa sparad data"
    ])

    if meny == "Visa bolag":
        visa_bolag_ett_i_taget(data)
    elif meny == "Lägg till nytt bolag":
        nytt_bolag_formular(data)
    elif meny == "Redigera bolag":
        redigeringsformular(data)
    elif meny == "Debug – Visa sparad data":
        visa_debug_info()

if __name__ == "__main__":
    main()
