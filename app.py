import streamlit as st
import json
import os

DATAFIL = "bolag_data.json"

def load_data():
    if os.path.exists(DATAFIL):
        with open(DATAFIL, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def save_data(data):
    with open(DATAFIL, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def lagg_till_bolag_form():
    with st.form(key="lagg_till_bolag_form"):
        namn = st.text_input("Bolagsnamn").strip()
        kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
        vinst_1 = st.number_input("Vinst i år", format="%.2f")
        vinst_2 = st.number_input("Vinst nästa år", format="%.2f")
        oms_tillv_1 = st.number_input("Omsättningstillväxt i år %", format="%.2f")
        oms_tillv_2 = st.number_input("Omsättningstillväxt nästa år %", format="%.2f")
        pe1 = st.number_input("P/E 1", format="%.2f")
        pe2 = st.number_input("P/E 2", format="%.2f")
        pe3 = st.number_input("P/E 3", format="%.2f")
        pe4 = st.number_input("P/E 4", format="%.2f")
        ps1 = st.number_input("P/S 1", format="%.2f")
        ps2 = st.number_input("P/S 2", format="%.2f")
        ps3 = st.number_input("P/S 3", format="%.2f")
        ps4 = st.number_input("P/S 4", format="%.2f")

        skickaknapp = st.form_submit_button("Lägg till bolag")

    if skickaknapp:
        if not namn:
            st.warning("Bolagsnamn får inte vara tomt!")
            return

        if namn in st.session_state.data:
            st.warning("Bolaget finns redan. Använd redigera istället.")
            return

        nytt_bolag = {
            "kurs": kurs,
            "vinst_1": vinst_1,
            "vinst_2": vinst_2,
            "oms_tillv_1": oms_tillv_1,
            "oms_tillv_2": oms_tillv_2,
            "pe1": pe1,
            "pe2": pe2,
            "pe3": pe3,
            "pe4": pe4,
            "ps1": ps1,
            "ps2": ps2,
            "ps3": ps3,
            "ps4": ps4
        }

        st.session_state.data[namn] = nytt_bolag
        save_data(st.session_state.data)
        st.success(f"Bolaget {namn} har lagts till!")

def redigera_bolag_form(data):
    bolag_namn = st.selectbox("Välj bolag att redigera", options=list(data.keys()))
    if bolag_namn:
        bolag = data[bolag_namn]

        with st.form(key="redigera_bolag_form"):
            kurs = st.number_input("Nuvarande kurs", value=bolag.get("kurs", 0.0), format="%.2f")
            vinst_1 = st.number_input("Vinst i år", value=bolag.get("vinst_1", 0.0), format="%.2f")
            vinst_2 = st.number_input("Vinst nästa år", value=bolag.get("vinst_2", 0.0), format="%.2f")
            oms_tillv_1 = st.number_input("Omsättningstillväxt i år %", value=bolag.get("oms_tillv_1", 0.0), format="%.2f")
            oms_tillv_2 = st.number_input("Omsättningstillväxt nästa år %", value=bolag.get("oms_tillv_2", 0.0), format="%.2f")
            pe1 = st.number_input("P/E 1", value=bolag.get("pe1", 0.0), format="%.2f")
            pe2 = st.number_input("P/E 2", value=bolag.get("pe2", 0.0), format="%.2f")
            pe3 = st.number_input("P/E 3", value=bolag.get("pe3", 0.0), format="%.2f")
            pe4 = st.number_input("P/E 4", value=bolag.get("pe4", 0.0), format="%.2f")
            ps1 = st.number_input("P/S 1", value=bolag.get("ps1", 0.0), format="%.2f")
            ps2 = st.number_input("P/S 2", value=bolag.get("ps2", 0.0), format="%.2f")
            ps3 = st.number_input("P/S 3", value=bolag.get("ps3", 0.0), format="%.2f")
            ps4 = st.number_input("P/S 4", value=bolag.get("ps4", 0.0), format="%.2f")

            skickaknapp = st.form_submit_button("Uppdatera bolag")

        if skickaknapp:
            uppdaterat_bolag = {
                "kurs": kurs,
                "vinst_1": vinst_1,
                "vinst_2": vinst_2,
                "oms_tillv_1": oms_tillv_1,
                "oms_tillv_2": oms_tillv_2,
                "pe1": pe1,
                "pe2": pe2,
                "pe3": pe3,
                "pe4": pe4,
                "ps1": ps1,
                "ps2": ps2,
                "ps3": ps3,
                "ps4": ps4
            }
            st.session_state.data[bolag_namn] = uppdaterat_bolag
            save_data(st.session_state.data)
            st.success(f"Bolaget {bolag_namn} har uppdaterats!")

def tabort_bolag_form(data):
    bolag_namn = st.selectbox("Välj bolag att ta bort", options=list(data.keys()))
    if bolag_namn:
        if st.button(f"Ta bort {bolag_namn}"):
            del st.session_state.data[bolag_namn]
            save_data(st.session_state.data)
            st.success(f"Bolaget {bolag_namn} har tagits bort!")

def visa_bolag_ett_i_taget(data):
    bolag_lista = list(data.keys())
    if "index" not in st.session_state:
        st.session_state.index = 0

    kol1, kol2, kol3 = st.columns([1,6,1])

    with kol1:
        if st.button("⬅️ Föregående"):
            st.session_state.index = max(0, st.session_state.index - 1)

    with kol3:
        if st.button("Nästa ➡️"):
            st.session_state.index = min(len(bolag_lista) - 1, st.session_state.index + 1)

    bolag_namn = bolag_lista[st.session_state.index]
    bolag = data[bolag_namn]

    st.markdown(f"### {bolag_namn}")
    st.write(f"**Nuvarande kurs:** {bolag['kurs']:.2f}")
    st.write(f"**Vinst i år:** {bolag['vinst_1']:.2f}")
    st.write(f"**Vinst nästa år:** {bolag['vinst_2']:.2f}")
    st.write(f"**Omsättningstillväxt i år %:** {bolag['oms_tillv_1']:.2f}")
    st.write(f"**Omsättningstillväxt nästa år %:** {bolag['oms_tillv_2']:.2f}")
    st.write(f"P/E 1: {bolag['pe1']:.2f}")
    st.write(f"P/E 2: {bolag['pe2']:.2f}")
    st.write(f"P/E 3: {bolag['pe3']:.2f}")
    st.write(f"P/E 4: {bolag['pe4']:.2f}")
    st.write(f"P/S 1: {bolag['ps1']:.2f}")
    st.write(f"P/S 2: {bolag['ps2']:.2f}")
    st.write(f"P/S 3: {bolag['ps3']:.2f}")
    st.write(f"P/S 4: {bolag['ps4']:.2f}")

def main():
    st.title("Aktieanalysapp med Mobilvy")

    # Initiera data i session_state om den inte finns
    if "data" not in st.session_state:
        st.session_state.data = load_data()

    # Sidval med meny
    menyval = st.sidebar.radio("Välj vy", ["Lägg till bolag", "Redigera bolag", "Ta bort bolag", "Visa bolag ett i taget"])

    if menyval == "Lägg till bolag":
        lagg_till_bolag_form()

    elif menyval == "Redigera bolag":
        if st.session_state.data:
            redigera_bolag_form(st.session_state.data)
        else:
            st.info("Inga bolag att redigera. Lägg till bolag först.")

    elif menyval == "Ta bort bolag":
        if st.session_state.data:
            tabort_bolag_form(st.session_state.data)
        else:
            st.info("Inga bolag att ta bort.")

    elif menyval == "Visa bolag ett i taget":
        if st.session_state.data:
            visa_bolag_ett_i_taget(st.session_state.data)
        else:
            st.info("Inga bolag att visa.")

if __name__ == "__main__":
    main()
