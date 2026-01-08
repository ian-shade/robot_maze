# Robot Maze Pathfinding Benchmark Results

## Overview
Comprehensive benchmark of pathfinding algorithms across multiple environment types, sizes, and motion models.

**Note:** This document reflects the **previous benchmark run**. The benchmark suite has been **updated with new configurations** (see [BENCHMARK_CHANGES.md](BENCHMARK_CHANGES.md) for details).

**Generated:** 2026-01-07 22:59:56
**Total Runs:** 6,720
**Successful Runs:** 4,360
**Success Rate:** 64.88%

### 🆕 Updated Test Configuration (Not Yet Run)
The benchmark suite has been updated to address tree algorithm failures and add comprehensive complexity analysis:
- **New map sizes**: 5×5, 7×7, 10×10, 15×15, 20×20 (progressive complexity)
- **Adaptive limits**: Tree algorithms now have size-based iteration limits
- **Expected improvement**: BFS-Tree and UCS-Tree should achieve >0% success on smaller maps
- **New visualization**: Complexity analysis plot (10×10, 15×15, 20×20 comparison)

See [BENCHMARK_CHANGES.md](BENCHMARK_CHANGES.md) for complete details.

---

## Key Findings

### 🏆 Best Algorithm by Metric

| Metric | Winner | Performance |
|--------|--------|-------------|
| **Fastest Execution** | A*-Graph-Manhattan | 0.000145s average |
| **Fewest Nodes Expanded** | A*-Graph-Manhattan | 37.46 nodes average |
| **Most Optimal Path** | A*-Tree-Euclidean | 14.64 path cost |
| **Most Memory Efficient** | A*-Graph-Manhattan | 85.67 memory usage |
| **Highest Success Rate** | Graph algorithms | 71.4% (all graph algorithms tied) |

### 💡 Critical Insights

1. **A*-Graph-Manhattan is the Overall Winner**
   - Fastest execution time (0.000145s)
   - Lowest node expansion (37.46 nodes)
   - Most memory efficient (85.67 units)
   - High success rate (71.4%)
   - Near-optimal paths (16.57 cost vs 14.64 optimal)

2. **Tree Algorithms Have Major Limitations** ⚠️ *Being addressed in updated tests*
   - **BFS-Tree**: 0% success rate (all runs timeout/fail) - *maps too large for iteration limits*
   - **UCS-Tree**: 0% success rate (all runs timeout/fail) - *maps too large for iteration limits*
   - **A*-Tree-Euclidean**: 57.1% success rate, very slow when working
   - **A*-Tree-Manhattan**: 71.4% success rate, moderate performance
   - Tree algorithms expand far more nodes due to no duplicate detection
   - **Update**: New benchmark includes 5×5 and 7×7 maps with increased limits for tree algorithms

3. **8-Directional Motion is Superior**
   - 76% shorter path cost (14.26 vs 18.70)
   - 62% faster execution (0.00039s vs 0.00101s)
   - 69% fewer nodes expanded (57.15 vs 185.23)
   - Allows diagonal movement for more direct paths

4. **Environment Complexity Impact**
   - **Corridor**: Fastest (0.000252s, 70.6 nodes)
   - **Simple obstacles**: Moderate (0.000503s, 98.9 nodes)
   - **Empty**: Most challenging (0.001118s, 167.6 nodes) - larger search space

---

## Algorithm Rankings

### Execution Time (Lower is Better)
| Rank | Algorithm | Avg Time (s) | Std Dev |
|------|-----------|--------------|---------|
| 1 | A*-Graph-Manhattan | 0.000145 | ±0.000126 |
| 2 | A*-Graph-Euclidean | 0.000227 | ±0.000159 |
| 3 | A*-Tree-Manhattan | 0.000411 | ±0.000692 |
| 4 | BFS-Graph | 0.000437 | ±0.000299 |
| 5 | UCS-Graph | 0.000604 | ±0.000690 |
| 6 | A*-Tree-Euclidean | 0.009675 | ±0.020160 |

### Nodes Expanded (Lower is Better)
| Rank | Algorithm | Avg Nodes | Std Dev |
|------|-----------|-----------|---------|
| 1 | A*-Graph-Manhattan | 37 | ±38 |
| 2 | A*-Graph-Euclidean | 57 | ±48 |
| 3 | BFS-Graph | 100 | ±47 |
| 4 | UCS-Graph | 100 | ±47 |
| 5 | A*-Tree-Manhattan | 102 | ±169 |
| 6 | A*-Tree-Euclidean | 1,321 | ±2,459 |

### Path Optimality (Lower Cost is Better)
| Rank | Algorithm | Avg Cost | Std Dev |
|------|-----------|----------|---------|
| 1 | A*-Tree-Euclidean | 14.64 | ±2.93 |
| 2 | A*-Graph-Euclidean | 16.51 | ±4.57 |
| 3 | BFS-Graph | 16.51 | ±4.57 |
| 4 | UCS-Graph | 16.51 | ±4.57 |
| 5 | A*-Tree-Manhattan | 16.56 | ±4.59 |
| 6 | A*-Graph-Manhattan | 16.57 | ±4.58 |

