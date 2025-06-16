import streamlit as st
import json
import os
from datetime import datetime

# Filnamn för att spara datan
DATAFIL = "bolag_data.json"

# ---------------------
# Ladda och spara data
# ---------------------
def ladda_data():
    if os.path.exists(DATAFIL):
        with open(DATAFIL, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def spara_data(data):
    with open(DATAFIL, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# -------------------------------
# Beräkna targetkurser och analys
# -------------------------------
def beräkna_targetkurser(bolag):
    try:
        pe_tal = [bolag.get(f"pe{i}", 0) for i in range(1, 5)]
        ps_tal = [bolag.get(f"ps{i}", 0) for i in range(1, 5)]
        snitt_pe = sum(pe_tal) / len(pe_tal)
        snitt_ps = sum(ps_tal) / len(ps_tal)

        vinst_i_ar = bolag.get("vinst_i_ar", 0)
        vinst_nasta_ar = bolag.get("vinst_nasta_ar", 0)
        tillv_i_ar = bolag.get("oms_tillv_i_ar", 0) / 100
        tillv_nasta_ar = bolag.get("oms_tillv_nasta_ar", 0) / 100
        nuvarande_ps = bolag.get("nuvarande_ps", 1)
        nuvarande_kurs = bolag.get("nuvarande_kurs", 1)

        # Targetkurs PE
        target_pe_iar = snitt_pe * vinst_i_ar * 0.9
        target_pe_nasta = snitt_pe * vinst_nasta_ar * 0.9

        # Targetkurs PS
        target_ps_iar = snitt_ps * tillv_i_ar / nuvarande_ps * nuvarande_kurs * 0.9
        target_ps_nasta = snitt_ps * tillv_i_ar * tillv_nasta_ar / nuvarande_ps * nuvarande_kurs * 0.9

        return {
            "target_pe_iar": round(target_pe_iar, 2),
            "target_pe_nasta": round(target_pe_nasta, 2),
            "target_ps_iar": round(target_ps_iar, 2),
            "target_ps_nasta": round(target_ps_nasta, 2),
        }
    except Exception as e:
        st.error(f"Fel vid beräkning av targetkurser: {e}")
        return {}

# Sidhuvud
st.set_page_config(page_title="Aktieanalys", layout="centered")
st.title("📊 Enkel Aktieanalys med Targetkurser")

# Ladda databas
data = ladda_data()

# Initiera session_state för navigering
if "valda_bolag" not in st.session_state:
    st.session_state.valda_bolag = list(data.keys())
if "index" not in st.session_state:
    st.session_state.index = 0

# Filtreringscheckbox
visa_endast_undervarderade = st.checkbox("Visa endast undervärderade bolag (>30%)", value=False)

# Funktion för att filtrera undervärderade bolag
def filtrera_undervarderade(data):
    filtrerade = []
    for namn, bolag in data.items():
        kurser = beräkna_targetkurser(bolag)
        nuvarande_kurs = bolag.get("nuvarande_kurs", 1)
        rabatt_pe = 1 - (nuvarande_kurs / kurser.get("target_pe_nasta", 1))
        rabatt_ps = 1 - (nuvarande_kurs / kurser.get("target_ps_nasta", 1))
        if rabatt_pe >= 0.3 or rabatt_ps >= 0.3:
            filtrerade.append(namn)
    return filtrerade

# Uppdatera visade bolag beroende på filtrering
if visa_endast_undervarderade:
    st.session_state.valda_bolag = filtrera_undervarderade(data)
else:
    st.session_state.valda_bolag = list(data.keys())

# Justera index om det behövs
if st.session_state.index >= len(st.session_state.valda_bolag):
    st.session_state.index = 0

# Välj aktivt bolag att visa
if st.session_state.valda_bolag:
    aktivt_bolag = st.session_state.valda_bolag[st.session_state.index]
    bolag = data[aktivt_bolag]
else:
    aktivt_bolag = None
    bolag = None

st.header("➕ Lägg till nytt bolag")

with st.form("nytt_bolag_form", clear_on_submit=True):
    namn = st.text_input("Bolagsnamn")
    nuvarande_kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")

    vinst_i_ar = st.number_input("Förväntad vinst i år", format="%.2f")
    vinst_nasta_ar = st.number_input("Förväntad vinst nästa år", format="%.2f")

    oms_tillv_i_ar = st.number_input("Omsättningstillväxt i år (%)", format="%.2f")
    oms_tillv_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", format="%.2f")

    pe_nu = st.number_input("Nuvarande P/E", format="%.2f")
    pe1 = st.number_input("P/E 1", format="%.2f")
    pe2 = st.number_input("P/E 2", format="%.2f")
    pe3 = st.number_input("P/E 3", format="%.2f")
    pe4 = st.number_input("P/E 4", format="%.2f")

    ps_nu = st.number_input("Nuvarande P/S", format="%.2f")
    ps1 = st.number_input("P/S 1", format="%.2f")
    ps2 = st.number_input("P/S 2", format="%.2f")
    ps3 = st.number_input("P/S 3", format="%.2f")
    ps4 = st.number_input("P/S 4", format="%.2f")

    submitted = st.form_submit_button("Spara bolag")

    if submitted and namn:
        data[namn] = {
            "nuvarande_kurs": nuvarande_kurs,
            "vinst_i_ar": vinst_i_ar,
            "vinst_nasta_ar": vinst_nasta_ar,
            "oms_tillv_i_ar": oms_tillv_i_ar,
            "oms_tillv_nasta_ar": oms_tillv_nasta_ar,
            "pe_nu": pe_nu,
            "pe1": pe1,
            "pe2": pe2,
            "pe3": pe3,
            "pe4": pe4,
            "ps_nu": ps_nu,
            "ps1": ps1,
            "ps2": ps2,
            "ps3": ps3,
            "ps4": ps4
        }
        spara_data(data)
        st.success(f"{namn} har sparats.")
        st.stop()  # Streamlit Cloud-säker uppdatering

st.header("📊 Bläddra bland bolag")

alla_bolag = list(data.keys())
if alla_bolag:
    if "index" not in st.session_state:
        st.session_state.index = 0

    def visa_bolag(index):
        bolagsnamn = alla_bolag[index]
        info = data[bolagsnamn]
        st.subheader(f"📌 {bolagsnamn}")

        nuvarande_kurs = info["nuvarande_kurs"]
        vinst_i_ar = info["vinst_i_ar"]
        vinst_nasta_ar = info["vinst_nasta_ar"]
        oms_tillv_i_ar = info["oms_tillv_i_ar"] / 100
        oms_tillv_nasta_ar = info["oms_tillv_nasta_ar"] / 100

        pe_nu = info["pe_nu"]
        ps_nu = info["ps_nu"]

        pe_snitt = (info["pe1"] + info["pe2"] + info["pe3"] + info["pe4"]) / 4
        ps_snitt = (info["ps1"] + info["ps2"] + info["ps3"] + info["ps4"]) / 4

        target_pe_i_ar = pe_snitt * vinst_i_ar * 0.9
        target_pe_nasta_ar = pe_snitt * vinst_nasta_ar * 0.9

        target_ps_i_ar = ps_snitt * oms_tillv_i_ar / ps_nu * nuvarande_kurs * 0.9
        target_ps_nasta_ar = ps_snitt * oms_tillv_i_ar * oms_tillv_nasta_ar / ps_nu * nuvarande_kurs * 0.9

        underv_pe_i_ar = (target_pe_i_ar - nuvarande_kurs) / nuvarande_kurs * 100
        underv_pe_nasta_ar = (target_pe_nasta_ar - nuvarande_kurs) / nuvarande_kurs * 100

        underv_ps_i_ar = (target_ps_i_ar - nuvarande_kurs) / nuvarande_kurs * 100
        underv_ps_nasta_ar = (target_ps_nasta_ar - nuvarande_kurs) / nuvarande_kurs * 100

        st.markdown(f"**Nuvarande kurs:** {nuvarande_kurs:.2f} kr")

        st.markdown(f"**🎯 Targetkurs P/E (i år):** {target_pe_i_ar:.2f} kr")
        st.markdown(f"**🎯 Targetkurs P/E (nästa år):** {target_pe_nasta_ar:.2f} kr")
        st.markdown(f"**📉 Undervärdering P/E (i år):** {underv_pe_i_ar:.1f}%")
        st.markdown(f"**📉 Undervärdering P/E (nästa år):** {underv_pe_nasta_ar:.1f}%")

        st.markdown("---")
        st.markdown(f"**🎯 Targetkurs P/S (i år):** {target_ps_i_ar:.2f} kr")
        st.markdown(f"**🎯 Targetkurs P/S (nästa år):** {target_ps_nasta_ar:.2f} kr")
        st.markdown(f"**📉 Undervärdering P/S (i år):** {underv_ps_i_ar:.1f}%")
        st.markdown(f"**📉 Undervärdering P/S (nästa år):** {underv_ps_nasta_ar:.1f}%")

        st.markdown("---")
        st.markdown(f"**📌 Köpvärd nivå (30% rabatt P/E i år):** {target_pe_i_ar * 0.7:.2f} kr")
        st.markdown(f"**📌 Köpvärd nivå (30% rabatt P/S i år):** {target_ps_i_ar * 0.7:.2f} kr")

    # Bläddringsknappar
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Föregående") and st.session_state.index > 0:
            st.session_state.index -= 1
            st.stop()
    with col3:
        if st.button("➡️ Nästa") and st.session_state.index < len(alla_bolag) - 1:
            st.session_state.index += 1
            st.stop()

    visa_bolag(st.session_state.index)
else:
    st.info("Inga bolag sparade ännu.")

st.header("✏️ Redigera bolag")

if data:
    valt_bolag = st.selectbox("Välj bolag att redigera", list(data.keys()), key="redigera_bolag_val")

    if valt_bolag:
        info = data[valt_bolag]
        visa_fler_falt = st.checkbox("Visa alla fält för redigering")

        with st.form("redigera_form"):
            ny_kurs = st.number_input("Nuvarande kurs", value=info["nuvarande_kurs"])

            if visa_fler_falt:
                vinst_i_ar = st.number_input("Vinst i år", value=info["vinst_i_ar"])
                vinst_nasta_ar = st.number_input("Vinst nästa år", value=info["vinst_nasta_ar"])
                oms_tillv_i_ar = st.number_input("Omsättningstillväxt i år (%)", value=info["oms_tillv_i_ar"])
                oms_tillv_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", value=info["oms_tillv_nasta_ar"])

                pe_nu = st.number_input("Nuvarande P/E", value=info["pe_nu"])
                pe1 = st.number_input("P/E 1", value=info["pe1"])
                pe2 = st.number_input("P/E 2", value=info["pe2"])
                pe3 = st.number_input("P/E 3", value=info["pe3"])
                pe4 = st.number_input("P/E 4", value=info["pe4"])

                ps_nu = st.number_input("Nuvarande P/S", value=info["ps_nu"])
                ps1 = st.number_input("P/S 1", value=info["ps1"])
                ps2 = st.number_input("P/S 2", value=info["ps2"])
                ps3 = st.number_input("P/S 3", value=info["ps3"])
                ps4 = st.number_input("P/S 4", value=info["ps4"])
            else:
                vinst_i_ar = info["vinst_i_ar"]
                vinst_nasta_ar = info["vinst_nasta_ar"]
                oms_tillv_i_ar = info["oms_tillv_i_ar"]
                oms_tillv_nasta_ar = info["oms_tillv_nasta_ar"]

                pe_nu = info["pe_nu"]
                pe1, pe2, pe3, pe4 = info["pe1"], info["pe2"], info["pe3"], info["pe4"]

                ps_nu = info["ps_nu"]
                ps1, ps2, ps3, ps4 = info["ps1"], info["ps2"], info["ps3"], info["ps4"]

            uppdatera = st.form_submit_button("Uppdatera")

        if uppdatera:
            data[valt_bolag] = {
                "nuvarande_kurs": ny_kurs,
                "vinst_i_ar": vinst_i_ar,
                "vinst_nasta_ar": vinst_nasta_ar,
                "oms_tillv_i_ar": oms_tillv_i_ar,
                "oms_tillv_nasta_ar": oms_tillv_nasta_ar,
                "pe_nu": pe_nu,
                "pe1": pe1, "pe2": pe2, "pe3": pe3, "pe4": pe4,
                "ps_nu": ps_nu,
                "ps1": ps1, "ps2": ps2, "ps3": ps3, "ps4": ps4,
            }
            spara_data(data)
            st.success(f"{valt_bolag} uppdaterat.")
            st.session_state["refresh"] = True
            st.stop()
else:
    st.info("Inga bolag att redigera.")

st.header("📊 Bolagsöversikt")

if data:
    visa_endast_undervarderade = st.checkbox("Visa endast undervärderade bolag (>30%)")

    def beräkna_targetkurser(info):
        snitt_pe = np.mean([info["pe1"], info["pe2"], info["pe3"], info["pe4"]])
        snitt_ps = np.mean([info["ps1"], info["ps2"], info["ps3"], info["ps4"]])

        target_pe_i_ar = snitt_pe * info["vinst_i_ar"] * 0.9
        target_pe_nasta_ar = snitt_pe * info["vinst_nasta_ar"] * 0.9

        target_ps_i_ar = snitt_ps * (info["oms_tillv_i_ar"] / info["ps_nu"]) * info["nuvarande_kurs"] * 0.9
        target_ps_nasta_ar = snitt_ps * (info["oms_tillv_i_ar"] / 100) * (info["oms_tillv_nasta_ar"] / 100) * info["nuvarande_kurs"] * 0.9

        return target_pe_i_ar, target_pe_nasta_ar, target_ps_i_ar, target_ps_nasta_ar

    bolagslista = []

    for namn, info in data.items():
        tpe1, tpe2, tps1, tps2 = beräkna_targetkurser(info)

        undervardering_pe = max(tpe1, tpe2) / info["nuvarande_kurs"] - 1
        undervardering_ps = max(tps1, tps2) / info["nuvarande_kurs"] - 1

        max_undervardering = max(undervardering_pe, undervardering_ps)

        if not visa_endast_undervarderade or max_undervardering >= 0.3:
            bolagslista.append({
                "Bolag": namn,
                "Nuvarande kurs": info["nuvarande_kurs"],
                "Targetkurs P/E (i år)": round(tpe1, 2),
                "Targetkurs P/E (nästa år)": round(tpe2, 2),
                "Targetkurs P/S (i år)": round(tps1, 2),
                "Targetkurs P/S (nästa år)": round(tps2, 2),
                "Undervärdering %": f"{round(max_undervardering * 100)}%",
                "Köpvärd nivå (-30%)": round(max(tpe1, tpe2, tps1, tps2) * 0.7, 2),
            })

    if bolagslista:
        df = pd.DataFrame(bolagslista).sort_values(by="Undervärdering %", ascending=False)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Inga bolag matchar filtret.")

    st.subheader("🗑️ Ta bort bolag")
    bolag_att_ta_bort = st.selectbox("Välj bolag att ta bort", list(data.keys()), key="ta_bort_bolag")
    if st.button("Ta bort"):
        data.pop(bolag_att_ta_bort)
        spara_data(data)
        st.success(f"{bolag_att_ta_bort} borttaget.")
        st.session_state["refresh"] = True
        st.stop()

    st.subheader("📱 Bläddra bland undervärderade bolag (mobilvy)")
    undervarderade_bolag = [
        namn for namn, info in data.items()
        if max(beräkna_targetkurser(info)) / info["nuvarande_kurs"] - 1 >= 0.3
    ]

    if undervarderade_bolag:
        if "bolag_index" not in st.session_state:
            st.session_state["bolag_index"] = 0

        index = st.session_state["bolag_index"]
        bolag_namn = undervarderade_bolag[index]
        info = data[bolag_namn]
        tpe1, tpe2, tps1, tps2 = beräkna_targetkurser(info)
        max_target = max(tpe1, tpe2, tps1, tps2)
        max_undervardering = max_target / info["nuvarande_kurs"] - 1

        st.markdown(f"### {bolag_namn}")
        st.write(f"Nuvarande kurs: {info['nuvarande_kurs']}")
        st.write(f"Targetkurs P/E (i år): {round(tpe1, 2)}")
        st.write(f"Targetkurs P/E (nästa år): {round(tpe2, 2)}")
        st.write(f"Targetkurs P/S (i år): {round(tps1, 2)}")
        st.write(f"Targetkurs P/S (nästa år): {round(tps2, 2)}")
        st.write(f"Undervärdering: {round(max_undervardering * 100)}%")
        st.write(f"Köpvärd nivå (-30%): {round(max_target * 0.7, 2)}")

        col1, col2 = st.columns(2)
        if col1.button("⬅️ Föregående") and index > 0:
            st.session_state["bolag_index"] -= 1
            st.experimental_rerun()
        if col2.button("➡️ Nästa") and index < len(undervarderade_bolag) - 1:
            st.session_state["bolag_index"] += 1
            st.experimental_rerun()
    else:
        st.info("Inga undervärderade bolag att visa.")
else:
    st.info("Inga bolag sparade ännu.")
