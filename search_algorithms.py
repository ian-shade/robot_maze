"""
SearchAlgorithms Class
Implements all search algorithms: BFS, DFS, UCS, A* (tree and graph versions)
"""

import time
from collections import deque
import heapq


class SearchAlgorithms:
    
    def __init__(self, problem, max_depth=100):
        self.problem = problem
        self.max_depth = max_depth
        self.results = {}  # Store results for comparison
    
    # ==================== BFS ALGORITHMS ====================
    
    def bfs_tree(self):
        start_time = time.time()
        
        frontier = deque([self.problem.get_initial_node()])
        nodes_expanded = 0
        max_frontier_size = 1
        
        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            node = frontier.popleft()
            nodes_expanded += 1
            
            # Goal test
            if self.problem.is_goal(node.state):
                elapsed_time = time.time() - start_time
                path = node.get_path()
                
                result = {
                    'node': node,
                    'path': path,
                    'cost': node.path_cost,
                    'time': elapsed_time,
                    'nodes_expanded': nodes_expanded,
                    'path_length': len(path),
                    'max_frontier_size': max_frontier_size,
                    'success': True
                }
                self.results['BFS-Tree'] = result
                return result
            
            # Depth limit check for tree search
            if node.depth < self.max_depth:
                # Expand node
                for successor in self.problem.get_successors(node):
                    frontier.append(successor)
        
        # No solution found
        elapsed_time = time.time() - start_time
        result = {
            'node': None,
            'path': [],
            'cost': float('inf'),
            'time': elapsed_time,
            'nodes_expanded': nodes_expanded,
            'path_length': 0,
            'max_frontier_size': max_frontier_size,
            'success': False
        }
        self.results['BFS-Tree'] = result
        return result
    
    def bfs_graph(self):
        start_time = time.time()

        frontier = deque([self.problem.get_initial_node()])
        explored = set()
        explored_order = []  # Track exploration order
        nodes_expanded = 0
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            node = frontier.popleft()

            # Goal test
            if self.problem.is_goal(node.state):
                elapsed_time = time.time() - start_time
                path = node.get_path()

                result = {
                    'node': node,
                    'path': path,
                    'cost': node.path_cost,
                    'time': elapsed_time,
                    'explored': explored,
                    'explored_order': explored_order,  # Add ordered list
                    'nodes_expanded': nodes_expanded,
                    'path_length': len(path),
                    'max_frontier_size': max_frontier_size,
                    'success': True
                }
                self.results['BFS-Graph'] = result
                return result

            # Mark as explored
            if node.state not in explored:
                explored.add(node.state)
                explored_order.append(node.state)  # Track order
                nodes_expanded += 1

                # Expand node
                for successor in self.problem.get_successors(node):
                    if successor.state not in explored:
                        frontier.append(successor)

        # No solution found
        elapsed_time = time.time() - start_time
        result = {
            'node': None,
            'path': [],
            'cost': float('inf'),
            'time': elapsed_time,
            'explored': explored,
            'explored_order': explored_order,  # Add ordered list
            'nodes_expanded': nodes_expanded,
            'path_length': 0,
            'max_frontier_size': max_frontier_size,
            'success': False
        }
        self.results['BFS-Graph'] = result
        return result
    
    # ==================== DFS ALGORITHMS ====================
    
    def dfs_tree(self):
        start_time = time.time()
        
        frontier = [self.problem.get_initial_node()]  # Use list as stack
        nodes_expanded = 0
        max_frontier_size = 1
        
        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            node = frontier.pop()  # LIFO - pop from end
            nodes_expanded += 1
            
            # Goal test
            if self.problem.is_goal(node.state):
                elapsed_time = time.time() - start_time
                path = node.get_path()
                
                result = {
                    'node': node,
                    'path': path,
                    'cost': node.path_cost,
                    'time': elapsed_time,
                    'nodes_expanded': nodes_expanded,
                    'path_length': len(path),
                    'max_frontier_size': max_frontier_size,
                    'success': True
                }
                self.results['DFS-Tree'] = result
                return result
            
            # Depth limit check for tree search
            if node.depth < self.max_depth:
                # Expand node (add in reverse to maintain left-to-right order)
                successors = self.problem.get_successors(node)
                for successor in reversed(successors):
                    frontier.append(successor)
        
        # No solution found
        elapsed_time = time.time() - start_time
        result = {
            'node': None,
            'path': [],
            'cost': float('inf'),
            'time': elapsed_time,
            'nodes_expanded': nodes_expanded,
            'path_length': 0,
            'max_frontier_size': max_frontier_size,
            'success': False
        }
        self.results['DFS-Tree'] = result
        return result
    
    def dfs_graph(self):
        start_time = time.time()

        frontier = [self.problem.get_initial_node()]
        explored = set()
        explored_order = []  # Track exploration order
        nodes_expanded = 0
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            node = frontier.pop()

            # Goal test
            if self.problem.is_goal(node.state):
                elapsed_time = time.time() - start_time
                path = node.get_path()

                result = {
                    'node': node,
                    'path': path,
                    'cost': node.path_cost,
                    'time': elapsed_time,
                    'explored': explored,
                    'explored_order': explored_order,  # Add ordered list
                    'nodes_expanded': nodes_expanded,
                    'path_length': len(path),
                    'max_frontier_size': max_frontier_size,
                    'success': True
                }
                self.results['DFS-Graph'] = result
                return result

            # Mark as explored
            if node.state not in explored:
                explored.add(node.state)
                explored_order.append(node.state)  # Track order
                nodes_expanded += 1

                # Expand node
                successors = self.problem.get_successors(node)
                for successor in reversed(successors):
                    if successor.state not in explored:
                        frontier.append(successor)

        # No solution found
        elapsed_time = time.time() - start_time
        result = {
            'node': None,
            'path': [],
            'cost': float('inf'),
            'time': elapsed_time,
            'explored': explored,
            'explored_order': explored_order,  # Add ordered list
            'nodes_expanded': nodes_expanded,
            'path_length': 0,
            'max_frontier_size': max_frontier_size,
            'success': False
        }
        self.results['DFS-Graph'] = result
        return result
    
    # ==================== UCS ALGORITHMS ====================
    
    def ucs_tree(self):
        start_time = time.time()
        
        initial_node = self.problem.get_initial_node()
        frontier = [(initial_node.path_cost, id(initial_node), initial_node)]
        heapq.heapify(frontier)
        nodes_expanded = 0
        max_frontier_size = 1
        
        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            _, _, node = heapq.heappop(frontier)
            nodes_expanded += 1
            
            # Goal test
            if self.problem.is_goal(node.state):
                elapsed_time = time.time() - start_time
                path = node.get_path()
                
                result = {
                    'node': node,
                    'path': path,
                    'cost': node.path_cost,
                    'time': elapsed_time,
                    'nodes_expanded': nodes_expanded,
                    'path_length': len(path),
                    'max_frontier_size': max_frontier_size,
                    'success': True
                }
                self.results['UCS-Tree'] = result
                return result
            
            # Depth limit check for tree search
            if node.depth < self.max_depth:
                # Expand node
                for successor in self.problem.get_successors(node):
                    heapq.heappush(frontier, (successor.path_cost, id(successor), successor))
        
        # No solution found
        elapsed_time = time.time() - start_time
        result = {
            'node': None,
            'path': [],
            'cost': float('inf'),
            'time': elapsed_time,
            'nodes_expanded': nodes_expanded,
            'path_length': 0,
            'max_frontier_size': max_frontier_size,
            'success': False
        }
        self.results['UCS-Tree'] = result
        return result
    
    def ucs_graph(self):
        start_time = time.time()

        initial_node = self.problem.get_initial_node()
        frontier = [(initial_node.path_cost, id(initial_node), initial_node)]
        heapq.heapify(frontier)
        explored = set()
        explored_order = []  # Track exploration order
        nodes_expanded = 0
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            _, _, node = heapq.heappop(frontier)

            # Goal test
            if self.problem.is_goal(node.state):
                elapsed_time = time.time() - start_time
                path = node.get_path()

                result = {
                    'node': node,
                    'path': path,
                    'cost': node.path_cost,
                    'time': elapsed_time,
                    'explored': explored,
                    'explored_order': explored_order,  # Add ordered list
                    'nodes_expanded': nodes_expanded,
                    'path_length': len(path),
                    'max_frontier_size': max_frontier_size,
                    'success': True
                }
                self.results['UCS-Graph'] = result
                return result

            # Mark as explored
            if node.state not in explored:
                explored.add(node.state)
                explored_order.append(node.state)  # Track order
                nodes_expanded += 1

                # Expand node
                for successor in self.problem.get_successors(node):
                    if successor.state not in explored:
                        heapq.heappush(frontier, (successor.path_cost, id(successor), successor))

        # No solution found
        elapsed_time = time.time() - start_time
        result = {
            'node': None,
            'path': [],
            'cost': float('inf'),
            'time': elapsed_time,
            'explored': explored,
            'explored_order': explored_order,  # Add ordered list
            'nodes_expanded': nodes_expanded,
            'path_length': 0,
            'max_frontier_size': max_frontier_size,
            'success': False
        }
        self.results['UCS-Graph'] = result
        return result
    
    # ==================== A* ALGORITHMS ====================
    
    def astar_tree(self, heuristic='euclidean'):
        start_time = time.time()
        
        # Select heuristic function
        if heuristic == 'manhattan':
            h_func = self.problem.heuristic_manhattan
        else:
            h_func = self.problem.heuristic_euclidean
        
        initial_node = self.problem.get_initial_node()
        f_initial = initial_node.path_cost + h_func(initial_node.state)
        frontier = [(f_initial, id(initial_node), initial_node)]
        heapq.heapify(frontier)
        nodes_expanded = 0
        max_frontier_size = 1
        
        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            _, _, node = heapq.heappop(frontier)
            nodes_expanded += 1
            
            # Goal test
            if self.problem.is_goal(node.state):
                elapsed_time = time.time() - start_time
                path = node.get_path()
                
                result = {
                    'node': node,
                    'path': path,
                    'cost': node.path_cost,
                    'time': elapsed_time,
                    'nodes_expanded': nodes_expanded,
                    'path_length': len(path),
                    'max_frontier_size': max_frontier_size,
                    'heuristic': heuristic,
                    'success': True
                }
                self.results['A*-Tree'] = result
                return result
            
            # Depth limit check for tree search
            if node.depth < self.max_depth:
                # Expand node
                for successor in self.problem.get_successors(node):
                    f_value = successor.path_cost + h_func(successor.state)
                    heapq.heappush(frontier, (f_value, id(successor), successor))
        
        # No solution found
        elapsed_time = time.time() - start_time
        result = {
            'node': None,
            'path': [],
            'cost': float('inf'),
            'time': elapsed_time,
            'nodes_expanded': nodes_expanded,
            'path_length': 0,
            'max_frontier_size': max_frontier_size,
            'heuristic': heuristic,
            'success': False
        }
        self.results['A*-Tree'] = result
        return result
    
    def astar_graph(self, heuristic='euclidean'):
        start_time = time.time()

        # Select heuristic function
        if heuristic == 'manhattan':
            h_func = self.problem.heuristic_manhattan
        else:
            h_func = self.problem.heuristic_euclidean

        initial_node = self.problem.get_initial_node()
        f_initial = initial_node.path_cost + h_func(initial_node.state)
        frontier = [(f_initial, id(initial_node), initial_node)]
        heapq.heapify(frontier)
        explored = set()
        explored_order = []  # Track exploration order
        nodes_expanded = 0
        max_frontier_size = 1

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            _, _, node = heapq.heappop(frontier)

            # Goal test
            if self.problem.is_goal(node.state):
                elapsed_time = time.time() - start_time
                path = node.get_path()

                result = {
                    'node': node,
                    'path': path,
                    'cost': node.path_cost,
                    'time': elapsed_time,
                    'explored': explored,
                    'explored_order': explored_order,  # Add ordered list
                    'nodes_expanded': nodes_expanded,
                    'path_length': len(path),
                    'max_frontier_size': max_frontier_size,
                    'heuristic': heuristic,
                    'success': True
                }
                self.results['A*-Graph'] = result
                return result

            # Mark as explored
            if node.state not in explored:
                explored.add(node.state)
                explored_order.append(node.state)  # Track order
                nodes_expanded += 1

                # Expand node
                for successor in self.problem.get_successors(node):
                    if successor.state not in explored:
                        f_value = successor.path_cost + h_func(successor.state)
                        heapq.heappush(frontier, (f_value, id(successor), successor))

        # No solution found
        elapsed_time = time.time() - start_time
        result = {
            'node': None,
            'path': [],
            'cost': float('inf'),
            'time': elapsed_time,
            'explored': explored,
            'explored_order': explored_order,  # Add ordered list
            'nodes_expanded': nodes_expanded,
            'path_length': 0,
            'max_frontier_size': max_frontier_size,
            'heuristic': heuristic,
            'success': False
        }
        self.results['A*-Graph'] = result
        return result
    
    # # ==================== UTILITY METHODS ====================
    
    # def run_all_algorithms(self, heuristic='euclidean'):
    #     """
    #     Run all 8 search algorithms and store results.
        
    #     Args:
    #         heuristic: Heuristic to use for A* ('euclidean' or 'manhattan')
        
    #     Returns:
    #         dict: Results for all algorithms
    #     """
    #     print("Running all search algorithms...")
    #     print("=" * 60)
        
    #     # Run tree search algorithms
    #     print("\n🌳 TREE SEARCH ALGORITHMS")
    #     print("-" * 60)
        
    #     print("Running BFS (Tree)...")
    #     self.bfs_tree()
        
    #     print("Running DFS (Tree)...")
    #     self.dfs_tree()
        
    #     print("Running UCS (Tree)...")
    #     self.ucs_tree()
        
    #     print("Running A* (Tree)...")
    #     self.astar_tree(heuristic)
        
    #     # Run graph search algorithms
    #     print("\n📊 GRAPH SEARCH ALGORITHMS")
    #     print("-" * 60)
        
    #     print("Running BFS (Graph)...")
    #     self.bfs_graph()
        
    #     print("Running DFS (Graph)...")
    #     self.dfs_graph()
        
    #     print("Running UCS (Graph)...")
    #     self.ucs_graph()
        
    #     print("Running A* (Graph)...")
    #     self.astar_graph(heuristic)
        
    #     print("\n✓ All algorithms completed!")
    #     return self.results
    
    # def print_results_summary(self):
    #     """Print a summary table of all algorithm results."""
    #     if not self.results:
    #         print("No results to display. Run algorithms first.")
    #         return
        
    #     print("\n" + "=" * 80)
    #     print("ALGORITHM PERFORMANCE SUMMARY")
    #     print("=" * 80)
        
    #     # Header
    #     print(f"{'Algorithm':<15} {'Time (s)':<12} {'Path Cost':<12} {'Path Length':<13} {'Nodes Exp.':<12} {'Success':<10}")
    #     print("-" * 80)
        
    #     # Results
    #     for name, result in self.results.items():
    #         time_str = f"{result['time']:.6f}"
    #         cost_str = f"{result['cost']:.2f}" if result['cost'] != float('inf') else "N/A"
    #         length_str = str(result['path_length'])
    #         nodes_str = str(result['nodes_expanded'])
    #         success_str = "✓" if result['success'] else "✗"
            
    #         print(f"{name:<15} {time_str:<12} {cost_str:<12} {length_str:<13} {nodes_str:<12} {success_str:<10}")
        
    #     print("=" * 80)
    
    # def get_comparison_data(self):
    #     """
    #     Get comparison data for visualization.
        
    #     Returns:
    #         dict: Paths and explored sets for each algorithm
    #     """
    #     comparison = {
    #         'paths': {},
    #         'explored': {},
    #         'costs': {},
    #         'times': {}
    #     }
        
    #     for name, result in self.results.items():
    #         if result['success']:
    #             comparison['paths'][name] = result['path']
    #             comparison['costs'][name] = result['cost']
    #             comparison['times'][name] = result['time']
                
    #             if 'explored' in result:
    #                 comparison['explored'][name] = result['explored']
        
    #     return comparison
