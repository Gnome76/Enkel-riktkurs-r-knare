import streamlit as st

def nytt_bolag_formular(data):
    st.write("### Lägg till nytt bolag (testversion)")
    with st.form(key="nytt_bolag_form"):
        namn = st.text_input("Bolagsnamn")
        submit = st.form_submit_button("Lägg till bolag")
        if submit:
            if namn.strip() == "":
                st.error("Bolagsnamn kan inte vara tomt.")
            else:
                data[namn.strip()] = {"testfält": 1}
                st.success(f"Bolag '{namn}' tillagt (test).")

def redigeringsformular(data):
    st.write("### Redigera bolag (testversion)")
    st.info("Redigeringsfunktionalitet är inte implementerad än.")
