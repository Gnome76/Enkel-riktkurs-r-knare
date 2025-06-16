def beräkna_targetkurser(data: dict, metod="pe"):
    try:
        kurs = float(data["nuvarande_kurs"])
        if metod == "pe":
            pe_tal = [float(data.get(f"pe{i}", 0)) for i in range(1, 5)]
            snitt_pe = sum(pe_tal) / len(pe_tal)
            vinst_i_ar = float(data.get("vinst_i_ar", 0))
            vinst_nasta_ar = float(data.get("vinst_nasta_ar", 0))
            target_pe_i_ar = snitt_pe * vinst_i_ar * 0.9
            target_pe_nasta_ar = snitt_pe * vinst_nasta_ar * 0.9
            return target_pe_i_ar, target_pe_nasta_ar

        elif metod == "ps":
            ps_tal = [float(data.get(f"ps{i}", 0)) for i in range(1, 5)]
            snitt_ps = sum(ps_tal) / len(ps_tal)
            tillv_i_ar = float(data.get("tillv_i_ar", 0)) / 100
            tillv_nasta_ar = float(data.get("tillv_nasta_ar", 0)) / 100
            nuvarande_ps = float(data.get("nuvarande_ps", 1)) or 1  # undvik division med 0

            target_ps_i_ar = (snitt_ps * tillv_i_ar / nuvarande_ps * kurs) * 0.9
            target_ps_nasta_ar = (snitt_ps * tillv_i_ar * tillv_nasta_ar / nuvarande_ps * kurs) * 0.9
            return target_ps_i_ar, target_ps_nasta_ar

    except Exception:
        return 0.0, 0.0


def beräkna_undervärdering(data: dict, metod="pe"):
    try:
        kurs = float(data["nuvarande_kurs"])
        target1, target2 = beräkna_targetkurser(data, metod)
        underv1 = (target1 - kurs) / kurs * 100
        underv2 = (target2 - kurs) / kurs * 100
        return underv1, underv2
    except Exception:
        return 0.0, 0.0
