"""
SearchAlgorithms Class
Implements all search algorithms: BFS, DFS, UCS, A* (tree and graph versions)
"""

import time
from collections import deque
import heapq


class SearchAlgorithms:

    def __init__(self, problem, max_depth=100, max_iterations=50000, timeout_seconds=30):
        self.problem = problem
        self.max_depth = max_depth
        self.max_iterations = max_iterations  # Maximum iterations before stopping
        self.timeout_seconds = timeout_seconds  # Maximum time before timeout
        self.results = {}  # Store results for comparison
    
    # ==================== BFS ALGORITHMS ====================
    
    def bfs_tree(self):
        start_time = time.time()

        frontier = deque([self.problem.get_initial_node()])
        nodes_expanded = 0
        max_frontier_size = 1
        iterations = 0

        while frontier:
            # Check timeout
            if time.time() - start_time > self.timeout_seconds:
                elapsed_time = time.time() - start_time
                raise TimeoutError(f"BFS-Tree exceeded timeout ({self.timeout_seconds}s). Tree algorithms may loop infinitely without visited state tracking. Consider using Graph version instead.")

            # Check iteration limit
            iterations += 1
            if iterations > self.max_iterations:
                elapsed_time = time.time() - start_time
                raise RuntimeError(f"BFS-Tree exceeded maximum iterations ({self.max_iterations}). Tree algorithms may explore too many nodes without visited state tracking. Consider using Graph version instead.")

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
        iterations = 0

        while frontier:
            # Check timeout
            if time.time() - start_time > self.timeout_seconds:
                elapsed_time = time.time() - start_time
                raise TimeoutError(f"DFS-Tree exceeded timeout ({self.timeout_seconds}s). Tree algorithms may loop infinitely without visited state tracking. Consider using Graph version instead.")

            # Check iteration limit
            iterations += 1
            if iterations > self.max_iterations:
                elapsed_time = time.time() - start_time
                raise RuntimeError(f"DFS-Tree exceeded maximum iterations ({self.max_iterations}). Tree algorithms may explore too many nodes without visited state tracking. Consider using Graph version instead.")

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
        iterations = 0

        while frontier:
            # Check timeout
            if time.time() - start_time > self.timeout_seconds:
                elapsed_time = time.time() - start_time
                raise TimeoutError(f"UCS-Tree exceeded timeout ({self.timeout_seconds}s). Tree algorithms may loop infinitely without visited state tracking. Consider using Graph version instead.")

            # Check iteration limit
            iterations += 1
            if iterations > self.max_iterations:
                elapsed_time = time.time() - start_time
                raise RuntimeError(f"UCS-Tree exceeded maximum iterations ({self.max_iterations}). Tree algorithms may explore too many nodes without visited state tracking. Consider using Graph version instead.")

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
        iterations = 0

        while frontier:
            # Check timeout
            if time.time() - start_time > self.timeout_seconds:
                elapsed_time = time.time() - start_time
                raise TimeoutError(f"A*-Tree exceeded timeout ({self.timeout_seconds}s). Tree algorithms may loop infinitely without visited state tracking. Consider using Graph version instead.")

            # Check iteration limit
            iterations += 1
            if iterations > self.max_iterations:
                elapsed_time = time.time() - start_time
                raise RuntimeError(f"A*-Tree exceeded maximum iterations ({self.max_iterations}). Tree algorithms may explore too many nodes without visited state tracking. Consider using Graph version instead.")

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