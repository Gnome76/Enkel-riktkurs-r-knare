import streamlit as st
import json
import os

FILNAMN = "bolag_data.json"

def las_data():
    if not os.path.exists(FILNAMN):
        return []
    try:
        with open(FILNAMN, "r", encoding="utf-8") as f:
            data = f.read().strip()
            if not data:
                return []
            return json.loads(data)
    except (json.JSONDecodeError, IOError):
        return []

def spara_data(bolag_list):
    with open(FILNAMN, "w", encoding="utf-8") as f:
        json.dump(bolag_list, f, ensure_ascii=False, indent=2)

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

    # Targetkurs P/E
    target_pe_iår = pe_snitt * bolag.get("vinst_iår", 0) * säkerhet
    target_pe_nästa_år = pe_snitt * bolag.get("vinst_nästa_år", 0) * säkerhet

    # Targetkurs P/S - omsättningstillväxt påverkar p/s, inte multipliceras med snittet
    nuvarande_ps = bolag.get("nuvarande_ps", 1) or 1
    nuvarande_kurs = bolag.get("nuvarande_kurs", 0)

    ps_iår_justerat = nuvarande_ps * (1 + tillväxt_iår)
    ps_nästa_år_justerat = ps_iår_justerat * (1 + tillväxt_nästa_år)

    target_ps_iår = ps_snitt * ps_iår_justerat / nuvarande_ps * nuvarande_kurs * säkerhet
    target_ps_nästa_år = ps_snitt * ps_nästa_år_justerat / nuvarande_ps * nuvarande_kurs * säkerhet

    # Undervärdering i %
    undervärdering_pe = 100 * (target_pe_nästa_år - nuvarande_kurs) / nuvarande_kurs if nuvarande_kurs else 0
    undervärdering_ps = 100 * (target_ps_nästa_år - nuvarande_kurs) / nuvarande_kurs if nuvarande_kurs else 0

    köp_pe = target_pe_nästa_år * 0.7
    köp_ps = target_ps_nästa_år * 0.7

    return {
        "target_pe_iår": target_pe_iår,
        "target_pe_nästa_år": target_pe_nästa_år,
        "target_ps_iår": target_ps_iår,
        "target_ps_nästa_år": target_ps_nästa_år,
        "undervardering_pe_pct": undervärdering_pe,
        "undervardering_ps_pct": undervärdering_ps,
        "köpvärd_pe": köp_pe,
        "köpvärd_ps": köp_ps,
    }

def uppdatera_berakningar(bolag_list):
    for bolag in bolag_list:
        resultat = berakna_targetkurser(bolag)
        bolag.update(resultat)

def filtrera_undervarderade(bolag_list, procent_grans=30):
    undervarderade = [
        b for b in bolag_list
        if max(b.get("undervardering_pe_pct", 0), b.get("undervardering_ps_pct", 0)) >= procent_grans
    ]
    undervarderade.sort(
        key=lambda b: max(b.get("undervardering_pe_pct", 0), b.get("undervardering_ps_pct", 0)),
        reverse=True
    )
    return undervarderade

