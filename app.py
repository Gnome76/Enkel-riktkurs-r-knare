import streamlit as st
import json
import os

FILNAMN = "bolag_data.json"

# === Datahantering ===

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

# === Beräkningar ===

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

    target_pe_iår = pe_snitt * bolag.get("vinst_iår", 0) * säkerhet
    target_pe_nästa_år = pe_snitt * bolag.get("vinst_nästa_år", 0) * säkerhet

    ps_iår_justerat = nuvarande_ps * (1 + tillväxt_iår)
    ps_nästa_år_justerat = ps_iår_justerat * (1 + tillväxt_nästa_år)

    target_ps_iår = ps_snitt * ps_iår_justerat / nuvarande_ps * nuvarande_kurs * säkerhet
    target_ps_nästa_år = ps_snitt * ps_nästa_år_justerat / nuvarande_ps * nuvarande_kurs * säkerhet

    undervärdering_pe = 100 * (target_pe_nästa_år - nuvarande_kurs) / nuvarande_kurs if nuvarande_kurs else 0
    undervärdering_ps = 100 * (target_ps_nästa_år - nuvarande_kurs) / nuvarande_kurs if nuvarande_kurs else 0

    return {
        "target_pe_iår": target_pe_iår,
        "target_pe_nästa_år": target_pe_nästa_år,
        "target_ps_iår": target_ps_iår,
        "target_ps_nästa_år": target_ps_nästa_år,
        "undervardering_pe_pct": undervärdering_pe,
        "undervardering_ps_pct": undervärdering_ps,
        "köpvärd_pe": target_pe_nästa_år * 0.7,
        "köpvärd_ps": target_ps_nästa_år * 0.7
    }

def uppdatera_berakningar(bolag_list):
    for bolag in bolag_list:
        bolag.update(berakna_targetkurser(bolag))

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

st.set_page_config(page_title="Aktieanalys", layout="centered")
st.title("📈 Enkel aktieanalys med riktkurser")

if "redigerat_bolag" not in st.session_state:
    st.session_state["redigerat_bolag"] = None

bolag_list = las_data()
uppdatera_berakningar(bolag_list)
bolag_namn_lista = [b["namn"] for b in bolag_list]

st.subheader("➕ Lägg till eller redigera bolag")

redigeringsval = st.selectbox(
    "Välj bolag att redigera (eller lämna tom för att lägga till nytt):",
    [""] + bolag_namn_lista,
    key="valj_redigering"
)

redigerat_bolag = next((b for b in bolag_list if b["namn"] == redigeringsval), None) if redigeringsval else None

