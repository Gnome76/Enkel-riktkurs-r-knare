import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "bolag_data.json"

# Initiera refresh-flagga för uppdatering i appen
if "refresh" not in st.session_state:
    st.session_state["refresh"] = False

# Hantera refresh-trigger
if st.session_state.get("refresh", False):
    st.session_state["refresh"] = False
    # Streamlit Cloud kan ha begränsningar, men vi försöker med omstart
    st.experimental_rerun()

# Läs in data från fil eller initiera tom lista i session_state
if "bolag_lista" not in st.session_state:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            st.session_state["bolag_lista"] = json.load(f)
    else:
        st.session_state["bolag_lista"] = []

bolag_lista = st.session_state["bolag_lista"]

def spara_data():
    # Spara i session_state och till fil
    st.session_state["bolag_lista"] = bolag_lista
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(bolag_lista, f, ensure_ascii=False, indent=2)


def berakna_targetkurs_pe(vinst_aar, pe_varden):
    # pe_varden är lista med P/E 1-4
    pe_snitt = sum(pe_varden) / len(pe_varden)
    target = pe_snitt * vinst_aar * 0.9  # säkerhetsmarginal 10%
    return target


def berakna_targetkurs_ps(nuvarande_ps, ps_varden, omsattningstillvaxt_aar, omsattningstillvaxt_nasta_aar, nuvarande_kurs):
    ps_snitt = sum(ps_varden) / len(ps_varden)
    # Targetkurs beräknas baserat på omsättningstillväxt och P/S
    target_i_aar = ps_snitt * omsattningstillvaxt_aar / nuvarande_ps * nuvarande_kurs * 0.9
    target_nasta_aar = ps_snitt * omsattningstillvaxt_aar * omsattningstillvaxt_nasta_aar / nuvarande_ps * nuvarande_kurs * 0.9
    return target_i_aar, target_nasta_aar


def berakna_undervaerdering(nuvarande_kurs, targetkurs):
    # % undervärdering = (targetkurs - kurs) / kurs * 100
    return round((targetkurs - nuvarande_kurs) / nuvarande_kurs * 100, 1)

st.title("Enkel Aktieanalysapp - Streamlit Cloud-anpassad")

menu = st.sidebar.selectbox("Välj vy", ["Visa alla bolag", "Lägg till nytt bolag", "Redigera bolag", "Ta bort bolag"])

if menu == "Visa alla bolag":
    if not bolag_lista:
        st.info("Ingen data tillgänglig. Lägg till bolag först.")
    else:
        # Visa checkbox för filtrering undervärderade > 30%
        visa_endast_undervarderade = st.checkbox("Visa endast undervärderade bolag (minst 30% rabatt)", value=False)

        # Bygg visningslista
        visningslista = []
        for bolag in bolag_lista:
            # Läs in värden
            try:
                vinst_aar = float(bolag.get("vinst_aar", 0))
                vinst_nasta_aar = float(bolag.get("vinst_nasta_aar", 0))
                nuvarande_kurs = float(bolag.get("nuvarande_kurs", 0))
                nuvarande_ps = float(bolag.get("nuvarande_ps", 1))
                oms_tillvaxt_aar = float(bolag.get("oms_tillvaxt_aar", 1))
                oms_tillvaxt_nasta_aar = float(bolag.get("oms_tillvaxt_nasta_aar", 1))
                pe_varden = [float(bolag.get(f"pe{i}", 0)) for i in range(1,5)]
                ps_varden = [float(bolag.get(f"ps{i}", 0)) for i in range(1,5)]

                target_pe_aar = berakna_targetkurs_pe(vinst_aar, pe_varden)
                target_pe_nasta_aar = berakna_targetkurs_pe(vinst_nasta_aar, pe_varden)
                target_ps_aar, target_ps_nasta_aar = berakna_targetkurs_ps(nuvarande_ps, ps_varden, oms_tillvaxt_aar, oms_tillvaxt_nasta_aar, nuvarande_kurs)

                undervardering_pe_aar = berakna_undervaerdering(nuvarande_kurs, target_pe_aar)
                undervardering_pe_nasta_aar = berakna_undervaerdering(nuvarande_kurs, target_pe_nasta_aar)
                undervardering_ps_aar = berakna_undervaerdering(nuvarande_kurs, target_ps_aar)
                undervardering_ps_nasta_aar = berakna_undervaerdering(nuvarande_kurs, target_ps_nasta_aar)

                undervardering_max = max(undervardering_pe_aar, undervardering_pe_nasta_aar, undervardering_ps_aar, undervardering_ps_nasta_aar)
            except Exception as e:
                st.error(f"Fel i data för {bolag.get('namn', 'okänt bolag')}: {e}")
                continue

            # Filtrera om checkbox är ikryssad
            if visa_endast_undervarderade and undervardering_max < 30:
                continue

            visningslista.append({
                "namn": bolag.get("namn", ""),
                "nuvarande_kurs": nuvarande_kurs,
                "target_pe_aar": target_pe_aar,
                "target_pe_nasta_aar": target_pe_nasta_aar,
                "target_ps_aar": target_ps_aar,
                "target_ps_nasta_aar": target_ps_nasta_aar,
                "undervardering_pe_aar": undervardering_pe_aar,
                "undervardering_pe_nasta_aar": undervardering_pe_nasta_aar,
                "undervardering_ps_aar": undervardering_ps_aar,
                "undervardering_ps_nasta_aar": undervardering_ps_nasta_aar,
                "undervardering_max": undervardering_max,
            })

        # Sortera efter max undervärdering, fallande
        visningslista = sorted(visningslista, key=lambda x: x["undervardering_max"], reverse=True)

        if not visningslista:
            st.info("Inga bolag matchar filtret.")
        else:
            # Visa tabell
            import pandas as pd
            df = pd.DataFrame(visningslista)
            st.dataframe(df.style.format({
                "nuvarande_kurs": "{:.2f}",
                "target_pe_aar": "{:.2f}",
                "target_pe_nasta_aar": "{:.2f}",
                "target_ps_aar": "{:.2f}",
                "target_ps_nasta_aar": "{:.2f}",
                "undervardering_pe_aar": "{:.1f}%",
                "undervardering_pe_nasta_aar": "{:.1f}%",
                "undervardering_ps_aar": "{:.1f}%",
                "undervardering_ps_nasta_aar": "{:.1f}%",
                "undervardering_max": "{:.1f}%",
            }))

