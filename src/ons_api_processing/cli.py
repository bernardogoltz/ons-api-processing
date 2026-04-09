import argparse
import json
from pathlib import Path

from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ons_api_processing.api.client import fetch_carga
from ons_api_processing.config import AREAS, BASE_URL, VARIAVEIS, DEFAULT_VARIAVEL
from ons_api_processing.processing.transform import parse_raw, add_time_features, daily_summary, hourly_summary
from ons_api_processing.export.output import save_parquet, plot_daily_load

console = Console()

ASSETS = Path(__file__).parent / "assets"

def parse_args():
    p = argparse.ArgumentParser(description="Baixa e processa carga verificada do ONS")
    p.add_argument("area", type=str, nargs="?", help="Código da área de carga (ex: SE, NE, SP)")
    p.add_argument("inicio", type=str, nargs="?", help="Data inicial (YYYY-MM-DD)")
    p.add_argument("fim", type=str, nargs="?", default=None, help="Data final (YYYY-MM-DD). Se omitido, usa a mesma data de inicio (dia único)")
    p.add_argument(
        "--variavel", "-v",
        type=str,
        default=DEFAULT_VARIAVEL,
        choices=list(VARIAVEIS),
        help=f"Variável a processar (padrão: {DEFAULT_VARIAVEL})",
    )
    p.add_argument("--plot", action="store_true", help="Gerar gráfico diário")
    p.add_argument("--dicionario", action="store_true", help="Exibe dicionário de dados da API")

    return p.parse_args()


def main():
    args = parse_args()

    if args.dicionario:
        show_dicionario()
        return
    
    
    variavel = args.variavel
    variavel_label = VARIAVEIS[variavel]
    fim = args.fim or args.inicio

    console.rule(f"[bold]ONS Carga Verificada — {args.area}")
    if fim == args.inicio:
        console.print(f"Data: {args.inicio}")
    else:
        console.print(f"Período: {args.inicio} → {fim}")
    console.print(f"Variável: [cyan]{variavel_label}[/cyan] ({variavel})")

    with console.status("Buscando dados na API..."):
        df = fetch_carga(args.area, args.inicio, fim)

    if df.empty:
        console.print("[red]Nenhum dado retornado.[/red]")
        return

    console.print(f"[green]{len(df)}[/green] registros recebidos")

    save_parquet(df, f"carga_{args.area}_{args.inicio}_{fim}.parquet", raw=True)

    df = parse_raw(df)
    df = add_time_features(df)
    single_day = fim == args.inicio

    if single_day:
        import datetime
        target_date = datetime.date.fromisoformat(args.inicio)
        hourly = hourly_summary(df, variavel=variavel)
        hourly = hourly[hourly["date"] == target_date]
        save_parquet(hourly, f"horario_{args.area}_{args.inicio}.parquet")

        table = Table(title=f"{variavel_label} — {args.inicio} (por hora)")
        table.add_column("Hora", justify="center")
        table.add_column("MWmed", justify="right")

        for _, row in hourly.iterrows():
            table.add_row(f"{int(row['hour']):02d}:00", f"{row['valor']:.1f}")

        console.print(table)
    else:
        summary = daily_summary(df, variavel=variavel)
        save_parquet(summary, f"resumo_{args.area}_{args.inicio}_{fim}.parquet")

        table = Table(title=f"Resumo Diário — {variavel_label}")
        table.add_column("Data")
        table.add_column("Média (MWmed)", justify="right")
        table.add_column("Máx", justify="right")
        table.add_column("Mín", justify="right")

        for _, row in summary.head(10).iterrows():
            table.add_row(
                str(row["date"]),
                f"{row['carga_media']:.1f}",
                f"{row['carga_max']:.1f}",
                f"{row['carga_min']:.1f}",
            )

        console.print(table)

    if args.plot:
        if single_day:
            hourly = hourly_summary(df, variavel=variavel)
            summary = daily_summary(df, variavel=variavel)
        fig = plot_daily_load(summary, variavel_label=variavel_label)
        fig.savefig(f"data/processed/carga_{args.area}.png", dpi=150)
        console.print("[green]Gráfico salvo[/green]")

