import streamlit as st
from data_handler import load_data
from view import visa_bolag

def main():
    st.title("Mina sparade bolag")

    # Ladda data
    data = load_data()
    st.text("Debug – inläst data från data.json")
    st.json(data)

    # Visa bolag
    if data:
        visa_bolag(data)
    else:
        st.write("Ingen data sparad ännu.")

if __name__ == "__main__":
    main()
