import streamlit as st
from data_handler import load_data, save_data

def main():
    st.title("Bolag Data")

    data = load_data()

    # Enkel inmatning
    namn = st.text_input("Bolagsnamn")
    kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")

    if st.button("Spara bolag"):
        if namn:
            data[namn] = {"kurs": kurs}
            save_data(data)
            st.success(f"Bolag {namn} sparat!")
        else:
            st.error("Ange ett bolagsnamn.")

    # Visa sparade bolag
    st.write("Sparade bolag:")
    st.json(data)

if __name__ == "__main__":
    main()
