"""Configuração compartilhada entre a carga e o dashboard."""
import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CSV = RAIZ / "data" / "IOT-temp.csv"
VIEWS_SQL = RAIZ / "sql" / "views.sql"

# Mesmos valores do docker-compose.yml. Dá pra sobrescrever com DATABASE_URL.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://iot:iot_senha@127.0.0.1:5432/iot",
)
