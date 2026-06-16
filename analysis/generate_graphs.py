"""Gera tabelas e graficos a partir dos CSVs de benchmark.

Saidas principais:
- results/summary_results.csv
- analysis/graphs/python_worst_vs_teorico.png
- analysis/graphs/java_worst_vs_teorico.png
- analysis/graphs/python_vs_java_worst.png
- analysis/graphs/casos_python.png
- analysis/graphs/casos_java.png
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

CASE_LABELS = {
    "best": "Melhor caso",
    "average": "Caso medio",
    "worst": "Pior caso",
}

CASE_ORDER = ["best", "average", "worst"]


def load_data(paths: list[Path]) -> pd.DataFrame:
    frames = []
    for path in paths:
        if path.exists():
            frame = pd.read_csv(path)
            frames.append(frame)
        else:
            print(f"Aviso: CSV nao encontrado: {path}")
    if not frames:
        raise FileNotFoundError("Nenhum CSV de benchmark encontrado. Execute os benchmarks primeiro.")
    df = pd.concat(frames, ignore_index=True)
    df["time_ms"] = pd.to_numeric(df["time_ms"], errors="coerce")
    df["recursive_calls"] = pd.to_numeric(df["recursive_calls"], errors="coerce")
    df["n"] = pd.to_numeric(df["n"], errors="coerce").astype(int)
    return df


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["language", "algorithm", "case", "n"], as_index=False)
        .agg(
            runs=("time_ms", "count"),
            mean_ms=("time_ms", "mean"),
            std_ms=("time_ms", "std"),
            min_ms=("time_ms", "min"),
            max_ms=("time_ms", "max"),
            mean_calls=("recursive_calls", "mean"),
        )
        .sort_values(["case", "language", "n"])
    )


def save_markdown_summary(summary: pd.DataFrame, out: Path) -> None:
    lines = ["# Resumo dos resultados", "", "Valores em milissegundos. Media e desvio-padrao calculados a partir das rodadas coletadas.", ""]
    for case in CASE_ORDER:
        subset = summary[summary["case"] == case]
        if subset.empty:
            continue
        lines.append(f"## {CASE_LABELS[case]}")
        lines.append("")
        lines.append("| Linguagem | n | Rodadas | Media (ms) | Desvio | Minimo | Maximo | Chamadas medias |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
        for _, row in subset.iterrows():
            lines.append(
                f"| {row['language']} | {int(row['n'])} | {int(row['runs'])} | "
                f"{row['mean_ms']:.6f} | {row['std_ms']:.6f} | {row['min_ms']:.6f} | "
                f"{row['max_ms']:.6f} | {row['mean_calls']:.2f} |"
            )
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")


def plot_theoretical_curve(summary: pd.DataFrame, language: str, out_dir: Path) -> None:
    subset = summary[(summary["language"] == language) & (summary["case"] == "worst")].sort_values("n")
    if subset.empty:
        return

    n_values = subset["n"].to_list()
    measured = subset["mean_ms"].to_list()
    first_n = n_values[0]
    first_time = max(measured[0], 1e-9)
    theoretical = [first_time * (2 ** (n - first_n)) for n in n_values]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(n_values, measured, marker="o", label="Tempo medido")
    ax.plot(n_values, theoretical, marker="x", linestyle="--", label="Curva teorica proporcional a 2^n")
    ax.set_title(f"{language} - pior caso: tempo medido vs curva teorica")
    ax.set_xlabel("Tamanho da entrada (n)")
    ax.set_ylabel("Tempo medio (ms)")
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / f"{language.lower()}_worst_vs_teorico.png", dpi=220)
    plt.close(fig)


def plot_python_vs_java_worst(summary: pd.DataFrame, out_dir: Path) -> None:
    subset = summary[summary["case"] == "worst"].copy()
    if subset.empty:
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    for language, group in subset.groupby("language"):
        group = group.sort_values("n")
        ax.plot(group["n"], group["mean_ms"], marker="o", label=language)
        std = group["std_ms"].fillna(0)
        ax.fill_between(group["n"], group["mean_ms"] - std, group["mean_ms"] + std, alpha=0.15)

    ax.set_title("Backtracking - pior caso: Python vs Java")
    ax.set_xlabel("Tamanho da entrada (n)")
    ax.set_ylabel("Tempo medio (ms)")
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / "python_vs_java_worst.png", dpi=220)
    plt.close(fig)


def plot_cases_by_language(summary: pd.DataFrame, language: str, out_dir: Path) -> None:
    subset = summary[summary["language"] == language]
    if subset.empty:
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    for case in CASE_ORDER:
        group = subset[subset["case"] == case].sort_values("n")
        if group.empty:
            continue
        ax.plot(group["n"], group["mean_ms"], marker="o", label=CASE_LABELS[case])

    ax.set_title(f"Backtracking em {language}: melhor, medio e pior caso")
    ax.set_xlabel("Tamanho da entrada (n)")
    ax.set_ylabel("Tempo medio (ms)")
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / f"casos_{language.lower()}.png", dpi=220)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera graficos e resumo estatistico dos benchmarks.")
    parser.add_argument("--python-csv", type=Path, default=Path("results/results_python.csv"))
    parser.add_argument("--java-csv", type=Path, default=Path("results/results_java.csv"))
    parser.add_argument("--out-dir", type=Path, default=Path("analysis/graphs"))
    parser.add_argument("--summary-out", type=Path, default=Path("results/summary_results.csv"))
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)

    df = load_data([args.python_csv, args.java_csv])
    summary = summarize(df)
    summary.to_csv(args.summary_out, index=False)
    save_markdown_summary(summary, args.summary_out.with_suffix(".md"))

    for language in sorted(summary["language"].unique()):
        plot_theoretical_curve(summary, language, args.out_dir)
        plot_cases_by_language(summary, language, args.out_dir)

    plot_python_vs_java_worst(summary, args.out_dir)

    print(f"Resumo CSV salvo em: {args.summary_out}")
    print(f"Resumo Markdown salvo em: {args.summary_out.with_suffix('.md')}")
    print(f"Graficos salvos em: {args.out_dir}")


if __name__ == "__main__":
    main()
