def beräkna_targetkurser(bolag):
    snitt_pe = (bolag["pe_1"] + bolag["pe_2"] + bolag["pe_3"] + bolag["pe_4"]) / 4
    snitt_ps = (bolag["ps_1"] + bolag["ps_2"] + bolag["ps_3"] + bolag["ps_4"]) / 4

    target_pe_i_ar = snitt_pe * bolag["vinst_i_ar"] * 0.9
    target_pe_nasta_ar = snitt_pe * bolag["vinst_nasta_ar"] * 0.9

    target_ps_i_ar = snitt_ps * bolag["oms_tillv_i_ar"] / bolag["ps_nuvarande"] * bolag["kurs"] * 0.9
    target_ps_nasta_ar = snitt_ps * bolag["oms_tillv_i_ar"] * bolag["oms_tillv_nasta_ar"] / bolag["ps_nuvarande"] * bolag["kurs"] * 0.9

    return {
        "target_pe_i_ar": round(target_pe_i_ar, 2),
        "target_pe_nasta_ar": round(target_pe_nasta_ar, 2),
        "target_ps_i_ar": round(target_ps_i_ar, 2),
        "target_ps_nasta_ar": round(target_ps_nasta_ar, 2)
    }

def beräkna_undervärdering(nuvarande_kurs, targetkurs):
    if targetkurs <= 0:
        return -100.0
    return round((targetkurs - nuvarande_kurs) / targetkurs * 100, 1)

def max_undervärdering(kurs, targets):
    värderingar = [
        beräkna_undervärdering(kurs, targets["target_pe_i_ar"]),
        beräkna_undervärdering(kurs, targets["target_pe_nasta_ar"]),
        beräkna_undervärdering(kurs, targets["target_ps_i_ar"]),
        beräkna_undervärdering(kurs, targets["target_ps_nasta_ar"]),
    ]
    return round(max(värderingar), 1)
