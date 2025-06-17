def berakna_targetkurser_och_undervardering(info):
    kurs = info["kurs"]
    vinst_i_ar = info["vinst_i_ar"]
    vinst_nasta_ar = info["vinst_nasta_ar"]
    oms_tillv_i_ar = info["oms_tillv_i_ar"]
    oms_tillv_nasta_ar = info["oms_tillv_nasta_ar"]

    snitt_pe = sum([info[f"pe_{i}"] for i in range(1, 5)]) / 4
    snitt_ps = sum([info[f"ps_{i}"] for i in range(1, 5)]) / 4
    pe_nuv = info["pe_nuvarande"]
    ps_nuv = info["ps_nuvarande"]

    # Targetkurser med 10 % säkerhetsmarginal
    target_pe_i_ar = snitt_pe * vinst_i_ar * 0.9
    target_pe_nasta_ar = snitt_pe * vinst_nasta_ar * 0.9

    target_ps_i_ar = snitt_ps * oms_tillv_i_ar / ps_nuv * kurs * 0.9
    target_ps_nasta_ar = snitt_ps * oms_tillv_i_ar * oms_tillv_nasta_ar / ps_nuv * kurs * 0.9

    undervardering_pe = (target_pe_nasta_ar - kurs) / kurs
    undervardering_ps = (target_ps_nasta_ar - kurs) / kurs
    max_undervardering = max(undervardering_pe, undervardering_ps) * 100

    return {
        "target_pe_i_ar": target_pe_i_ar,
        "target_pe_nasta_ar": target_pe_nasta_ar,
        "target_ps_i_ar": target_ps_i_ar,
        "target_ps_nasta_ar": target_ps_nasta_ar,
        "undervardering_procent": max_undervardering
    }
