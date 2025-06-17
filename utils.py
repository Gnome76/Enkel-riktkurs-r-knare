def berakna_targetkurser_och_undervardering(info):
    kurs = info.get("kurs", 0)
    pe_nuvarande = info.get("pe_nuvarande", 1)
    ps_nuvarande = info.get("ps_nuvarande", 1)

    pe_lista = [info.get(f"pe_{i}", 0) for i in range(1, 5)]
    ps_lista = [info.get(f"ps_{i}", 0) for i in range(1, 5)]

    pe_snitt = sum(pe_lista) / len(pe_lista) if pe_lista else 0
    ps_snitt = sum(ps_lista) / len(ps_lista) if ps_lista else 0

    vinst_i_ar = info.get("vinst_i_ar", 0)
    vinst_nasta_ar = info.get("vinst_nasta_ar", 0)

    oms_tillv_i_ar = info.get("oms_tillv_i_ar", 1)
    oms_tillv_nasta_ar = info.get("oms_tillv_nasta_ar", 1)

    # Target P/E
    target_pe_i_ar = pe_snitt * vinst_i_ar * 0.9
    target_pe_nasta_ar = pe_snitt * vinst_nasta_ar * 0.9

    # Target P/S
    target_ps_i_ar = ps_snitt * oms_tillv_i_ar / ps_nuvarande * kurs * 0.9 if ps_nuvarande else 0
    target_ps_nasta_ar = ps_snitt * oms_tillv_i_ar * oms_tillv_nasta_ar / ps_nuvarande * kurs * 0.9 if ps_nuvarande else 0

    # Undervärdering
    max_target = max(target_pe_i_ar, target_pe_nasta_ar, target_ps_i_ar, target_ps_nasta_ar)
    undervardering = ((max_target - kurs) / kurs) * 100 if kurs else 0

    return {
        "target_pe_i_ar": target_pe_i_ar,
        "target_pe_nasta_ar": target_pe_nasta_ar,
        "target_ps_i_ar": target_ps_i_ar,
        "target_ps_nasta_ar": target_ps_nasta_ar,
        "max_undervardering": undervardering
    }
