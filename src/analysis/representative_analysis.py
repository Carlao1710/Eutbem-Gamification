import pandas as pd

def process_representative_data(representantes_data):
    data = []
    for rep in representantes_data["Representantes"]:
        data.append({
            "Nome": rep["Nome"],
            "Cotas Ativas": rep["Cotas"]["Ativa"],
            "Cotas Pagas": rep["Cotas"]["Pago"],
            "Cotas Atrasadas": rep["Cotas"]["Atrasado"],
            "Contratos Ativos (R$)": float(rep["Contratos"]["Total Ativos"].replace("R$", "").replace(",", "").strip()),
            "Contratos Cancelados (R$)": float(rep["Contratos"]["Total Cancelados"].replace("R$", "").replace(",", "").strip()),
        })
    return pd.DataFrame(data)

def process_weekly_data(semanal_data):
    data = []
    for week in semanal_data["Semanas"]:
        # Ajustar valores para remover caracteres desnecessários
        total_contratos = week["Total de Contratos"].replace("R$", "").replace(".", "").replace(",", ".").strip()
        week_data = {
            "Semana": week["Semana"],
            "Total de Contratos (R$)": float(total_contratos),
        }
        for rep in week.keys():
            if rep not in ["Semana", "Inicio", "Fim", "Total de Contratos"]:
                valor_rep = week[rep].replace("R$", "").replace(".", "").replace(",", ".").strip()
                week_data[rep] = float(valor_rep)
        data.append(week_data)
    return pd.DataFrame(data)