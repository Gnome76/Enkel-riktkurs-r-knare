def snitt(*args):
    värden = [v for v in args if v > 0]
    return sum(värden) / len(värden) if värden else 0

def berakna_targetkurser(b):
    snitt_pe = snitt(b["pe1"], b["pe2"], b["pe3"], b["pe4"])
    snitt_ps = snitt(b["ps1"], b["ps2"], b["ps3"], b["ps4"])

    säkerhetsmarginal = 0.9  # 10% säkerhetsmarginal

    # Targetkurs P/E
    target_pe_i_ar = snitt_pe * b["vinst_i_ar"] * säkerhetsmarginal
    target_pe_nastaar = snitt_pe * b["vinst_nastaar"] * säkerhetsmarginal

    # Targetkurs P/S
    try:
        ps_factor_i_ar = (snitt_ps * (b["tillvaxt_i_ar"] / 100)) / b["nuvarande_ps"]
        target_ps_i_ar = ps_factor_i_ar * b["nuvarande_kurs"] * säkerhetsmarginal
    except ZeroDivisionError:
        target_ps_i_ar = 0

    try:
        ps_factor_nastaar = (snitt_ps * (b["tillvaxt_i_ar"] / 100) * (b["tillvaxt_nastaar"] / 100)) / b["nuvarande_ps"]
        target_ps_nastaar = ps_factor_nastaar * b["nuvarande_kurs"] * säkerhetsmarginal
    except ZeroDivisionError:
        target_ps_nastaar = 0

    # Undervärdering
    max_target = max(target_pe_i_ar, target_pe_nastaar, target_ps_i_ar, target_ps_nastaar)
    if b["nuvarande_kurs"] > 0:
        undervardering_pct = round(((max_target - b["nuvarande_kurs"]) / b["nuvarande_kurs"]) * 100, 1)
    else:
        undervardering_pct = 0

    # Köpvärd nivå (targetkurs -30%)
    köp_nivå = round(max_target * 0.7, 2)

    return {
        "target_pe_i_ar": round(target_pe_i_ar, 2),
        "target_pe_nastaar": round(target_pe_nastaar, 2),
        "target_ps_i_ar": round(target_ps_i_ar, 2),
        "target_ps_nastaar": round(target_ps_nastaar, 2),
        "undervardering_pct": undervardering_pct,
        "kopvarde_niva": köp_nivå
    }
