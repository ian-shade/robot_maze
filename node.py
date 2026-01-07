class Node:
    """
    Represents a node in the search tree/graph.
    
    Attributes:
        state: The state associated with this node (x, y coordinates)
        parent: Reference to the parent node
        action: The action taken to reach this node from parent
        path_cost: Cost from initial state to this node (g(n))
        depth: Depth of the node in the search tree
    """
    
    def __init__(self, state, parent=None, action=None, path_cost=0):
        
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0 if parent is None else parent.depth + 1
        
    def __repr__(self):

        # String representation of the node.
        return f"Node(state={self.state}, cost={self.path_cost}, depth={self.depth})"
    
    def __eq__(self, other):
        # Check equality based on state.
        if isinstance(other, Node):
            return self.state == other.state
        return False
    
    def __hash__(self):
        # Hash based on state for use in sets and dictionaries.
        return hash(self.state)
    
    def __lt__(self, other):
        # Less than comparison for priority queue (based on path cost).
        return self.path_cost < other.path_cost
    
    def get_path(self):
        # List of states from initial to current
        path = []
        current = self
        while current is not None:
            path.append(current.state)
            current = current.parent
        return list(reversed(path))
    
    def get_actions(self):
        # List of actions from initial to current
        actions = []
        current = self
        while current.parent is not None:
            actions.append(current.action)
            current = current.parent
        return list(reversed(actions))
