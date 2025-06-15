def berakna_targetkurser(bolag):
    # Säkerhetsmarginal
    sm = 0.9

    # Undvik division med noll
    if bolag["nuvarande_pe"] == 0 or bolag["nuvarande_ps"] == 0:
        return {}

    # Snittvärden
    snitt_pe = sum([bolag.get(f"pe{i}", 0) for i in range(1, 5)]) / 4
    snitt_ps = sum([bolag.get(f"ps{i}", 0) for i in range(1, 5)]) / 4

    # Targetkurser P/E
    target_pe_iar = snitt_pe * bolag["vinst_iar"] * sm
    target_pe_nastaar = snitt_pe * bolag["vinst_nastaar"] * sm

    # Targetkurser P/S
    oms_tillv_iar_faktor = bolag["oms_tillv_iar"] / 100
    oms_tillv_nastaar_faktor = bolag["oms_tillv_nastaar"] / 100

    target_ps_iar = (snitt_ps * oms_tillv_iar_faktor / bolag["nuvarande_ps"]) * bolag["nuvarande_kurs"] * sm
    target_ps_nastaar = (snitt_ps * oms_tillv_iar_faktor * oms_tillv_nastaar_faktor / bolag["nuvarande_ps"]) * bolag["nuvarande_kurs"] * sm

    # Undervärdering P/E och P/S (nästa år)
    undervardering_pe_pct = (target_pe_nastaar - bolag["nuvarande_kurs"]) / bolag["nuvarande_kurs"] * 100
    undervardering_ps_pct = (target_ps_nastaar - bolag["nuvarande_kurs"]) / bolag["nuvarande_kurs"] * 100

    # Köpvärd nivå (30 % rabatt)
    kopvard_pe = target_pe_nastaar * 0.7
    kopvard_ps = target_ps_nastaar * 0.7

    return {
        "target_pe_iar": round(target_pe_iar, 2),
        "target_pe_nastaar": round(target_pe_nastaar, 2),
        "target_ps_iar": round(target_ps_iar, 2),
        "target_ps_nastaar": round(target_ps_nastaar, 2),
        "undervardering_pe_pct": round(undervardering_pe_pct, 1),
        "undervardering_ps_pct": round(undervardering_ps_pct, 1),
        "kopvard_pe": round(kopvard_pe, 2),
        "kopvard_ps": round(kopvard_ps, 2)
    }
