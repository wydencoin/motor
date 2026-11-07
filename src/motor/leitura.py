"""Lê a planilha SISET e devolve um DataFrame normalizado (tipos limpos, N/A -> None)."""
import pandas as pd

COLUNAS_OBRIGATORIAS = [
    "COD_MATRICULA", "BU", "CR_PER_ANT", "DT_ULT_ACESSO", "DT_ULT_ACESSO_SAVA",
    "DT_ULT_ACESSO_SIA", "PERC_PRESENCA_2_SEMANAS", "ADESAO_SM_DISC_ONLINE",
    "ADESAO_SM1_DISC_PRES", "ADESAO_SM2_DISC_PRES",
]
DATAS = ["DT_ULT_ACESSO", "DT_ULT_ACESSO_APP", "DT_ULT_ACESSO_SAVA", "DT_ULT_ACESSO_SIA"]
ADESAO = ["ADESAO_SM_DISC_ONLINE", "ADESAO_SM1_DISC_PRES", "ADESAO_SM2_DISC_PRES"]


def _adesao(v):
    s = str(v).strip().upper()
    if s in ("1", "1.0"):
        return "SIM"
    if s == "PARCIAL":
        return "PARCIAL"
    if s in ("0", "0.0"):
        return "NAO"
    return None  # N/A ou vazio = não se aplica


def normalizar(df: pd.DataFrame) -> pd.DataFrame:
    faltando = [c for c in COLUNAS_OBRIGATORIAS if c not in df.columns]
    if faltando:
        raise ValueError(f"colunas faltando na planilha: {faltando}")
    df = df.copy()
    df["COD_MATRICULA"] = df["COD_MATRICULA"].astype(str)
    for c in DATAS:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    df["PERC_PRESENCA_2_SEMANAS"] = pd.to_numeric(df["PERC_PRESENCA_2_SEMANAS"], errors="coerce")
    df["CR_PER_ANT"] = pd.to_numeric(df["CR_PER_ANT"], errors="coerce")
    for c in ADESAO:
        df[c] = df[c].map(_adesao)
    return df


def ler_planilha(caminho: str) -> pd.DataFrame:
    # keep_default_na=False preserva "N/A" como texto para tratarmos de propósito
    return normalizar(pd.read_excel(caminho, keep_default_na=False, na_values=[""]))
