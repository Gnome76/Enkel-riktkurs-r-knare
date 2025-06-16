import streamlit as st

def nytt_bolag_formular(data):
    st.subheader("Lägg till nytt bolag")

    with st.form(key="nytt_bolag_form"):
        namn = st.text_input("Bolagsnamn")
        kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
        submit = st.form_submit_button("Lägg till")

        if submit:
            if namn.strip() == "":
                st.error("Bolagsnamn får inte vara tomt.")
                return

            # Lägg till bolaget i data-dict
            data[namn] = {
                "namn": namn,
                "nuvarande_kurs": kurs,
            }
            st.success(f"Bolag {namn} tillagt!")

def redigeringsformular(data):
    st.write("Här kommer redigeringsformuläret snart.")
