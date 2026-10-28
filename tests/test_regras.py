import pandas as pd
from motor.leitura import normalizar
from motor.regras import regras_de_ciclo, regras_de_simulado, regras_de_semestre

BASE = {"BU": "PRESENCIAL", "CR_PER_ANT": 8.5, "DT_ULT_ACESSO": "2026-10-16", "DT_ULT_ACESSO_SAVA": None,
        "DT_ULT_ACESSO_SIA": None, "PERC_PRESENCA_2_SEMANAS": "N/A", "ADESAO_SM_DISC_ONLINE": "N/A",
        "ADESAO_SM1_DISC_PRES": "N/A", "ADESAO_SM2_DISC_PRES": "N/A"}

def df(*linhas):
    return normalizar(pd.DataFrame([{**BASE, "COD_MATRICULA": f"T{i}", **l} for i, l in enumerate(linhas)]))

def regras(emissoes, mat):
    return sorted(e.regra for e in emissoes if e.matricula == mat)

def test_acesso_sia_dentro_e_fora_dos_15_dias():
    e = regras_de_ciclo(df({"DT_ULT_ACESSO_SIA": "2026-10-02"}, {"DT_ULT_ACESSO_SIA": "2026-10-01"}), "2026-10-17")
    assert regras(e, "T0") == ["SIA_15D"]      # 15 dias: paga
    assert regras(e, "T1") == []               # 16 dias: não paga

def test_presenca_faixas():
    e = regras_de_ciclo(df({"PERC_PRESENCA_2_SEMANAS": 1}, {"PERC_PRESENCA_2_SEMANAS": 0.666667}, {"PERC_PRESENCA_2_SEMANAS": 0.5}), "2026-10-17")
    assert regras(e, "T0") == ["PRES_100"] and regras(e, "T1") == ["PRES_60"] and regras(e, "T2") == []

def test_digital_ganha_dig_estudo_pelo_ambiente_virtual():
    e = regras_de_ciclo(df({"BU": "DIGITAL", "DT_ULT_ACESSO_SAVA": "2026-10-10"}), "2026-10-17")
    assert regras(e, "T0") == ["DIG_ESTUDO", "SAVA_15D"]

def test_simulado_sim_parcial_e_na():
    e = regras_de_simulado(df({"ADESAO_SM1_DISC_PRES": 1}, {"ADESAO_SM1_DISC_PRES": "PARCIAL"}, {}), "ADESAO_SM1_DISC_PRES")
    assert [x.regra for x in e] == ["SIM_FEZ", "SIM_PARCIAL"]

def test_cr_vazio_nao_paga():
    e = regras_de_semestre(df({"CR_PER_ANT": 9.1}, {"CR_PER_ANT": None}, {"CR_PER_ANT": 6.9}))
    assert [(x.matricula, x.regra) for x in e] == [("T0", "CR_9")]
