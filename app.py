import streamlit as st
import json
import os
from datetime import datetime

DATA_PATH = "bolag_data.json"

# --- Funktioner för att läsa och spara data ---

def las_data():
    if not os.path.exists(DATA_PATH):
        return []
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                return []
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def spara_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# --- Initiera session_state med bolagslista ---

if "bolag_list" not in st.session_state:
    st.session_state.bolag_list = las_data()

# --- Hjälpfunktion för att hitta bolag i listan ---

def hitta_bolag(namn):
    for bolag in st.session_state.bolag_list:
        if bolag["namn"].lower() == namn.lower():
            return bolag
    return None

st.title("Aktieanalys - Riktkurser och Undervärdering")

# --- Form för att lägga till nytt bolag ---

with st.expander("Lägg till nytt bolag"):
    with st.form(key="form_lagg_till"):
        namn = st.text_input("Bolagsnamn", key="nytt_namn")
        kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f", key="ny_kurs")

        vinst_forra_aret = st.number_input("Vinst förra året", format="%.2f", key="vinst_fj")
        vinst_i_ar = st.number_input("Förväntad vinst i år", format="%.2f", key="vinst_i_ar")
        vinst_nasta_ar = st.number_input("Förväntad vinst nästa år", format="%.2f", key="vinst_nasta_ar")

        omsattning_forra_aret = st.number_input("Omsättning förra året", format="%.2f", key="oms_fj")
        omsattningstillvaxt_ar = st.number_input("Omsättningstillväxt i år (%)", format="%.2f", key="oms_tillvaxt_ar")
        omsattningstillvaxt_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", format="%.2f", key="oms_tillvaxt_nasta_ar")

        nuvarande_pe = st.number_input("Nuvarande P/E", min_value=0.0, format="%.2f", key="nuvarande_pe")

        pe1 = st.number_input("P/E 1", min_value=0.0, format="%.2f", key="pe1")
        pe2 = st.number_input("P/E 2", min_value=0.0, format="%.2f", key="pe2")
        pe3 = st.number_input("P/E 3", min_value=0.0, format="%.2f", key="pe3")
        pe4 = st.number_input("P/E 4", min_value=0.0, format="%.2f", key="pe4")

        nuvarande_ps = st.number_input("Nuvarande P/S", min_value=0.0, format="%.2f", key="nuvarande_ps")

        ps1 = st.number_input("P/S 1", min_value=0.0, format="%.2f", key="ps1")
        ps2 = st.number_input("P/S 2", min_value=0.0, format="%.2f", key="ps2")
        ps3 = st.number_input("P/S 3", min_value=0.0, format="%.2f", key="ps3")
        ps4 = st.number_input("P/S 4", min_value=0.0, format="%.2f", key="ps4")

        submit = st.form_submit_button("Lägg till bolag")

        if submit:
            if namn.strip() == "":
                st.error("Ange ett bolagsnamn!")
            else:
                # Kolla om bolaget redan finns
                existerande = hitta_bolag(namn)
                if existerande:
                    st.error("Bolaget finns redan, använd redigera.")
                else:
                    nytt_bolag = {
                        "namn": namn.strip(),
                        "kurs": kurs,
                        "vinst_forra_aret": vinst_forra_aret,
                        "vinst_i_ar": vinst_i_ar,
                        "vinst_nasta_ar": vinst_nasta_ar,
                        "omsattning_forra_aret": omsattning_forra_aret,
                        "omsattningstillvaxt_ar": omsattningstillvaxt_ar / 100.0,
                        "omsattningstillvaxt_nasta_ar": omsattningstillvaxt_nasta_ar / 100.0,
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
                        "insatt_datum": datetime.now().isoformat(),
                        "senast_andrad": datetime.now().isoformat(),
                    }
                    st.session_state.bolag_list.append(nytt_bolag)
                    spara_data(st.session_state.bolag_list)
                    st.success(f"Bolag '{namn}' tillagt!")
                    # Rensa formulärfälten (kan sättas i session_state om önskas)

# --- Välj bolag för redigering eller borttagning ---