def visa_inmatningsform(key_prefix, bolag=None):
    with st.form(key=f"form_{key_prefix}"):
        namn = st.text_input("Bolagsnamn", value=bolag.get("namn", "") if bolag else "")
        nuvarande_kurs = st.number_input("Nuvarande kurs", value=bolag.get("nuvarande_kurs", 0.0), format="%.2f")
        vinst_iår = st.number_input("Vinst i år", value=bolag.get("vinst_iår", 0.0), format="%.2f")
        vinst_nästa_år = st.number_input("Vinst nästa år", value=bolag.get("vinst_nästa_år", 0.0), format="%.2f")
        tillväxt_iår = st.number_input("Omsättningstillväxt i år %", value=bolag.get("tillväxt_iår", 0.0), format="%.2f")
        tillväxt_nästa_år = st.number_input("Omsättningstillväxt nästa år %", value=bolag.get("tillväxt_nästa_år", 0.0), format="%.2f")

        pe_1 = st.number_input("P/E 1", value=bolag.get("pe_1", 0.0), format="%.2f")
        pe_2 = st.number_input("P/E 2", value=bolag.get("pe_2", 0.0), format="%.2f")
        pe_3 = st.number_input("P/E 3", value=bolag.get("pe_3", 0.0), format="%.2f")
        pe_4 = st.number_input("P/E 4", value=bolag.get("pe_4", 0.0), format="%.2f")

        nuvarande_ps = st.number_input("Nuvarande P/S", value=bolag.get("nuvarande_ps", 0.0), format="%.2f")
        ps_1 = st.number_input("P/S 1", value=bolag.get("ps_1", 0.0), format="%.2f")
        ps_2 = st.number_input("P/S 2", value=bolag.get("ps_2", 0.0), format="%.2f")
        ps_3 = st.number_input("P/S 3", value=bolag.get("ps_3", 0.0), format="%.2f")
        ps_4 = st.number_input("P/S 4", value=bolag.get("ps_4", 0.0), format="%.2f")

        skickaknapp = st.form_submit_button("Spara")

    if skickaknapp:
        nytt_bolag = {
            "namn": namn,
            "nuvarande_kurs": nuvarande_kurs,
            "vinst_iår": vinst_iår,
            "vinst_nästa_år": vinst_nästa_år,
            "tillväxt_iår": tillväxt_iår,
            "tillväxt_nästa_år": tillväxt_nästa_år,
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
        return nytt_bolag
    return None

def main():
    st.title("Aktieanalys med Targetkurser och Undervärdering")

    if "bolag_list" not in st.session_state:
        st.session_state["bolag_list"] = las_data()

    # Visa formulär för nytt bolag
    st.header("Lägg till nytt bolag")
    nytt_bolag = visa_inmatningsform("nytt")

    if nytt_bolag:
        st.session_state["bolag_list"].append(nytt_bolag)
        uppdatera_berakningar(st.session_state["bolag_list"])
        spara_data(st.session_state["bolag_list"])
        st.success(f"Bolag '{nytt_bolag['namn']}' tillagt!")

    # Uppdatera beräkningar för alla bolag
    uppdatera_berakningar(st.session_state["bolag_list"])

    # Visa filter för undervärderade bolag
    undervarderade_endast = st.checkbox("Visa endast undervärderade (>30%)", value=False)

    bolag_att_visa = filtrera_undervarderade(st.session_state["bolag_list"]) if undervarderade_endast else st.session_state["bolag_list"]

    st.header("Bolagslista")

    for bolag in bolag_att_visa:
        visa_bolag(bolag)

def visa_bolag(bolag):
    st.subheader(bolag.get("namn", "Okänt bolag"))
    st.write(f"Nuvarande kurs: {bolag.get('nuvarande_kurs', 0):.2f} SEK")

    st.write(f"Targetkurs P/E i år: {bolag.get('target_pe_iår', 0):.2f} SEK")
    st.write(f"Targetkurs P/E nästa år: {bolag.get('target_pe_nästa_år', 0):.2f} SEK")
    st.write(f"Targetkurs P/S i år: {bolag.get('target_ps_iår', 0):.2f} SEK")
    st.write(f"Targetkurs P/S nästa år: {bolag.get('target_ps_nästa_år', 0):.2f} SEK")

    st.write(f"Undervärdering P/E (%): {bolag.get('undervardering_pe_pct', 0):.2f}")
    st.write(f"Undervärdering P/S (%): {bolag.get('undervardering_ps_pct', 0):.2f}")

    st.write(f"Köpvärd P/E: {bolag.get('köpvärd_pe', 0):.2f} SEK")
    st.write(f"Köpvärd P/S: {bolag.get('köpvärd_ps', 0):.2f} SEK")

    st.markdown("---")

if __name__ == "__main__":
    main()
