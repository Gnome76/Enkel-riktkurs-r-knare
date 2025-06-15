import streamlit as st
import json
import os
from datetime import datetime

DATAFIL = "bolag_data.json"

def las_data():
    if not os.path.exists(DATAFIL):
        return []
    try:
        with open(DATAFIL, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def spara_data(data):
    with open(DATAFIL, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

st.set_page_config(page_title="Enkel riktkurs-räknare", layout="centered")

st.title("Enkel riktkurs-räknare")

# Ladda bolagsdata
bolag_list = las_data()

if "bolag_list" not in st.session_state:
    st.session_state.bolag_list = bolag_list

def berakna_targetkurser(bolag):
    # Beräkna medelvärden för P/E och P/S
    pe_varden = [bolag.get(f"pe{i}", None) for i in range(1, 5) if bolag.get(f"pe{i}") is not None]
    ps_varden = [bolag.get(f"ps{i}", None) for i in range(1, 5) if bolag.get(f"ps{i}") is not None]
    
    if pe_varden:
        pe_snitt = sum(pe_varden) / len(pe_varden)
    else:
        pe_snitt = None
    if ps_varden:
        ps_snitt = sum(ps_varden) / len(ps_varden)
    else:
        ps_snitt = None

    vinst_ar = bolag.get("vinst_i_ar")
    vinst_nasta_ar = bolag.get("vinst_nasta_ar")
    oms_tillvxt_ar = bolag.get("omsattningstillvaxt_i_ar")
    oms_tillvxt_nasta_ar = bolag.get("omsattningstillvaxt_nasta_ar")
    nuvarande_kurs = bolag.get("nuvarande_kurs")

    target_pe_i_ar = (pe_snitt * vinst_ar * 0.9) if pe_snitt and vinst_ar else None
    target_pe_nasta_ar = (pe_snitt * vinst_nasta_ar * 0.9) if pe_snitt and vinst_nasta_ar else None
    
    # För target P/S används omsättningstillväxt som faktor
    if ps_snitt and oms_tillvxt_ar and nuvarande_kurs and bolag.get("nuvarande_ps"):
        target_ps_i_ar = ps_snitt * (1 + oms_tillvxt_ar/100) * nuvarande_kurs * 0.9
    else:
        target_ps_i_ar = None

    if ps_snitt and oms_tillvxt_ar and oms_tillvxt_nasta_ar and nuvarande_kurs and bolag.get("nuvarande_ps"):
        target_ps_nasta_ar = ps_snitt * (1 + oms_tillvxt_ar/100) * (1 + oms_tillvxt_nasta_ar/100) * nuvarande_kurs * 0.9
    else:
        target_ps_nasta_ar = None

    return target_pe_i_ar, target_pe_nasta_ar, target_ps_i_ar, target_ps_nasta_ar


with st.form(key="lagg_till_bolag_form"):
    st.subheader("Lägg till / uppdatera bolag")
    namn = st.text_input("Bolagsnamn").strip()
    nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
    vinst_i_ar = st.number_input("Vinst i år", format="%.2f")
    vinst_nasta_ar = st.number_input("Vinst nästa år", format="%.2f")
    omsattningstillvaxt_i_ar = st.number_input("Omsättningstillväxt i år (%)", format="%.2f")
    omsattningstillvaxt_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", format="%.2f")

    nuvarande_pe = st.number_input("Nuvarande P/E", min_value=0.0, format="%.2f")
    pe1 = st.number_input("P/E 1", min_value=0.0, format="%.2f")
    pe2 = st.number_input("P/E 2", min_value=0.0, format="%.2f")
    pe3 = st.number_input("P/E 3", min_value=0.0, format="%.2f")
    pe4 = st.number_input("P/E 4", min_value=0.0, format="%.2f")

    nuvarande_ps = st.number_input("Nuvarande P/S", min_value=0.0, format="%.2f")
    ps1 = st.number_input("P/S 1", min_value=0.0, format="%.2f")
    ps2 = st.number_input("P/S 2", min_value=0.0, format="%.2f")
    ps3 = st.number_input("P/S 3", min_value=0.0, format="%.2f")
    ps4 = st.number_input("P/S 4", min_value=0.0, format="%.2f")

    submit = st.form_submit_button("Spara bolag")

    if submit:
        if namn == "":
            st.warning("Ange bolagsnamn.")
        else:
            nytt_bolag = {
                "namn": namn,
                "nuvarande_kurs": nuvarande_kurs,
                "vinst_i_ar": vinst_i_ar,
                "vinst_nasta_ar": vinst_nasta_ar,
                "omsattningstillvaxt_i_ar": omsattningstillvaxt_i_ar,
                "omsattningstillvaxt_nasta_ar": omsattningstillvaxt_nasta_ar,
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
                "insatt_datum": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "senast_andrad": None
            }

            # Kontrollera om bolaget redan finns, uppdatera isf
            idx = next((i for i, b in enumerate(st.session_state.bolag_list) if b["namn"].lower() == namn.lower()), None)
            if idx is not None:
                nytt_bolag["insatt_datum"] = st.session_state.bolag_list[idx]["insatt_datum"]
                nytt_bolag["senast_andrad"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.bolag_list[idx] = nytt_bolag
                st.success(f"Bolaget '{namn}' uppdaterades.")
            else:
                st.session_state.bolag_list.append(nytt_bolag)
                st.success(f"Bolaget '{namn}' tillagt.")

            spara_data(st.session_state.bolag_list)
            st.experimental_rerun()

st.header("Sparade bolag")

if not st.session_state.bolag_list:
    st.info("Inga bolag sparade ännu.")
else:
    # Välj bolag att visa/redigera
    valt_bolag_namn = st.selectbox("Välj bolag att visa/redigera", options=[b["namn"] for b in st.session_state.bolag_list])

    bolag = next((b for b in st.session_state.bolag_list if b["namn"] == valt_bolag_namn), None)
    if bolag:
        target_pe_i_ar, target_pe_nasta_ar, target_ps_i_ar, target_ps_nasta_ar = berakna_targetkurser(bolag)

        # Beräkna undervärdering (i procent) för P/E och P/S
        undervar_pe_i_ar = (1 - bolag["nuvarande_kurs"] / target_pe_i_ar) * 100 if target_pe_i_ar else None
        undervar_pe_nasta_ar = (1 - bolag["nuvarande_kurs"] / target_pe_nasta_ar) * 100 if target_pe_nasta_ar else None
        undervar_ps_i_ar = (1 - bolag["nuvarande_kurs"] / target_ps_i_ar) * 100 if target_ps_i_ar else None
        undervar_ps_nasta_ar = (1 - bolag["nuvarande_kurs"] / target_ps_nasta_ar) * 100 if target_ps_nasta_ar else None

        st.subheader(f"Information för {bolag['namn']}")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Nuvarande kurs:** {bolag['nuvarande_kurs']:.2f}")
            st.markdown(f"**Vinst i år:** {bolag['vinst_i_ar']:.2f}")
            st.markdown(f"**Vinst nästa år:** {bolag['vinst_nasta_ar']:.2f}")
            st.markdown(f"**Omsättningstillväxt i år (%):** {bolag['omsattningstillvaxt_i_ar']:.2f}")
            st.markdown(f"**Omsättningstillväxt nästa år (%):** {bolag['omsattningstillvaxt_nasta_ar']:.2f}")

            st.markdown(f"**Nuvarande P/E:** {bolag['nuvarande_pe']:.2f}")
            st.markdown(f"P/E 1: {bolag['pe1']:.2f}")
            st.markdown(f"P/E 2: {bolag['pe2']:.2f}")
            st.markdown(f"P/E 3: {bolag['pe3']:.2f}")
            st.markdown(f"P/E 4: {bolag['pe4']:.2f}")

        with col2:
            st.markdown(f"**Nuvarande P/S:** {bolag['nuvarande_ps']:.2f}")
            st.markdown(f"P/S 1: {bolag['ps1']:.2f}")
            st.markdown(f"P/S 2: {bolag['ps2']:.2f}")
            st.markdown(f"P/S 3: {bolag['ps3']:.2f}")
            st.markdown(f"P/S 4: {bolag['ps4']:.2f}")

            st.markdown("### Targetkurser och undervärdering")
            st.markdown(f"**Targetkurs P/E (i år):** {target_pe_i_ar:.2f}" if target_pe_i_ar else "Targetkurs P/E (i år): -")
            st.markdown(f"**Targetkurs P/E (nästa år):** {target_pe_nasta_ar:.2f}" if target_pe_nasta_ar else "Targetkurs P/E (nästa år): -")
            st.markdown(f"**Targetkurs P/S (i år):** {target_ps_i_ar:.2f}" if target_ps_i_ar else "Targetkurs P/S (i år): -")
            st.markdown(f"**Targetkurs P/S (nästa år):** {target_ps_nasta_ar:.2f}" if target_ps_nasta_ar else "Targetkurs P/S (nästa år): -")

            st.markdown(f"**Undervärdering P/E (i år):** {undervar_pe_i_ar:.1f}%" if undervar_pe_i_ar is not None else "Undervärdering P/E (i år): -")
            st.markdown(f"**Undervärdering P/E (nästa år):** {undervar_pe_nasta_ar:.1f}%" if undervar_pe_nasta_ar is not None else "Undervärdering P/E (nästa år): -")
            st.markdown(f"**Undervärdering P/S (i år):** {undervar_ps_i_ar:.1f}%" if undervar_ps_i_ar is not None else "Undervärdering P/S (i år): -")
            st.markdown(f"**Undervärdering P/S (nästa år):** {undervar_ps_nasta_ar:.1f}%" if undervar_ps_nasta_ar is not None else "Undervärdering P/S (nästa år): -")

            # Köpvärde med 30% marginal
            if target_pe_i_ar:
                kopvarde_pe = target_pe_i_ar * 0.7
                st.markdown(f"**Köpvärd kurs P/E (i år) med 30% marginal:** {kopvarde_pe:.2f}")
            if target_ps_i_ar:
                kopvarde_ps = target_ps_i_ar * 0.7
                st.markdown(f"**Köpvärd kurs P/S (i år) med 30% marginal:** {kopvarde_ps:.2f}")

        # Borttagning av bolag
        if st.button(f"Ta bort bolag '{bolag['namn']}'"):
            st.session_state.bolag_list = [b for b in st.session_state.bolag_list if b["namn"] != bolag["namn"]]
            spara_data(st.session_state.bolag_list)
            st.success(f"Bolaget '{bolag['namn']}' togs bort.")
            st.experimental_rerun()

st.header("Undervärderade bolag")

def hogsta_undervardering(bolag):
    target_pe_i_ar, target_pe_nasta_ar, target_ps_i_ar, target_ps_nasta_ar = berakna_targetkurser(bolag)
    nuv_kurs = bolag["nuvarande_kurs"]
    undervar_pe_i_ar = (1 - nuv_kurs / target_pe_i_ar) if target_pe_i_ar else 0
    undervar_pe_nasta_ar = (1 - nuv_kurs / target_pe_nasta_ar) if target_pe_nasta_ar else 0
    undervar_ps_i_ar = (1 - nuv_kurs / target_ps_i_ar) if target_ps_i_ar else 0
    undervar_ps_nasta_ar = (1 - nuv_kurs / target_ps_nasta_ar) if target_ps_nasta_ar else 0
    return max(undervar_pe_i_ar, undervar_pe_nasta_ar, undervar_ps_i_ar, undervar_ps_nasta_ar)

visa_undervardade_endast = st.checkbox("Visa endast bolag med minst 30% undervärdering", value=False)

# Skapa lista med bolag och beräkningar
visningslista = []
for b in st.session_state.bolag_list:
    target_pe_i_ar, target_pe_nasta_ar, target_ps_i_ar, target_ps_nasta_ar = berakna_targetkurser(b)
    nuv_kurs = b["nuvarande_kurs"]

    undervar_pe_i_ar = (1 - nuv_kurs / target_pe_i_ar) * 100 if target_pe_i_ar else None
    undervar_pe_nasta_ar = (1 - nuv_kurs / target_pe_nasta_ar) * 100 if target_pe_nasta_ar else None
    undervar_ps_i_ar = (1 - nuv_kurs / target_ps_i_ar) * 100 if target_ps_i_ar else None
    undervar_ps_nasta_ar = (1 - nuv_kurs / target_ps_nasta_ar) * 100 if target_ps_nasta_ar else None

    max_undervar = max(
        undervar_pe_i_ar or 0,
        undervar_pe_nasta_ar or 0,
        undervar_ps_i_ar or 0,
        undervar_ps_nasta_ar or 0
    )

    if visa_undervardade_endast and max_undervar < 30:
        continue

    visningslista.append({
        "namn": b["namn"],
        "nuvarande_kurs": nuv_kurs,
        "target_pe_i_ar": target_pe_i_ar,
        "target_pe_nasta_ar": target_pe_nasta_ar,
        "target_ps_i_ar": target_ps_i_ar,
        "target_ps_nasta_ar": target_ps_nasta_ar,
        "max_undervar": max_undervar
    })

# Sortera listan på max undervärdering (störst först)
visningslista.sort(key=lambda x: x["max_undervar"], reverse=True)

if not visningslista:
    st.info("Inga bolag att visa enligt filter.")
else:
    # Visa tabell med viktig info
    import pandas as pd

    df = pd.DataFrame(visningslista)
    df_display = df[["namn", "nuvarande_kurs", "target_pe_i_ar", "target_pe_nasta_ar", "target_ps_i_ar", "target_ps_nasta_ar", "max_undervar"]]
    df_display = df_display.rename(columns={
        "namn": "Bolag",
        "nuvarande_kurs": "Nuvarande kurs",
        "target_pe_i_ar": "Targetkurs P/E (i år)",
        "target_pe_nasta_ar": "Targetkurs P/E (nästa år)",
        "target_ps_i_ar": "Targetkurs P/S (i år)",
        "target_ps_nasta_ar": "Targetkurs P/S (nästa år)",
        "max_undervar": "Max undervärdering (%)"
    })
    df_display["Max undervärdering (%)"] = df_display["Max undervärdering (%)"].apply(lambda x: f"{x:.1f} %")
    df_display[["Nuvarande kurs", "Targetkurs P/E (i år)", "Targetkurs P/E (nästa år)", "Targetkurs P/S (i år)", "Targetkurs P/S (nästa år)"]] = \
        df_display[["Nuvarande kurs", "Targetkurs P/E (i år)", "Targetkurs P/E (nästa år)", "Targetkurs P/S (i år)", "Targetkurs P/S (nästa år)"]].round(2)

    st.dataframe(df_display.reset_index(drop=True))

st.header("Lägg till nytt bolag")

with st.form(key="lagg_till_bolag_form"):
    namn = st.text_input("Bolagsnamn", max_chars=50)
    nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
    vinst_i_ar = st.number_input("Vinst i år", format="%.2f")
    vinst_nasta_ar = st.number_input("Vinst nästa år", format="%.2f")
    omsattningstillvaxt_i_ar = st.number_input("Omsättningstillväxt i år (%)", min_value=0.0, format="%.2f")
    omsattningstillvaxt_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", min_value=0.0, format="%.2f")
    nuvarande_pe = st.number_input("Nuvarande P/E", min_value=0.0, format="%.2f")
    pe_1 = st.number_input("P/E 1", min_value=0.0, format="%.2f")
    pe_2 = st.number_input("P/E 2", min_value=0.0, format="%.2f")
    pe_3 = st.number_input("P/E 3", min_value=0.0, format="%.2f")
    pe_4 = st.number_input("P/E 4", min_value=0.0, format="%.2f")
    nuvarande_ps = st.number_input("Nuvarande P/S", min_value=0.0, format="%.2f")
    ps_1 = st.number_input("P/S 1", min_value=0.0, format="%.2f")
    ps_2 = st.number_input("P/S 2", min_value=0.0, format="%.2f")
    ps_3 = st.number_input("P/S 3", min_value=0.0, format="%.2f")
    ps_4 = st.number_input("P/S 4", min_value=0.0, format="%.2f")

    lagg_till = st.form_submit_button("Lägg till bolag")

if lagg_till:
    nytt_bolag = {
        "namn": namn,
        "nuvarande_kurs": nuvarande_kurs,
        "vinst_i_ar": vinst_i_ar,
        "vinst_nasta_ar": vinst_nasta_ar,
        "omsattningstillvaxt_i_ar": omsattningstillvaxt_i_ar,
        "omsattningstillvaxt_nasta_ar": omsattningstillvaxt_nasta_ar,
        "nuvarande_pe": nuvarande_pe,
        "pe_1": pe_1,
        "pe_2": pe_2,
        "pe_3": pe_3,
        "pe_4": pe_4,
        "nuvarande_ps": nuvarande_ps,
        "ps_1": ps_1,
        "ps_2": ps_2,
        "ps_3": ps_3,
        "ps_4": ps_4,
    }
    st.session_state.bolag_list.append(nytt_bolag)
    spara_data(st.session_state.bolag_list)
    st.success(f"Bolaget '{namn}' har lagts till!")
    st.experimental_rerun()
