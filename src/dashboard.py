"""Dashboard Streamlit com os dados das views do PostgreSQL.

Uso: streamlit run src/dashboard.py
"""
import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine

from config import DATABASE_URL

st.set_page_config(page_title="Temperaturas IoT", layout="wide")


@st.cache_resource
def get_engine():
    return create_engine(DATABASE_URL)


@st.cache_data(ttl=300)
def load_data(view_name: str) -> pd.DataFrame:
    # view_name vem sempre de uma lista fixa aqui no arquivo, nunca do usuário.
    return pd.read_sql(f"SELECT * FROM {view_name}", get_engine())


st.title("Dashboard de Temperaturas IoT")
st.caption("Leituras de um sensor entre julho e dezembro de 2018, armazenadas no PostgreSQL.")

df_media = load_data("avg_temp_por_dispositivo")
df_hora = load_data("leituras_por_hora")
df_dia = load_data("temp_max_min_por_dia")

c1, c2, c3 = st.columns(3)
c1.metric("Leituras", f"{int(df_media['total_leituras'].sum()):,}".replace(",", "."))
c2.metric("Maior temperatura", f"{int(df_dia['temp_max'].max())} °C")
c3.metric("Menor temperatura", f"{int(df_dia['temp_min'].min())} °C")

# Gráfico 1: média por ambiente
st.header("Média de temperatura por ambiente")
fig1 = px.bar(df_media, x="ambiente", y="avg_temp", color="ambiente", text="avg_temp",
              labels={"ambiente": "Ambiente", "avg_temp": "Temperatura média (°C)"})
fig1.update_layout(showlegend=False)
st.plotly_chart(fig1, use_container_width=True)

# Gráfico 2: leituras por hora
st.header("Leituras por hora do dia")
fig2 = px.line(df_hora, x="hora", y="contagem", markers=True,
               labels={"hora": "Hora do dia", "contagem": "Número de leituras"})
st.plotly_chart(fig2, use_container_width=True)

# Gráfico 3: máxima e mínima por dia
st.header("Temperaturas máximas e mínimas por dia")
fig3 = px.line(df_dia, x="data", y=["temp_max", "temp_min"],
               labels={"data": "Data", "value": "Temperatura (°C)", "variable": ""})
st.plotly_chart(fig3, use_container_width=True)
