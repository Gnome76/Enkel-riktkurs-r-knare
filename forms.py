import streamlit as st

def nytt_bolag_formular(data, on_submit):
    with st.form(key="nytt_bolag_form"):
        bolagsnamn = st.text_input("Bolagsnamn")
        nuvarande_kurs = st.number_input("Nuvarande kurs (kr)", min_value=0.0, format="%.2f")
        
        # P/E
        nuvarande_pe = st.number_input("Nuvarande P/E", min_value=0.0, format="%.2f")
        pe1 = st.number_input("P/E 1", min_value=0.0, format="%.2f")
        pe2 = st.number_input("P/E 2", min_value=0.0, format="%.2f")
        pe3 = st.number_input("P/E 3", min_value=0.0, format="%.2f")
        pe4 = st.number_input("P/E 4", min_value=0.0, format="%.2f")
        
        # P/S
        nuvarande_ps = st.number_input("Nuvarande P/S", min_value=0.0, format="%.2f")
        ps1 = st.number_input("P/S 1", min_value=0.0, format="%.2f")
        ps2 = st.number_input("P/S 2", min_value=0.0, format="%.2f")
        ps3 = st.number_input("P/S 3", min_value=0.0, format="%.2f")
        ps4 = st.number_input("P/S 4", min_value=0.0, format="%.2f")
        
        # Vinst
        vinst_ar = st.number_input("Vinst i år", format="%.2f")
        vinst_nasta_ar = st.number_input("Vinst nästa år", format="%.2f")
        
        # Omsättningstillväxt i %
        oms_tillv_ar = st.number_input("Omsättningstillväxt i år (%)", format="%.2f")
        oms_tillv_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", format="%.2f")
        
        submit = st.form_submit_button("Lägg till bolag")
        
        if submit:
            ny_data = {
                "bolagsnamn": bolagsnamn,
                "nuvarande_kurs": nuvarande_kurs,
                "nuvarande_pe": nuvarande_pe,
                "pe1": pe1,
                "pe2": pe2,
                "pe3": pe3,
                "pe4": pe4,
                "nuvarande_ps": nuvarande_ps,
                "ps1": ps1,
                "ps2": ps2,
                "ps3": ps3,
                "ps4": ps4,
                "vinst_ar": vinst_ar,
                "vinst_nasta_ar": vinst_nasta_ar,
                "oms_tillv_ar": oms_tillv_ar,
                "oms_tillv_nasta_ar": oms_tillv_nasta_ar,
            }
            on_submit(ny_data)


def redigeringsformular(data, valt_bolag, on_submit):
    if valt_bolag not in data:
        st.warning("Bolaget finns inte att redigera.")
        return

    info = data[valt_bolag]

    with st.form(key=f"redigera_form_{valt_bolag}"):
        bolagsnamn = st.text_input("Bolagsnamn", value=valt_bolag)
        nuvarande_kurs = st.number_input("Nuvarande kurs (kr)", min_value=0.0, format="%.2f", value=info.get("nuvarande_kurs", 0.0))
        
        # P/E
        nuvarande_pe = st.number_input("Nuvarande P/E", min_value=0.0, format="%.2f", value=info.get("nuvarande_pe", 0.0))
        pe1 = st.number_input("P/E 1", min_value=0.0, format="%.2f", value=info.get("pe1", 0.0))
        pe2 = st.number_input("P/E 2", min_value=0.0, format="%.2f", value=info.get("pe2", 0.0))
        pe3 = st.number_input("P/E 3", min_value=0.0, format="%.2f", value=info.get("pe3", 0.0))
        pe4 = st.number_input("P/E 4", min_value=0.0, format="%.2f", value=info.get("pe4", 0.0))
        
        # P/S
        nuvarande_ps = st.number_input("Nuvarande P/S", min_value=0.0, format="%.2f", value=info.get("nuvarande_ps", 0.0))
        ps1 = st.number_input("P/S 1", min_value=0.0, format="%.2f", value=info.get("ps1", 0.0))
        ps2 = st.number_input("P/S 2", min_value=0.0, format="%.2f", value=info.get("ps2", 0.0))
        ps3 = st.number_input("P/S 3", min_value=0.0, format="%.2f", value=info.get("ps3", 0.0))
        ps4 = st.number_input("P/S 4", min_value=0.0, format="%.2f", value=info.get("ps4", 0.0))
        
        # Vinst
        vinst_ar = st.number_input("Vinst i år", format="%.2f", value=info.get("vinst_ar", 0.0))
        vinst_nasta_ar = st.number_input("Vinst nästa år", format="%.2f", value=info.get("vinst_nasta_ar", 0.0))
        
        # Omsättningstillväxt i %
        oms_tillv_ar = st.number_input("Omsättningstillväxt i år (%)", format="%.2f", value=info.get("oms_tillv_ar", 0.0))
        oms_tillv_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", format="%.2f", value=info.get("oms_tillv_nasta_ar", 0.0))
        
        submit = st.form_submit_button("Uppdatera bolag")
        
        if submit:
            ny_data = {
                "bolagsnamn": bolagsnamn,
                "nuvarande_kurs": nuvarande_kurs,
                "nuvarande_pe": nuvarande_pe,
                "pe1": pe1,
                "pe2": pe2,
                "pe3": pe3,
                "pe4": pe4,
                "nuvarande_ps": nuvarande_ps,
                "ps1": ps1,
                "ps2": ps2,
                "ps3": ps3,
                "ps4": ps4,
                "vinst_ar": vinst_ar,
                "vinst_nasta_ar": vinst_nasta_ar,
                "oms_tillv_ar": oms_tillv_ar,
                "oms_tillv_nasta_ar": oms_tillv_nasta_ar,
            }
            on_submit(valt_bolag, ny_data)
