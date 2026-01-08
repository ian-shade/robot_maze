# Quick Start: Running the Updated Benchmark

## What Changed?

### Problem Fixed
- **BFS-Tree and UCS-Tree had 0% success rate** → Now testing on smaller maps (5×5, 7×7) with higher iteration limits

### New Features
- **Progressive complexity**: 5×5, 7×7, 10×10, 15×15, 20×20 map sizes
- **Adaptive limits**: Tree algorithms get more iterations on smaller maps
- **New visualization**: Complexity analysis showing performance across map sizes
- **Enhanced reports**: Detailed breakdown by map size

## Running the Benchmark

```bash
# From project root
python benchmark_suite.py
```

## What to Expect

### Runtime
- **1-3 hours** depending on your system
- More configurations tested (~320 vs previous 112)
- ~12,000+ total executions

### Output Files

All files saved to `benchmark_results/`:

#### CSV Data
- `benchmark_results_YYYYMMDD_HHMMSS.csv` - Raw data

#### Visualizations (13 total)
1. Algorithm comparison
2. Environment impact
3. Motion model comparison
4. Heuristic comparison
5. Tree vs Graph comparison
6. Execution time distribution
7. Time vs nodes scatter
8. Cost vs length
9. Memory efficiency
10. Success rate
11. Overall efficiency
12. Performance consistency
13. **NEW: Complexity analysis** (10×10, 15×15, 20×20)

#### Reports
- `benchmark_report.txt` - Comprehensive statistics including:
  - Algorithm rankings
  - Success rates
  - Environment impact
  - **NEW: Complexity analysis by map size**
  - **NEW: Algorithm performance per map size**

## Expected Results

### Tree Algorithms
- **BFS-Tree**: Should achieve >0% success on 5×5 and 7×7 maps
- **UCS-Tree**: Should achieve >0% success on 5×5 and 7×7 maps
- **A*-Tree**: Should show better success rates on smaller maps

### Complexity Analysis
- Clear visualization of how algorithms scale with map size
- Performance trends across 10×10, 15×15, 20×20
- Memory and time growth patterns

## Benchmark Configuration Summary

| Map Size | Tree Iterations | Tree Timeout | Tree Trials |
|----------|----------------|--------------|-------------|
| 5×5      | 500,000        | 60s          | 50          |
| 7×7      | 500,000        | 60s          | 50          |
| 10×10    | 300,000        | 45s          | 20          |
| 15×15    | 100,000        | 30s          | 10          |
| 20×20    | 100,000        | 30s          | 10          |

Graph algorithms: 1,000,000 iterations, 60s timeout, 100 trials (all sizes)

## Environment Types Tested

| Map Size | Environments |
|----------|-------------|
| 5×5, 7×7 | empty, simple_obstacles |
| 10×10, 15×15, 20×20 | empty, simple_obstacles, corridor, rooms, dense |

## Next Steps

1. **Run the benchmark**: `python benchmark_suite.py`
2. **Wait for completion**: 1-3 hours
3. **Review results**: Check `benchmark_results/` folder
4. **Compare with old results**: See [BENCHMARK_SUMMARY.md](BENCHMARK_SUMMARY.md)

## Questions?

See detailed documentation:
- [BENCHMARK_CHANGES.md](BENCHMARK_CHANGES.md) - What changed and why
- [BENCHMARK_SUMMARY.md](BENCHMARK_SUMMARY.md) - Previous results and methodology
- [benchmark_suite.py](benchmark_suite.py) - Source code
