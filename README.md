# Subconjunto Soma (Subset Sum) - Backtracking

Projeto para a disciplina **Teoria da Computação**, com foco na análise teórica e experimental do algoritmo de **backtracking** aplicado ao problema **Subconjunto Soma (Subset Sum)**.

## Estrutura dos entregáveis

```text
subset_sum_backtracking_entrega_final/
├── README.md
├── CHECKLIST_ENTREGA.md
├── run_all.sh
├── relatorio/
│   ├── Relatorio_Subset_Sum_Backtracking_Focado.docx
│   └── Relatorio_Subset_Sum_Backtracking_Focado.pdf
├── slides/
│   ├── Apresentacao_Subset_Sum_Backtracking.pptx
│   └── Apresentacao_Subset_Sum_Backtracking.pdf
├── data/
│   ├── generate_instances.py
│   └── instances.csv               # gerado automaticamente
├── python/
│   ├── subset_sum.py
│   ├── benchmark.py
│   └── requirements.txt
├── java/
│   ├── README.md
│   └── src/
│       ├── SubsetSum.java
│       └── Benchmark.java
├── analysis/
│   ├── generate_graphs.py
│   ├── README.md
│   └── graphs/                     # gerado automaticamente
└── results/                        # CSVs gerados automaticamente
```

## Entregáveis principais

- **Relatório em PDF:** `relatorio/Relatorio_Subset_Sum_Backtracking_Focado.pdf`
- **Slides da apresentação:** `slides/Apresentacao_Subset_Sum_Backtracking.pptx`
- **Código-fonte:** pastas `python/`, `java/`, `data/` e `analysis/`
- **Repositório GitHub:** após subir estes arquivos, inserir o link no relatório e no Classroom.

## Como executar tudo no Linux/macOS

A partir da raiz do projeto:

```bash
chmod +x run_all.sh
./run_all.sh
```

O script executa quatro etapas:

1. gera as mesmas instâncias para Python e Java;
2. executa o benchmark em Python;
3. compila e executa o benchmark em Java;
4. gera tabelas agregadas e gráficos.

## Como executar manualmente

### 1. Gerar entradas padronizadas

```bash
python3 data/generate_instances.py --runs 30 --sizes 8 10 12 14 15 16 18 20 --out data/instances.csv
```

### 2. Executar Python

```bash
python3 python/benchmark.py --instances data/instances.csv --out results/results_python.csv
```

### 3. Executar Java

```bash
javac -d java/out java/src/SubsetSum.java java/src/Benchmark.java
java -cp java/out Benchmark --instances data/instances.csv --out results/results_java.csv
```

### 4. Gerar gráficos e resumo estatístico

```bash
python3 analysis/generate_graphs.py \
  --python-csv results/results_python.csv \
  --java-csv results/results_java.csv \
  --out-dir analysis/graphs \
  --summary-out results/summary_results.csv
```

## Arquivos gerados após a execução

```text
results/results_python.csv
results/results_java.csv
results/summary_results.csv
results/summary_results.md
analysis/graphs/python_worst_vs_teorico.png
analysis/graphs/java_worst_vs_teorico.png
analysis/graphs/python_vs_java_worst.png
analysis/graphs/casos_python.png
analysis/graphs/casos_java.png
```

## Metodologia experimental

- Linguagens: Python e Java.
- Medição em Python: `time.perf_counter()`.
- Medição em Java: `System.nanoTime()`.
- Cenários: melhor caso, caso médio e pior caso.
- Rodadas: 30 por tamanho de entrada e cenário.
- Tamanhos principais: `n = 10`, `n = 15`, `n = 20`.
- Tamanhos adicionais para gráficos: `n = 8`, `12`, `14`, `16`, `18`.
- Pior caso: `W = soma(S) + 1`, impossibilitando solução e evitando ativação da poda `somaAtual > W`.

## Observação importante

Os benchmarks devem ser executados no computador da equipe antes da entrega final. Assim, os tempos, gráficos e conclusões refletem o hardware descrito no relatório.

Depois de rodar os testes, preencher no relatório:

- processador;
- memória RAM;
- sistema operacional;
- versão do Python;
- versão do Java;
- tabelas e gráficos obtidos.

## Sugestão para GitHub

Crie um repositório chamado, por exemplo:

```text
subset-sum-backtracking-teoria
```

Depois, suba esta pasta inteira e coloque o link no relatório e no Classroom.
