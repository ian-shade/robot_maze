"""
Comprehensive Benchmark Suite for Robot Maze Pathfinding Algorithms

This script runs extensive benchmarks across all algorithms with various:
- Environment configurations (size, complexity)
- Robot motion models (4-directional, 8-directional)
- Algorithm parameters (max_depth, heuristics)
- Multiple trials for statistical significance
"""

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from environment import Environment
from robot import Robot
from problem import PathfindingProblem
from search_algorithms import SearchAlgorithms
import warnings
warnings.filterwarnings('ignore')

# Set professional plotting style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class BenchmarkSuite:
    def __init__(self, num_trials=100, output_dir='benchmark_results'):
        self.num_trials = num_trials
        self.output_dir = output_dir
        self.results = []

    def create_environment_config(self, env_type, size):
        """Create different environment configurations"""
        env = Environment(width=size, height=size, has_border=True)

        if env_type == 'empty':
            # Just borders
            start = (1, 1)
            goal = (size-2, size-2)

        elif env_type == 'simple_obstacles':
            # Few scattered obstacles
            obstacles = int(size * size * 0.1)  # 10% obstacles
            np.random.seed(42)
            for _ in range(obstacles):
                x, y = np.random.randint(1, size-1), np.random.randint(1, size-1)
                if (x, y) != (1, 1) and (x, y) != (size-2, size-2):
                    env.add_obstacle(x, y)
            start = (1, 1)
            goal = (size-2, size-2)

        elif env_type == 'corridor':
            # Create a corridor maze
            for y in range(2, size-2, 2):
                for x in range(2, size-3):
                    env.add_obstacle(x, y)
            start = (1, 1)
            goal = (size-2, size-2)

        elif env_type == 'rooms':
            # Create room-like structure
            mid = size // 2
            # Vertical walls
            for y in range(1, size-1):
                if y != mid:
                    env.add_obstacle(mid, y)
            # Horizontal walls
            for x in range(1, size-1):
                if x != mid:
                    env.add_obstacle(x, mid)
            start = (1, 1)
            goal = (size-2, size-2)

        elif env_type == 'dense':
            # Dense obstacles
            obstacles = int(size * size * 0.3)  # 30% obstacles
            np.random.seed(123)
            for _ in range(obstacles):
                x, y = np.random.randint(1, size-1), np.random.randint(1, size-1)
                if (x, y) != (1, 1) and (x, y) != (size-2, size-2):
                    env.add_obstacle(x, y)
            start = (1, 1)
            goal = (size-2, size-2)

        env.set_initial_state(*start)
        env.set_goal_state(*goal)
        return env

    def run_algorithm_safe(self, algo_func, algo_name, timeout=30):
        """Run algorithm with error handling"""
        try:
            result = algo_func()
            return result
        except (TimeoutError, RuntimeError) as e:
            return {
                'success': False,
                'time': timeout,
                'nodes_expanded': 0,
                'path_length': 0,
                'cost': float('inf'),
                'movement_time': 0,
                'max_frontier_size': 0,
                'max_memory_usage': 0,
                'error': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'time': 0,
                'nodes_expanded': 0,
                'path_length': 0,
                'cost': float('inf'),
                'movement_time': 0,
                'max_frontier_size': 0,
                'max_memory_usage': 0,
                'error': f"Unexpected error: {str(e)}"
            }

    def run_single_benchmark(self, env_config, motion_type, algorithm_name,
                            max_depth=10000, max_iterations=500000, timeout=30):
        """Run a single algorithm benchmark"""
        env_type, size = env_config
        env = self.create_environment_config(env_type, size)

        # Setup robot
        robot = Robot()
        if motion_type == '4-directional':
            robot.set_4_directional_model()
        elif motion_type == '8-directional':
            robot.set_8_directional_model()

        problem = PathfindingProblem(env, robot)
        search = SearchAlgorithms(problem, max_depth=max_depth,
                                 max_iterations=max_iterations,
                                 timeout_seconds=timeout)

        # Run algorithm
        if algorithm_name == 'BFS-Tree':
            result = self.run_algorithm_safe(search.bfs_tree, algorithm_name, timeout)
        elif algorithm_name == 'BFS-Graph':
            result = self.run_algorithm_safe(search.bfs_graph, algorithm_name, timeout)
        elif algorithm_name == 'DFS-Tree':
            result = self.run_algorithm_safe(search.dfs_tree, algorithm_name, timeout)
        elif algorithm_name == 'DFS-Graph':
            result = self.run_algorithm_safe(search.dfs_graph, algorithm_name, timeout)
        elif algorithm_name == 'UCS-Tree':
            result = self.run_algorithm_safe(search.ucs_tree, algorithm_name, timeout)
        elif algorithm_name == 'UCS-Graph':
            result = self.run_algorithm_safe(search.ucs_graph, algorithm_name, timeout)
        elif algorithm_name == 'A*-Tree-Euclidean':
            result = self.run_algorithm_safe(lambda: search.astar_tree('euclidean'), algorithm_name, timeout)
        elif algorithm_name == 'A*-Tree-Manhattan':
            result = self.run_algorithm_safe(lambda: search.astar_tree('manhattan'), algorithm_name, timeout)
        elif algorithm_name == 'A*-Graph-Euclidean':
            result = self.run_algorithm_safe(lambda: search.astar_graph('euclidean'), algorithm_name, timeout)
        elif algorithm_name == 'A*-Graph-Manhattan':
            result = self.run_algorithm_safe(lambda: search.astar_graph('manhattan'), algorithm_name, timeout)
        else:
            return None

        # Package results
        return {
            'algorithm': algorithm_name,
            'env_type': env_type,
            'env_size': size,
            'motion_type': motion_type,
            'success': result.get('success', False),
            'time': result.get('time', 0),
            'nodes_expanded': result.get('nodes_expanded', 0),
            'path_length': result.get('path_length', 0),
            'path_cost': result.get('cost', float('inf')),
            'movement_time': result.get('movement_time', 0),
            'max_frontier_size': result.get('max_frontier_size', 0),
            'max_memory_usage': result.get('max_memory_usage', 0),
            'max_depth': max_depth,
            'max_iterations': max_iterations,
            'error': result.get('error', None)
        }

    def run_full_benchmark(self):
        """Run comprehensive benchmarks"""
        print("="*80)
        print("ROBOT MAZE PATHFINDING BENCHMARK SUITE")
        print("="*80)
        print(f"Number of trials per configuration: {self.num_trials}")
        print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)

        # Define test configurations with progressive complexity
        # Format: (env_type, size, complexity_level)
        env_configs = [
            # Small maps (good for tree algorithms)
            ('empty', 5),
            ('simple_obstacles', 5),
            ('empty', 7),
            ('simple_obstacles', 7),

            # Medium maps (10x10)
            ('empty', 10),
            ('simple_obstacles', 10),
            ('corridor', 10),
            ('rooms', 10),
            ('dense', 10),

            # Large maps (15x15)
            ('empty', 15),
            ('simple_obstacles', 15),
            ('corridor', 15),
            ('rooms', 15),
            ('dense', 15),

            # Extra large maps (20x20)
            ('empty', 20),
            ('simple_obstacles', 20),
            ('corridor', 20),
            ('rooms', 20),
            ('dense', 20),
        ]

        motion_types = ['4-directional', '8-directional']

        # Graph algorithms (more reliable)
        graph_algorithms = [
            'BFS-Graph',
            # 'DFS-Graph',
            'UCS-Graph',
            'A*-Graph-Euclidean',
            'A*-Graph-Manhattan'
        ]

        # Tree algorithms (limited iterations to prevent infinite loops)
        tree_algorithms = [
            'BFS-Tree',
            # 'DFS-Tree',
            'UCS-Tree',
            'A*-Tree-Euclidean',
            'A*-Tree-Manhattan'
        ]

        total_configs = len(env_configs) * len(motion_types) * (len(graph_algorithms) + len(tree_algorithms))
        current = 0

        for env_config in env_configs:
            for motion_type in motion_types:
                # Run graph algorithms with multiple trials
                for algo in graph_algorithms:
                    current += 1
                    print(f"\n[{current}/{total_configs}] Running {algo} on {env_config[0]} {env_config[1]}x{env_config[1]} with {motion_type}")

                    for trial in range(self.num_trials):
                        result = self.run_single_benchmark(
                            env_config, motion_type, algo,
                            max_depth=50000, max_iterations=1000000, timeout=60
                        )
                        if result:
                            result['trial'] = trial
                            self.results.append(result)

                        if (trial + 1) % 20 == 0:
                            print(f"  Progress: {trial + 1}/{self.num_trials} trials completed")

                # Run tree algorithms with adaptive limits based on size
                for algo in tree_algorithms:
                    current += 1
                    env_type, size = env_config
                    print(f"\n[{current}/{total_configs}] Running {algo} on {env_type} {size}x{size} with {motion_type}")

                    # Adaptive limits based on map size
                    if size <= 7:
                        max_depth = 10000
                        max_iterations = 500000
                        timeout = 60
                        num_tree_trials = min(50, self.num_trials)
                        print(f"  (Small map: increased limits for tree algorithms)")
                    elif size <= 10:
                        max_depth = 8000
                        max_iterations = 300000
                        timeout = 45
                        num_tree_trials = min(20, self.num_trials)
                        print(f"  (Medium map: moderate limits for tree algorithms)")
                    else:
                        max_depth = 5000
                        max_iterations = 100000
                        timeout = 30
                        num_tree_trials = min(10, self.num_trials)
                        print(f"  (Large map: conservative limits for tree algorithms)")

                    for trial in range(num_tree_trials):
                        result = self.run_single_benchmark(
                            env_config, motion_type, algo,
                            max_depth=max_depth, max_iterations=max_iterations, timeout=timeout
                        )
                        if result:
                            result['trial'] = trial
                            self.results.append(result)

                        if (trial + 1) % max(5, num_tree_trials // 4) == 0:
                            print(f"  Progress: {trial + 1}/{num_tree_trials} trials completed")

        print("\n" + "="*80)
        print(f"Benchmark completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total results collected: {len(self.results)}")
        print("="*80)

        return pd.DataFrame(self.results)

    def save_results(self, df, filename=None):
        """Save results to CSV"""
        if filename is None:
            filename = f"{self.output_dir}/benchmark_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        print(f"\nResults saved to: {filename}")
        return filename


class BenchmarkVisualizer:
    """Create professional visualizations for benchmark results"""

    def __init__(self, df, output_dir='benchmark_results'):
        self.df = df
        self.output_dir = output_dir
        # Filter only successful runs for most visualizations
        self.df_success = df[df['success'] == True].copy()

    def plot_algorithm_comparison(self):
        """Compare algorithms across different metrics"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Algorithm Performance Comparison', fontsize=16, fontweight='bold')

        metrics = [
            ('time', 'Execution Time (seconds)', axes[0, 0]),
            ('nodes_expanded', 'Nodes Expanded', axes[0, 1]),
            ('path_cost', 'Path Cost', axes[1, 0]),
            ('max_memory_usage', 'Max Memory Usage', axes[1, 1])
        ]

        for metric, title, ax in metrics:
            data = self.df_success.groupby('algorithm')[metric].agg(['mean', 'std']).reset_index()
            data = data.sort_values('mean', ascending=False)

            x = range(len(data))
            ax.barh(x, data['mean'], xerr=data['std'], capsize=5, alpha=0.7, edgecolor='black')
            ax.set_yticks(x)
            ax.set_yticklabels(data['algorithm'], fontsize=9)
            ax.set_xlabel(title, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)

            # Add value labels
            for i, (mean, std) in enumerate(zip(data['mean'], data['std'])):
                ax.text(mean, i, f' {mean:.3f}', va='center', fontsize=8)

        plt.tight_layout()
        filename = f'{self.output_dir}/01_algorithm_comparison.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Saved: {filename}")
        plt.close()

    def plot_environment_impact(self):
        """Show how environment affects performance"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Environment Impact on Algorithm Performance', fontsize=16, fontweight='bold')

        # Focus on graph algorithms (more reliable)
        graph_algos = [a for a in self.df_success['algorithm'].unique() if 'Graph' in a]
        df_graph = self.df_success[self.df_success['algorithm'].isin(graph_algos)]

        # Time by environment
        ax = axes[0, 0]
        pivot = df_graph.pivot_table(values='time', index='env_type', columns='algorithm', aggfunc='mean')
        pivot.plot(kind='bar', ax=ax, width=0.8)
        ax.set_title('Execution Time by Environment', fontweight='bold')
        ax.set_ylabel('Time (seconds)')
        ax.set_xlabel('Environment Type')
        ax.legend(title='Algorithm', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        ax.grid(axis='y', alpha=0.3)

        # Nodes expanded by environment
        ax = axes[0, 1]
        pivot = df_graph.pivot_table(values='nodes_expanded', index='env_type', columns='algorithm', aggfunc='mean')
        pivot.plot(kind='bar', ax=ax, width=0.8)
        ax.set_title('Nodes Expanded by Environment', fontweight='bold')
        ax.set_ylabel('Nodes Expanded')
        ax.set_xlabel('Environment Type')
        ax.legend(title='Algorithm', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        ax.grid(axis='y', alpha=0.3)

        # Size impact
        ax = axes[1, 0]
        size_data = df_graph.groupby(['env_size', 'algorithm'])['time'].mean().reset_index()
        for algo in graph_algos:
            data = size_data[size_data['algorithm'] == algo]
            ax.plot(data['env_size'], data['time'], marker='o', label=algo, linewidth=2)
        ax.set_title('Execution Time vs Environment Size', fontweight='bold')
        ax.set_xlabel('Environment Size')
        ax.set_ylabel('Time (seconds)')
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)

        # Success rate by environment
        ax = axes[1, 1]
        success_rate = self.df.groupby(['env_type', 'algorithm'])['success'].mean().reset_index()
        pivot = success_rate.pivot(index='env_type', columns='algorithm', values='success')
        pivot.plot(kind='bar', ax=ax, width=0.8)
        ax.set_title('Success Rate by Environment', fontweight='bold')
        ax.set_ylabel('Success Rate')
        ax.set_xlabel('Environment Type')
        ax.set_ylim([0, 1.1])
        ax.legend(title='Algorithm', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        filename = f'{self.output_dir}/02_environment_impact.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Saved: {filename}")
        plt.close()

    def plot_motion_model_comparison(self):
        """Compare 4-directional vs 8-directional motion"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Motion Model Comparison (4-dir vs 8-dir)', fontsize=16, fontweight='bold')

        # Path cost comparison
        ax = axes[0, 0]
        motion_data = self.df_success.groupby(['algorithm', 'motion_type'])['path_cost'].mean().reset_index()
        pivot = motion_data.pivot(index='algorithm', columns='motion_type', values='path_cost')
        pivot.plot(kind='barh', ax=ax)
        ax.set_title('Average Path Cost by Motion Model', fontweight='bold')
        ax.set_xlabel('Path Cost')
        ax.legend(title='Motion Model')
        ax.grid(axis='x', alpha=0.3)

        # Execution time comparison
        ax = axes[0, 1]
        motion_data = self.df_success.groupby(['algorithm', 'motion_type'])['time'].mean().reset_index()
        pivot = motion_data.pivot(index='algorithm', columns='motion_type', values='time')
        pivot.plot(kind='barh', ax=ax)
        ax.set_title('Average Execution Time by Motion Model', fontweight='bold')
        ax.set_xlabel('Time (seconds)')
        ax.legend(title='Motion Model')
        ax.grid(axis='x', alpha=0.3)

        # Nodes expanded
        ax = axes[1, 0]
        motion_data = self.df_success.groupby(['algorithm', 'motion_type'])['nodes_expanded'].mean().reset_index()
        pivot = motion_data.pivot(index='algorithm', columns='motion_type', values='nodes_expanded')
        pivot.plot(kind='barh', ax=ax)
        ax.set_title('Average Nodes Expanded by Motion Model', fontweight='bold')
        ax.set_xlabel('Nodes Expanded')
        ax.legend(title='Motion Model')
        ax.grid(axis='x', alpha=0.3)

        # Path length
        ax = axes[1, 1]
        motion_data = self.df_success.groupby(['algorithm', 'motion_type'])['path_length'].mean().reset_index()
        pivot = motion_data.pivot(index='algorithm', columns='motion_type', values='path_length')
        pivot.plot(kind='barh', ax=ax)
        ax.set_title('Average Path Length by Motion Model', fontweight='bold')
        ax.set_xlabel('Path Length (steps)')
        ax.legend(title='Motion Model')
        ax.grid(axis='x', alpha=0.3)

        plt.tight_layout()
        filename = f'{self.output_dir}/03_motion_model_comparison.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Saved: {filename}")
        plt.close()

    def plot_heuristic_comparison(self):
        """Compare A* heuristics"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('A* Heuristic Comparison (Euclidean vs Manhattan)', fontsize=16, fontweight='bold')

        # Filter A* algorithms
        astar_algos = [a for a in self.df_success['algorithm'].unique() if 'A*' in a]
        df_astar = self.df_success[self.df_success['algorithm'].isin(astar_algos)]

        metrics = [
            ('time', 'Execution Time (seconds)', axes[0, 0]),
            ('nodes_expanded', 'Nodes Expanded', axes[0, 1]),
            ('path_cost', 'Path Cost', axes[1, 0]),
            ('max_frontier_size', 'Max Frontier Size', axes[1, 1])
        ]

        for metric, title, ax in metrics:
            data = df_astar.groupby('algorithm')[metric].agg(['mean', 'std']).reset_index()
            data = data.sort_values('mean', ascending=False)

            colors = ['#FF6B6B' if 'Manhattan' in a else '#4ECDC4' for a in data['algorithm']]
            x = range(len(data))
            ax.barh(x, data['mean'], xerr=data['std'], capsize=5, alpha=0.7,
                   edgecolor='black', color=colors)
            ax.set_yticks(x)
            ax.set_yticklabels(data['algorithm'], fontsize=9)
            ax.set_xlabel(title, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)

            for i, mean in enumerate(data['mean']):
                ax.text(mean, i, f' {mean:.3f}', va='center', fontsize=8)

        plt.tight_layout()
        filename = f'{self.output_dir}/04_heuristic_comparison.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Saved: {filename}")
        plt.close()

    def plot_tree_vs_graph(self):
        """Compare tree vs graph versions"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Tree Search vs Graph Search Comparison', fontsize=16, fontweight='bold')

        # Extract base algorithm names
        self.df_success['base_algo'] = self.df_success['algorithm'].apply(
            lambda x: x.split('-')[0] if '-' in x else x
        )
        self.df_success['search_type'] = self.df_success['algorithm'].apply(
            lambda x: 'Tree' if 'Tree' in x else 'Graph'
        )

        metrics = [
            ('time', 'Execution Time (seconds)', axes[0, 0]),
            ('nodes_expanded', 'Nodes Expanded', axes[0, 1]),
            ('max_memory_usage', 'Max Memory Usage', axes[1, 0]),
            ('path_cost', 'Path Cost', axes[1, 1])
        ]

        for metric, title, ax in metrics:
            data = self.df_success.groupby(['base_algo', 'search_type'])[metric].mean().reset_index()
            pivot = data.pivot(index='base_algo', columns='search_type', values=metric)
            pivot.plot(kind='bar', ax=ax, width=0.7, color=['#FF6B6B', '#4ECDC4'])
            ax.set_title(title, fontweight='bold')
            ax.set_ylabel(title)
            ax.set_xlabel('Algorithm')
            ax.legend(title='Search Type')
            ax.grid(axis='y', alpha=0.3)
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        plt.tight_layout()
        filename = f'{self.output_dir}/05_tree_vs_graph.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Saved: {filename}")
        plt.close()

    def plot_complexity_analysis(self):
        """Analyze performance across different map sizes (complexity levels)"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Performance vs Map Complexity (10x10, 15x15, 20x20)', fontsize=16, fontweight='bold')

        graph_algos = [a for a in self.df_success['algorithm'].unique() if 'Graph' in a]
        df_graph = self.df_success[self.df_success['algorithm'].isin(graph_algos)]

        # Filter for key sizes: 10, 15, 20
        key_sizes = [10, 15, 20]
        df_complexity = df_graph[df_graph['env_size'].isin(key_sizes)]

        # Time vs Size
        ax = axes[0, 0]
        for algo in graph_algos:
            data = df_complexity[df_complexity['algorithm'] == algo].groupby('env_size')['time'].mean()
            ax.plot(data.index, data.values, marker='o', label=algo, linewidth=2, markersize=8)
        ax.set_xlabel('Map Size (NxN)', fontweight='bold')
        ax.set_ylabel('Execution Time (seconds)', fontweight='bold')
        ax.set_title('Execution Time vs Map Complexity', fontweight='bold')
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)
        ax.set_xticks(key_sizes)

        # Nodes Expanded vs Size
        ax = axes[0, 1]
        for algo in graph_algos:
            data = df_complexity[df_complexity['algorithm'] == algo].groupby('env_size')['nodes_expanded'].mean()
            ax.plot(data.index, data.values, marker='s', label=algo, linewidth=2, markersize=8)
        ax.set_xlabel('Map Size (NxN)', fontweight='bold')
        ax.set_ylabel('Nodes Expanded', fontweight='bold')
        ax.set_title('Nodes Expanded vs Map Complexity', fontweight='bold')
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)
        ax.set_xticks(key_sizes)

        # Memory Usage vs Size
        ax = axes[1, 0]
        for algo in graph_algos:
            data = df_complexity[df_complexity['algorithm'] == algo].groupby('env_size')['max_memory_usage'].mean()
            ax.plot(data.index, data.values, marker='^', label=algo, linewidth=2, markersize=8)
        ax.set_xlabel('Map Size (NxN)', fontweight='bold')
        ax.set_ylabel('Max Memory Usage', fontweight='bold')
        ax.set_title('Memory Usage vs Map Complexity', fontweight='bold')
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)
        ax.set_xticks(key_sizes)

        # Success Rate vs Size
        ax = axes[1, 1]
        success_by_size = self.df.groupby(['env_size', 'algorithm'])['success'].mean().reset_index()
        success_by_size = success_by_size[success_by_size['env_size'].isin(key_sizes)]
        for algo in graph_algos:
            data = success_by_size[success_by_size['algorithm'] == algo]
            ax.plot(data['env_size'], data['success'], marker='D', label=algo, linewidth=2, markersize=8)
        ax.set_xlabel('Map Size (NxN)', fontweight='bold')
        ax.set_ylabel('Success Rate', fontweight='bold')
        ax.set_title('Success Rate vs Map Complexity', fontweight='bold')
        ax.set_ylim([0, 1.1])
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)
        ax.set_xticks(key_sizes)

        plt.tight_layout()
        filename = f'{self.output_dir}/13_complexity_analysis.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Saved: {filename}")
        plt.close()

    def plot_statistical_summary(self):
        """Create comprehensive statistical summary as separate files"""
        graph_algos = [a for a in self.df_success['algorithm'].unique() if 'Graph' in a]

        # 1. Distribution of execution times (violin plot)
        fig, ax = plt.subplots(figsize=(14, 6))
        df_plot = self.df_success[self.df_success['algorithm'].isin(graph_algos)]
        sns.violinplot(data=df_plot, x='algorithm', y='time', ax=ax)
        ax.set_title('Distribution of Execution Times (Graph Algorithms)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Time (seconds)')
        ax.set_xlabel('Algorithm')
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        filename = f'{self.output_dir}/06_execution_time_distribution.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Saved: {filename}")
        plt.close()

        # 2. Time vs Nodes Expanded scatter
        fig, ax = plt.subplots(figsize=(10, 6))
        for algo in graph_algos[:5]:  # Top 5 to avoid clutter
            data = self.df_success[self.df_success['algorithm'] == algo]
            ax.scatter(data['nodes_expanded'], data['time'], alpha=0.6, label=algo, s=20)
        ax.set_xlabel('Nodes Expanded')
        ax.set_ylabel('Time (seconds)')
        ax.set_title('Time vs Nodes Expanded', fontsize=14, fontweight='bold')
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)
        plt.tight_layout()
        filename = f'{self.output_dir}/07_time_vs_nodes.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Saved: {filename}")
        plt.close()

        # 3. Path cost vs Path length
        fig, ax = plt.subplots(figsize=(10, 6))
        for algo in graph_algos[:5]:
            data = self.df_success[self.df_success['algorithm'] == algo]
            ax.scatter(data['path_length'], data['path_cost'], alpha=0.6, label=algo, s=20)
        ax.set_xlabel('Path Length')
        ax.set_ylabel('Path Cost')
        ax.set_title('Path Cost vs Path Length', fontsize=14, fontweight='bold')
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)
        plt.tight_layout()
        filename = f'{self.output_dir}/08_cost_vs_length.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Saved: {filename}")
        plt.close()

        # 4. Memory efficiency
        fig, ax = plt.subplots(figsize=(10, 6))
        mem_data = self.df_success.groupby('algorithm')['max_memory_usage'].mean().sort_values()
        ax.barh(range(len(mem_data)), mem_data.values, color='coral', alpha=0.7, edgecolor='black')
        ax.set_yticks(range(len(mem_data)))
        ax.set_yticklabels(mem_data.index, fontsize=9)
        ax.set_xlabel('Average Memory Usage')
        ax.set_title('Memory Efficiency', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        filename = f'{self.output_dir}/09_memory_efficiency.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Saved: {filename}")
        plt.close()

        # 5. Overall success rate
        fig, ax = plt.subplots(figsize=(10, 6))
        success_rate = self.df.groupby('algorithm')['success'].mean().sort_values(ascending=False)
        colors = ['green' if x >= 0.9 else 'orange' if x >= 0.7 else 'red' for x in success_rate.values]
        ax.bar(range(len(success_rate)), success_rate.values, color=colors, alpha=0.7, edgecolor='black')
        ax.set_xticks(range(len(success_rate)))
        ax.set_xticklabels(success_rate.index, rotation=45, ha='right', fontsize=9)
        ax.set_ylabel('Success Rate')
        ax.set_title('Algorithm Success Rate', fontsize=14, fontweight='bold')
        ax.set_ylim([0, 1.1])
        ax.axhline(y=0.9, color='green', linestyle='--', alpha=0.5, label='90%')
        ax.grid(axis='y', alpha=0.3)
        ax.legend()
        plt.tight_layout()
        filename = f'{self.output_dir}/10_success_rate.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Saved: {filename}")
        plt.close()

        # 6. Efficiency score (time * nodes / path_cost)
        fig, ax = plt.subplots(figsize=(10, 6))
        self.df_success['efficiency'] = (self.df_success['time'] * self.df_success['nodes_expanded']) / (self.df_success['path_cost'] + 0.001)
        eff_data = self.df_success.groupby('algorithm')['efficiency'].mean().sort_values()
        ax.barh(range(len(eff_data)), eff_data.values, color='skyblue', alpha=0.7, edgecolor='black')
        ax.set_yticks(range(len(eff_data)))
        ax.set_yticklabels(eff_data.index, fontsize=9)
        ax.set_xlabel('Efficiency Score (lower is better)')
        ax.set_title('Overall Efficiency', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        filename = f'{self.output_dir}/11_overall_efficiency.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Saved: {filename}")
        plt.close()

        # 7. Performance consistency (coefficient of variation)
        fig, ax = plt.subplots(figsize=(10, 6))
        cv_data = self.df_success.groupby('algorithm')['time'].apply(lambda x: x.std() / x.mean()).sort_values()
        ax.barh(range(len(cv_data)), cv_data.values, color='lightgreen', alpha=0.7, edgecolor='black')
        ax.set_yticks(range(len(cv_data)))
        ax.set_yticklabels(cv_data.index, fontsize=9)
        ax.set_xlabel('Coefficient of Variation (lower is more consistent)')
        ax.set_title('Performance Consistency', fontsize=14, fontweight='bold')
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        filename = f'{self.output_dir}/12_performance_consistency.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Saved: {filename}")
        plt.close()

    def generate_report(self):
        """Generate text report with statistics"""
        report_filename = f'{self.output_dir}/benchmark_report.txt'

        with open(report_filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write("ROBOT MAZE PATHFINDING BENCHMARK REPORT\n")
            f.write("="*80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total runs: {len(self.df)}\n")
            f.write(f"Successful runs: {len(self.df_success)}\n")
            f.write(f"Success rate: {len(self.df_success)/len(self.df)*100:.2f}%\n")
            f.write("="*80 + "\n\n")

            f.write("ALGORITHM RANKING BY EXECUTION TIME\n")
            f.write("-"*80 + "\n")
            time_rank = self.df_success.groupby('algorithm')['time'].agg(['mean', 'std', 'min', 'max']).sort_values('mean')
            f.write(time_rank.to_string())
            f.write("\n\n")

            f.write("ALGORITHM RANKING BY NODES EXPANDED\n")
            f.write("-"*80 + "\n")
            nodes_rank = self.df_success.groupby('algorithm')['nodes_expanded'].agg(['mean', 'std', 'min', 'max']).sort_values('mean')
            f.write(nodes_rank.to_string())
            f.write("\n\n")

            f.write("ALGORITHM RANKING BY PATH COST (OPTIMALITY)\n")
            f.write("-"*80 + "\n")
            cost_rank = self.df_success.groupby('algorithm')['path_cost'].agg(['mean', 'std', 'min', 'max']).sort_values('mean')
            f.write(cost_rank.to_string())
            f.write("\n\n")

            f.write("ALGORITHM RANKING BY MEMORY USAGE\n")
            f.write("-"*80 + "\n")
            mem_rank = self.df_success.groupby('algorithm')['max_memory_usage'].agg(['mean', 'std', 'min', 'max']).sort_values('mean')
            f.write(mem_rank.to_string())
            f.write("\n\n")

            f.write("SUCCESS RATE BY ALGORITHM\n")
            f.write("-"*80 + "\n")
            success_stats = self.df.groupby('algorithm')['success'].agg(['sum', 'count', 'mean']).sort_values('mean', ascending=False)
            success_stats.columns = ['Successes', 'Total Runs', 'Success Rate']
            f.write(success_stats.to_string())
            f.write("\n\n")

            f.write("PERFORMANCE BY ENVIRONMENT TYPE\n")
            f.write("-"*80 + "\n")
            env_stats = self.df_success.groupby('env_type')[['time', 'nodes_expanded', 'path_cost']].mean()
            f.write(env_stats.to_string())
            f.write("\n\n")

            f.write("MOTION MODEL COMPARISON\n")
            f.write("-"*80 + "\n")
            motion_stats = self.df_success.groupby('motion_type')[['time', 'path_cost', 'path_length', 'nodes_expanded']].mean()
            f.write(motion_stats.to_string())
            f.write("\n\n")

            f.write("COMPLEXITY ANALYSIS (Map Size Impact)\n")
            f.write("-"*80 + "\n")
            size_stats = self.df_success.groupby('env_size')[['time', 'nodes_expanded', 'path_cost', 'max_memory_usage']].mean()
            f.write(size_stats.to_string())
            f.write("\n\n")

            # Detailed breakdown by size
            f.write("ALGORITHM PERFORMANCE BY MAP SIZE\n")
            f.write("-"*80 + "\n")
            for size in sorted(self.df_success['env_size'].unique()):
                df_size = self.df_success[self.df_success['env_size'] == size]
                f.write(f"\n{size}x{size} Maps:\n")
                algo_stats = df_size.groupby('algorithm')['time'].agg(['mean', 'count']).sort_values('mean')
                f.write(algo_stats.to_string())
                f.write("\n")
            f.write("\n")

            f.write("="*80 + "\n")
            f.write("KEY FINDINGS\n")
            f.write("="*80 + "\n")

            # Best algorithm by metric
            best_time = time_rank.index[0]
            best_nodes = nodes_rank.index[0]
            best_cost = cost_rank.index[0]
            best_memory = mem_rank.index[0]

            f.write(f"Fastest algorithm: {best_time}\n")
            f.write(f"Most efficient (fewest nodes): {best_nodes}\n")
            f.write(f"Most optimal (lowest cost): {best_cost}\n")
            f.write(f"Most memory efficient: {best_memory}\n")

        print(f"\nReport saved to: {report_filename}")

    def generate_all_plots(self):
        """Generate all visualizations"""
        print("\n" + "="*80)
        print("GENERATING VISUALIZATIONS")
        print("="*80)

        import os
        os.makedirs(self.output_dir, exist_ok=True)

        self.plot_algorithm_comparison()
        self.plot_environment_impact()
        self.plot_motion_model_comparison()
        self.plot_heuristic_comparison()
        self.plot_tree_vs_graph()
        self.plot_complexity_analysis()  # New complexity analysis plot
        self.plot_statistical_summary()
        self.generate_report()

        print("\n" + "="*80)
        print(f"All visualizations saved to: {self.output_dir}/")
        print("="*80)


def main():
    """Main execution function"""
    import os
    os.makedirs('benchmark_results', exist_ok=True)

    # Run benchmark suite
    benchmark = BenchmarkSuite(num_trials=100, output_dir='benchmark_results')
    results_df = benchmark.run_full_benchmark()

    # Save results
    csv_file = benchmark.save_results(results_df)

    # Generate visualizations
    visualizer = BenchmarkVisualizer(results_df, output_dir='benchmark_results')
    visualizer.generate_all_plots()

    print("\n" + "="*80)
    print("BENCHMARK SUITE COMPLETED SUCCESSFULLY")
    print("="*80)
    print(f"Results CSV: {csv_file}")
    print(f"Visualizations: benchmark_results/")
    print("="*80)


if __name__ == '__main__':
    main()
