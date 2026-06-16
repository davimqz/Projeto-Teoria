import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public final class Benchmark {
    private record Instance(int instanceId, String scenario, int n, int run, int target, int sumValues, int[] values) {}
    private record Measurement(double seconds, boolean exists, long calls) {}

    public static void main(String[] args) throws IOException {
        Locale.setDefault(Locale.US);

        Path instancesPath = Path.of("data/instances.csv");
        Path out = Path.of("results/results_java.csv");
        boolean onlyPrimarySizes = false;

        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case "--instances" -> {
                    if (i + 1 >= args.length) {
                        throw new IllegalArgumentException("Falta valor para --instances");
                    }
                    instancesPath = Path.of(args[++i]);
                }
                case "--out" -> {
                    if (i + 1 >= args.length) {
                        throw new IllegalArgumentException("Falta valor para --out");
                    }
                    out = Path.of(args[++i]);
                }
                case "--only-primary-sizes" -> onlyPrimarySizes = true;
                default -> throw new IllegalArgumentException("Argumento desconhecido: " + args[i]);
            }
        }

        List<Instance> instances = loadInstances(instancesPath);
        if (onlyPrimarySizes) {
            instances = instances.stream().filter(instance -> instance.n == 10 || instance.n == 15 || instance.n == 20).toList();
        }

        warmUp();
        writeMeasurements(out, instances);

        System.out.println("CSV Java gerado: " + out);
        System.out.println("Linhas medidas: " + instances.size());
    }

    private static List<Instance> loadInstances(Path path) throws IOException {
        List<Instance> instances = new ArrayList<>();
        try (BufferedReader reader = Files.newBufferedReader(path)) {
            String header = reader.readLine();
            if (header == null) {
                throw new IOException("CSV vazio: " + path);
            }

            String line;
            while ((line = reader.readLine()) != null) {
                if (line.isBlank()) {
                    continue;
                }
                String[] parts = line.split(",", 7);
                if (parts.length != 7) {
                    throw new IOException("Linha invalida no CSV de instancias: " + line);
                }
                int[] values = parseValues(parts[6]);
                instances.add(new Instance(
                        Integer.parseInt(parts[0]),
                        parts[1],
                        Integer.parseInt(parts[2]),
                        Integer.parseInt(parts[3]),
                        Integer.parseInt(parts[4]),
                        Integer.parseInt(parts[5]),
                        values
                ));
            }
        }
        return instances;
    }

    private static int[] parseValues(String rawValues) {
        String[] tokens = rawValues.trim().split("\\s+");
        int[] values = new int[tokens.length];
        for (int i = 0; i < tokens.length; i++) {
            values[i] = Integer.parseInt(tokens[i]);
        }
        return values;
    }

    private static void warmUp() {
        SubsetSum solver = new SubsetSum();
        int[] values = {7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47};
        int target = 10_000;
        for (int i = 0; i < 500; i++) {
            solver.solve(values, target, true);
        }
    }

    private static void writeMeasurements(Path out, List<Instance> instances) throws IOException {
        Path parent = out.getParent();
        if (parent != null) {
            Files.createDirectories(parent);
        }

        try (BufferedWriter writer = Files.newBufferedWriter(out)) {
            writer.write("language,algorithm,instance_id,case,n,run,target,sum_values,exists,recursive_calls,time_seconds,time_ms\n");
            for (Instance instance : instances) {
                Measurement measurement = runOne(instance.values, instance.target);
                writer.write(String.format(Locale.US,
                        "Java,Backtracking,%d,%s,%d,%d,%d,%d,%s,%d,%.10f,%.6f%n",
                        instance.instanceId,
                        instance.scenario,
                        instance.n,
                        instance.run,
                        instance.target,
                        instance.sumValues,
                        Boolean.toString(measurement.exists),
                        measurement.calls,
                        measurement.seconds,
                        measurement.seconds * 1000.0
                ));
            }
        }
    }

    private static Measurement runOne(int[] values, int target) {
        SubsetSum solver = new SubsetSum();
        long start = System.nanoTime();
        SubsetSum.Result result = solver.solve(values, target, true);
        long end = System.nanoTime();
        return new Measurement((end - start) / 1_000_000_000.0, result.exists, result.calls);
    }
}
