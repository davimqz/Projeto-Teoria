# Subconjunto Soma (Subset Sum) — Backtracking

Este repositório contém a implementação e a infraestrutura de experimentos para o estudo do algoritmo de backtracking aplicado ao problema Subconjunto Soma (Subset Sum), desenvolvido para a disciplina **Teoria da Computação**.

## Sumário

- Descrição
- Requisitos
- Estrutura do projeto
- Execução rápida (Linux/macOS e Windows)
- Como reproduzir os experimentos
- Saída esperada
- Contribuições e contatos

## Descrição

O objetivo é comparar implementações em Python e Java, medir tempos (melhor, médio e pior caso) e gerar tabelas e gráficos que suportem a análise experimental.

## Requisitos

- Python 3.8+ (recomenda-se criar um ambiente virtual)
- Dependências Python em `requirements.txt` (instale com `pip install -r requirements.txt`)
- JDK (Java 11+ recomendado)
- Ferramenta de shell (para `run_all.sh`) — no Windows use Git Bash, WSL ou adapte os comandos manualmente

## Estrutura do projeto

Principais pastas e arquivos:

- `data/` — scripts para gerar instâncias (`generate_instances.py`) e o CSV `instances.csv` gerado
- `python/` — implementação Python (`subset_sum.py`) e benchmark (`benchmark.py`)
- `java/src/` — implementação Java (`SubsetSum.java`, `Benchmark.java`) e `java/README.md` com detalhes Java
- `analysis/` — scripts para gerar gráficos (`generate_graphs.py`) e a pasta `analysis/graphs/` com figuras geradas
- `results/` — CSVs e resumo gerados pelos benchmarks
- `run_all.sh` — script que automatiza geração de instâncias, execução dos benchmarks e geração de gráficos

## Execução rápida

Linux / macOS (a partir da raiz do projeto):

```bash
chmod +x run_all.sh
./run_all.sh
```

Windows (recomendações):

- Use Git Bash ou WSL para executar `run_all.sh` tal como acima. Ou execute manualmente os passos abaixo no PowerShell/Prompt:

1) Gerar instâncias (exemplo):

```powershell
python data/generate_instances.py --runs 30 --sizes 8 10 12 14 15 16 18 20 --out data/instances.csv
```

2) Executar benchmark em Python:

```powershell
pip install -r requirements.txt
python python/benchmark.py --instances data/instances.csv --out results/results_python.csv
```

3) Compilar e executar benchmark em Java:

```powershell
javac -d java/out java/src/*.java
java -cp java/out Benchmark --instances data/instances.csv --out results/results_java.csv
```

4) Gerar gráficos e resumo:

```powershell
python analysis/generate_graphs.py \
  --python-csv results/results_python.csv \
  --java-csv results/results_java.csv \
  --out-dir analysis/graphs \
  --summary-out results/summary_results.csv
```

## Como reproduzir os experimentos (passo a passo)

1. Garantir dependências (ver seção Requisitos).
2. Gerar `data/instances.csv` com `data/generate_instances.py`.
3. Executar `python/benchmark.py` e `java/Benchmark` apontando para o mesmo `instances.csv`.
4. Agregar resultados em `results/` e gerar gráficos com `analysis/generate_graphs.py`.
5. Anotar o ambiente de execução (CPU, RAM, SO, versões de Python/Java) no relatório.

## Saída esperada

Após execução completa, os arquivos principais gerados são:

- `results/results_python.csv`
- `results/results_java.csv`
- `results/summary_results.csv`
- `results/summary_results.md`
- Gráficos em `analysis/graphs/` (ex.: `python_worst_vs_teorico.png`)

## Boas práticas e observações

- Execute os benchmarks em um ambiente com pouca variação de carga para obter tempos consistentes.
- Use o mesmo `instances.csv` para Python e Java para comparar resultados.
- O pior caso experimental foi definido como `W = soma(S) + 1` (sem solução), para forçar exploração máxima.

## Contribuição

Abra uma issue ou envie um pull request. Para mudanças que afetam reprodutibilidade, atualize também `results/` e `analysis/` conforme necessário.

## Referências e contato

Para detalhes sobre a metodologia e resultados, veja o relatório em `relatorio/`. Para dúvidas, contate o autor do trabalho (incluir e-mail no repositório se desejar).

---

Arquivo atualizado automaticamente para facilitar execução em Windows e Linux. Se quiser, posso ajustar a seção de instalação passo a passo ou adicionar badges e instruções para GitHub Actions.
