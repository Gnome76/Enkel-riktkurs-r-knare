import streamlit as st

def nytt_bolag_formular(data):
    st.header("Lägg till nytt bolag")
    with st.form(key="nytt_bolag_form"):
        namn = st.text_input("Bolagsnamn")
        nuvarande_kurs = st.number_input("Nuvarande kurs (kr)", min_value=0.0, format="%.2f")
        
        nuvarande_pe = st.number_input("Nuvarande P/E", min_value=0.0, format="%.2f")
        pe_1 = st.number_input("P/E 1", min_value=0.0, format="%.2f")
        pe_2 = st.number_input("P/E 2", min_value=0.0, format="%.2f")
        pe_3 = st.number_input("P/E 3", min_value=0.0, format="%.2f")
        pe_4 = st.number_input("P/E 4", min_value=0.0, format="%.2f")
        
        nuvarande_ps = st.number_input("Nuvarande P/S", min_value=0.0, format="%.2f")
        ps_1 = st.number_input("P/S 1", min_value=0.0, format="%.2f")
        ps_2 = st.number_input("P/S 2", min_value=0.0, format="%.2f")
        ps_3 = st.number_input("P/S 3", min_value=0.0, format="%.2f")
        ps_4 = st.number_input("P/S 4", min_value=0.0, format="%.2f")
        
        vinst_i_ar = st.number_input("Vinst i år", format="%.2f")
        vinst_nasta_ar = st.number_input("Vinst nästa år", format="%.2f")
        
        oms_tillvaxt_i_ar = st.number_input("Omsättningstillväxt i år (%)", format="%.2f")
        oms_tillvaxt_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", format="%.2f")
        
        submit = st.form_submit_button("Lägg till bolag")

        if submit:
            if namn.strip() == "":
                st.error("Bolagsnamn kan inte vara tomt.")
                return
            
            if namn in data:
                st.error("Bolaget finns redan.")
                return
            
            data[namn] = {
                "nuvarande_kurs": nuvarande_kurs,
                "nuvarande_pe": nuvarande_pe,
                "pe_1": pe_1,
                "pe_2": pe_2,
                "pe_3": pe_3,
                "pe_4": pe_4,
                "nuvarande_ps": nuvarande_ps,
                "ps_1": ps_1,
                "ps_2": ps_2,
                "ps_3": ps_3,
                "ps_4": ps_4,
                "vinst_i_ar": vinst_i_ar,
                "vinst_nasta_ar": vinst_nasta_ar,
                "oms_tillvaxt_i_ar": oms_tillvaxt_i_ar,
                "oms_tillvaxt_nasta_ar": oms_tillvaxt_nasta_ar,
            }
            st.success(f"Bolag '{namn}' tillagt!")

def redigeringsformular(data):
    st.header("Redigera befintligt bolag")

    bolagslista = list(data.keys())
    valt_bolag = st.selectbox("Välj bolag att redigera", bolagslista)

    if valt_bolag:
        info = data[valt_bolag]
        with st.form(key="redigera_bolag_form"):
            nuvarande_kurs = st.number_input("Nuvarande kurs (kr)", value=info.get("nuvarande_kurs", 0.0), format="%.2f")
            
            nuvarande_pe = st.number_input("Nuvarande P/E", value=info.get("nuvarande_pe", 0.0), format="%.2f")
            pe_1 = st.number_input("P/E 1", value=info.get("pe_1", 0.0), format="%.2f")
            pe_2 = st.number_input("P/E 2", value=info.get("pe_2", 0.0), format="%.2f")
            pe_3 = st.number_input("P/E 3", value=info.get("pe_3", 0.0), format="%.2f")
            pe_4 = st.number_input("P/E 4", value=info.get("pe_4", 0.0), format="%.2f")
            
            nuvarande_ps = st.number_input("Nuvarande P/S", value=info.get("nuvarande_ps", 0.0), format="%.2f")
            ps_1 = st.number_input("P/S 1", value=info.get("ps_1", 0.0), format="%.2f")
            ps_2 = st.number_input("P/S 2", value=info.get("ps_2", 0.0), format="%.2f")
            ps_3 = st.number_input("P/S 3", value=info.get("ps_3", 0.0), format="%.2f")
            ps_4 = st.number_input("P/S 4", value=info.get("ps_4", 0.0), format="%.2f")
            
            vinst_i_ar = st.number_input("Vinst i år", value=info.get("vinst_i_ar", 0.0), format="%.2f")
            vinst_nasta_ar = st.number_input("Vinst nästa år", value=info.get("vinst_nasta_ar", 0.0), format="%.2f")
            
            oms_tillvaxt_i_ar = st.number_input("Omsättningstillväxt i år (%)", value=info.get("oms_tillvaxt_i_ar", 0.0), format="%.2f")
            oms_tillvaxt_nasta_ar = st.number_input("Omsättningstillväxt nästa år (%)", value=info.get("oms_tillvaxt_nasta_ar", 0.0), format="%.2f")

            submit = st.form_submit_button("Uppdatera bolag")

            if submit:
                data[valt_bolag] = {
                    "nuvarande_kurs": nuvarande_kurs,
                    "nuvarande_pe": nuvarande_pe,
                    "pe_1": pe_1,
                    "pe_2": pe_2,
                    "pe_3": pe_3,
                    "pe_4": pe_4,
                    "nuvarande_ps": nuvarande_ps,
                    "ps_1": ps_1,
                    "ps_2": ps_2,
                    "ps_3": ps_3,
                    "ps_4": ps_4,
                    "vinst_i_ar": vinst_i_ar,
                    "vinst_nasta_ar": vinst_nasta_ar,
                    "oms_tillvaxt_i_ar": oms_tillvaxt_i_ar,
                    "oms_tillvaxt_nasta_ar": oms_tillvaxt_nasta_ar,
                }
                st.success(f"Bolag '{valt_bolag}' uppdaterat!")
