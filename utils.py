def beräkna_targetkurser(b, metod="pe"):
    snitt_pe = sum(b["pe"]) / 4
    snitt_ps = sum(b["ps"]) / 4

    if metod == "pe":
        target_i_ar = snitt_pe * b["vinst_i_ar"] * 0.9
        target_nasta = snitt_pe * b["vinst_nasta_ar"] * 0.9
    elif metod == "ps":
        tillv_kombo = b["tillvaxt_i_ar"] * b["tillvaxt_nasta_ar"]
        target_i_ar = snitt_ps * b["tillvaxt_i_ar"] / b["nuvarande_ps"] * b["nuvarande_kurs"] * 0.9
        target_nasta = snitt_ps * tillv_kombo / b["nuvarande_ps"] * b["nuvarande_kurs"] * 0.9
    else:
        target_i_ar = target_nasta = 0

    return target_i_ar, target_nasta

def beräkna_undervärdering(kurs, target):
    if target == 0:
        return 0
    return int(round((target - kurs) / target * 100))
