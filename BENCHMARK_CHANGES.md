# Benchmark Suite Updates

## Problem Identified

The previous benchmark configuration had **BFS-Tree and UCS-Tree with 0% success rate** because:

1. **Iteration limits too low**: Tree algorithms were limited to 100,000 iterations
2. **Maps too large**: Even on empty 10x10 maps, tree algorithms couldn't complete
3. **No size progression**: Missing smaller maps where tree algorithms can succeed

## Changes Made

### 1. Added Progressive Map Sizes

**New map size progression:**
- **5x5**: Very small (good for tree algorithms)
- **7x7**: Small (tree algorithms should work)
- **10x10**: Medium (as requested)
- **15x15**: Large (as requested)
- **20x20**: Extra large (as requested)

**Environment types per size:**
- Small maps (5x5, 7x7): `empty`, `simple_obstacles`
- Medium/Large/XL maps (10x10, 15x15, 20x20): `empty`, `simple_obstacles`, `corridor`, `rooms`, `dense`

### 2. Adaptive Algorithm Limits

Tree algorithms now use **adaptive limits based on map size**:

| Map Size | Max Depth | Max Iterations | Timeout | Trials |
|----------|-----------|----------------|---------|--------|
| ≤ 7x7    | 10,000    | 500,000        | 60s     | 50     |
| ≤ 10x10  | 8,000     | 300,000        | 45s     | 20     |
| > 10x10  | 5,000     | 100,000        | 30s     | 10     |

**Graph algorithms** remain unchanged:
- Max depth: 50,000
- Max iterations: 1,000,000
- Timeout: 60s
- Trials: 100

### 3. New Visualization: Complexity Analysis

Added a new plot (`13_complexity_analysis.png`) that shows:
- Execution time vs map size (10x10, 15x15, 20x20)
- Nodes expanded vs map size
- Memory usage vs map size
- Success rate vs map size

This directly addresses your request for **complexity level comparisons**.

### 4. Enhanced Report

The benchmark report now includes:
- **Complexity Analysis section**: Overall performance metrics by map size
- **Algorithm Performance by Map Size**: Detailed breakdown showing how each algorithm performs on each map size

## Expected Outcomes

With these changes:

1. **BFS-Tree and UCS-Tree should now succeed** on smaller maps (5x5, 7x7)
2. **Comprehensive complexity comparison** across 10x10, 15x15, and 20x20 maps
3. **Better understanding** of how map size affects algorithm performance
4. **More granular data** for research and analysis

## Running the Updated Benchmark

```bash
python benchmark_suite.py
```

This will generate:
- CSV file with all results
- 13 visualization plots (including the new complexity analysis)
- Comprehensive text report with complexity analysis

## Total Test Configurations

- **Environment configs**: 20 (5 sizes × 4-5 env types)
- **Motion types**: 2 (4-directional, 8-directional)
- **Graph algorithms**: 4 (BFS, UCS, A*-Euclidean, A*-Manhattan)
- **Tree algorithms**: 4 (BFS, UCS, A*-Euclidean, A*-Manhattan)

**Total**: ~320 unique configurations (before trials)
