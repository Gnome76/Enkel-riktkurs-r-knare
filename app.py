import streamlit as st
import json
import os

FILNAMN = "bolag_data.json"

# Läs data från fil
def las_data():
    if not os.path.exists(FILNAMN):
        return []
    with open(FILNAMN, "r", encoding="utf-8") as f:
        return json.load(f)

# Spara data till fil
def spara_data(data):
    with open(FILNAMN, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def medelvärde(lista):
    if not lista:
        return 0
    return sum(lista) / len(lista)

def berakna_targetkurser(bolag):
    säkerhet = 0.9

    pe_värden = [bolag.get(f"pe_{i}", 0) for i in range(1, 5)]
    pe_snitt = medelvärde(pe_värden)

    ps_värden = [bolag.get(f"ps_{i}", 0) for i in range(1, 5)]
    ps_snitt = medelvärde(ps_värden)

    tillväxt_iår = bolag.get("tillväxt_iår", 0) / 100
    tillväxt_nästa_år = bolag.get("tillväxt_nästa_år", 0) / 100

    nuvarande_ps = bolag.get("nuvarande_ps", 1) or 1
    nuvarande_kurs = bolag.get("nuvarande_kurs", 0)

    # Target P/E
    target_pe_iår = pe_snitt * bolag.get("vinst_iår", 0) * säkerhet
    target_pe_nästa_år = pe_snitt * bolag.get("vinst_nästa_år", 0) * säkerhet

    # Target P/S justerad med omsättningstillväxt
    ps_iår_justerad = ps_snitt * (1 + tillväxt_iår)
    ps_nästa_år_justerad = ps_snitt * (1 + tillväxt_iår) * (1 + tillväxt_nästa_år)

    target_ps_iår = ps_iår_justerad / nuvarande_ps * nuvarande_kurs * säkerhet
    target_ps_nästa_år = ps_nästa_år_justerad / nuvarande_ps * nuvarande_kurs * säkerhet

    undervärdering_pe = 100 * (target_pe_nästa_år - nuvarande_kurs) / nuvarande_kurs if nuvarande_kurs else 0
    undervärdering_ps = 100 * (target_ps_nästa_år - nuvarande_kurs) / nuvarande_kurs if nuvarande_kurs else 0

    köp_pe = target_pe_nästa_år * 0.7
    köp_ps = target_ps_nästa_år * 0.7

    bolag.update({
        "target_pe_iår": target_pe_iår,
        "target_pe_nästa_år": target_pe_nästa_år,
        "target_ps_iår": target_ps_iår,
        "target_ps_nästa_år": target_ps_nästa_år,
        "undervardering_pe_pct": undervärdering_pe,
        "undervardering_ps_pct": undervärdering_ps,
        "köpvärd_pe": köp_pe,
        "köpvärd_ps": köp_ps,
    })

def filtrera_undervarderade(bolag_list, procent_grans=30):
    undervarderade = [
        b for b in bolag_list
        if max(b.get("undervardering_pe_pct", 0), b.get("undervardering_ps_pct", 0)) >= procent_grans
    ]
    undervarderade.sort(key=lambda b: max(b.get("undervardering_pe_pct", 0), b.get("undervardering_ps_pct", 0)), reverse=True)
    return undervarderade

def nytt_bolag_form(key):
    with st.form(key):
        namn = st.text_input("Bolagsnamn")
        nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
        vinst_iår = st.number_input("Vinst i år", format="%.2f")
        vinst_nästa_år = st.number_input("Vinst nästa år", format="%.2f")
        tillväxt_iår = st.number_input("Omsättningstillväxt i år (%)", format="%.2f")
        tillväxt_nästa_år = st.number_input("Omsättningstillväxt nästa år (%)", format="%.2f")

        pe_1 = st.number_input("P/E 1", min_value=0.0, format="%.2f")
        pe_2 = st.number_input("P/E 2", min_value=0.0, format="%.2f")
        pe_3 = st.number_input("P/E 3", min_value=0.0, format="%.2f")
        pe_4 = st.number_input("P/E 4", min_value=0.0, format="%.2f")

        ps_1 = st.number_input("P/S 1", min_value=0.0, format="%.2f")
        ps_2 = st.number_input("P/S 2", min_value=0.0, format="%.2f")
        ps_3 = st.number_input("P/S 3", min_value=0.0, format="%.2f")
        ps_4 = st.number_input("P/S 4", min_value=0.0, format="%.2f")

        nuvarande_ps = st.number_input("Nuvarande P/S", min_value=0.01, format="%.2f")

        submit = st.form_submit_button("Lägg till bolag")

    if submit and namn.strip():
        return {
            "namn": namn.strip(),
            "nuvarande_kurs": nuvarande_kurs,
            "vinst_iår": vinst_iår,
            "vinst_nästa_år": vinst_nästa_år,
            "tillväxt_iår": tillväxt_iår,
            "tillväxt_nästa_år": tillväxt_nästa_år,
            "pe_1": pe_1,
            "pe_2": pe_2,
            "pe_3": pe_3,
            "pe_4": pe_4,
            "ps_1": ps_1,
            "ps_2": ps_2,
            "ps_3": ps_3,
            "ps_4": ps_4,
            "nuvarande_ps": nuvarande_ps,
        }
    return None

def visa_lista(bolag_list):
    for bolag in bolag_list:
        with st.expander(bolag["namn"]):
            st.write(f"Nuvarande kurs: {bolag['nuvarande_kurs']:.2f} SEK")

            st.write("### Targetkurser")
            st.write(f"P/E i år: {bolag['target_pe_iår']:.2f} SEK")
            st.write(f"P/E nästa år: {bolag['target_pe_nästa_år']:.2f} SEK")
            st.write(f"P/S i år: {bolag['target_ps_iår']:.2f} SEK")
            st.write(f"P/S nästa år: {bolag['target_ps_nästa_år']:.2f} SEK")

            st.write("### Undervärdering")
            st.write(f"P/E undervärdering: {bolag['undervardering_pe_pct']:.2f} %")
            st.write(f"P/S undervärdering: {bolag['undervardering_ps_pct']:.2f} %")

            st.write("### Köpvärd nivå (30% rabatt)")
            st.write(f"P/E köpvärd kurs: {bolag['köpvärd_pe']:.2f} SEK")
            st.write(f"P/S köpvärd kurs: {bolag['köpvärd_ps']:.2f} SEK")

def main():
    st.title("Aktieanalys med Targetkurser och Undervärdering")

    if "bolag_list" not in st.session_state:
        st.session_state["bolag_list"] = las_data()

    nytt = nytt_bolag_form("nytt_bolag_form")
    if nytt:
        berakna_targetkurser(nytt)
        st.session_state["bolag_list"].append(nytt)
        spara_data(st.session_state["bolag_list"])
        st.success(f"Bolag {nytt['namn']} tillagt!")

    # Uppdatera targetkurser för alla bolag (om data ändrats externt)
    for bolag in st.session_state["bolag_list"]:
        berakna_targetkurser(bolag)

    visa_undervarderade = st.checkbox("Visa endast undervärderade (>30%)", value=False)
    lista = st.session_state["bolag_list"]
    if visa_undervarderade:
        lista = filtrera_undervarderade(lista)

    visa_lista(lista)

if __name__ == "__main__":
    main()
