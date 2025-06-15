def berakna_targetkurser(bolag):
    """
    Beräknar targetkurser och undervärdering för ett bolag baserat på angivna nyckeltal.
    Modifierar och returnerar bolaget med nya fält.
    """

    säkerhetsmarginal = 0.9  # 10% säkerhetsmarginal

    # Medelvärden P/E och P/S
    pe_medel = sum([bolag.get(f"pe{i}", 0) for i in range(1, 5)]) / 4
    ps_medel = sum([bolag.get(f"ps{i}", 0) for i in range(1, 5)]) / 4

    # Targetkurs P/E
    try:
        bolag["target_pe_aar"] = round(pe_medel * bolag["vinst_aar"] * säkerhetsmarginal, 2)
    except:
        bolag["target_pe_aar"] = 0.0

    try:
        bolag["target_pe_nasta_aar"] = round(pe_medel * bolag["vinst_nasta_aar"] * säkerhetsmarginal, 2)
    except:
        bolag["target_pe_nasta_aar"] = 0.0

    # Targetkurs P/S
    try:
        tillvaxt_aar = bolag["omsattningstillvaxt_aar"]
        bolag["target_ps_aar"] = round((ps_medel * tillvaxt_aar / bolag["nuvarande_ps"]) * bolag["nuvarande_kurs"] * säkerhetsmarginal, 2)
    except:
        bolag["target_ps_aar"] = 0.0

    try:
        tillvaxt_total = bolag["omsattningstillvaxt_aar"] * bolag["omsattningstillvaxt_nasta_aar"]
        bolag["target_ps_nasta_aar"] = round((ps_medel * tillvaxt_total / bolag["nuvarande_ps"]) * bolag["nuvarande_kurs"] * säkerhetsmarginal, 2)
    except:
        bolag["target_ps_nasta_aar"] = 0.0

    # Undervärdering
    try:
        underv_pe = (bolag["target_pe_nasta_aar"] / bolag["nuvarande_kurs"]) - 1
    except:
        underv_pe = 0.0

    try:
        underv_ps = (bolag["target_ps_nasta_aar"] / bolag["nuvarande_kurs"]) - 1
    except:
        underv_ps = 0.0

    bolag["undervardering_pct"] = round(max(underv_pe, underv_ps) * 100, 1)  # Mest fördelaktiga

    # Köpvärd nivå (30% rabatt från target)
    bolag["koptillfalle_pe"] = round(bolag["target_pe_nasta_aar"] * 0.7, 2)
    bolag["koptillfalle_ps"] = round(bolag["target_ps_nasta_aar"] * 0.7, 2)

    return bolag
