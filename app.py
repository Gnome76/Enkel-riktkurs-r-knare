import streamlit as st
from data_handler import load_data

def main():
    st.title("Mina sparade bolag")
    data = load_data()
    
    if data:
        st.json(data)  # Visar hela JSON-datan snyggt
    else:
        st.write("Ingen data sparad ännu.")

if __name__ == "__main__":
    main()
