def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

def medelvarde(lista):
    tal = [safe_float(x) for x in lista if safe_float(x) is not None]
    if not tal:
        return None
    return sum(tal) / len(tal)

def beräkna_targetkurser(info: dict, metod: str = "pe"):
    # Metod kan vara "pe" eller "ps"
    # För P/E: targetkurs = medelvärde av P/E 1-4 * vinst (i år eller nästa år) * 0.9 (säkerhetsmarginal)
    # För P/S: targetkurs = medelvärde av P/S 1-4 * (omsättningstillväxt i år och nästa år) * nuvarande kurs * 0.9

    nuvarande_kurs = safe_float(info.get("nuvarande_kurs"))
    if metod == "pe":
        pe_varden = [info.get(f"pe_{i}") for i in range(1, 5)]
        pe_varden_float = [safe_float(x) for x in pe_varden]
        pe_medel = medelvarde(pe_varden_float)
        vinst_i_ar = safe_float(info.get("vinst_i_ar"))
        vinst_nasta_ar = safe_float(info.get("vinst_nasta_ar"))

        if pe_medel is None or vinst_i_ar is None or vinst_nasta_ar is None:
            return None

        target_i_ar = pe_medel * vinst_i_ar * 0.9
        target_nasta_ar = pe_medel * vinst_nasta_ar * 0.9
        return target_i_ar, target_nasta_ar

    elif metod == "ps":
        ps_varden = [info.get(f"ps_{i}") for i in range(1, 5)]
        ps_varden_float = [safe_float(x) for x in ps_varden]
        ps_medel = medelvarde(ps_varden_float)

        oms_tillvxt_i_ar = safe_float(info.get("oms_tillvxt_i_ar"))  # i procent, t.ex 10 för 10%
        oms_tillvxt_nasta_ar = safe_float(info.get("oms_tillvxt_nasta_ar"))

        if ps_medel is None or oms_tillvxt_i_ar is None or oms_tillvxt_nasta_ar is None or nuvarande_kurs is None:
            return None

        # Omvandla procent till decimal, t.ex 10% -> 1.10
        oms_faktor_i_ar = 1 + oms_tillvxt_i_ar / 100
        oms_faktor_nasta_ar = 1 + oms_tillvxt_nasta_ar / 100

        # Targetkurs P/S i år och nästa år
        target_i_ar = ps_medel * oms_faktor_i_ar * nuvarande_kurs * 0.9
        target_nasta_ar = ps_medel * oms_faktor_i_ar * oms_faktor_nasta_ar * nuvarande_kurs * 0.9

        return target_i_ar, target_nasta_ar

    else:
        return None


def beräkna_undervärdering(info: dict, metod: str = "pe"):
    # Undervärdering i % = (targetkurs - nuvarande kurs) / targetkurs * 100
    nuvarande_kurs = safe_float(info.get("nuvarande_kurs"))
    target = beräkna_targetkurser(info, metod)
    if nuvarande_kurs is None or target is None:
        return None
    target_i_ar, target_nasta_ar = target
    underv_i_ar = ((target_i_ar - nuvarande_kurs) / target_i_ar) * 100 if target_i_ar else None
    underv_nasta_ar = ((target_nasta_ar - nuvarande_kurs) / target_nasta_ar) * 100 if target_nasta_ar else None
    return underv_i_ar, underv_nasta_ar
