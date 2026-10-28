"""Gera uma planilha FALSA com as mesmas colunas da SISET, para desenvolver sem dados reais."""
import random, sys
import pandas as pd

def gerar(n=40, seed=7):
    rnd = random.Random(seed)
    ref = pd.Timestamp("2026-10-17")
    linhas = []
    for i in range(n):
        digital = rnd.random() < 0.15
        d = lambda: (ref - pd.Timedelta(days=rnd.choice([1, 3, 7, 12, 20, 40, 90]))) if rnd.random() > 0.3 else None
        linhas.append({
            "COD_MATRICULA": f"TESTE{i:04d}", "NOM_ALUNO": None, "END_EMAIL": None,
            "BU": "DIGITAL" if digital else "PRESENCIAL", "NOM_CURSO": "SISTEMAS DE INFORMACAO",
            "CR_PER_ANT": round(rnd.uniform(5, 10), 2), "DT_ULT_ACESSO": d() or ref, "DT_ULT_ACESSO_APP": d(),
            "DT_ULT_ACESSO_SAVA": d(), "DT_ULT_ACESSO_SIA": d(), "FAIXA_ACESSO": None, "FAIXA_PRESENCA_15_DIAS": None,
            "PERC_PRESENCA_2_SEMANAS": "N/A" if digital else rnd.choice([0, 0.5, 0.666667, 0.8, 1.0]),
            "ADESAO_SM_DISC_ONLINE": rnd.choice([0, 1, "PARCIAL", "N/A"]),
            "ADESAO_SM1_DISC_PRES": "N/A" if digital else rnd.choice([0, 1, "PARCIAL"]),
            "ADESAO_SM2_DISC_PRES": "N/A" if digital else 0, "ADESAO_SM_DISC_PRES": None,
        })
    return pd.DataFrame(linhas)

if __name__ == "__main__":
    saida = sys.argv[1] if len(sys.argv) > 1 else "dados_exemplo/planilha_falsa.xlsx"
    gerar().to_excel(saida, index=False)
    print("gerado:", saida)
