def medelvärde(lista):
    if not lista:
        return 0
    return sum(lista) / len(lista)

def berakna_targetkurser(bolag):
    # Säkerhetsmarginal 10 %
    säkerhet = 0.9

    # Snitt P/E 1-4
    pe_värden = [bolag.get(f"pe_{i}", 0) for i in range(1, 5)]
    pe_snitt = medelvärde(pe_värden)

    # Snitt P/S 1-4
    ps_värden = [bolag.get(f"ps_{i}", 0) for i in range(1, 5)]
    ps_snitt = medelvärde(ps_värden)

    # Omvandla procent till decimal
    tillväxt_iår = bolag.get("tillväxt_iår", 0) / 100
    tillväxt_nästa_år = bolag.get("tillväxt_nästa_år", 0) / 100

    # Beräkningar targetkurs P/E
    target_pe_iår = pe_snitt * bolag.get("vinst_år", 0) * säkerhet
    target_pe_nästa_år = pe_snitt * bolag.get("vinst_nästa_år", 0) * säkerhet

    # Beräkningar targetkurs P/S
    nuvarande_ps = bolag.get("nuvarande_ps", 1) or 1  # undvik division med 0
    nuvarande_kurs = bolag.get("nuvarande_kurs", 0)

    target_ps_iår = ps_snitt * (tillväxt_iår / nuvarande_ps) * nuvarande_kurs * säkerhet
    target_ps_nästa_år = ps_snitt * ((tillväxt_iår * tillväxt_nästa_år) / nuvarande_ps) * nuvarande_kurs * säkerhet

    # Undervärdering i %
    undervärdering_pe = 100 * (target_pe_nästa_år - nuvarande_kurs) / nuvarande_kurs if nuvarande_kurs else 0
    undervärdering_ps = 100 * (target_ps_nästa_år - nuvarande_kurs) / nuvarande_kurs if nuvarande_kurs else 0

    # Köpvärd nivå (30% rabatt)
    köp_pe = target_pe_nästa_år * 0.7
    köp_ps = target_ps_nästa_år * 0.7

    return {
        "target_pe_iår": target_pe_iår,
        "target_pe_nästa_år": target_pe_nästa_år,
        "target_ps_iår": target_ps_iår,
        "target_ps_nästa_år": target_ps_nästa_år,
        "undervardering_pe_pct": undervärdering_pe,
        "undervardering_ps_pct": undervärdering_ps,
        "köpvärd_pe": köp_pe,
        "köpvärd_ps": köp_ps,
    }

def filtrera_undervarderade(bolag_list, procent_grans=30):
    """Returnerar bolag som är undervärderade med minst procent_grans enligt target P/E nästa år"""
    undervarderade = [
        b for b in bolag_list
        if b.get("undervardering_pe_pct", 0) >= procent_grans
    ]
    # Sortera efter mest undervärderade först (högst procentsats)
    undervarderade.sort(key=lambda b: b.get("undervardering_pe_pct", 0), reverse=True)
    return undervarderade
