import streamlit as st
from datetime import datetime

def redigeringsformular(data):
    st.subheader("✏️ Redigera befintligt bolag")

    if not data:
        st.info("Inga bolag finns att redigera ännu.")
        return

    bolagslista = list(data.keys())
    valt_bolag = st.selectbox("Välj bolag att redigera", bolagslista)

    if valt_bolag:
        bolag = data[valt_bolag]

        with st.form(key="redigeringsformulär"):
            nuvarande_kurs = st.number_input("Nuvarande kurs", value=bolag.get("nuvarande_kurs", 0.0), step=0.1)
            pe_nuvarande = st.number_input("Nuvarande P/E", value=bolag.get("pe_nuvarande", 0.0), step=0.1)
            ps_nuvarande = st.number_input("Nuvarande P/S", value=bolag.get("ps_nuvarande", 0.0), step=0.1)

            pe_1 = st.number_input("P/E år 1", value=bolag.get("pe_1", 0.0), step=0.1)
            pe_2 = st.number_input("P/E år 2", value=bolag.get("pe_2", 0.0), step=0.1)
            pe_3 = st.number_input("P/E år 3", value=bolag.get("pe_3", 0.0), step=0.1)
            pe_4 = st.number_input("P/E år 4", value=bolag.get("pe_4", 0.0), step=0.1)

            ps_1 = st.number_input("P/S år 1", value=bolag.get("ps_1", 0.0), step=0.1)
            ps_2 = st.number_input("P/S år 2", value=bolag.get("ps_2", 0.0), step=0.1)
            ps_3 = st.number_input("P/S år 3", value=bolag.get("ps_3", 0.0), step=0.1)
            ps_4 = st.number_input("P/S år 4", value=bolag.get("ps_4", 0.0), step=0.1)

            submit = st.form_submit_button("💾 Spara ändringar")

        if submit:
            bolag["nuvarande_kurs"] = nuvarande_kurs
            bolag["pe_nuvarande"] = pe_nuvarande
            bolag["ps_nuvarande"] = ps_nuvarande
            bolag["pe_1"] = pe_1
            bolag["pe_2"] = pe_2
            bolag["pe_3"] = pe_3
            bolag["pe_4"] = pe_4
            bolag["ps_1"] = ps_1
            bolag["ps_2"] = ps_2
            bolag["ps_3"] = ps_3
            bolag["ps_4"] = ps_4
            bolag["senast_andrad"] = datetime.now().strftime("%Y-%m-%d")

            st.success(f"{valt_bolag} har uppdaterats.")
