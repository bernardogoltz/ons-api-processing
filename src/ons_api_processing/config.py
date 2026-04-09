from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"

BASE_URL = "https://apicarga.ons.org.br/prd/cargaverificada"

VARIAVEIS = {
    "val_cargaglobal": "Carga Global",
    "val_cargaglobalsmmg": "Carga Global s/ MMGD",
    "val_cargammgd": "Carga MMGD",
    "val_cargaglobalcons": "Carga Global Consistida",
    "val_consistencia": "Consistência",
    "val_cargasupervisionada": "Carga Supervisionada",
    "val_carganaosupervisionada": "Carga Não Supervisionada",
}

DEFAULT_VARIAVEL = "val_cargaglobal"

AREAS = {
    "Submercado": {
        "SECO": "SE/CO – Sudeste / Centro-Oeste",
        "N": "N – Norte",
        "NE": "NE – Nordeste",
        "S": "S – Sul",
    },
    "Área Geoelétrica": {
        "BASE": "BASE – Bahia / Sergipe",
        "MA": "MA – Maranhão",
        "DF": "DF – Distrito Federal",
        "GO": "GO – Goiás",
        "MS": "MS – Mato Grosso do Sul",
        "AM": "AM – Amazonas",
        "AP": "AP – Amapá",
        "RR": "RR – Roraima",
        "PI": "PI – Piauí",
        "TON": "TON – Tocantins Norte",
        "AC": "AC – Acre",
        "RS": "RS – Rio Grande do Sul",
        "SP": "SP – São Paulo",
        "MT": "MT – Mato Grosso",
        "TOCO": "TOCO – Tocantins",
        "BAOE": "BAOE – Bahia Oeste",
        "PBRN": "PBRN – Paraíba / Rio Grande do Norte",
        "PR": "PR – Paraná",
        "ES": "ES – Espírito Santo",
        "MG": "MG – Minas Gerais",
        "SC": "SC – Santa Catarina",
        "CE": "CE – Ceará",
        "RO": "RO – Rondônia",
        "PA": "PA – Pará",
        "RJ": "RJ – Rio de Janeiro",
        "ALPE": "ALPE – Alagoas / Pernambuco",
    },
    "Perdas": {
        "PEN": "PEN – Perdas Norte",
        "PES": "PES – Perdas Sul",
        "PENE": "PENE – Perdas Nordeste",
        "PESE": "PESE – Perdas Sudeste",
    },
}