### Memory Efficiency (Lower is Better)
| Rank | Algorithm | Avg Memory | Std Dev |
|------|-----------|------------|---------|
| 1 | A*-Graph-Manhattan | 86 | ±55 |
| 2 | A*-Graph-Euclidean | 94 | ±42 |
| 3 | UCS-Graph | 114 | ±53 |
| 4 | BFS-Graph | 118 | ±58 |
| 5 | A*-Tree-Manhattan | 277 | ±459 |
| 6 | A*-Tree-Euclidean | 3,540 | ±6,898 |

### Success Rate
| Algorithm | Successes | Total Runs | Rate |
|-----------|-----------|------------|------|
| A*-Graph-Euclidean | 1000 | 1400 | 71.4% |
| A*-Graph-Manhattan | 1000 | 1400 | 71.4% |
| BFS-Graph | 1000 | 1400 | 71.4% |
| UCS-Graph | 1000 | 1400 | 71.4% |
| A*-Tree-Manhattan | 200 | 280 | 71.4% |
| A*-Tree-Euclidean | 160 | 280 | 57.1% |
| BFS-Tree | 0 | 280 | 0.0% |
| UCS-Tree | 0 | 280 | 0.0% |

---

## Motion Model Comparison

| Motion Type | Avg Time (s) | Path Cost | Path Length | Nodes Expanded |
|-------------|--------------|-----------|-------------|----------------|
| **8-directional** | 0.000389 | 14.26 | 12.05 | 57.15 |
| **4-directional** | 0.001013 | 18.70 | 19.70 | 185.23 |
| **Improvement** | **62% faster** | **76% shorter** | **39% shorter** | **69% fewer** |

### Recommendation
**Use 8-directional motion model** for all applications. It provides dramatically better performance across all metrics due to diagonal movement capabilities.

---

## Environment Impact

| Environment | Avg Time (s) | Nodes Expanded | Path Cost |
|-------------|--------------|----------------|-----------|
| Corridor | 0.000252 | 70.63 | 17.13 |
| Simple Obstacles | 0.000503 | 98.89 | 16.46 |
| Empty | 0.001118 | 167.58 | 16.13 |

### Observations
- Corridor environments are most efficient due to constrained search space
- Simple obstacles provide good balance of complexity
- Empty environments have largest search space despite no obstacles

---

## Recommendations

### For Production Use
**Use A*-Graph-Manhattan with 8-directional motion**
- Best overall performance (0.000145s average)
- High reliability (71.4% success)
- Minimal memory usage (86 units)
- Minimal node expansion (37 nodes)
- Near-optimal paths (16.57 vs 14.64 optimal)

### For Optimal Paths
**Use A*-Graph-Euclidean with 8-directional motion**
- Better path quality (16.51 cost)
- Still very fast (0.000227s average)
- Good balance of speed and optimality
- Reliable (71.4% success)
- Only 57% slower than Manhattan but same path quality as BFS/UCS

### What to Avoid
- **Never use tree-based BFS or UCS** - 0% success rate due to infinite loops
- **Avoid A*-Tree-Euclidean** - 57.1% success rate, extremely slow (0.0097s), high memory (3,540 units)
- **Avoid 4-directional motion** - significantly worse on all metrics

### Special Cases
- **A*-Tree-Manhattan**: Only if you need optimal paths but can't use graph search (71.4% success, 0.000411s)
- **BFS-Graph**: Simple implementation, guaranteed shortest path in unweighted graphs
- **UCS-Graph**: Good for weighted graphs when heuristic unavailable

---

## Generated Visualizations

### Current Visualizations (12 graphs from previous run)

1. **01_algorithm_comparison.png** - Overall performance metrics comparison
2. **02_environment_impact.png** - How environment affects each algorithm
3. **03_motion_model_comparison.png** - 4-dir vs 8-dir detailed comparison
4. **04_heuristic_comparison.png** - Euclidean vs Manhattan heuristics
5. **05_tree_vs_graph.png** - Tree search vs graph search comparison
6. **06_execution_time_distribution.png** - Distribution of execution times (violin plot)
7. **07_time_vs_nodes.png** - Scatter plot showing time vs nodes expanded
8. **08_cost_vs_length.png** - Path cost vs path length relationship
9. **09_memory_efficiency.png** - Memory usage comparison
10. **10_success_rate.png** - Success rates by algorithm
11. **11_overall_efficiency.png** - Efficiency score (time × nodes / cost)
12. **12_performance_consistency.png** - Coefficient of variation for consistency

### 🆕 New Visualization (in updated suite)
13. **13_complexity_analysis.png** - Performance vs map complexity (10×10, 15×15, 20×20)
    - Execution time vs size
    - Nodes expanded vs size
    - Memory usage vs size
    - Success rate vs size

All visualizations are saved in [benchmark_results/](benchmark_results/)

---

## Files Generated

- `benchmark_results_20260107_225948.csv` - Raw data (815 KB)
- `benchmark_report.txt` - Detailed text report
- `01_algorithm_comparison.png` through `12_performance_consistency.png` - Visualizations

