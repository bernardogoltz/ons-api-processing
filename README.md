# ons-api-processing

[![Python](https://img.shields.io/badge/python-3.12+-blue)](https://www.python.org)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

O `ons-api-processing` é um pacote Python para consulta, processamento e exportação dos dados de carga verificada semi-horária disponibilizados pela API de [Dados Abertos do ONS](https://dados.ons.org.br/dataset/carga-energia-verificada). Os dados cobrem todas as áreas geoelétricas e submercados do Sistema Interligado Nacional (SIN).

## Instalação

Requer [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
git clone https://github.com/bernardogoltz/ons-api-processing.git
cd ons-api-processing
uv sync
```

## Uso

```bash
# Período — resumo diário
uv run ons-carga SP 2024-01-01 2024-01-31

# Dia único — carga hora a hora
uv run ons-carga SE 2024-01-15

# Escolher variável
uv run ons-carga NE 2024-06-01 2024-06-30 -v val_cargammgd

# Com gráfico
uv run ons-carga SP 2024-01-01 2024-01-31 --plot

# Help: dicionário de dados, áreas e variáveis disponíveis
uv run ons-carga --dicionario
```

## Via Python

```python
from ons_api_processing.api.client import fetch_carga
from ons_api_processing.processing.transform import parse_raw, add_time_features

df = fetch_carga("SP", "2024-01-01", "2024-01-31")
df = parse_raw(df)
df = add_time_features(df)
```

## Licença

[MIT](LICENSE)
