import json
from pathlib import Path
from typing import Optional

import pandas as pd
from fastapi import FastAPI

app = FastAPI(title="API de Vendas")
CSV = Path(__file__).resolve().parent.parent / "data" / "vendas.csv"


def carregar() -> pd.DataFrame:
    df = pd.read_csv(CSV, parse_dates=["data"])
    df["receita"] = df["quantidade"] * df["preco_unitario"]
    return df


@app.get("/api/filtros")
def filtros():
    df = carregar()
    return {
        "padarias": sorted(df["padaria"].unique().tolist()),
        "produtos": sorted(df["produto"].unique().tolist()),
    }


@app.get("/api/vendas")
def vendas(padaria: Optional[str] = None, produto: Optional[str] = None):
    df = carregar()

    if padaria:
        df = df[df["padaria"] == padaria]
    if produto:
        df = df[df["produto"] == produto]

    por_mes = df.groupby(df["data"].dt.strftime("%Y-%m"))["receita"].sum()

    ultimas = df.sort_values("data", ascending=False).head(10).copy()
    ultimas["data"] = ultimas["data"].dt.strftime("%d/%m/%Y")

    return {
        "filtro": {
            "receita_total": float(df["receita"].sum()),
            "pedidos": int(len(df)),
            "ticket_medio": float(df["receita"].mean()) if len(df) else 0.0,
        },
        "grafico": {
            "meses": por_mes.index.tolist(),
            "valores": [round(float(v), 2) for v in por_mes.values],
        },
        "tabela": json.loads(ultimas.to_json(orient="records")),
    }
