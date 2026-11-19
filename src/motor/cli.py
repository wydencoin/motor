"""Uso:
motor planilha.xlsx --data-ref 2026-10-17 --ciclo 2026-10-B          # prévia
motor planilha.xlsx --data-ref 2026-10-17 --ciclo 2026-10-B --enviar # envia à API
"""

import argparse
import os
import sys

import pandas as pd
import requests

from .leitura import ler_planilha
from .regras import regras_de_ciclo


def main(argv=None):
    p = argparse.ArgumentParser(description="Motor de recompensas WydenCoin")
    p.add_argument("planilha")
    p.add_argument("--data-ref", required=True, help="data de extração da planilha (AAAA-MM-DD)")
    p.add_argument("--ciclo", required=True, help="ex.: 2026-10-B")
    p.add_argument("--enviar", action="store_true")
    a = p.parse_args(argv)

    emissoes = regras_de_ciclo(ler_planilha(a.planilha), a.data_ref)
    tab = pd.DataFrame([e.__dict__ for e in emissoes])
    total_wc = tab["valor"].sum() if not tab.empty else 0
    total_alunos = tab["matricula"].nunique() if not tab.empty else 0
    print(f"{len(tab)} emissões, {total_wc} WC, {total_alunos} alunos")
    if not tab.empty:
        print(tab.groupby("regra")["valor"].agg(["count", "sum"]).to_string())

    if a.enviar:
        url, token = os.environ["API_URL"], os.environ["INTERNAL_API_TOKEN"]
        corpo = {"ciclo": a.ciclo, "emissoes": tab.to_dict(orient="records")}
        r = requests.post(
            f"{url}/internal/emissoes",
            json=corpo,
            headers={"Authorization": f"Bearer {token}"},
            timeout=60,
        )
        print("API respondeu", r.status_code, r.text[:200])
        return 0 if r.ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
