# Implementação Java

Compile a partir da raiz do projeto:

```bash
javac -d java/out java/src/SubsetSum.java java/src/Benchmark.java
```

Execute o benchmark usando as mesmas instâncias usadas pelo Python:

```bash
java -cp java/out Benchmark --instances data/instances.csv --out results/results_java.csv
```

O programa usa `System.nanoTime()` para medição, conforme recomendado no roteiro.
