import streamlit as st
from data_handler import load_data, save_data

def nytt_bolag_form():
    st.header("Lägg till nytt bolag")

    with st.form("nytt_bolag_form", clear_on_submit=True):
        namn = st.text_input("Bolagsnamn").strip()
        nuvarande_kurs = st.number_input("Nuvarande kurs (kr)", min_value=0.0, format="%.2f")
        # Här kan du lägga till fler fält enligt din datastruktur...

        submitted = st.form_submit_button("Lägg till bolag")

    if submitted:
        if not namn:
            st.error("Bolagsnamn måste fyllas i.")
            return

        data = load_data()
        if namn in data:
            st.error(f"Bolaget '{namn}' finns redan. Använd redigeringsfunktionen istället.")
            return

        data[namn] = {
            "nuvarande_kurs": nuvarande_kurs,
            # Lägg till fler fält här...
        }
        save_data(data)
        st.success(f"Bolaget '{namn}' har lagts till.")

def redigera_bolag_form():
    st.header("Redigera befintligt bolag")

    data = load_data()
    if not data:
        st.info("Inga bolag finns att redigera än.")
        return

    bolagslista = list(data.keys())
    valt_bolag = st.selectbox("Välj bolag att redigera", bolagslista)

    if valt_bolag:
        info = data[valt_bolag]

        with st.form("redigera_bolag_form"):
            nuvarande_kurs = st.number_input(
                "Nuvarande kurs (kr)",
                min_value=0.0,
                value=info.get("nuvarande_kurs", 0.0),
                format="%.2f"
            )
            # Lägg till fler fält för redigering här...

            submitted = st.form_submit_button("Uppdatera bolag")

        if submitted:
            data[valt_bolag]["nuvarande_kurs"] = nuvarande_kurs
            # Uppdatera fler fält här...

            save_data(data)
            st.success(f"Bolaget '{valt_bolag}' har uppdaterats.")

def main():
    st.title("Aktieanalysapp")

    meny = ["Visa bolag ett i taget", "Lägg till nytt bolag", "Redigera bolag"]
    val = st.sidebar.selectbox("Välj vy", meny)

    if val == "Visa bolag ett i taget":
        from view import visa_bolag_ett_i_taget
        visa_bolag_ett_i_taget()

    elif val == "Lägg till nytt bolag":
        nytt_bolag_form()

    elif val == "Redigera bolag":
        redigera_bolag_form()

if __name__ == "__main__":
    main()