if menu == "Lägg till nytt bolag":
    with st.form(key="form_lagg_till_nytt", clear_on_submit=True):
        namn = st.text_input("Bolagsnamn", key="nytt_namn")
        nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f", key="ny_kurs")
        vinst_aar = st.number_input("Vinst i år", format="%.2f", key="ny_vinst_aar")
        vinst_nasta_aar = st.number_input("Vinst nästa år", format="%.2f", key="ny_vinst_nasta_aar")
        oms_tillvaxt_aar = st.number_input("Omsättningstillväxt i år (decimal, t.ex. 1.05 = 5%)", min_value=0.0, value=1.0, format="%.3f", key="ny_oms_tillvaxt_aar")
        oms_tillvaxt_nasta_aar = st.number_input("Omsättningstillväxt nästa år (decimal)", min_value=0.0, value=1.0, format="%.3f", key="ny_oms_tillvaxt_nasta_aar")
        nuvarande_ps = st.number_input("Nuvarande P/S", min_value=0.0, format="%.2f", key="ny_nuvarande_ps")

        pe1 = st.number_input("P/E 1", min_value=0.0, format="%.2f", key="ny_pe1")
        pe2 = st.number_input("P/E 2", min_value=0.0, format="%.2f", key="ny_pe2")
        pe3 = st.number_input("P/E 3", min_value=0.0, format="%.2f", key="ny_pe3")
        pe4 = st.number_input("P/E 4", min_value=0.0, format="%.2f", key="ny_pe4")

        ps1 = st.number_input("P/S 1", min_value=0.0, format="%.2f", key="ny_ps1")
        ps2 = st.number_input("P/S 2", min_value=0.0, format="%.2f", key="ny_ps2")
        ps3 = st.number_input("P/S 3", min_value=0.0, format="%.2f", key="ny_ps3")
        ps4 = st.number_input("P/S 4", min_value=0.0, format="%.2f", key="ny_ps4")

        submitted = st.form_submit_button("Spara nytt bolag")

    if submitted:
        nytt_bolag = {
            "namn": namn,
            "nuvarande_kurs": nuvarande_kurs,
            "vinst_aar": vinst_aar,
            "vinst_nasta_aar": vinst_nasta_aar,
            "oms_tillvaxt_aar": oms_tillvaxt_aar,
            "oms_tillvaxt_nasta_aar": oms_tillvaxt_nasta_aar,
            "nuvarande_ps": nuvarande_ps,
            "pe1": pe1,
            "pe2": pe2,
            "pe3": pe3,
            "pe4": pe4,
            "ps1": ps1,
            "ps2": ps2,
            "ps3": ps3,
            "ps4": ps4,
            "insatt_datum": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "senast_andrad": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        bolag_lista.append(nytt_bolag)
        spara_data()
        st.success(f"Bolag '{namn}' sparat!")
        st.session_state["refresh"] = True
        st.stop()

if menu == "Redigera bolag":
    if not bolag_lista:
        st.info("Ingen data tillgänglig att redigera.")
    else:
        namn_vald = st.selectbox("Välj bolag att redigera", [b["namn"] for b in bolag_lista], key="redigera_val")
        bolag = next((b for b in bolag_lista if b["namn"] == namn_vald), None)
        if bolag:
            with st.form(key="form_redigera_bolag", clear_on_submit=False):
                # Visa fält med nuvarande värden för redigering
                namn = st.text_input("Bolagsnamn", value=bolag.get("namn", ""), key="edit_namn")
                nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f", value=bolag.get("nuvarande_kurs", 0.0), key="edit_kurs")
                vinst_aar = st.number_input("Vinst i år", format="%.2f", value=bolag.get("vinst_aar", 0.0), key="edit_vinst_aar")
                vinst_nasta_aar = st.number_input("Vinst nästa år", format="%.2f", value=bolag.get("vinst_nasta_aar", 0.0), key="edit_vinst_nasta_aar")
                oms_tillvaxt_aar = st.number_input("Omsättningstillväxt i år (decimal)", min_value=0.0, value=bolag.get("oms_tillvaxt_aar", 1.0), format="%.3f", key="edit_oms_tillvaxt_aar")
                oms_tillvaxt_nasta_aar = st.number_input("Omsättningstillväxt nästa år (decimal)", min_value=0.0, value=bolag.get("oms_tillvaxt_nasta_aar", 1.0), format="%.3f", key="edit_oms_tillvaxt_nasta_aar")
                nuvarande_ps = st.number_input("Nuvarande P/S", min_value=0.0, format="%.2f", value=bolag.get("nuvarande_ps", 0.0), key="edit_nuvarande_ps")

                pe1 = st.number_input("P/E 1", min_value=0.0, format="%.2f", value=bolag.get("pe1", 0.0), key="edit_pe1")
                pe2 = st.number_input("P/E 2", min_value=0.0, format="%.2f", value=bolag.get("pe2", 0.0), key="edit_pe2")
                pe3 = st.number_input("P/E 3", min_value=0.0, format="%.2f", value=bolag.get("pe3", 0.0), key="edit_pe3")
                pe4 = st.number_input("P/E 4", min_value=0.0, format="%.2f", value=bolag.get("pe4", 0.0), key="edit_pe4")

                ps1 = st.number_input("P/S 1", min_value=0.0, format="%.2f", value=bolag.get("ps1", 0.0), key="edit_ps1")
                ps2 = st.number_input("P/S 2", min_value=0.0, format="%.2f", value=bolag.get("ps2", 0.0), key="edit_ps2")
                ps3 = st.number_input("P/S 3", min_value=0.0, format="%.2f", value=bolag.get("ps3", 0.0), key="edit_ps3")
                ps4 = st.number_input("P/S 4", min_value=0.0, format="%.2f", value=bolag.get("ps4", 0.0), key="edit_ps4")

                submitted = st.form_submit_button("Uppdatera bolag")

            if submitted:
                # Uppdatera bolagets data i listan
                bolag["namn"] = namn
                bolag["nuvarande_kurs"] = nuvarande_kurs
                bolag["vinst_aar"] = vinst_aar
                bolag["vinst_nasta_aar"] = vinst_nasta_aar
                bolag["oms_tillvaxt_aar"] = oms_tillvaxt_aar
                bolag["oms_tillvaxt_nasta_aar"] = oms_tillvaxt_nasta_aar
                bolag["nuvarande_ps"] = nuvarande_ps
                bolag["pe1"] = pe1
                bolag["pe2"] = pe2
                bolag["pe3"] = pe3
                bolag["pe4"] = pe4
                bolag["ps1"] = ps1
                bolag["ps2"] = ps2
                bolag["ps3"] = ps3
                bolag["ps4"] = ps4
                bolag["senast_andrad"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                spara_data()
                st.success(f"Bolaget '{namn}' har uppdaterats.")
                st.session_state["refresh"] = True
                st.stop()
