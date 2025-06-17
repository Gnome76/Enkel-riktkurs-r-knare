import streamlit as st
from data_handler import load_data, save_data

def main():
    st.title("Mina sparade bolag")

    data = load_data()

    # Felsökning – visa vad som laddats in
    st.subheader("Debug – inläst data från data.json")
    st.json(data)

    st.subheader("Sparade bolag:")
    if not data:
        st.info("Ingen data sparad ännu.")
    else:
        for namn, info in data.items():
            st.markdown(f"### {namn}")
            st.write(info)

if __name__ == "__main__":
    main()