if len(st.session_state.bolag_list) > 0:
    valt_bolag_namn = st.selectbox("Välj bolag att redigera eller ta bort", options=[b["namn"] for b in st.session_state.bolag_list], key="valt_bolag")

    bolag = hitta_bolag(valt_bolag_namn)
    if bolag:
        with st.expander(f"Redigera bolag: {bolag['namn']}"):
            with st.form(key="form_redigera"):
                kurs = st.number_input("Nuvarande kurs", value=bolag["kurs"], format="%.2f", key="edit_kurs")
                vinst_forra_aret = st.number_input("Vinst förra året", value=bolag["vinst_forra_aret"], format="%.2f", key="edit_vinst_fj")
                vinst_i_ar = st.number_input("Förväntad vinst i år", value=bolag["vinst_i_ar"], format="%.2f", key="edit_vinst_i_ar")
                vinst_nasta_ar = st.number_input("Förväntad vinst nästa år", value=bolag["vinst_nasta_ar"], format="%.2f", key="edit_vinst_nasta_ar")
                omsattning_forra_aret = st.number_input("Omsättning förra året", value=bolag["omsattning_forra_aret"], format="%.2f", key="edit_oms_fj")
                omsattningstillvaxt_ar = st.number_input("Omsättningstillväxt i år (%)", value=bolag["omsattningstillvaxt_ar"] * 100, format="%.2f", key="edit_oms_tillvaxt_ar")
                omsattningstillvaxt_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", value=bolag["omsattningstillvaxt_nasta_ar"] * 100, format="%.2f", key="edit_oms_tillvaxt_nasta_ar")

                nuvarande_pe = st.number_input("Nuvarande P/E", value=bolag["nuvarande_pe"], format="%.2f", key="edit_nuvarande_pe")
                pe1 = st.number_input("P/E 1", value=bolag["pe1"], format="%.2f", key="edit_pe1")
                pe2 = st.number_input("P/E 2", value=bolag["pe2"], format="%.2f", key="edit_pe2")
                pe3 = st.number_input("P/E 3", value=bolag["pe3"], format="%.2f", key="edit_pe3")
                pe4 = st.number_input("P/E 4", value=bolag["pe4"], format="%.2f", key="edit_pe4")

                nuvarande_ps = st.number_input("Nuvarande P/S", value=bolag["nuvarande_ps"], format="%.2f", key="edit_nuvarande_ps")
                ps1 = st.number_input("P/S 1", value=bolag["ps1"], format="%.2f", key="edit_ps1")
                ps2 = st.number_input("P/S 2", value=bolag["ps2"], format="%.2f", key="edit_ps2")
                ps3 = st.number_input("P/S 3", value=bolag["ps3"], format="%.2f", key="edit_ps3")
                ps4 = st.number_input("P/S 4", value=bolag["ps4"], format="%.2f", key="edit_ps4")

                submit_edit = st.form_submit_button("Uppdatera bolag")

                if submit_edit:
                    bolag["kurs"] = kurs
                    bolag["vinst_forra_aret"] = vinst_forra_aret
                    bolag["vinst_i_ar"] = vinst_i_ar
                    bolag["vinst_nasta_ar"] = vinst_nasta_ar
                    bolag["omsattning_forra_aret"] = omsattning_forra_aret
                    bolag["omsattningstillvaxt_ar"] = omsattningstillvaxt_ar / 100.0
                    bolag["omsattningstillvaxt_nasta_ar"] = omsattningstillvaxt_nasta_ar / 100.0
                    bolag["nuvarande_pe"] = nuvarande_pe
                    bolag["pe1"] = pe1
                    bolag["pe2"] = pe2
                    bolag["pe3"] = pe3
                    bolag["pe4"] = pe4
                    bolag["nuvarande_ps"] = nuvarande_ps
                    bolag["ps1"] = ps1
                    bolag["ps2"] = ps2
                    bolag["ps3"] = ps3
                    bolag["ps4"] = ps4
                    bolag["senast_andrad"] = datetime.now().isoformat()
                    spara_data(st.session_state.bolag_list)
                    st.success(f"Bolag '{bolag['namn']}' uppdaterat!")

        # Borttagning av bolag
        if st.button(f"Ta bort bolag '{bolag['namn']}'"):
            st.session_state.bolag_list = [b for b in st.session_state.bolag_list if b["namn"] != bolag["namn"]]
            spara_data(st.session_state.bolag_list)
            st.success(f"Bolag '{bolag['namn']}' borttaget!")
            st.experimental_rerun()

# --- Funktion för beräkningar av targetkurser och undervärdering ---

