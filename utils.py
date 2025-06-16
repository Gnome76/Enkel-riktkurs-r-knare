import streamlit as st

def beräkna_targetkurser(info, metod="pe"):
    st.write("🔍 DEBUG: beräkna_targetkurser info =", info)
    st.write("🔍 DEBUG: metod =", metod)

    try:
        kurs = float(info.get("nuvarande_kurs", 0))

        if metod == "pe":
            pe_tal = [float(info.get(f"pe{i}", 0)) for i in range(1, 5)]
            pe_snitt = sum(pe_tal) / len(pe_tal)
            vinst_i_ar = float(info.get("vinst_i_ar", 0))
            vinst_nasta_ar = float(info.get("vinst_nasta_ar", 0))

            target_i_ar = round(pe_snitt * vinst_i_ar * 0.9, 2)
            target_nasta_ar = round(pe_snitt * vinst_nasta_ar * 0.9, 2)
            return target_i_ar, target_nasta_ar

        elif metod == "ps":
            ps_tal = [float(info.get(f"ps{i}", 0)) for i in range(1, 5)]
            ps_snitt = sum(ps_tal) / len(ps_tal)
            tillv_i_ar = float(info.get("oms_tillv_i_ar", 0)) / 100
            tillv_nasta_ar = float(info.get("oms_tillv_nasta_ar", 0)) / 100
            nuvarande_ps = float(info.get("nuvarande_ps", 1))  # för att undvika div/0

            target_i_ar = round(ps_snitt * tillv_i_ar / nuvarande_ps * kurs * 0.9, 2)
            target_nasta_ar = round(ps_snitt * tillv_i_ar * tillv_nasta_ar / nuvarande_ps * kurs * 0.9, 2)
            return target_i_ar, target_nasta_ar

        else:
            st.warning("⚠️ Okänd metod i beräkna_targetkurser.")
            return None, None

    except Exception as e:
        st.error(f"Fel i beräkna_targetkurser: {e}")
        return None, None


def beräkna_undervärdering(nuvarande_kurs, targetkurs):
    try:
        if targetkurs and targetkurs > 0:
            undervärdering = round((1 - nuvarande_kurs / targetkurs) * 100, 1)
            return undervärdering
        else:
            return None
    except Exception as e:
        st.error(f"Fel i beräkna_undervärdering: {e}")
        return None
