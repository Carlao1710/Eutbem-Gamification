import streamlit as st
from src.dashboard.admin_dashboard import admin_dashboard
from src.dashboard.representative_dashboard import representative_dashboard

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