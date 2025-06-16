import streamlit as st

def beräkna_targetkurser(info, metod="pe"):
    st.write("🔍 DEBUG: Data till beräkna_targetkurser:", info)

    try:
        nuvarande_kurs = info.get("nuvarande_kurs", 0)
        nuvarande_ps = info.get("nuvarande_ps", 0)

        pe_tal = [info.get(f"pe{i}", 0) for i in range(1, 5)]
        ps_tal = [info.get(f"ps{i}", 0) for i in range(1, 5)]

        snitt_pe = sum(pe_tal) / len(pe_tal) if all(pe_tal) else 0
        snitt_ps = sum(ps_tal) / len(ps_tal) if all(ps_tal) else 0

        vinst_i_ar = info.get("vinst_i_ar", 0)
        vinst_nasta_ar = info.get("vinst_nasta_ar", 0)

        tillvaxt_i_ar = info.get("oms_tillv_i_ar", 0) / 100
        tillvaxt_nasta_ar = info.get("oms_tillv_nasta_ar", 0) / 100

        säkerhetsmarginal = 0.9

        if metod == "pe" and snitt_pe > 0:
            target_i_ar = snitt_pe * vinst_i_ar * säkerhetsmarginal
            target_nasta = snitt_pe * vinst_nasta_ar * säkerhetsmarginal
        elif metod == "ps" and snitt_ps > 0 and nuvarande_ps > 0:
            faktor_i_ar = tillvaxt_i_ar
            faktor_nasta = tillvaxt_i_ar * tillvaxt_nasta_ar

            target_i_ar = snitt_ps * faktor_i_ar / nuvarande_ps * nuvarande_kurs * säkerhetsmarginal
            target_nasta = snitt_ps * faktor_nasta / nuvarande_ps * nuvarande_kurs * säkerhetsmarginal
        else:
            return None

        return round(target_i_ar, 2), round(target_nasta, 2)

    except Exception as e:
        st.error(f"Fel vid beräkning av targetkurser: {e}")
        return None

def beräkna_undervärdering(info, metod="pe"):
    try:
        nuvarande_kurs = info.get("nuvarande_kurs")
        if nuvarande_kurs in [None, 0]:
            return None

        result = beräkna_targetkurser(info, metod=metod)
        if not result:
            return None

        target_i_ar, target_nasta = result

        underv_i_ar = ((target_i_ar - nuvarande_kurs) / nuvarande_kurs) * 100
        underv_nasta = ((target_nasta - nuvarande_kurs) / nuvarande_kurs) * 100

        return round(underv_i_ar), round(underv_nasta)

    except Exception as e:
        st.error(f"Fel vid beräkning av undervärdering: {e}")
        return None
