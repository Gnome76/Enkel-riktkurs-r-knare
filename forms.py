import streamlit as st

def nytt_bolag_formular(data):
    st.write("### Lägg till nytt bolag (minimal testversion)")

    with st.form(key="nytt_bolag_form"):
        namn = st.text_input("Bolagsnamn").strip()
        submit = st.form_submit_button("Lägg till bolag")

        if submit:
            if not namn:
                st.error("Bolagsnamn kan inte vara tomt!")
                return
            # Lägg till bolaget i datan
            data[namn] = {"kurs": 0.0}  # Minimal placeholder
            st.success(f"Bolag '{namn}' tillagt!")
            st.write(f"DEBUG: data innehåller nu: {list(data.keys())}")
