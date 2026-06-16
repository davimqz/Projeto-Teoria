public final class SubsetSum {
    public static final class Result {
        public final boolean exists;
        public final long calls;

        public Result(boolean exists, long calls) {
            this.exists = exists;
            this.calls = calls;
        }
    }

    private long calls;

    public Result solve(int[] values, int target, boolean usePruning) {
        this.calls = 0L;
        boolean exists = search(values, target, 0, 0, usePruning);
        return new Result(exists, this.calls);
    }

    private boolean search(int[] values, int target, int index, int currentSum, boolean usePruning) {
        calls++;

        if (currentSum == target) {
            return true;
        }

        if (index == values.length) {
            return false;
        }

        if (usePruning && currentSum > target) {
            return false;
        }

        if (search(values, target, index + 1, currentSum + values[index], usePruning)) {
            return true;
        }

        return search(values, target, index + 1, currentSum, usePruning);
    }
}