---

## Methodology

### Previous Test Configuration (Results Shown Above)
- **100 trials** per configuration for graph algorithms
- **20 trials** per configuration for tree algorithms
- **7 environment types** tested (empty 10x10, empty 15x15, simple obstacles 10x10, simple obstacles 15x15, corridor 12x12, rooms 15x15, dense 10x10)
- **2 motion models** tested (4-directional, 8-directional)
- **8 algorithms** benchmarked (excluding DFS variants)
- **Multiple sizes** (10×10, 12×12, 15×15)
- **Timeout:** 60 seconds for graph algorithms, 30 seconds for tree algorithms
- **Max depth:** 50,000 for graph, 5,000 for tree
- **Max iterations:** 1,000,000 for graph, 100,000 for tree

Total test configurations: 112
Total algorithm executions: 6,720
Data collected: 815 KB

### 🆕 Updated Test Configuration (Pending Execution)
- **Trials**: 100 for graph algorithms, 10-50 for tree algorithms (size-dependent)
- **Map sizes**: 5×5, 7×7, 10×10, 15×15, 20×20 (progressive complexity)
- **Environment types**:
  - Small maps (5×5, 7×7): empty, simple_obstacles
  - Medium+ maps (10×10, 15×15, 20×20): empty, simple_obstacles, corridor, rooms, dense
- **Adaptive limits for tree algorithms**:
  - ≤7×7 maps: 500,000 iterations, 60s timeout, 50 trials
  - ≤10×10 maps: 300,000 iterations, 45s timeout, 20 trials
  - >10×10 maps: 100,000 iterations, 30s timeout, 10 trials
- **New visualization**: Complexity analysis (13_complexity_analysis.png)

Expected total configurations: ~320
Expected executions: ~12,000+

See [BENCHMARK_CHANGES.md](BENCHMARK_CHANGES.md) for complete details.

---

## Algorithm Comparison Summary

### Graph Algorithms (Recommended)
All graph algorithms maintain a visited set to prevent revisiting nodes:

- **A*-Graph-Manhattan**: ⭐ Best overall - fastest, most efficient
- **A*-Graph-Euclidean**: ⭐ Best for optimal paths - balanced speed/quality
- **BFS-Graph**: Simple, guaranteed shortest path in unweighted graphs
- **UCS-Graph**: Good for weighted graphs, explores uniformly

### Tree Algorithms (Limited Use)
Tree algorithms do not track visited nodes, leading to potential re-exploration:

- **A*-Tree-Manhattan**: Acceptable for constrained environments
- **A*-Tree-Euclidean**: Often slow and unreliable (57% success)
- **BFS-Tree**: ❌ Never use - 0% success rate
- **UCS-Tree**: ❌ Never use - 0% success rate

---

## Performance Highlights

### Speed Champion: A*-Graph-Manhattan
- **0.000145s** average execution time
- 36% faster than A*-Graph-Euclidean
- 67% faster than BFS-Graph
- 4,166% faster than A*-Tree-Euclidean

### Efficiency Champion: A*-Graph-Manhattan
- **37.46 nodes** expanded on average
- 34% fewer nodes than A*-Graph-Euclidean
- 63% fewer nodes than BFS/UCS
- 97% fewer nodes than A*-Tree-Euclidean

### Optimality Champion: A*-Tree-Euclidean
- **14.64** average path cost
- 11% better than graph algorithms (16.51)
- But 6,600% slower and 4,000% more memory
- **Trade-off not worth it** - use A*-Graph-Euclidean instead

---

## Conclusion

**A*-Graph-Manhattan with 8-directional motion** is the clear winner for robot maze pathfinding, offering the best combination of speed, efficiency, and reliability.

For applications requiring better path optimality, use **A*-Graph-Euclidean with 8-directional motion**, which provides the same path quality as BFS/UCS but is significantly faster.

Tree-based BFS and UCS should never be used in maze pathfinding due to 0% success rates. Tree-based A* algorithms should only be used in special cases where graph search is not feasible, and even then, Manhattan heuristic is strongly preferred over Euclidean.

The 8-directional motion model is superior in every way to 4-directional, providing 62% faster execution, 76% shorter paths, and 69% fewer nodes expanded.

---

## 🚀 Running the Updated Benchmark

To run the updated benchmark suite with new map sizes and adaptive tree algorithm limits:

```bash
python benchmark_suite.py
```

This will:
- Test on 5×5, 7×7, 10×10, 15×15, and 20×20 maps
- Use adaptive iteration limits for tree algorithms
- Generate 13 visualizations (including new complexity analysis)
- Create comprehensive reports with complexity breakdowns
- Verify if BFS-Tree and UCS-Tree can succeed on smaller maps

**Expected runtime**: 1-3 hours depending on your system

**Expected improvements**:
- BFS-Tree and UCS-Tree should achieve >0% success rate on 5×5 and 7×7 maps
- Better understanding of algorithm scaling across complexity levels
- More granular data for research and analysis

See [BENCHMARK_CHANGES.md](BENCHMARK_CHANGES.md) for detailed changes and rationale.
