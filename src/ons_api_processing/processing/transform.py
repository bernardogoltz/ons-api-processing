import pandas as pd

def parse_raw(df: pd.DataFrame) -> pd.DataFrame:
    """Ajusta tipos do DataFrame cru da API."""
    df["din_referenciautc"] = pd.to_datetime(df["din_referenciautc"])
    df["dat_referencia"] = pd.to_datetime(df["dat_referencia"])

    cols_val = [c for c in df.columns if c.startswith("val_")]
    df[cols_val] = df[cols_val].apply(pd.to_numeric, errors="coerce")

    return df


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona colunas derivadas de datetime."""
    df = df.copy()
    dt = df["din_referenciautc"]
    df["date"] = dt.dt.date
    df["hour"] = dt.dt.hour
    df["month"] = dt.dt.month
    df["weekday"] = dt.dt.weekday  # 0=Mon 6=Sun
    return df


def hourly_summary(df: pd.DataFrame, variavel: str = "val_cargaglobal") -> pd.DataFrame:
    """Agrega carga semi-horária em resumo horário (média das duas semi-horas de cada hora)."""
    return (
        df.groupby(["date", "hour", "cod_areacarga"])[variavel]
        .mean()
        .rename("valor")
        .reset_index()
        .sort_values(["date", "hour"])
    )


def daily_summary(df: pd.DataFrame, variavel: str = "val_cargaglobal") -> pd.DataFrame:
    """Agrega carga semi-horária em resumo diário por área."""
    return (
        df.groupby(["date", "cod_areacarga"])[variavel]
        .agg(["mean", "max", "min", "count"])
        .rename(columns={"mean": "carga_media", "max": "carga_max", "min": "carga_min", "count": "n_registros"})
        .reset_index()
    )