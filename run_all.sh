#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3}"

mkdir -p results analysis/graphs java/out

echo "[1/4] Gerando instancias padronizadas..."
"$PYTHON_BIN" data/generate_instances.py --runs 30 --sizes 8 10 12 14 15 16 18 20 --out data/instances.csv

echo "[2/4] Executando benchmark Python..."
"$PYTHON_BIN" python/benchmark.py --instances data/instances.csv --out results/results_python.csv

echo "[3/4] Compilando e executando benchmark Java..."
javac -d java/out java/src/SubsetSum.java java/src/Benchmark.java
java -cp java/out Benchmark --instances data/instances.csv --out results/results_java.csv

echo "[4/4] Gerando tabelas e graficos..."
"$PYTHON_BIN" analysis/generate_graphs.py \
  --python-csv results/results_python.csv \
  --java-csv results/results_java.csv \
  --out-dir analysis/graphs \
  --summary-out results/summary_results.csv

echo "Concluido. Veja results/ e analysis/graphs/."