with st.form(key="inmatning_formulär"):
    namn = st.text_input("Bolagsnamn", value=redigerat_bolag["namn"] if redigerat_bolag else "")
    nuvarande_kurs = st.number_input("Nuvarande kurs", value=redigerat_bolag["nuvarande_kurs"] if redigerat_bolag else 0.0)
    vinst_iår = st.number_input("Vinst i år", value=redigerat_bolag["vinst_iår"] if redigerat_bolag else 0.0)
    vinst_nästa_år = st.number_input("Vinst nästa år", value=redigerat_bolag["vinst_nästa_år"] if redigerat_bolag else 0.0)
    tillväxt_iår = st.number_input("Omsättningstillväxt i år (%)", value=redigerat_bolag["tillväxt_iår"] if redigerat_bolag else 0.0)
    tillväxt_nästa_år = st.number_input("Omsättningstillväxt nästa år (%)", value=redigerat_bolag["tillväxt_nästa_år"] if redigerat_bolag else 0.0)

    nuvarande_pe = st.number_input("Nuvarande P/E", value=redigerat_bolag["nuvarande_pe"] if redigerat_bolag else 0.0)
    pe_1 = st.number_input("P/E 1", value=redigerat_bolag["pe_1"] if redigerat_bolag else 0.0)
    pe_2 = st.number_input("P/E 2", value=redigerat_bolag["pe_2"] if redigerat_bolag else 0.0)
    pe_3 = st.number_input("P/E 3", value=redigerat_bolag["pe_3"] if redigerat_bolag else 0.0)
    pe_4 = st.number_input("P/E 4", value=redigerat_bolag["pe_4"] if redigerat_bolag else 0.0)

    nuvarande_ps = st.number_input("Nuvarande P/S", value=redigerat_bolag["nuvarande_ps"] if redigerat_bolag else 0.0)
    ps_1 = st.number_input("P/S 1", value=redigerat_bolag["ps_1"] if redigerat_bolag else 0.0)
    ps_2 = st.number_input("P/S 2", value=redigerat_bolag["ps_2"] if redigerat_bolag else 0.0)
    ps_3 = st.number_input("P/S 3", value=redigerat_bolag["ps_3"] if redigerat_bolag else 0.0)
    ps_4 = st.number_input("P/S 4", value=redigerat_bolag["ps_4"] if redigerat_bolag else 0.0)

    submitted = st.form_submit_button("💾 Spara")

    if submitted and namn:
        nytt_bolag = {
            "namn": namn,
            "nuvarande_kurs": nuvarande_kurs,
            "vinst_iår": vinst_iår,
            "vinst_nästa_år": vinst_nästa_år,
            "tillväxt_iår": tillväxt_iår,
            "tillväxt_nästa_år": tillväxt_nästa_år,
            "nuvarande_pe": nuvarande_pe,
            "pe_1": pe_1, "pe_2": pe_2, "pe_3": pe_3, "pe_4": pe_4,
            "nuvarande_ps": nuvarande_ps,
            "ps_1": ps_1, "ps_2": ps_2, "ps_3": ps_3, "ps_4": ps_4
        }

        if redigerat_bolag:
            index = bolag_list.index(redigerat_bolag)
            bolag_list[index] = nytt_bolag
            st.success(f"Uppdaterade {namn}")
        else:
            bolag_list.append(nytt_bolag)
            st.success(f"La till {namn}")

        uppdatera_berakningar(bolag_list)
        spara_data(bolag_list)
        st.experimental_rerun()

st.subheader("📊 Översikt och analys")

# Checkbox för att visa endast undervärderade bolag (minst 30% rabatt)
visa_undervarderade = st.checkbox("Visa endast undervärderade bolag (minst 30% rabatt)")

# Funktion för att avgöra undervärdering (minst 30%)
def ar_undervarderad(b):
    undervard_pe = b.get("undervardering_pe", 0)
    undervard_ps = b.get("undervardering_ps", 0)
    return (undervard_pe >= 30) or (undervard_ps >= 30)

if visa_undervarderade:
    filtrerad_lista = [b for b in bolag_list if ar_undervarderad(b)]
else:
    filtrerad_lista = bolag_list

# Sortera efter störst undervärdering (max av P/E och P/S)
filtrerad_lista.sort(key=lambda b: max(b.get("undervardering_pe", 0), b.get("undervardering_ps", 0)), reverse=True)

# Visa tabell med bolag och viktiga värden
tabell_data = []
for b in filtrerad_lista:
    tabell_data.append({
        "Namn": b["namn"],
        "Nuvarande kurs": b["nuvarande_kurs"],
        "Targetkurs P/E (i år)": round(b["target_pe_iar"], 2),
        "Targetkurs P/E (nästa år)": round(b["target_pe_nasta"], 2),
        "Targetkurs P/S (i år)": round(b["target_ps_iar"], 2),
        "Targetkurs P/S (nästa år)": round(b["target_ps_nasta"], 2),
        "Undervärdering P/E (%)": round(b["undervardering_pe"], 2),
        "Undervärdering P/S (%)": round(b["undervardering_ps"], 2),
    })

st.table(tabell_data)

# Navigering för att visa ett bolag i taget
if "aktuell_index" not in st.session_state:
    st.session_state["aktuell_index"] = 0

antal_bolag = len(filtrerad_lista)

