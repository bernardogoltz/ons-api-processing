import pandas as pd 
import requests

from ons_api_processing.config import BASE_URL

def _quarter_ranges(inicio: str, fim: str) -> list[tuple[str, str]]:
    ts_inicio = pd.Timestamp(inicio)
    ts_fim = pd.Timestamp(fim)
    quarter_start = ts_inicio.to_period("Q").start_time
    trimestres = pd.date_range(quarter_start, ts_fim, freq="QS")
    batches = []
    for q in trimestres:
        batch_start = q.strftime("%Y-%m-%d")
        batch_end = (q + pd.offsets.QuarterEnd(0)).strftime("%Y-%m-%d")
        batches.append((batch_start, batch_end))
    return batches


def fetch_carga(area: str, inicio: str, fim: str, timeout: float = 30.0) -> pd.DataFrame:
    ts_inicio = pd.Timestamp(inicio, tz="UTC")
    ts_fim = pd.Timestamp(fim, tz="UTC")

    dfs = []
    for batch_start, batch_end in _quarter_ranges(inicio, fim):
        r = requests.get(
            BASE_URL,
            params={"dat_inicio": batch_start, "dat_fim": batch_end, "cod_areacarga": area},
            timeout=timeout,
        )
        if r.status_code == 200 and r.json():
            dfs.append(pd.DataFrame(r.json()))

    if not dfs:
        return pd.DataFrame()

    df = pd.concat(dfs, ignore_index=True)
    df["din_referenciautc"] = pd.to_datetime(df["din_referenciautc"])
    df = df.sort_values("din_referenciautc").reset_index(drop=True)

    agora = pd.Timestamp.now(tz="UTC")
    limite = min(ts_fim + pd.Timedelta(days=1), agora)
    mask = (df["din_referenciautc"] >= ts_inicio) & (df["din_referenciautc"] <= limite)
    return df.loc[mask].reset_index(drop=True)