import streamlit as st
from data_handler import load_data
from view import visa_alla_bolag, visa_ett_bolag

def main():
    st.set_page_config(page_title="Enkel riktkursräknare", layout="centered")
    st.title("📈 Enkel riktkursräknare")
    
    # Ladda data från JSON
    data = load_data()

    # Visa debug-data
    st.subheader("Debug – inläst data från data.json")
    st.json(data)

    # Menyval
    val = st.radio("Vad vill du göra?", ["Visa alla bolag", "Visa ett bolag"])

    if not data:
        st.warning("Ingen data sparad ännu.")
        return

    if val == "Visa alla bolag":
        visa_alla_bolag(data)
    elif val == "Visa ett bolag":
        bolagslista = list(data.keys())
        valt_bolag = st.selectbox("Välj bolag", bolagslista)
        visa_ett_bolag(data, valt_bolag)

if __name__ == "__main__":
    main()
