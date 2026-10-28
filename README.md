# motor — WydenCoin

Motor de recompensas em Python: lê a planilha de indicadores, aplica as regras e envia as emissões aprovadas para a API. Responsável: **Henrique**.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
python dados_exemplo/gerar.py                       # cria uma planilha FALSA
python -m motor.cli dados_exemplo/planilha_falsa.xlsx --data-ref 2026-10-17 --ciclo 2026-10-B
```
Com `--enviar`, manda para a API (variáveis `API_URL` e `INTERNAL_API_TOKEN`).

**Planilhas reais nunca entram no repositório** (o `.gitignore` bloqueia `.xlsx` e `.csv`). Guarde-as na pasta privada do projeto.

## Pendências
- Regras de evolução (`VOLTOU`, `PRES_SUBIU`) precisam de duas extrações.
- `ESTUDO_30` e `ESTUDO_SUBIU` aguardam a coluna de tempo de estudo.
- Ler os valores da tabela `regras` no banco em vez de `VALORES_PADRAO`.
