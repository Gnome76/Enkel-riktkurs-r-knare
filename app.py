import streamlit as st
import json
import os
from datetime import datetime

DATAFIL = "bolag_data.json"

def load_data():
    if not os.path.exists(DATAFIL):
        return {}
    with open(DATAFIL, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_data(data):
    with open(DATAFIL, "w") as f:
        json.dump(data, f, indent=4)

def beräkna_targetkurser(bolag):
    try:
        pe_snitt = sum([bolag.get(f"pe{i}", 0) for i in range(1, 5)]) / 4
        ps_snitt = sum([bolag.get(f"ps{i}", 0) for i in range(1, 5)]) / 4
        vinst_i_ar = bolag.get("vinst_i_ar", 0)
        vinst_nasta_ar = bolag.get("vinst_nasta_ar", 0)
        tillv_i_ar = bolag.get("tillv_i_ar", 0) / 100
        tillv_nasta_ar = bolag.get("tillv_nasta_ar", 0) / 100
        kurs = bolag.get("kurs", 0)
        ps_nu = bolag.get("ps_nu", 1) or 1

        target_pe_1 = pe_snitt * vinst_i_ar * 0.9
        target_pe_2 = pe_snitt * vinst_nasta_ar * 0.9
        target_ps_1 = ps_snitt * tillv_i_ar / ps_nu * kurs * 0.9
        target_ps_2 = ps_snitt * tillv_i_ar * tillv_nasta_ar / ps_nu * kurs * 0.9

        return target_pe_1, target_pe_2, target_ps_1, target_ps_2
    except Exception:
        return 0, 0, 0, 0

def nytt_bolag_form(data):
    with st.form(key="form_nytt_bolag"):
        st.subheader("Lägg till nytt bolag")

        namn = st.text_input("Bolagsnamn").strip()
        kurs = st.number_input("Nuvarande kurs", min_value=0.0, format="%.2f")
        vinst_i_ar = st.number_input("Vinst i år", format="%.2f")
        vinst_nasta_ar = st.number_input("Vinst nästa år", format="%.2f")

        omsattning_fj = st.number_input("Omsättning förra året", format="%.2f")
        tillv_i_ar = st.number_input("Omsättningstillväxt i år (%)", format="%.2f")
        tillv_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", format="%.2f")

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

        submit = st.form_submit_button("Spara bolag")

        if submit:
            if namn == "":
                st.error("Ange bolagsnamn.")
                return

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            data[namn] = {
                "kurs": kurs,
                "vinst_i_ar": vinst_i_ar,
                "vinst_nasta_ar": vinst_nasta_ar,
                "omsattning_fj": omsattning_fj,
                "tillv_i_ar": tillv_i_ar,
                "tillv_nasta_ar": tillv_nasta_ar,
                "pe_nu": pe_nu,
                "pe1": pe1,
                "pe2": pe2,
                "pe3": pe3,
                "pe4": pe4,
                "ps_nu": ps_nu,
                "ps1": ps1,
                "ps2": ps2,
                "ps3": ps3,
                "ps4": ps4,
                "insatt_datum": now,
                "senast_andrad": now,
            }
            save_data(data)
            st.success(f"{namn} sparat!")

def berakna_targetkurs_pe(vinst, pe_list):
    if len(pe_list) == 0 or vinst <= 0:
        return 0.0
    pe_medeltal = sum(pe_list) / len(pe_list)
    return round(vinst * pe_medeltal * 0.9, 2)  # 10% säkerhetsmarginal

def berakna_targetkurs_ps(nuvarande_kurs, ps_list, tillv_i_ar, tillv_nasta_ar):
    if len(ps_list) == 0 or nuvarande_kurs <= 0:
        return 0.0
    ps_medeltal = sum(ps_list) / len(ps_list)
    tillv_medel = (tillv_i_ar + tillv_nasta_ar) / 2 / 100  # Omvandla procent till decimal
    return round(nuvarande_kurs * ps_medeltal * tillv_medel * 0.9, 2)

def visa_alla_bolag(data):
    st.subheader("Översikt över sparade bolag")

    if not data:
        st.info("Inga bolag sparade än.")
        return

    tabell_data = []
    for namn, info in data.items():
        pe_list = [info.get("pe1", 0), info.get("pe2", 0), info.get("pe3", 0), info.get("pe4", 0)]
        pe_list = [x for x in pe_list if x > 0]
        ps_list = [info.get("ps1", 0), info.get("ps2", 0), info.get("ps3", 0), info.get("ps4", 0)]
        ps_list = [x for x in ps_list if x > 0]

        target_pe_i_ar = berakna_targetkurs_pe(info.get("vinst_i_ar", 0), pe_list)
        target_pe_nasta_ar = berakna_targetkurs_pe(info.get("vinst_nasta_ar", 0), pe_list)

        target_ps = berakna_targetkurs_ps(
            info.get("kurs", 0),
            ps_list,
            info.get("tillv_i_ar", 0),
            info.get("tillv_nasta_ar", 0),
        )

        undervardering_pe = 0
        undervardering_ps = 0

        kurs = info.get("kurs", 0)
        if target_pe_i_ar > 0:
            undervardering_pe = round((target_pe_i_ar - kurs) / target_pe_i_ar * 100, 1)
        if target_ps > 0:
            undervardering_ps = round((target_ps - kurs) / target_ps * 100, 1)

        undervardering = max(undervardering_pe, undervardering_ps)

        tabell_data.append({
            "Bolag": namn,
            "Kurs": kurs,
            "Targetkurs P/E i år": target_pe_i_ar,
            "Targetkurs P/E nästa år": target_pe_nasta_ar,
            "Targetkurs P/S": target_ps,
            "Undervärdering %": undervardering,
        })

    df = pd.DataFrame(tabell_data)
    df = df.sort_values(by="Undervärdering %", ascending=False)

    # Visa filtrering för minst 30% undervärdering
    visa_endast_undervarderade = st.checkbox("Visa endast bolag med minst 30% undervärdering", value=False)
    if visa_endast_undervarderade:
        df = df[df["Undervärdering %"] >= 30]

    st.dataframe(df.reset_index(drop=True))

def redigera_bolag(data):
    st.subheader("Redigera befintligt bolag")

    valda_bolag = list(data.keys())
    if not valda_bolag:
        st.info("Inga bolag att redigera.")
        return data

    valt_bolag = st.selectbox("Välj bolag att redigera", valda_bolag)

    if valt_bolag:
        bolag_info = data[valt_bolag]

        with st.form(key=f"form_redigera_{valt_bolag}"):
            kurs = st.number_input("Nuvarande kurs", value=bolag_info.get("kurs", 0.0), step=0.1, format="%.2f")
            vinst_i_ar = st.number_input("Vinst i år", value=bolag_info.get("vinst_i_ar", 0.0), format="%.2f")
            vinst_nasta_ar = st.number_input("Vinst nästa år", value=bolag_info.get("vinst_nasta_ar", 0.0), format="%.2f")
            tillv_i_ar = st.number_input("Omsättningstillväxt i år %", value=bolag_info.get("tillv_i_ar", 0.0), format="%.2f")
            tillv_nasta_ar = st.number_input("Omsättningstillväxt nästa år %", value=bolag_info.get("tillv_nasta_ar", 0.0), format="%.2f")

            pe1 = st.number_input("P/E 1", value=bolag_info.get("pe1", 0.0), format="%.2f")
            pe2 = st.number_input("P/E 2", value=bolag_info.get("pe2", 0.0), format="%.2f")
            pe3 = st.number_input("P/E 3", value=bolag_info.get("pe3", 0.0), format="%.2f")
            pe4 = st.number_input("P/E 4", value=bolag_info.get("pe4", 0.0), format="%.2f")

            ps1 = st.number_input("P/S 1", value=bolag_info.get("ps1", 0.0), format="%.2f")
            ps2 = st.number_input("P/S 2", value=bolag_info.get("ps2", 0.0), format="%.2f")
            ps3 = st.number_input("P/S 3", value=bolag_info.get("ps3", 0.0), format="%.2f")
            ps4 = st.number_input("P/S 4", value=bolag_info.get("ps4", 0.0), format="%.2f")

            uppdatera = st.form_submit_button("Uppdatera bolag")

            if uppdatera:
                data[valt_bolag] = {
                    "kurs": kurs,
                    "vinst_i_ar": vinst_i_ar,
                    "vinst_nasta_ar": vinst_nasta_ar,
                    "tillv_i_ar": tillv_i_ar,
                    "tillv_nasta_ar": tillv_nasta_ar,
                    "pe1": pe1,
                    "pe2": pe2,
                    "pe3": pe3,
                    "pe4": pe4,
                    "ps1": ps1,
                    "ps2": ps2,
                    "ps3": ps3,
                    "ps4": ps4,
                }
                st.success(f"{valt_bolag} har uppdaterats.")
                save_data(data)

    return data

def ta_bort_bolag(data):
    st.subheader("Ta bort bolag")

    valda_bolag = list(data.keys())
    if not valda_bolag:
        st.info("Inga bolag att ta bort.")
        return data

    valt_bolag = st.selectbox("Välj bolag att ta bort", valda_bolag)

    if valt_bolag:
        if st.button(f"Ta bort {valt_bolag}"):
            data.pop(valt_bolag)
            st.success(f"{valt_bolag} har tagits bort.")
            save_data(data)

    return data

def main():
    st.title("Enkel Aktieanalys – Riktkursräknare")

    data = load_data()
    if "valda_bolag" not in st.session_state:
        st.session_state.valda_bolag = list(data.keys())

    menu = ["Lägg till bolag", "Redigera bolag", "Visa alla bolag", "Ta bort bolag"]
    choice = st.sidebar.selectbox("Meny", menu)

    if choice == "Lägg till bolag":
        data = lagg_till_bolag(data)
        st.session_state.valda_bolag = list(data.keys())

    elif choice == "Redigera bolag":
        data = redigera_bolag(data)
        st.session_state.valda_bolag = list(data.keys())

    elif choice == "Visa alla bolag":
        visa_alla_bolag(data)

    elif choice == "Ta bort bolag":
        data = ta_bort_bolag(data)
        st.session_state.valda_bolag = list(data.keys())

if __name__ == "__main__":
    main()

def berakna_riktkurser(bolag):
    """
    Beräknar targetkurs P/E och P/S baserat på P/E 1-4, P/S 1-4, vinst i år och nästa år, samt omsättningstillväxt.
    Säkerhetsmarginal på 10% (0.9) appliceras.
    """
    pe_values = [bolag.get(f"pe{i}", None) for i in range(1,5)]
    ps_values = [bolag.get(f"ps{i}", None) for i in range(1,5)]
    
    # Filtrera bort None och 0 för att undvika fel
    pe_values = [v for v in pe_values if v is not None and v > 0]
    ps_values = [v for v in ps_values if v is not None and v > 0]
    
    if not pe_values or not ps_values:
        return None  # Kan ej beräkna utan data
    
    pe_snitt = sum(pe_values) / len(pe_values)
    ps_snitt = sum(ps_values) / len(ps_values)

    vinst_ar = bolag.get("vinst_i_ar", 0)
    vinst_nasta_ar = bolag.get("vinst_nasta_ar", 0)
    oms_tillvxt_ar = bolag.get("oms_tillvxt_i_ar", 0) / 100  # omvandlas till decimal
    oms_tillvxt_nasta_ar = bolag.get("oms_tillvxt_nasta_ar", 0) / 100
    nuvarande_kurs = bolag.get("nuvarande_kurs", 0)
    nuvarande_ps = bolag.get("nuvarande_ps", 1)  # Undvik division med 0

    # Targetkurs P/E med säkerhetsmarginal
    target_pe_ar = pe_snitt * vinst_ar * 0.9
    target_pe_nasta_ar = pe_snitt * vinst_nasta_ar * 0.9

    # Targetkurs P/S med omsättningstillväxt och säkerhetsmarginal
    target_ps_ar = ps_snitt * (1 + oms_tillvxt_ar) * nuvarande_kurs * 0.9
    target_ps_nasta_ar = ps_snitt * (1 + oms_tillvxt_ar) * (1 + oms_tillvxt_nasta_ar) * nuvarande_kurs * 0.9

    return {
        "target_pe_ar": target_pe_ar,
        "target_pe_nasta_ar": target_pe_nasta_ar,
        "target_ps_ar": target_ps_ar,
        "target_ps_nasta_ar": target_ps_nasta_ar
    }


def visa_riktkurser_och_undervardering(bolag):
    """
    Visar beräknade riktkurser och undervärdering för ett bolag.
    """
    nuvarande_kurs = bolag.get("nuvarande_kurs", 0)
    targets = berakna_riktkurser(bolag)
    if not targets:
        st.warning("Ej tillräckligt data för att beräkna riktkurser.")
        return

    # Beräkna undervärdering i %
    undervard_pe_ar = (targets["target_pe_ar"] - nuvarande_kurs) / nuvarande_kurs * 100 if nuvarande_kurs else 0
    undervard_pe_nasta_ar = (targets["target_pe_nasta_ar"] - nuvarande_kurs) / nuvarande_kurs * 100 if nuvarande_kurs else 0
    undervard_ps_ar = (targets["target_ps_ar"] - nuvarande_kurs) / nuvarande_kurs * 100 if nuvarande_kurs else 0
    undervard_ps_nasta_ar = (targets["target_ps_nasta_ar"] - nuvarande_kurs) / nuvarande_kurs * 100 if nuvarande_kurs else 0

    st.markdown("### Riktkurser och undervärdering")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Targetkurs P/E (i år):** {:.2f} kr".format(targets["target_pe_ar"]))
        st.write("**Undervärdering P/E (i år):** {:.1f}%".format(undervard_pe_ar))
        st.write("**Targetkurs P/E (nästa år):** {:.2f} kr".format(targets["target_pe_nasta_ar"]))
        st.write("**Undervärdering P/E (nästa år):** {:.1f}%".format(undervard_pe_nasta_ar))

    with col2:
        st.write("**Targetkurs P/S (i år):** {:.2f} kr".format(targets["target_ps_ar"]))
        st.write("**Undervärdering P/S (i år):** {:.1f}%".format(undervard_ps_ar))
        st.write("**Targetkurs P/S (nästa år):** {:.2f} kr".format(targets["target_ps_nasta_ar"]))
        st.write("**Undervärdering P/S (nästa år):** {:.1f}%".format(undervard_ps_nasta_ar))

    # Köpvärd nivå = targetkurs minus 30%
    st.markdown("### Köpvärd nivå (30% rabatt)")
    st.write("P/E (i år): {:.2f} kr".format(targets["target_pe_ar"] * 0.7))
    st.write("P/E (nästa år): {:.2f} kr".format(targets["target_pe_nasta_ar"] * 0.7))
    st.write("P/S (i år): {:.2f} kr".format(targets["target_ps_ar"] * 0.7))
    st.write("P/S (nästa år): {:.2f} kr".format(targets["target_ps_nasta_ar"] * 0.7))
