"""Lê o CSV de leituras de temperatura e grava no PostgreSQL.

Uso: python src/carga.py
"""
import pandas as pd
from sqlalchemy import create_engine, text

from config import CSV, DATABASE_URL, VIEWS_SQL


def ler_csv() -> pd.DataFrame:
    df = pd.read_csv(CSV)

    # Nomes de coluna do CSV têm barra ("room_id/id"), ruim de usar em SQL.
    df = df.rename(columns={
        "room_id/id": "device_id",
        "noted_date": "noted_at",
        "temp": "temperature",
        "out/in": "ambiente",
    })

    # Datas no formato dia-mês-ano hora:minuto.
    df["noted_at"] = pd.to_datetime(df["noted_at"], format="%d-%m-%Y %H:%M")

    # Um id aparece duas vezes no arquivo. Fica a primeira ocorrência.
    antes = len(df)
    df = df.drop_duplicates(subset="id", keep="first")
    print(f"{antes - len(df)} linha(s) duplicada(s) removida(s)")

    df["ambiente"] = df["ambiente"].str.lower().map({"in": "interno", "out": "externo"})
    return df


def main() -> None:
    df = ler_csv()
    engine = create_engine(DATABASE_URL)

    with engine.begin() as conn:
        # Views dependem da tabela, então saem antes de recriá-la.
        for v in ("avg_temp_por_dispositivo", "leituras_por_hora", "temp_max_min_por_dia"):
            conn.execute(text(f"DROP VIEW IF EXISTS {v}"))
        conn.execute(text("DROP TABLE IF EXISTS temperature_readings"))
        conn.execute(text("""
            CREATE TABLE temperature_readings (
                id          TEXT PRIMARY KEY,
                device_id   TEXT        NOT NULL,
                noted_at    TIMESTAMP   NOT NULL,
                temperature INTEGER     NOT NULL,
                ambiente    TEXT        NOT NULL CHECK (ambiente IN ('interno', 'externo'))
            )
        """))

    df.to_sql("temperature_readings", engine, if_exists="append", index=False,
              chunksize=5000, method="multi")

    with engine.begin() as conn:
        conn.exec_driver_sql(VIEWS_SQL.read_text(encoding="utf-8"))
        total = conn.execute(text("SELECT COUNT(*) FROM temperature_readings")).scalar()
    print(f"{total} leituras gravadas e views criadas")


if __name__ == "__main__":
    main()
