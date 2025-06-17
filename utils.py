def berakna_targetkurser_och_undervardering(data):
    """
    Tar emot en dict med flera bolag: {bolagsnamn: info_dict, ...}
    Beräknar targetkurser och undervärdering för varje bolag.
    Returnerar en dict med samma struktur och extra nycklar.
    """
    resultat = {}
    for bolag, info in data.items():
        kurs = info.get("kurs", 0)
        pe_1 = info.get("pe_1", 0)
        pe_2 = info.get("pe_2", 0)
        pe_3 = info.get("pe_3", 0)
        pe_4 = info.get("pe_4", 0)
        ps_1 = info.get("ps_1", 0)
        ps_2 = info.get("ps_2", 0)
        ps_3 = info.get("ps_3", 0)
        ps_4 = info.get("ps_4", 0)
        vinst_i_ar = info.get("vinst_i_ar", 0)
        vinst_nasta_ar = info.get("vinst_nasta_ar", 0)
        oms_tillv_i_ar = info.get("oms_tillv_i_ar", 0)
        oms_tillv_nasta_ar = info.get("oms_tillv_nasta_ar", 0)
        ps_nuvarande = info.get("ps_nuvarande", 0)

        pe_snitt = sum([pe_1, pe_2, pe_3, pe_4]) / 4 if all(isinstance(x, (int, float)) for x in [pe_1, pe_2, pe_3, pe_4]) else 0
        ps_snitt = sum([ps_1, ps_2, ps_3, ps_4]) / 4 if all(isinstance(x, (int, float)) for x in [ps_1, ps_2, ps_3, ps_4]) else 0

        target_pe_i_ar = pe_snitt * vinst_i_ar * 0.9
        target_pe_nasta_ar = pe_snitt * vinst_nasta_ar * 0.9

        target_ps_i_ar = ps_snitt * oms_tillv_i_ar * kurs * 0.9 if ps_nuvarande != 0 else 0
        target_ps_nasta_ar = ps_snitt * oms_tillv_i_ar * oms_tillv_nasta_ar * kurs * 0.9 if ps_nuvarande != 0 else 0

        undervardering_pe = ((target_pe_i_ar - kurs) / kurs * 100) if kurs != 0 else 0
        undervardering_ps = ((target_ps_i_ar - kurs) / kurs * 100) if kurs != 0 else 0
        max_undervardering = max(undervardering_pe, undervardering_ps)

        resultat[bolag] = {
            **info,
            "target_pe_i_ar": target_pe_i_ar,
            "target_pe_nasta_ar": target_pe_nasta_ar,
            "target_ps_i_ar": target_ps_i_ar,
            "target_ps_nasta_ar": target_ps_nasta_ar,
            "undervardering_procent": max_undervardering,
        }
    return resultat

def berakna_targetkurser_och_undervardering_enkel(info):
    """
    Tar emot en dict med info för ett bolag.
    Returnerar dict med beräkningar och nya nycklar.
    """
    kurs = info.get("kurs", 0)
    pe_1 = info.get("pe_1", 0)
    pe_2 = info.get("pe_2", 0)
    pe_3 = info.get("pe_3", 0)
    pe_4 = info.get("pe_4", 0)
    ps_1 = info.get("ps_1", 0)
    ps_2 = info.get("ps_2", 0)
    ps_3 = info.get("ps_3", 0)
    ps_4 = info.get("ps_4", 0)
    vinst_i_ar = info.get("vinst_i_ar", 0)
    vinst_nasta_ar = info.get("vinst_nasta_ar", 0)
    oms_tillv_i_ar = info.get("oms_tillv_i_ar", 0)
    oms_tillv_nasta_ar = info.get("oms_tillv_nasta_ar", 0)
    ps_nuvarande = info.get("ps_nuvarande", 0)

    pe_snitt = sum([pe_1, pe_2, pe_3, pe_4]) / 4 if all(isinstance(x, (int, float)) for x in [pe_1, pe_2, pe_3, pe_4]) else 0
    ps_snitt = sum([ps_1, ps_2, ps_3, ps_4]) / 4 if all(isinstance(x, (int, float)) for x in [ps_1, ps_2, ps_3, ps_4]) else 0

    target_pe_i_ar = pe_snitt * vinst_i_ar * 0.9
    target_pe_nasta_ar = pe_snitt * vinst_nasta_ar * 0.9

    target_ps_i_ar = ps_snitt * oms_tillv_i_ar * kurs * 0.9 if ps_nuvarande != 0 else 0
    target_ps_nasta_ar = ps_snitt * oms_tillv_i_ar * oms_tillv_nasta_ar * kurs * 0.9 if ps_nuvarande != 0 else 0

    undervardering_pe = ((target_pe_i_ar - kurs) / kurs * 100) if kurs != 0 else 0
    undervardering_ps = ((target_ps_i_ar - kurs) / kurs * 100) if kurs != 0 else 0
    max_undervardering = max(undervardering_pe, undervardering_ps)

    return {
        **info,
        "target_pe_i_ar": target_pe_i_ar,
        "target_pe_nasta_ar": target_pe_nasta_ar,
        "target_ps_i_ar": target_ps_i_ar,
        "target_ps_nasta_ar": target_ps_nasta_ar,
        "undervardering_procent": max_undervardering,
    }


def formattera_kurs(kurs):
    """Formaterar ett kursvärde med två decimaler och 'kr' efter."""
    try:
        return f"{float(kurs):.2f} kr"
    except (ValueError, TypeError):
        return "N/A"


def formattera_procent(varde):
    """Formaterar ett värde som procent med en decimal och % efter."""
    try:
        return f"{float(varde):.1f} %"
    except (ValueError, TypeError):
        return "N/A"
