"""Benchmark do Subset Sum por backtracking em Python.

Le instancias de data/instances.csv, executa o algoritmo e salva os tempos em CSV.
O arquivo de instancias e compartilhado com Java para garantir comparacao justa.
"""
from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path

from subset_sum import subset_sum_backtracking


FIELDNAMES = [
    "language",
    "algorithm",
    "instance_id",
    "case",
    "n",
    "run",
    "target",
    "sum_values",
    "exists",
    "recursive_calls",
    "time_seconds",
    "time_ms",
]


def load_instances(path: Path) -> list[dict[str, object]]:
    instances: list[dict[str, object]] = []
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            values = [int(part) for part in row["values"].split() if part]
            instances.append({
                "instance_id": int(row["instance_id"]),
                "case": row["case"],
                "n": int(row["n"]),
                "run": int(row["run"]),
                "target": int(row["target"]),
                "sum_values": int(row["sum_values"]),
                "values": values,
            })
    return instances


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa benchmark Python do Subset Sum por backtracking.")
    parser.add_argument("--instances", type=Path, default=Path("data/instances.csv"))
    parser.add_argument("--out", type=Path, default=Path("results/results_python.csv"))
    parser.add_argument("--only-primary-sizes", action="store_true", help="Usa apenas n=10, 15 e 20.")
    args = parser.parse_args()

    instances = load_instances(args.instances)
    if args.only_primary_sizes:
        instances = [inst for inst in instances if inst["n"] in {10, 15, 20}]

    rows = []
    for inst in instances:
        values = inst["values"]
        assert isinstance(values, list)
        start = time.perf_counter()
        result = subset_sum_backtracking(values, int(inst["target"]), use_pruning=True)
        elapsed_seconds = time.perf_counter() - start
        rows.append({
            "language": "Python",
            "algorithm": "Backtracking",
            "instance_id": inst["instance_id"],
            "case": inst["case"],
            "n": inst["n"],
            "run": inst["run"],
            "target": inst["target"],
            "sum_values": inst["sum_values"],
            "exists": str(result.exists).lower(),
            "recursive_calls": result.calls,
            "time_seconds": f"{elapsed_seconds:.10f}",
            "time_ms": f"{elapsed_seconds * 1000:.6f}",
        })

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV Python gerado: {args.out}")
    print(f"Linhas medidas: {len(rows)}")


if __name__ == "__main__":
    main()
