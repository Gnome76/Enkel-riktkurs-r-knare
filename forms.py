import streamlit as st

def bolag_form(bolag=None, key_prefix="nytt"):
    """
    Visar ett formulär för att lägga till eller redigera ett bolag.

    :param bolag: dict med befintliga data för redigering, eller None för nytt bolag
    :param key_prefix: prefix för Streamlit form keys för att undvika krockar
    :return: dict med ifylld data eller None om formuläret inte skickades
    """
    with st.form(key=f"{key_prefix}_form"):
        namn = st.text_input("Bolagsnamn", value=bolag.get("namn") if bolag else "", key=f"{key_prefix}_namn")
        nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f",
                                         value=bolag.get("nuvarande_kurs", 0.0) if bolag else 0.0, key=f"{key_prefix}_nuvarande_kurs")
        
        # P/E
        nuvarande_pe = st.number_input("Nuvarande P/E", min_value=0.0, format="%.2f",
                                      value=bolag.get("nuvarande_pe", 0.0) if bolag else 0.0, key=f"{key_prefix}_nuvarande_pe")
        pe1 = st.number_input("P/E 1", min_value=0.0, format="%.2f",
                              value=bolag.get("pe1", 0.0) if bolag else 0.0, key=f"{key_prefix}_pe1")
        pe2 = st.number_input("P/E 2", min_value=0.0, format="%.2f",
                              value=bolag.get("pe2", 0.0) if bolag else 0.0, key=f"{key_prefix}_pe2")
        pe3 = st.number_input("P/E 3", min_value=0.0, format="%.2f",
                              value=bolag.get("pe3", 0.0) if bolag else 0.0, key=f"{key_prefix}_pe3")
        pe4 = st.number_input("P/E 4", min_value=0.0, format="%.2f",
                              value=bolag.get("pe4", 0.0) if bolag else 0.0, key=f"{key_prefix}_pe4")

        # P/S
        nuvarande_ps = st.number_input("Nuvarande P/S", min_value=0.0, format="%.2f",
                                      value=bolag.get("nuvarande_ps", 0.0) if bolag else 0.0, key=f"{key_prefix}_nuvarande_ps")
        ps1 = st.number_input("P/S 1", min_value=0.0, format="%.2f",
                              value=bolag.get("ps1", 0.0) if bolag else 0.0, key=f"{key_prefix}_ps1")
        ps2 = st.number_input("P/S 2", min_value=0.0, format="%.2f",
                              value=bolag.get("ps2", 0.0) if bolag else 0.0, key=f"{key_prefix}_ps2")
        ps3 = st.number_input("P/S 3", min_value=0.0, format="%.2f",
                              value=bolag.get("ps3", 0.0) if bolag else 0.0, key=f"{key_prefix}_ps3")
        ps4 = st.number_input("P/S 4", min_value=0.0, format="%.2f",
                              value=bolag.get("ps4", 0.0) if bolag else 0.0, key=f"{key_prefix}_ps4")

        # Vinst och omsättningstillväxt
        vinst_aar = st.number_input("Förväntad vinst i år", format="%.2f",
                                   value=bolag.get("vinst_aar", 0.0) if bolag else 0.0, key=f"{key_prefix}_vinst_aar")
        vinst_nasta_aar = st.number_input("Förväntad vinst nästa år", format="%.2f",
                                          value=bolag.get("vinst_nasta_aar", 0.0) if bolag else 0.0, key=f"{key_prefix}_vinst_nasta_aar")
        omsattningstillvaxt_aar = st.number_input("Omsättningstillväxt i år (%)", format="%.2f",
                                                  value=bolag.get("omsattningstillvaxt_aar", 0.0) if bolag else 0.0, key=f"{key_prefix}_omsattningstillvaxt_aar")
        omsattningstillvaxt_nasta_aar = st.number_input("Omsättningstillväxt nästa år (%)", format="%.2f",
                                                       value=bolag.get("omsattningstillvaxt_nasta_aar", 0.0) if bolag else 0.0, key=f"{key_prefix}_omsattningstillvaxt_nasta_aar")

        submit = st.form_submit_button("Spara")

    if submit:
        return {
            "namn": namn.strip(),
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
            "vinst_aar": vinst_aar,
            "vinst_nasta_aar": vinst_nasta_aar,
            "omsattningstillvaxt_aar": omsattningstillvaxt_aar / 100,  # procentsats till decimal
            "omsattningstillvaxt_nasta_aar": omsattningstillvaxt_nasta_aar / 100,  # procentsats till decimal
        }
    return None
