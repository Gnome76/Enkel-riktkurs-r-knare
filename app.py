import streamlit as st
import json
import os
from datetime import datetime

DATA_FILE = "bolag_data.json"

def las_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def spara_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Läs in data när appen startar
bolag_list = las_data()

def berakna_targetkurser(bolag):
    # Exempel: snitt av P/E 1-4
    pe_varden = [bolag.get(f"pe{i}", None) for i in range(1, 5)]
    pe_varden = [v for v in pe_varden if v is not None and isinstance(v, (int,float))]
    if len(pe_varden) == 0:
        snitt_pe = 0
    else:
        snitt_pe = sum(pe_varden) / len(pe_varden)
    
    # Targetkurs baserat på vinst i år och nästa år, med 10% säkerhetsmarginal
    vinst_ar = bolag.get("vinst_ar", 0)
    vinst_nasta_ar = bolag.get("vinst_nasta_ar", 0)
    target_pe_ar = snitt_pe * vinst_ar * 0.9
    target_pe_nasta_ar = snitt_pe * vinst_nasta_ar * 0.9

    # Snitt av P/S 1-4
    ps_varden = [bolag.get(f"ps{i}", None) for i in range(1, 5)]
    ps_varden = [v for v in ps_varden if v is not None and isinstance(v, (int,float))]
    if len(ps_varden) == 0:
        snitt_ps = 0
    else:
        snitt_ps = sum(ps_varden) / len(ps_varden)
    
    oms_tillvxt_ar = bolag.get("oms_tillvxt_ar", 0) / 100  # procent -> decimal
    oms_tillvxt_nasta_ar = bolag.get("oms_tillvxt_nasta_ar", 0) / 100

    nuv_ps = bolag.get("ps_nuvarande", 1)
    kurs = bolag.get("kurs", 0)

    target_ps_ar = snitt_ps * oms_tillvxt_ar * kurs * 0.9 if nuv_ps != 0 else 0
    target_ps_nasta_ar = snitt_ps * oms_tillvxt_ar * oms_tillvxt_nasta_ar * kurs * 0.9 if nuv_ps != 0 else 0

    return {
        "target_pe_ar": target_pe_ar,
        "target_pe_nasta_ar": target_pe_nasta_ar,
        "target_ps_ar": target_ps_ar,
        "target_ps_nasta_ar": target_ps_nasta_ar,
    }

def berakna_undervardering(kurs, target):
    if kurs == 0 or target == 0:
        return 0
    return round((target - kurs) / kurs * 100, 1)  # i procent

