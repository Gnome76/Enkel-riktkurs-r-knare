import streamlit as st

# --- Hjälpfunktioner ---

def medelvärde(lista):
    if not lista:
        return 0
    return sum(lista) / len(lista)

def berakna_targetkurser(bolag):
    säkerhet = 0.9

    pe_värden = [bolag.get(f"pe_{i}", 0) for i in range(1,5)]
    pe_snitt = medelvärde(pe_värden)

    ps_värden = [bolag.get(f"ps_{i}", 0) for i in range(1,5)]
    ps_snitt = medelvärde(ps_värden)

    tillväxt_iår = bolag.get("oms_tillvaxt_i_ar", 0) / 100
    tillväxt_nästa_år = bolag.get("oms_tillvaxt_nasta_ar", 0) / 100

    target_pe_iår = pe_snitt * bolag.get("vinst_i_ar", 0) * säkerhet
    target_pe_nästa_år = pe_snitt * bolag.get("vinst_nasta_ar", 0) * säkerhet

    nuvarande_ps = bolag.get("nuvarande_ps", 1) or 1
    nuvarande_kurs = bolag.get("nuvarande_kurs", 0)

    target_ps_iår = ps_snitt * (tillväxt_iår / nuvarande_ps) * nuvarande_kurs * säkerhet
    target_ps_nästa_år = ps_snitt * ((tillväxt_iår * tillväxt_nästa_år) / nuvarande_ps) * nuvarande_kurs * säkerhet

    undervardering_pe_pct = 100 * (target_pe_nästa_år - nuvarande_kurs) / nuvarande_kurs if nuvarande_kurs else 0
    undervardering_ps_pct = 100 * (target_ps_nästa_år - nuvarande_kurs) / nuvarande_kurs if nuvarande_kurs else 0

    köp_pe = target_pe_nästa_år * 0.7
    köp_ps = target_ps_nästa_år * 0.7

    # Lägg till i bolaget
    bolag.update({
        "target_pe_iar": target_pe_iår,
        "target_pe_nasta_ar": target_pe_nästa_år,
        "target_ps_iar": target_ps_iår,
        "target_ps_nasta_ar": target_ps_nästa_år,
        "undervardering_pe_pct": undervardering_pe_pct,
        "undervardering_ps_pct": undervardering_ps_pct,
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

# Initiera session_state för bolagslista
if "bolag_list" not in st.session_state:
    st.session_state.bolag_list = []

st.title("Aktieanalys med Targetkurser och Undervärdering")

with st.form(key="nytt_bolag_form"):
    st.subheader("Lägg till nytt bolag")
    namn = st.text_input("Bolagsnamn")
    nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
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
    vinst_i_ar = st.number_input("Förväntad vinst i år", format="%.2f")
    vinst_nasta_ar = st.number_input("Förväntad vinst nästa år", format="%.2f")
    oms_tillvaxt_i_ar = st.number_input("Omsättningstillväxt i år (%)", format="%.2f")
    oms_tillvaxt_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", format="%.2f")
    knapp = st.form_submit_button("Lägg till bolag")

if knapp:
    if namn.strip() == "":
        st.error("Ange ett bolagsnamn.")
    else:
        nytt_bolag = {
            "namn": namn.strip(),
            "nuvarande_kurs": nuvarande_kurs,
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
            "vinst_i_ar": vinst_i_ar,
            "vinst_nasta_ar": vinst_nasta_ar,
            "oms_tillvaxt_i_ar": oms_tillvaxt_i_ar,
            "oms_tillvaxt_nasta_ar": oms_tillvaxt_nasta_ar,
        }
        berakna_targetkurser(nytt_bolag)
        st.session_state.bolag_list.append(nytt_bolag)
        st.success(f"Bolag {namn} tillagt!")

st.write("---")

visa_undervarderade = st.checkbox("Visa endast undervärderade bolag (minst 30%)")

if visa_undervarderade:
    bolag_att_visas = filtrera_undervarderade(st.session_state.bolag_list)
else:
    bolag_att_visas = st.session_state.bolag_list

if not bolag_att_visas:
    st.info("Inga bolag att visa.")
else:
    for b in bolag_att_visas:
        st.subheader(b["namn"])
        st.write(f"Nuvarande kurs: {b['nuvarande_kurs']:.2f} SEK")
        st.write(f"Targetkurs P/E i år: {b['target_pe_iar']:.2f} SEK")
        st.write(f"Targetkurs P/E nästa år: {b['target_pe_nasta_ar']:.2f} SEK")
        st.write(f"Targetkurs P/S i år: {b['target_ps_iar']:.2f} SEK")
        st.write(f"Targetkurs P/S nästa år: {b['target_ps_nasta_ar']:.2f} SEK")
        st.write(f"Undervärdering P/E: {b['undervardering_pe_pct']:.1f} %")
        st.write(f"Undervärdering P/S: {b['undervardering_ps_pct']:.1f} %")
        st.write(f"Köpvärd nivå P/E: {b['köpvärd_pe']:.2f} SEK")
        st.write(f"Köpvärd nivå P/S: {b['köpvärd_ps']:.2f} SEK")
        st.write("---")

st.write("---")
st.subheader("Ta bort bolag")

if st.session_state.bolag_list:
    namn_att_ta_bort = st.selectbox("Välj bolag att ta bort", [b["namn"] for b in st.session_state.bolag_list])
    if st.button("Ta bort valt bolag"):
        st.session_state.bolag_list = [b for b in st.session_state.bolag_list if b["namn"] != namn_att_ta_bort]
        st.success(f"Bolaget {namn_att_ta_bort} har tagits bort.")
else:
    st.info("Inga bolag att ta bort.")
