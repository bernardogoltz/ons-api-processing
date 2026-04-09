# ons-api-processing

> Cliente Python para download e processamento de dados de carga verificada da API do ONS.

[![Python](https://img.shields.io/badge/python-3.12+-blue)](https://www.python.org)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


O `ons-api-processing` é um pacote Python para consulta, processamento e exportação dos dados de carga verificada semi-horária disponibilizados pela API de [Dados Abertos do ONS](https://dados.ons.org.br/dataset/carga-energia-verificada). Os dados cobrem todas as áreas geoelétricas e submercados do Sistema Interligado Nacional (SIN).

## Funcionalidades

- Download de carga verificada semi-horária com batching trimestral automático
- Parsing e tipagem dos dados brutos da API
- Geração de features temporais (hora, mês, dia da semana)
- Agregação em resumo diário por área de carga
- Exportação em Parquet e visualização com Matplotlib
- CLI interativa com Rich, incluindo dicionário de dados integrado

## Exemplo Rápido

Via linha de comando:

```bash
# Carga de São Paulo, janeiro de 2024
uv run ons-carga SP 2024-01-01 2024-01-31

# Com gráfico
uv run ons-carga SP 2024-01-01 2024-01-31 --plot

# Dicionário de dados e áreas disponíveis
uv run ons-carga --dicionario
```

Via Python:

```python
from ons_api_processing.api.client import fetch_carga
from ons_api_processing.processing.transform import parse_raw, add_time_features

df = fetch_carga("SP", "2024-01-01", "2024-01-31")
df = parse_raw(df)
df = add_time_features(df)
```

### Instalação do `uv`

O projeto usa [uv](https://docs.astral.sh/uv/) como gerenciador de pacotes e ambientes virtuais.

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**pip:**
```bash
pip install uv
```

**pipx:**
```bash
pipx install uv
```

Após instalar, feche e reabra o terminal. Verifique com `uv --version`.

Mais opções de instalação em [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/).

## Instalação

```bash
git clone https://github.com/bernardogoltz/ons-api-processing.git
cd ons-api-processing
uv sync
```

O `uv sync` cria o ambiente virtual (`.venv/`), instala todas as dependências e o pacote em modo editável automaticamente.
