import streamlit as st
import sys
import os
from src.dashboard.admin_dashboard import admin_dashboard
from src.dashboard.representative_dashboard import representative_dashboard

# Adicionar o diretório 'src' ao caminho de módulos
sys.path.append(os.path.abspath("src"))

st.set_page_config(
    page_title="Eutbem Gamification Platform",
    page_icon="🌟",
    layout="wide"
)

st.title("Eutbem Gamification Platform")
st.write("Selecione o dashboard que deseja acessar:")

# Navegação entre dashboards
option = st.selectbox("Escolha o dashboard", ["Admin", "Representante"])

if option == "Admin":
    admin_dashboard()
elif option == "Representante":
    representative_dashboard()