import streamlit as st
from google_sheets_handler import load_data, save_data

def main():
    st.title("Bolag - Läsa och Spara med Google Sheets")

    sheet, data = load_data()

    # Visa befintliga bolag
    st.subheader("Sparade bolag")
    if data:
        for i, bolag in enumerate(data):
            st.write(f"{i+1}. {bolag}")
    else:
        st.write("Inga bolag sparade ännu.")

    # Lägg till nytt bolag
    st.subheader("Lägg till nytt bolag")
    with st.form("nytt_bolag_form"):
        namn = st.text_input("Bolagsnamn")
        kurs = st.number_input("Kurs", min_value=0.0, format="%.4f")
        pe_nuvarande = st.number_input("P/E nuvarande", min_value=0.0, format="%.4f")
        # Du kan lägga till fler fält efter behov här...
        submitted = st.form_submit_button("Lägg till bolag")

    if submitted:
        nytt_bolag = {
            "namn": namn,
            "kurs": kurs,
            "pe_nuvarande": pe_nuvarande
            # fler fält...
        }
        data.append(nytt_bolag)
        save_data(sheet, data)
        st.success(f"Bolaget {namn} sparades!")
        st.experimental_rerun()

if __name__ == "__main__":
    main()
