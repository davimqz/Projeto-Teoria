"""Gera instancias padronizadas para os benchmarks em Python e Java.

A ideia e garantir que as duas linguagens recebam exatamente os mesmos vetores e alvos,
evitaria comparacoes entre entradas diferentes. O arquivo gerado e CSV simples e nao depende
de bibliotecas externas.
"""
from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

DEFAULT_SIZES = [8, 10, 12, 14, 15, 16, 18, 20]
DEFAULT_RUNS = 30
DEFAULT_SEED = 20260616


def make_best_case(n: int, rng: random.Random) -> tuple[list[int], int]:
    target = 1000
    values = [target] + [rng.randint(1, 500) for _ in range(n - 1)]
    return values, target


def make_average_case(n: int, rng: random.Random) -> tuple[list[int], int]:
    values = [rng.randint(1, 1000) for _ in range(n)]
    total = sum(values)
    low = max(1, int(total * 0.40))
    high = max(low, int(total * 0.60))
    target = rng.randint(low, high)
    return values, target


def make_worst_case(n: int, rng: random.Random) -> tuple[list[int], int]:
    values = [rng.randint(1, 1000) for _ in range(n)]
    target = sum(values) + 1
    return values, target


CASE_BUILDERS = {
    "best": make_best_case,
    "average": make_average_case,
    "worst": make_worst_case,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera data/instances.csv para benchmarks.")
    parser.add_argument("--sizes", type=int, nargs="+", default=DEFAULT_SIZES)
    parser.add_argument("--runs", type=int, default=DEFAULT_RUNS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out", type=Path, default=Path("data/instances.csv"))
    args = parser.parse_args()

    rows = []
    instance_id = 1
    for case_name, builder in CASE_BUILDERS.items():
        for n in args.sizes:
            for run in range(1, args.runs + 1):
                rng_seed = args.seed + n * 1000 + run * 17 + {"best": 1, "average": 2, "worst": 3}[case_name] * 100000
                rng = random.Random(rng_seed)
                values, target = builder(n, rng)
                rows.append({
                    "instance_id": instance_id,
                    "case": case_name,
                    "n": n,
                    "run": run,
                    "target": target,
                    "sum_values": sum(values),
                    "values": " ".join(str(v) for v in values),
                })
                instance_id += 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["instance_id", "case", "n", "run", "target", "sum_values", "values"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Instancias geradas: {args.out}")
    print(f"Total de linhas: {len(rows)}")


if __name__ == "__main__":
    main()
