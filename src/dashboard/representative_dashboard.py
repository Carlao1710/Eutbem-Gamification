import streamlit as st
from src.utils.load_json import load_json
from src.analysis.representative_analysis import process_representative_data, process_weekly_data
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Função para salvar e carregar missões
def load_missions():
    try:
        return pd.read_csv("data/missions.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Representante", "Meta", "Tipo", "Valor", "Status"])

def save_missions(missions_df):
    missions_df.to_csv("data/missions.csv", index=False)

def representative_dashboard():
    representantes_data = load_json("data/representantes.json")
    semanal_data = load_json("data/semanal.json")
    metas_data = load_json("data/metas.json")

    # Processar os dados
    representative_df = process_representative_data(representantes_data)
    weekly_df = process_weekly_data(semanal_data)

    # Carregar as missões existentes
    missions_df = load_missions()

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

    # Metas
    st.header(f"Metas de {selected_rep}")
    selected_month = st.selectbox("Selecione o Mês", metas_data["Meses"].keys())
    rep_goal_data = pd.DataFrame(metas_data["Meses"][selected_month])
    rep_goal_data = rep_goal_data[rep_goal_data["Representante"] == selected_rep]

    if not rep_goal_data.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Meta (R$)", f"R$ {float(rep_goal_data['Meta'].values[0].replace('R$', '').replace(',', '').strip()):,.2f}")
        col2.metric("Atingimento (R$)", f"R$ {float(rep_goal_data['Atingimento'].values[0].replace('R$', '').replace(',', '').strip()):,.2f}")
        col3.metric("% Atingimento", rep_goal_data["% Atingimento"].values[0])

        # Calcular o percentual de atingimento
        atingido = float(rep_goal_data["% Atingimento"].values[0].replace("%", "").strip())

        # Definir cor do card com base no atingimento
        if atingido <= 30:
            card_color = "#FFCDD2"  # Vermelho Claro
            text_color = "#D32F2F"  # Vermelho Escuro
        elif 31 <= atingido <= 65:
            card_color = "#FFE0B2"  # Laranja Claro
            text_color = "#F57C00"  # Laranja Escuro
        else:
            card_color = "#C8E6C9"  # Verde Claro
            text_color = "#388E3C"  # Verde Escuro

        # Card Colorido
        st.subheader("Indicadores Visuais")
        st.markdown(
            f"""
            <div style="background-color: {card_color}; padding: 20px; border-radius: 10px; text-align: center;">
                <h3 style="color: {text_color};">Atingimento</h3>
                <h1 style="color: {text_color};">R$ {float(rep_goal_data['Atingimento'].values[0].replace('R$', '').replace(',', '').strip()):,.2f}</h1>
                <p style="color: {text_color};">{rep_goal_data['% Atingimento'].values[0]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.write("Nenhuma meta encontrada para este mês.")