def lagg_till_bolag(bolag_list, nytt_bolag):
    nytt_bolag["insatt_datum"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nytt_bolag["senast_andrad"] = nytt_bolag["insatt_datum"]
    bolag_list.append(nytt_bolag)
    spara_data(bolag_list)

def uppdatera_bolag(bolag_list, index, nya_data):
    nya_data["insatt_datum"] = bolag_list[index].get("insatt_datum", "")
    nya_data["senast_andrad"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bolag_list[index] = nya_data
    spara_data(bolag_list)

def ta_bort_bolag(bolag_list, index):
    bolag_list.pop(index)
    spara_data(bolag_list)

st.title("Aktieanalys - Hantera Bolag")

with st.expander("Lägg till nytt bolag"):
    with st.form(key="form_lagg_till"):
        namn = st.text_input("Bolagsnamn")
        kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
        vinst_ar = st.number_input("Vinst i år", min_value=0.0, format="%.2f")
        vinst_nasta_ar = st.number_input("Vinst nästa år", min_value=0.0, format="%.2f")
        oms_tillvxt_ar = st.number_input("Omsättningstillväxt i år (%)", format="%.2f")
        oms_tillvxt_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", format="%.2f")
        pe1 = st.number_input("P/E 1", min_value=0.0, format="%.2f")
        pe2 = st.number_input("P/E 2", min_value=0.0, format="%.2f")
        pe3 = st.number_input("P/E 3", min_value=0.0, format="%.2f")
        pe4 = st.number_input("P/E 4", min_value=0.0, format="%.2f")
        ps_nuvarande = st.number_input("Nuvarande P/S", min_value=0.0, format="%.2f")
        ps1 = st.number_input("P/S 1", min_value=0.0, format="%.2f")
        ps2 = st.number_input("P/S 2", min_value=0.0, format="%.2f")
        ps3 = st.number_input("P/S 3", min_value=0.0, format="%.2f")
        ps4 = st.number_input("P/S 4", min_value=0.0, format="%.2f")

        submit = st.form_submit_button("Lägg till bolag")

    if submit:
        nytt_bolag = {
            "namn": namn,
            "kurs": kurs,
            "vinst_ar": vinst_ar,
            "vinst_nasta_ar": vinst_nasta_ar,
            "oms_tillvxt_ar": oms_tillvxt_ar,
            "oms_tillvxt_nasta_ar": oms_tillvxt_nasta_ar,
            "pe1": pe1,
            "pe2": pe2,
            "pe3": pe3,
            "pe4": pe4,
            "ps_nuvarande": ps_nuvarande,
            "ps1": ps1,
            "ps2": ps2,
            "ps3": ps3,
            "ps4": ps4,
        }
        lagg_till_bolag(bolag_list, nytt_bolag)
        st.success(f"Bolaget '{namn}' tillagt!")
        st.experimental_rerun()

st.header("Redigera eller ta bort befintligt bolag")

if len(bolag_list) == 0:
    st.info("Inga bolag sparade ännu.")
else:
    # Välj bolag att redigera
    namn_lista = [b["namn"] for b in bolag_list]
    valt_bolag_namn = st.selectbox("Välj bolag att redigera eller ta bort", namn_lista)
    index = namn_lista.index(valt_bolag_namn)
    bolag = bolag_list[index]

    with st.form(key=f"form_redigera_{index}"):
        namn = st.text_input("Bolagsnamn", value=bolag.get("namn", ""))
        kurs = st.number_input("Nuvarande kurs", value=bolag.get("kurs", 0.0), format="%.2f", min_value=0.0)
        vinst_ar = st.number_input("Vinst i år", value=bolag.get("vinst_ar", 0.0), format="%.2f", min_value=0.0)
        vinst_nasta_ar = st.number_input("Vinst nästa år", value=bolag.get("vinst_nasta_ar", 0.0), format="%.2f", min_value=0.0)
        oms_tillvxt_ar = st.number_input("Omsättningstillväxt i år (%)", value=bolag.get("oms_tillvxt_ar", 0.0), format="%.2f")
        oms_tillvxt_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", value=bolag.get("oms_tillvxt_nasta_ar", 0.0), format="%.2f")
        pe1 = st.number_input("P/E 1", value=bolag.get("pe1", 0.0), format="%.2f", min_value=0.0)
        pe2 = st.number_input("P/E 2", value=bolag.get("pe2", 0.0), format="%.2f", min_value=0.0)
        pe3 = st.number_input("P/E 3", value=bolag.get("pe3", 0.0), format="%.2f", min_value=0.0)
        pe4 = st.number_input("P/E 4", value=bolag.get("pe4", 0.0), format="%.2f", min_value=0.0)
        ps_nuvarande = st.number_input("Nuvarande P/S", value=bolag.get("ps_nuvarande", 0.0), format="%.2f", min_value=0.0)
        ps1 = st.number_input("P/S 1", value=bolag.get("ps1", 0.0), format="%.2f", min_value=0.0)
        ps2 = st.number_input("P/S 2", value=bolag.get("ps2", 0.0), format="%.2f", min_value=0.0)
        ps3 = st.number_input("P/S 3", value=bolag.get("ps3", 0.0), format="%.2f", min_value=0.0)
        ps4 = st.number_input("P/S 4", value=bolag.get("ps4", 0.0), format="%.2f", min_value=0.0)

        submit = st.form_submit_button("Uppdatera bolag")
        delete = st.form_submit_button("Ta bort bolag")

    if submit:
        nya_data = {
            "namn": namn,
            "kurs": kurs,
            "vinst_ar": vinst_ar,
            "vinst_nasta_ar": vinst_nasta_ar,
            "oms_tillvxt_ar": oms_tillvxt_ar,
            "oms_tillvxt_nasta_ar": oms_tillvxt_nasta_ar,
            "pe1": pe1,
            "pe2": pe2,
            "pe3": pe3,
            "pe4": pe4,
            "ps_nuvarande": ps_nuvarande,
            "ps1": ps1,
            "ps2": ps2,
            "ps3": ps3,
            "ps4": ps4,
        }
        uppdatera_bolag(bolag_list, index, nya_data)
        st.success(f"Bolaget '{namn}' uppdaterat!")
        st.experimental_rerun()

    if delete:
        ta_bort_bolag(bolag_list, index)
        st.success(f"Bolaget '{valt_bolag_namn}' borttaget!")
        st.experimental_rerun()

st.header("Bolagsöversikt och undervärdering")

if len(bolag_list) == 0:
    st.info("Inga bolag att visa.")
else:
    for bolag in bolag_list:
        targets = berakna_targetkurser(bolag)
        kurs = bolag.get("kurs", 0)
        u_pe_ar = berakna_undervardering(kurs, targets["target_pe_ar"])
        u_pe_nasta_ar = berakna_undervardering(kurs, targets["target_pe_nasta_ar"])
        u_ps_ar = berakna_undervardering(kurs, targets["target_ps_ar"])
        u_ps_nasta_ar = berakna_undervardering(kurs, targets["target_ps_nasta_ar"])

        st.subheader(bolag["namn"])
        st.write(f"Nuvarande kurs: {kurs:.2f} kr")
        st.write(f"Targetkurs P/E i år: {targets['target_pe_ar']:.2f} kr (Undervärdering: {u_pe_ar} %)")
        st.write(f"Targetkurs P/E nästa år: {targets['target_pe_nasta_ar']:.2f} kr (Undervärdering: {u_pe_nasta_ar} %)")
        st.write(f"Targetkurs P/S i år: {targets['target_ps_ar']:.2f} kr (Undervärdering: {u_ps_ar} %)")
        st.write(f"Targetkurs P/S nästa år: {targets['target_ps_nasta_ar']:.2f} kr (Undervärdering: {u_ps_nasta_ar} %)")

        safe_kop = min(targets['target_pe_ar'], targets['target_ps_ar']) * 0.7
        st.write(f"Köpvärd nivå (30% rabatt): {safe_kop:.2f} kr")
        st.write("---")
