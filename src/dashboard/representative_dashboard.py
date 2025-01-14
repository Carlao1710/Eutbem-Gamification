import streamlit as st
from src.utils.load_json import load_json
from src.analysis.representative_analysis import process_representative_data, process_weekly_data

def representative_dashboard():
    representantes_data = load_json("data/representantes.json")
    semanal_data = load_json("data/semanal.json")

    # Processar os dados
    representative_df = process_representative_data(representantes_data)
    weekly_df = process_weekly_data(semanal_data)

    # Selecionar Representante
    representative_names = representative_df["Nome"].tolist()
    selected_rep = st.selectbox("Selecione o Representante", representative_names)

    # Dados do Representante Selecionado
    rep_data = representative_df[representative_df["Nome"] == selected_rep]
    st.header(f"Resumo de {selected_rep}")
    col1, col2 = st.columns(2)
    col1.metric("Cotas Ativas", int(rep_data["Cotas Ativas"]))
    col1.metric("Cotas Pagas", int(rep_data["Cotas Pagas"]))
    col2.metric("Contratos Ativos (R$)", f"R$ {float(rep_data['Contratos Ativos (R$)']):,.2f}")
    col2.metric("Contratos Cancelados (R$)", f"R$ {float(rep_data['Contratos Cancelados (R$)']):,.2f}")

    # Performance Semanal
    st.header(f"Evolução Semanal de {selected_rep}")
    rep_weekly = weekly_df[["Semana", selected_rep]].rename(columns={selected_rep: "Contratos (R$)"})
    st.line_chart(rep_weekly.set_index("Semana")["Contratos (R$)"])