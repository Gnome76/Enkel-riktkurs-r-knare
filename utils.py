def berakna_undervarderingar(bolag: dict):
    kurs = bolag.get("kurs", 1.0)
    pe_tal = [bolag.get(f"pe_{i}", 0.0) for i in range(1, 5)]
    ps_tal = [bolag.get(f"ps_{i}", 0.0) for i in range(1, 5)]
    pe_nuvarande = bolag.get("pe_nuvarande", 1.0)
    ps_nuvarande = bolag.get("ps_nuvarande", 1.0)
    vinst_i_ar = bolag.get("vinst_i_ar", 0.01)
    vinst_nasta_ar = bolag.get("vinst_nasta_ar", 0.01)
    oms_tillv_i_ar = bolag.get("oms_tillv_i_ar", 0.01)
    oms_tillv_nasta_ar = bolag.get("oms_tillv_nasta_ar", 0.01)

    pe_snitt = sum(pe_tal) / len(pe_tal) if pe_tal else 0.0
    ps_snitt = sum(ps_tal) / len(ps_tal) if ps_tal else 0.0

    pe_target_i_ar = pe_snitt * vinst_i_ar * 0.9
    pe_target_nasta_ar = pe_snitt * vinst_nasta_ar * 0.9
    ps_target_i_ar = ps_snitt * oms_tillv_i_ar / ps_nuvarande * kurs * 0.9
    ps_target_nasta_ar = ps_snitt * oms_tillv_i_ar * oms_tillv_nasta_ar / ps_nuvarande * kurs * 0.9

    undervardering_pe = max(((pe_target_i_ar - kurs) / kurs) * 100, ((pe_target_nasta_ar - kurs) / kurs) * 100)
    undervardering_ps = max(((ps_target_i_ar - kurs) / kurs) * 100, ((ps_target_nasta_ar - kurs) / kurs) * 100)
    undervardering = max(undervardering_pe, undervardering_ps)

    return pe_target_i_ar, pe_target_nasta_ar, ps_target_i_ar, ps_target_nasta_ar, undervardering