def show_dicionario():
    console.print()
    console.rule("[bold cyan]ONS Carga Verificada — Help & Referência[/bold cyan]")
    console.print()

    # --- Uso ---
    usage = Text.assemble(
        ("Uso básico:\n\n", "bold"),
        ("  uv run ons-carga ", "green"),
        ("<area> <inicio>", "yellow"),
        (" [fim]", "yellow"),
        (" [--variavel VAR] [--plot]\n\n", "dim"),
        ("Exemplos:\n\n", "bold"),
        ("  uv run ons-carga SE   2024-01-15", "green"),
        ("                    ← dia único\n", "dim"),
        ("  uv run ons-carga SE   2024-01-01 2024-01-31\n", "green"),
        ("  uv run ons-carga NE   2024-06-01 2024-06-30 --plot\n", "green"),
        ("  uv run ons-carga SP   2025-03-01 2025-03-31 -v val_cargammgd\n", "green"),
        ("  uv run ons-carga SECO 2024-01-01 2024-12-31 --variavel val_cargaglobalsmmg\n\n", "green"),
        ("Opções:\n\n", "bold"),
        ("  -v, --variavel ", "yellow"),
        (f"Variável a processar (padrão: {DEFAULT_VARIAVEL})\n", ""),
        ("  --plot         ", "yellow"),
        ("Gera gráfico de carga diária (PNG)\n", ""),
        ("  --dicionario   ", "yellow"),
        ("Exibe esta referência\n", ""),
    )
    console.print(Panel(usage, title="Como usar", border_style="blue", padding=(1, 2)))

    # --- API ---
    api_info = Text.assemble(
        ("Endpoint:\n", "bold"),
        (f"  {BASE_URL}\n\n", "cyan"),
        ("Parâmetros de query:\n\n", "bold"),
        ("  dat_inicio     ", "yellow"), ("Data inicial (YYYY-MM-DD)\n", ""),
        ("  dat_fim        ", "yellow"), ("Data final (YYYY-MM-DD)\n", ""),
        ("  cod_areacarga  ", "yellow"), ("Código da área (ver tabelas abaixo)\n\n", ""),
        ("Resposta:\n", "bold"),
        ("  JSON array com registros semi-horários (30 min) em UTC\n", ""),
    )
    console.print(Panel(api_info, title="API – Carga Verificada", border_style="blue", padding=(1, 2)))

    # --- Variáveis disponíveis ---
    var_table = Table(
        show_lines=False,
        border_style="dim",
        title_style="bold",
    )
    var_table.add_column("Código (--variavel)", style="green", no_wrap=True)
    var_table.add_column("Descrição")
    var_table.add_column("", justify="center", width=7)

    for code, label in VARIAVEIS.items():
        marker = "[bold yellow]★[/bold yellow]" if code == DEFAULT_VARIAVEL else ""
        var_table.add_row(code, label, marker)

    console.print(Panel(var_table, title="Variáveis Disponíveis  (★ = padrão)", border_style="blue", padding=(1, 2)))

    # --- Áreas de Carga ---
    area_tables = []
    for group_name, codes in AREAS.items():
        t = Table(
            title=f"[bold]{group_name}[/bold]",
            show_lines=False,
            border_style="dim",
            title_style="bold magenta",
            pad_edge=False,
        )
        t.add_column("Código", style="green", min_width=6)
        t.add_column("Descrição")
        for code, desc in codes.items():
            t.add_row(code, desc)
        area_tables.append(t)

    console.print(Panel(
        Columns(area_tables, equal=True, expand=True),
        title="Áreas de Carga Disponíveis",
        border_style="blue",
        padding=(1, 2),
    ))

    # --- Dicionário de dados ---
    with open(ASSETS / "dicionario_carga_verificada.json", encoding="utf-8") as f:
        data = json.load(f)

    dict_table = Table(
        title="[bold]Campos do retorno da API[/bold]",
        show_lines=True,
        border_style="dim",
        title_style="bold",
    )
    dict_table.add_column("Campo", style="green", no_wrap=True)
    dict_table.add_column("Descrição")

    for item in data["dicionario_simplificado"]:
        dict_table.add_row(item["codigo"], item["descricao"])

    console.print(Panel(dict_table, title="Dicionário de Dados", border_style="blue", padding=(1, 2)))
    console.print()


if __name__ == "__main__":
    main()