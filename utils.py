def berakna_targetkurser_och_undervardering(bolag):
    """
    Beräknar targetkurser och undervärdering baserat på inmatade nyckeltal.

    Args:
        bolag (dict): Dictionary med bolagsdata

    Returns:
        dict: Dictionary med beräknade targetkurser och undervärdering i procent
    """
    # Läs in värden från bolag, med default 0 om saknas
    kurs = bolag.get("kurs", 0)
    pe_nuvarande = bolag.get("pe_nuvarande", 0)
    pe_1 = bolag.get("pe_1", 0)
    pe_2 = bolag.get("pe_2", 0)
    pe_3 = bolag.get("pe_3", 0)
    pe_4 = bolag.get("pe_4", 0)

    ps_nuvarande = bolag.get("ps_nuvarande", 0)
    ps_1 = bolag.get("ps_1", 0)
    ps_2 = bolag.get("ps_2", 0)
    ps_3 = bolag.get("ps_3", 0)
    ps_4 = bolag.get("ps_4", 0)
    vinst_i_ar = bolag.get("vinst_i_ar", 0)
    vinst_nasta_ar = bolag.get("vinst_nasta_ar", 0)
    oms_tillv_i_ar = bolag.get("oms_tillv_i_ar", 0)
    oms_tillv_nasta_ar = bolag.get("oms_tillv_nasta_ar", 0)

    # Medelvärde P/E och P/S
    pe_values = [pe_1, pe_2, pe_3, pe_4]
    pe_values = [v for v in pe_values if v > 0]
    pe_medel = sum(pe_values) / len(pe_values) if pe_values else 0

    ps_values = [ps_1, ps_2, ps_3, ps_4]
    ps_values = [v for v in ps_values if v > 0]
    ps_medel = sum(ps_values) / len(ps_values) if ps_values else 0

    # Targetkurs P/E (i år och nästa år) med 10% säkerhetsmarginal
    target_pe_i_ar = pe_medel * vinst_i_ar * 0.9 if pe_medel > 0 else 0
    target_pe_nasta_ar = pe_medel * vinst_nasta_ar * 0.9 if pe_medel > 0 else 0

    # Targetkurs P/S (i år och nästa år)
    target_ps_i_ar = 0
    target_ps_nasta_ar = 0
    if ps_medel > 0 and ps_nuvarande > 0:
        target_ps_i_ar = ps_medel * oms_tillv_i_ar * kurs * 0.9
        target_ps_nasta_ar = ps_medel * oms_tillv_i_ar * oms_tillv_nasta_ar * kurs * 0.9

    # Beräkna undervärdering i procent baserat på max av P/E och P/S
    undervard_pe_i_ar = (target_pe_i_ar - kurs) / kurs * 100 if kurs > 0 else 0
    undervard_pe_nasta_ar = (target_pe_nasta_ar - kurs) / kurs * 100 if kurs > 0 else 0
    undervard_ps_i_ar = (target_ps_i_ar - kurs) / kurs * 100 if kurs > 0 else 0
    undervard_ps_nasta_ar = (target_ps_nasta_ar - kurs) / kurs * 100 if kurs > 0 else 0

    undervard_max = max(undervard_pe_i_ar, undervard_pe_nasta_ar, undervard_ps_i_ar, undervard_ps_nasta_ar)

    return {
        "target_pe_i_ar": round(target_pe_i_ar, 2),
        "target_pe_nasta_ar": round(target_pe_nasta_ar, 2),
        "target_ps_i_ar": round(target_ps_i_ar, 2),
        "target_ps_nasta_ar": round(target_ps_nasta_ar, 2),
        "undervardering_procent": round(undervard_max, 1),
    }
