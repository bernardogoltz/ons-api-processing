from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from ons_api_processing.config import DATA_RAW, DATA_PROCESSED


def save_parquet(df: pd.DataFrame, filename: str, raw: bool = False) -> Path:
    """Salva DataFrame como parquet. raw=True salva em data/raw, senão data/processed."""
    output_dir = DATA_RAW if raw else DATA_PROCESSED
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / filename
    df.to_parquet(path, index=False)
    return path


def plot_daily_load(
    df: pd.DataFrame,
    variavel_label: str = "Carga Global",
    title: str | None = None,
) -> plt.Figure:
    """Plota carga média diária por área."""
    fig, ax = plt.subplots(figsize=(12, 5))

    for area in sorted(df["cod_areacarga"].unique()):
        subset = df[df["cod_areacarga"] == area]
        ax.plot(subset["date"], subset["carga_media"], label=area, linewidth=0.8)

    ax.set_title(title or f"{variavel_label} — Verificada Diária")
    ax.set_xlabel("Data")
    ax.set_ylabel(f"{variavel_label} (MWmed)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig