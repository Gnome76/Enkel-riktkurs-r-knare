import streamlit as st

def main():
    data = load_data()
    st.write("Inläst data:")
    st.json(data)

if __name__ == "__main__":
    main()
