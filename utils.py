def berakna_targetkurser(info):
    try:
        # Nuvarande värden
        kurs = info.get("kurs", 0)
        pe_nu = info.get("pe_nu", 0)
        ps_nu = info.get("ps_nu", 0)

        # Vinst
        vinst_1 = info.get("vinst_i_ar", 0)
        vinst_2 = info.get("vinst_nasta_ar", 0)

        # Tillväxt
        tillvaxt_1 = info.get("oms_tillvaxt_i_ar", 0) / 100
        tillvaxt_2 = info.get("oms_tillvaxt_nasta_ar", 0) / 100

        # P/E-data
        pe_tal = [info.get(f"pe_{i}", 0) for i in range(1, 5)]
        pe_snitt = sum(pe_tal) / len(pe_tal) if pe_tal else 0
        pe_snitt *= 0.9  # säkerhetsmarginal 10 %

        # P/S-data
        ps_tal = [info.get(f"ps_{i}", 0) for i in range(1, 5)]
        ps_snitt = sum(ps_tal) / len(ps_tal) if ps_tal else 0
        ps_snitt *= 0.9  # säkerhetsmarginal 10 %

        # Target P/E
        target_pe_1 = pe_snitt * vinst_1
        target_pe_2 = pe_snitt * vinst_2

        # Target P/S
        target_ps_1 = ps_snitt * tillvaxt_1 * kurs / ps_nu if ps_nu > 0 else 0
        target_ps_2 = ps_snitt * tillvaxt_1 * tillvaxt_2 * kurs / ps_nu if ps_nu > 0 else 0

        # Undervärdering i %
        underv_pe_1 = ((target_pe_1 - kurs) / kurs) * 100 if kurs > 0 else 0
        underv_pe_2 = ((target_pe_2 - kurs) / kurs) * 100 if kurs > 0 else 0

        underv_ps_1 = ((target_ps_1 - kurs) / kurs) * 100 if kurs > 0 else 0
        underv_ps_2 = ((target_ps_2 - kurs) / kurs) * 100 if kurs > 0 else 0

        # Köpvärd nivå = targetkurs minus 30 %
        kopvard_pe_1 = target_pe_1 * 0.7
        kopvard_pe_2 = target_pe_2 * 0.7
        kopvard_ps_1 = target_ps_1 * 0.7
        kopvard_ps_2 = target_ps_2 * 0.7

        return {
            "target_pe_1": round(target_pe_1, 2),
            "target_pe_2": round(target_pe_2, 2),
            "target_ps_1": round(target_ps_1, 2),
            "target_ps_2": round(target_ps_2, 2),
            "underv_pe_1": round(underv_pe_1, 1),
            "underv_pe_2": round(underv_pe_2, 1),
            "underv_ps_1": round(underv_ps_1, 1),
            "underv_ps_2": round(underv_ps_2, 1),
            "kopvard_pe_1": round(kopvard_pe_1, 2),
            "kopvard_pe_2": round(kopvard_pe_2, 2),
            "kopvard_ps_1": round(kopvard_ps_1, 2),
            "kopvard_ps_2": round(kopvard_ps_2, 2),
        }

    except Exception as e:
        return {
            "target_pe_1": 0,
            "target_pe_2": 0,
            "target_ps_1": 0,
            "target_ps_2": 0,
            "underv_pe_1": 0,
            "underv_pe_2": 0,
            "underv_ps_1": 0,
            "underv_ps_2": 0,
            "kopvard_pe_1": 0,
            "kopvard_pe_2": 0,
            "kopvard_ps_1": 0,
            "kopvard_ps_2": 0,
        }
