def snitt(lista):
    filtered = [x for x in lista if x > 0]
    return sum(filtered) / len(filtered) if filtered else 0

def berakna_targetkurs_pe(vinst_1, vinst_2, pe1, pe2, pe3, pe4):
    pe_snitt = snitt([pe1, pe2, pe3, pe4])
    # 10% säkerhetsmarginal
    target_1 = pe_snitt * vinst_1 * 0.9 if vinst_1 and pe_snitt else 0
    target_2 = pe_snitt * vinst_2 * 0.9 if vinst_2 and pe_snitt else 0
    return target_1, target_2

def berakna_targetkurs_ps(kurs, oms_tillv_1, oms_tillv_2, ps1, ps2, ps3, ps4):
    ps_snitt = snitt([ps1, ps2, ps3, ps4])
    # Multiplicerar omsättningstillväxt (procent / 100)
    oms_tillv_1_frac = oms_tillv_1 / 100 if oms_tillv_1 else 0
    oms_tillv_2_frac = oms_tillv_2 / 100 if oms_tillv_2 else 0
    if kurs and ps_snitt and oms_tillv_1_frac:
        target_1 = ps_snitt * oms_tillv_1_frac * kurs * 0.9
    else:
        target_1 = 0
    if kurs and ps_snitt and oms_tillv_1_frac and oms_tillv_2_frac:
        target_2 = ps_snitt * oms_tillv_1_frac * oms_tillv_2_frac * kurs * 0.9
    else:
        target_2 = 0
    return target_1, target_2

def berakna_undervardering(kurs, targetkurs):
    if not kurs or not targetkurs:
        return 0
    return (targetkurs - kurs) / kurs * 100
