import streamlit as st
from src.utils.load_json import load_json
from src.analysis.representative_analysis import process_representative_data, process_weekly_data

def admin_dashboard():
    representantes_data = load_json("data/representantes.json")
    semanal_data = load_json("data/semanal.json")

    # Processar os dados
    representative_df = process_representative_data(representantes_data)
    weekly_df = process_weekly_data(semanal_data)

    st.header("Resumo Geral")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cotas Ativas", representative_df["Cotas Ativas"].sum())
    col2.metric("Total Contratos Ativos (R$)", f"R$ {representative_df['Contratos Ativos (R$)'].sum():,.2f}")
    col3.metric("Total Contratos Cancelados (R$)", f"R$ {representative_df['Contratos Cancelados (R$)'].sum():,.2f}")

    st.header("Desempenho dos Representantes")
    st.dataframe(representative_df)

    st.header("Evolução Semanal de Contratos")
    st.line_chart(weekly_df.set_index("Semana")["Total de Contratos (R$)"])