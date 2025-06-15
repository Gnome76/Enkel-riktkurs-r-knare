def medelvärde(lista):
    if not lista:
        return 0
    return sum(lista) / len(lista)

def berakna_targetkurser(bolag):
    säkerhet = 0.9  # 10 % säkerhetsmarginal

    # Snitt P/E och P/S
    pe_värden = [bolag.get(f"pe_{i}", 0) for i in range(1, 5)]
    ps_värden = [bolag.get(f"ps_{i}", 0) for i in range(1, 5)]
    pe_snitt = medelvärde(pe_värden)
    ps_snitt = medelvärde(ps_värden)

    # Tillväxt omräknad från procent
    tillväxt_iår = bolag.get("oms_tillvaxt_i_ar", 0) / 100
    tillväxt_nästa_år = bolag.get("oms_tillvaxt_nasta_ar", 0) / 100

    # Targetkurs P/E
    target_pe_iår = pe_snitt * bolag.get("vinst_i_ar", 0) * säkerhet
    target_pe_nasta_år = pe_snitt * bolag.get("vinst_nasta_ar", 0) * säkerhet

    # Targetkurs P/S
    nuvarande_ps = bolag.get("nuvarande_ps", 1) or 1  # undvik div 0
    nuvarande_kurs = bolag.get("nuvarande_kurs", 0)
    target_ps_iår = ps_snitt * (tillväxt_iår / nuvarande_ps) * nuvarande_kurs * säkerhet
    target_ps_nasta_år = ps_snitt * ((tillväxt_iår * tillväxt_nästa_år) / nuvarande_ps) * nuvarande_kurs * säkerhet

    # Undervärdering i procent
    underv_pe = 100 * (target_pe_nasta_år - nuvarande_kurs) / nuvarande_kurs if nuvarande_kurs else 0
    underv_ps = 100 * (target_ps_nasta_år - nuvarande_kurs) / nuvarande_kurs if nuvarande_kurs else 0

    # Köpvärda nivåer (30 % rabatt)
    köp_pe = target_pe_nasta_år * 0.7
    köp_ps = target_ps_nasta_år * 0.7

    return {
        "target_pe_iår": target_pe_iår,
        "target_pe_nasta_år": target_pe_nasta_år,
        "target_ps_iår": target_ps_iår,
        "target_ps_nasta_år": target_ps_nasta_år,
        "undervardering_pe_pct": underv_pe,
        "undervardering_ps_pct": underv_ps,
        "köpvärd_pe": köp_pe,
        "köpvärd_ps": köp_ps,
    }

def filtrera_undervarderade(bolag_list, procent_grans=30):
    """Returnerar bolag som är undervärderade med minst procent_grans enligt P/E eller P/S"""
    undervarderade = [
        b for b in bolag_list
        if b.get("undervardering_pe_pct", 0) >= procent_grans
        or b.get("undervardering_ps_pct", 0) >= procent_grans
    ]
    # Sortera efter den högsta undervärderingen (av P/E eller P/S)
    undervarderade.sort(
        key=lambda b: max(
            b.get("undervardering_pe_pct", 0),
            b.get("undervardering_ps_pct", 0)
        ),
        reverse=True
    )
    return undervarderade
