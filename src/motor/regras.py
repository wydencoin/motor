"""Regras de recompensa v0 (ver docs/regras/regras-v0.md). Valores vêm da tabela `regras` no banco;
VALORES_PADRAO é só para rodar localmente."""
from dataclasses import dataclass
import pandas as pd

VALORES_PADRAO = {
    "SIA_15D": 20, "SAVA_15D": 20, "PRES_100": 40, "PRES_60": 20, "DIG_ESTUDO": 40,
    "SIM_FEZ": 100, "SIM_PARCIAL": 50, "CR_9": 150, "CR_8": 100, "CR_7": 50,
}


@dataclass(frozen=True)
class Emissao:
    matricula: str
    regra: str
    valor: int


def _dias(ref: pd.Timestamp, data) -> float:
    return (ref - data).days if pd.notna(data) else float("inf")


def regras_de_ciclo(df: pd.DataFrame, data_ref: str, valores=VALORES_PADRAO) -> list[Emissao]:
    """Regras pagas a cada ciclo de 15 dias."""
    ref = pd.Timestamp(data_ref)
    out: list[Emissao] = []
    for _, a in df.iterrows():
        m, digital = a["COD_MATRICULA"], a["BU"] == "DIGITAL"
        sava_ok = _dias(ref, a["DT_ULT_ACESSO_SAVA"]) <= 15
        if _dias(ref, a["DT_ULT_ACESSO_SIA"]) <= 15:
            out.append(Emissao(m, "SIA_15D", valores["SIA_15D"]))
        if sava_ok:
            out.append(Emissao(m, "SAVA_15D", valores["SAVA_15D"]))
        p = a["PERC_PRESENCA_2_SEMANAS"]
        if digital:
            if sava_ok:
                out.append(Emissao(m, "DIG_ESTUDO", valores["DIG_ESTUDO"]))
        elif pd.notna(p):
            if p >= 1:
                out.append(Emissao(m, "PRES_100", valores["PRES_100"]))
            elif p >= 0.6:
                out.append(Emissao(m, "PRES_60", valores["PRES_60"]))
    return out


def regras_de_simulado(df: pd.DataFrame, coluna: str, valores=VALORES_PADRAO) -> list[Emissao]:
    """Paga uma vez por simulado (coluna de adesão)."""
    out = []
    for _, a in df.iterrows():
        if a[coluna] == "SIM":
            out.append(Emissao(a["COD_MATRICULA"], "SIM_FEZ", valores["SIM_FEZ"]))
        elif a[coluna] == "PARCIAL":
            out.append(Emissao(a["COD_MATRICULA"], "SIM_PARCIAL", valores["SIM_PARCIAL"]))
    return out


def regras_de_semestre(df: pd.DataFrame, valores=VALORES_PADRAO) -> list[Emissao]:
    out = []
    for _, a in df.iterrows():
        cr = a["CR_PER_ANT"]
        if pd.isna(cr):
            continue
        regra = "CR_9" if cr >= 9 else "CR_8" if cr >= 8 else "CR_7" if cr >= 7 else None
        if regra:
            out.append(Emissao(a["COD_MATRICULA"], regra, valores[regra]))
    return out
