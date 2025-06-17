def berakna_targetkurser_och_undervardering(data):
    resultat = {}
    for bolag, info in data.items():
        kurs = info.get("kurs", 0.0)

        # Vinst
        vinst_i_ar = info.get("vinst_i_ar", 0.0)
        vinst_nasta_ar = info.get("vinst_nasta_ar", 0.0)

        # Omsättningstillväxt
        tillv_i_ar = info.get("oms_tillv_i_ar", 1.0)
        tillv_nasta_ar = info.get("oms_tillv_nasta_ar", 1.0)

        # PE-siffror
        pe_nuvarande = info.get("pe_nuvarande", 1.0)
        pe_snitt = sum([info.get(f"pe_{i}", 0.0) for i in range(1, 5)]) / 4

        # PS-siffror
        ps_nuvarande = info.get("ps_nuvarande", 1.0)
        ps_snitt = sum([info.get(f"ps_{i}", 0.0) for i in range(1, 5)]) / 4

        # Targetkurser
        target_pe_i_ar = pe_snitt * vinst_i_ar * 0.9
        target_pe_nasta_ar = pe_snitt * vinst_nasta_ar * 0.9

        target_ps_i_ar = ps_snitt * tillv_i_ar / ps_nuvarande * kurs * 0.9
        target_ps_nasta_ar = ps_snitt * tillv_i_ar * tillv_nasta_ar / ps_nuvarande * kurs * 0.9

        # Undervärdering i procent jämfört med högsta target
        max_target = max(target_pe_i_ar, target_pe_nasta_ar, target_ps_i_ar, target_ps_nasta_ar)
        undervardering = (max_target - kurs) / kurs * 100

        resultat[bolag] = {
            "target_pe_i_ar": target_pe_i_ar,
            "target_pe_nasta_ar": target_pe_nasta_ar,
            "target_ps_i_ar": target_ps_i_ar,
            "target_ps_nasta_ar": target_ps_nasta_ar,
            "undervardering_procent": undervardering,
        }

    return resultat