def berakna_targetkurs_pe(bolag):
    pe_list = [bolag.get(k, 0) for k in ["pe1", "pe2", "pe3", "pe4"] if bolag.get(k, 0) > 0]
    if len(pe_list) == 0:
        return (None, None)
    pe_snitt = sum(pe_list) / len(pe_list)
    target_i_ar = pe_snitt * bolag["vinst_i_ar"] * 0.9  # 10% säkerhetsmarginal
    target_nasta_ar = pe_snitt * bolag["vinst_nasta_ar"] * 0.9
    return target_i_ar, target_nasta_ar

def berakna_targetkurs_ps(bolag):
    ps_list = [bolag.get(k, 0) for k in ["ps1", "ps2", "ps3", "ps4"] if bolag.get(k, 0) > 0]
    if len(ps_list) == 0 or bolag["nuvarande_ps"] == 0:
        return (None, None)
    ps_snitt = sum(ps_list) / len(ps_list)
    oms_tillvaxt_ar = bolag["omsattningstillvaxt_ar"]
    oms_tillvaxt_nasta_ar = bolag["omsattningstillvaxt_nasta_ar"]

    target_i_ar = ps_snitt * (1 + oms_tillvaxt_ar) * bolag["nuvarande_ps"] * bolag["kurs"] * 0.9
    target_nasta_ar = ps_snitt * (1 + oms_tillvaxt_ar) * (1 + oms_tillvaxt_nasta_ar) * bolag["nuvarande_ps"] * bolag["kurs"] * 0.9
    return target_i_ar, target_nasta_ar

def berakna_undervardering(nuvarande_kurs, target_kurs):
    if target_kurs is None or target_kurs == 0:
        return None
    diff = target_kurs - nuvarande_kurs
    return diff / target_kurs * 100

# --- Visa bolagets beräkningar och info ---

if len(st.session_state.bolag_list) > 0:
    st.header("Bolagsinformation och analys")

    # Mobilvy: visa ett bolag i taget med nästa/föregående
    valt_index = st.session_state.get("valda_index", 0)

    col1, col2, col3 = st.columns([1,2,1])
    with col1:
        if st.button("← Föregående"):
            valt_index = (valt_index - 1) % len(st.session_state.bolag_list)
            st.session_state.valda_index = valt_index
            st.experimental_rerun()
    with col3:
        if st.button("Nästa →"):
            valt_index = (valt_index + 1) % len(st.session_state.bolag_list)
            st.session_state.valda_index = valt_index
            st.experimental_rerun()

    bolag = st.session_state.bolag_list[valt_index]

    st.subheader(f"{bolag['namn']}")

    target_pe_i_ar, target_pe_nasta_ar = berakna_targetkurs_pe(bolag)
    target_ps_i_ar, target_ps_nasta_ar = berakna_targetkurs_ps(bolag)

    underv_pe_i_ar = berakna_undervardering(bolag["kurs"], target_pe_i_ar)
    underv_pe_nasta_ar = berakna_undervardering(bolag["kurs"], target_pe_nasta_ar)
    underv_ps_i_ar = berakna_undervardering(bolag["kurs"], target_ps_i_ar)
    underv_ps_nasta_ar = berakna_undervardering(bolag["kurs"], target_ps_nasta_ar)

    def format_pct(x):
        return f"{x:.1f} %" if x is not None else "-"

    st.markdown(f"""
    **Nuvarande kurs:** {bolag['kurs']:.2f}  
    **Targetkurs P/E (i år):** {target_pe_i_ar:.2f if target_pe_i_ar else '-'}  
    **Targetkurs P/E (nästa år):** {target_pe_nasta_ar:.2f if target_pe_nasta_ar else '-'}  
    **Undervärdering P/E (i år):** {format_pct(underv_pe_i_ar)}  
    **Undervärdering P/E (nästa år):** {format_pct(underv_pe_nasta_ar)}  
    **Köpvärd P/E (30% rabatt):** {(target_pe_i_ar * 0.7):.2f if target_pe_i_ar else '-'}  
    ---
    **Targetkurs P/S (i år):** {target_ps_i_ar:.2f if target_ps_i_ar else '-'}  
    **Targetkurs P/S (nästa år):** {target_ps_nasta_ar:.2f if target_ps_nasta_ar else '-'}  
    **Undervärdering P/S (i år):** {format_pct(underv_ps_i_ar)}  
    **Undervärdering P/S (nästa år):** {format_pct(underv_ps_nasta_ar)}  
    **Köpvärd P/S (30% rabatt):** {(target_ps_i_ar * 0.7):.2f if target_ps_i_ar else '-'}  
    """)

else:
    st.info("Inga bolag sparade än. Lägg till bolag ovan.")
