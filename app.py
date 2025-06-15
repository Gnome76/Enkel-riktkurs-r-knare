import streamlit as st
from forms import visa_inmatningsform
from utils import berakna_targetkurser, filtrera_undervarderade
from data_handler import las_data, spara_data

def main():
    st.title("Aktieanalys – Undervärdering P/E & P/S")

    # Ladda bolagsdata från JSON
    bolag_list = las_data()

    # Visa formulär för nytt bolag
    nytt_bolag = visa_inmatningsform()
    if nytt_bolag:
        # Beräkna targetkurser och undervärdering
        berakna_targetkurser(nytt_bolag)
        bolag_list.append(nytt_bolag)
        spara_data(bolag_list)
        st.success(f"Bolaget '{nytt_bolag['namn']}' har lagts till.")

    # Beräkna targetkurser för alla bolag (för säkerhets skull)
    for bolag in bolag_list:
        berakna_targetkurser(bolag)

    # Checkbox för filtrering undervärderade bolag
    visa_endast_undervarderade = st.checkbox("Visa endast undervärderade (≥30%)")

    # Filtrera om valt
    att_visas = (
        filtrera_undervarderade(bolag_list, 30)
        if visa_endast_undervarderade
        else bolag_list
    )

    if not att_visas:
        st.info("Inga bolag att visa.")
        return

    # Visa bolagslista i tabell
    import pandas as pd

    df = pd.DataFrame(att_visas)

    # Välj kolumner att visa och formatera undervärderingsprocent
    kolumner = [
        "namn",
        "nuvarande_kurs",
        "target_pe_iår",
        "target_pe_nästa_år",
        "target_ps_iår",
        "target_ps_nästa_år",
        "undervardering_pe_pct",
        "undervardering_ps_pct",
        "köpvärd_pe",
        "köpvärd_ps",
    ]
    df_vis = df[kolumner].copy()
    df_vis["undervardering_pe_pct"] = df_vis["undervardering_pe_pct"].map("{:.1f}%".format)
    df_vis["undervardering_ps_pct"] = df_vis["undervardering_ps_pct"].map("{:.1f}%".format)
    df_vis["nuvarande_kurs"] = df_vis["nuvarande_kurs"].map("{:.2f}".format)
    df_vis["target_pe_iår"] = df_vis["target_pe_iår"].map("{:.2f}".format)
    df_vis["target_pe_nästa_år"] = df_vis["target_pe_nästa_år"].map("{:.2f}".format)
    df_vis["target_ps_iår"] = df_vis["target_ps_iår"].map("{:.2f}".format)
    df_vis["target_ps_nästa_år"] = df_vis["target_ps_nästa_år"].map("{:.2f}".format)
    df_vis["köpvärd_pe"] = df_vis["köpvärd_pe"].map("{:.2f}".format)
    df_vis["köpvärd_ps"] = df_vis["köpvärd_ps"].map("{:.2f}".format)

    st.dataframe(df_vis.style.set_properties(**{"text-align": "center"}))

if __name__ == "__main__":
    main()
