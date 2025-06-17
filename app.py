import streamlit as st
from data_handler import load_data
from view import visa_alla_bolag, visa_ett_bolag

def main():
    st.set_page_config(page_title="Aktieanalys", layout="centered")
    st.title("📈 Enkel riktkursräknare")

    # Ladda data
    data = load_data()

    # Visa alla sparade bolag i JSON-format
    visa_alla_bolag(data)

    # Visa enskilt bolag via rullista
    if data:
        st.subheader("Välj ett bolag att visa")
        valt_bolag = st.selectbox("Bolag", list(data.keys()), index=0)
        visa_ett_bolag(data, valt_bolag)
    else:
        st.info("Ingen data tillgänglig att visa.")

if __name__ == "__main__":
    main()
