import streamlit as st
from src.utils.load_json import load_json
from src.analysis.representative_analysis import process_representative_data, process_weekly_data
import plotly.graph_objects as go

def admin_dashboard():
    # Carregar dados
    representantes_data = load_json("data/representantes.json")
    semanal_data = load_json("data/semanal.json")

    # Processar os dados
    representative_df = process_representative_data(representantes_data)
    weekly_df = process_weekly_data(semanal_data)

    # Seção: Resumo Geral
    st.header("Resumo Geral")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cotas Ativas", representative_df["Cotas Ativas"].sum())
    col2.metric("Total Contratos Ativos (R$)", f"R$ {representative_df['Contratos Ativos (R$)'].sum():,.2f}")
    col3.metric("Total Contratos Cancelados (R$)", f"R$ {representative_df['Contratos Cancelados (R$)'].sum():,.2f}")

    # Seção: Meta Global Mensal
    st.header("Meta Global Mensal")

    # Adicionar campo para definir meta
    global_target = st.number_input(
        "Defina a Meta Global Mensal (R$):",
        min_value=0.0,
        value=1000000.0,  # Meta padrão
        step=10000.0,
        format="%.2f",
    )

    # Calcular o progresso atual
    total_current = weekly_df["Total de Contratos (R$)"].sum()

    # Exibir o progresso
    st.subheader("Progresso Atual")
    st.write(f"Meta Mensal: **R$ {global_target:,.2f}**")
    st.write(f"Total Atual: **R$ {total_current:,.2f}**")

    # Gráfico de progresso
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=total_current,
        delta={"reference": global_target, "position": "top"},
        gauge={
            "axis": {"range": [0, global_target * 1.2]},  # 20% além da meta para contexto
            "bar": {"color": "green" if total_current >= global_target else "red"},
            "steps": [
                {"range": [0, global_target], "color": "#d3d3d3"},
            ],
        },
        title={"text": "Progresso da Meta Mensal"},
    ))
    st.plotly_chart(fig, use_container_width=True)

    # Seção: Desempenho dos Representantes
    st.header("Desempenho dos Representantes")
    st.dataframe(representative_df)

    # Seção: Evolução Semanal de Contratos
    st.header("Evolução Semanal de Contratos")
    st.line_chart(weekly_df.set_index("Semana")["Total de Contratos (R$)"])