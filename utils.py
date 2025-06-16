def beräkna_targetkurser(bolag: dict) -> dict:
    """
    Beräkna targetkurser baserat på:
    - Nuvarande P/E och P/E 1-4
    - Nuvarande P/S och P/S 1-4
    - Vinst i år och nästa år
    - Omsättningstillväxt i år och nästa år

    Säkerhetsmarginal på 10% (0.9) appliceras på targetkurser.

    Returnerar en dict med:
    {
        "targetkurs_pe_i_år": float,
        "targetkurs_pe_nästa_år": float,
        "targetkurs_ps_i_år": float,
        "targetkurs_ps_nästa_år": float
    }
    """

    # Extrahera nödvändiga värden, med fallback till 0 om saknas
    nuvarande_pe = float(bolag.get("nuvarande_pe", 0) or 0)
    pe_1 = float(bolag.get("pe_1", 0) or 0)
    pe_2 = float(bolag.get("pe_2", 0) or 0)
    pe_3 = float(bolag.get("pe_3", 0) or 0)
    pe_4 = float(bolag.get("pe_4", 0) or 0)

    nuvarande_ps = float(bolag.get("nuvarande_ps", 0) or 0)
    ps_1 = float(bolag.get("ps_1", 0) or 0)
    ps_2 = float(bolag.get("ps_2", 0) or 0)
    ps_3 = float(bolag.get("ps_3", 0) or 0)
    ps_4 = float(bolag.get("ps_4", 0) or 0)

    vinst_i_år = float(bolag.get("vinst_i_år", 0) or 0)
    vinst_nästa_år = float(bolag.get("vinst_nästa_år", 0) or 0)

    omsättningstillväxt_i_år = float(bolag.get("omsättningstillväxt_i_år", 0) or 0) / 100
    omsättningstillväxt_nästa_år = float(bolag.get("omsättningstillväxt_nästa_år", 0) or 0) / 100

    nuvarande_kurs = float(bolag.get("nuvarande_kurs", 0) or 0)

    # Beräkna snitt P/E och P/S (P/E 1-4 och P/S 1-4)
    pe_list = [pe_1, pe_2, pe_3, pe_4]
    ps_list = [ps_1, ps_2, ps_3, ps_4]

    pe_list = [x for x in pe_list if x > 0]
    ps_list = [x for x in ps_list if x > 0]

    snitt_pe = sum(pe_list) / len(pe_list) if pe_list else 0
    snitt_ps = sum(ps_list) / len(ps_list) if ps_list else 0

    säkerhetsmarginal = 0.9

    # Targetkurser P/E
    targetkurs_pe_i_år = snitt_pe * vinst_i_år * säkerhetsmarginal if snitt_pe and vinst_i_år else 0
    targetkurs_pe_nästa_år = snitt_pe * vinst_nästa_år * säkerhetsmarginal if snitt_pe and vinst_nästa_år else 0

    # Targetkurser P/S
    # Formeln: snitt_ps * omsättningstillväxt * nuvarande_kurs * säkerhetsmarginal
    # För nästa år multiplicerar vi omsättningstillväxt i år och nästa år
    targetkurs_ps_i_år = snitt_ps * omsättningstillväxt_i_år * nuvarande_kurs * säkerhetsmarginal if snitt_ps and omsättningstillväxt_i_år and nuvarande_kurs else 0
    targetkurs_ps_nästa_år = snitt_ps * omsättningstillväxt_i_år * omsättningstillväxt_nästa_år * nuvarande_kurs * säkerhetsmarginal if snitt_ps and omsättningstillväxt_i_år and omsättningstillväxt_nästa_år and nuvarande_kurs else 0

    return {
        "targetkurs_pe_i_år": targetkurs_pe_i_år,
        "targetkurs_pe_nästa_år": targetkurs_pe_nästa_år,
        "targetkurs_ps_i_år": targetkurs_ps_i_år,
        "targetkurs_ps_nästa_år": targetkurs_ps_nästa_år
    }

def beräkna_undervärdering(nuvarande_kurs: float, targetkurs: float) -> float:
    """
    Beräkna undervärdering i procent mellan nuvarande kurs och targetkurs.
    Returnerar positivt värde om kursen är undervärderad.
    """

    if not nuvarande_kurs or not targetkurs:
        return 0.0
    return round((targetkurs - nuvarande_kurs) / nuvarande_kurs * 100, 2)