if antal_bolag > 0:
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("⬅️ Föregående"):
            st.session_state["aktuell_index"] = max(st.session_state["aktuell_index"] - 1, 0)
    with col3:
        if st.button("Nästa ➡️"):
            st.session_state["aktuell_index"] = min(st.session_state["aktuell_index"] + 1, antal_bolag - 1)

    bolag_visas = filtrerad_lista[st.session_state["aktuell_index"]]
    st.markdown(f"### {bolag_visas['namn']}")

    # Visa detaljerad info för valt bolag
    st.write(f"**Nuvarande kurs:** {bolag_visas['nuvarande_kurs']}")
    st.write(f"**Targetkurs P/E (i år):** {bolag_visas['target_pe_iar']}")
    st.write(f"**Targetkurs P/E (nästa år):** {bolag_visas['target_pe_nasta']}")
    st.write(f"**Targetkurs P/S (i år):** {bolag_visas['target_ps_iar']}")
    st.write(f"**Targetkurs P/S (nästa år):** {bolag_visas['target_ps_nasta']}")
    st.write(f"**Undervärdering P/E (%):** {bolag_visas['undervardering_pe']:.2f}%")
    st.write(f"**Undervärdering P/S (%):** {bolag_visas['undervardering_ps']:.2f}%")

    # Knapp för att ta bort bolag
    if st.button(f"🗑 Ta bort {bolag_visas['namn']}"):
        bolag_list.remove(bolag_visas)
        spara_data(bolag_list)
        st.session_state["aktuell_index"] = max(0, st.session_state["aktuell_index"] - 1)
        st.success(f"{bolag_visas['namn']} har tagits bort.")
        st.experimental_rerun()
else:
    st.info("Inga bolag att visa.")

# ---------- Hjälpfunktioner för beräkningar ----------

def berakna_targetkurser(bolag):
    """
    Beräkna targetkurser och undervärdering baserat på bolagsdata.
    Uppdaterar bolaget i listan med nya värden.
    """
    try:
        # P/E - medel av P/E 1-4
        pe_list = [bolag.get(f"pe_{i}", None) for i in range(1, 5)]
        pe_list = [p for p in pe_list if p is not None and p > 0]
        if not pe_list:
            return bolag  # kan inte beräkna utan P/E data
        pe_snitt = sum(pe_list) / len(pe_list)

        # P/S - medel av P/S 1-4
        ps_list = [bolag.get(f"ps_{i}", None) for i in range(1, 5)]
        ps_list = [p for p in ps_list if p is not None and p > 0]
        if not ps_list:
            return bolag  # kan inte beräkna utan P/S data
        ps_snitt = sum(ps_list) / len(ps_list)

        # Säkerhetsmarginal 10%
        säkerhetsmarginal = 0.9

        # Vinst i år och nästa år
        vinst_iar = bolag.get("vinst_iar", 0)
        vinst_nasta = bolag.get("vinst_nasta", 0)

        # Omsättningstillväxt i år och nästa år (% som decimaltal)
        oms_tillv_iar = bolag.get("oms_tillv_iar", 0) / 100
        oms_tillv_nasta = bolag.get("oms_tillv_nasta", 0) / 100

        # Nuvarande kurs
        kurs = bolag.get("nuvarande_kurs", 1)

        # Targetkurser P/E
        bolag["target_pe_iar"] = pe_snitt * vinst_iar * säkerhetsmarginal
        bolag["target_pe_nasta"] = pe_snitt * vinst_nasta * säkerhetsmarginal

        # Targetkurser P/S
        # Formeln: snitt P/S * omsättningstillväxt * kurs * säkerhetsmarginal
        # Omsättningstillväxt i år och nästa år multipliceras för nästa år
        bolag["target_ps_iar"] = ps_snitt * oms_tillv_iar * kurs * säkerhetsmarginal
        bolag["target_ps_nasta"] = ps_snitt * oms_tillv_iar * oms_tillv_nasta * kurs * säkerhetsmarginal

        # Undervärdering i procent
        # Hur mycket kursen är lägre än targetkursen, i %
        undervard_pe = max(0, (1 - kurs / bolag["target_pe_iar"]) * 100) if bolag["target_pe_iar"] > 0 else 0
        undervard_ps = max(0, (1 - kurs / bolag["target_ps_iar"]) * 100) if bolag["target_ps_iar"] > 0 else 0

        bolag["undervardering_pe"] = undervard_pe
        bolag["undervardering_ps"] = undervard_ps

    except Exception as e:
        st.error(f"Fel vid beräkning av targetkurser för {bolag.get('namn', '')}: {e}")

    return bolag


# ---------- Uppdatera beräkningar för alla bolag ----------

for i, bolag in enumerate(bolag_list):
    bolag_list[i] = berakna_targetkurser(bolag)

# Spara data efter uppdatering
spara_data(bolag_list)

# ---------- Avslutande information ----------

st.markdown("---")
st.write("© 2025 Aktieanalysappen – utvecklad av ChatGPT")
