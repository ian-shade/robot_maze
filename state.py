class State:
    """
    Represents a state in the pathfinding problem.
    For this 2D grid problem, a state is simply a position (x, y).
    
    Attributes:
        x: X coordinate in the grid
        y: Y coordinate in the grid
    """
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        """String representation of the state."""
        return f"State({self.x}, {self.y})"
    
    def __eq__(self, other):
        """Check equality of states."""
        if isinstance(other, State):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, tuple):
            return self.x == other[0] and self.y == other[1]
        return False
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def as_tuple(self):
        return (self.x, self.y)
    
    def manhattan_distance(self, other):
        # Calculate Manhattan distance to another state (int).

        if isinstance(other, State):
            return abs(self.x - other.x) + abs(self.y - other.y)
        elif isinstance(other, tuple):
            return abs(self.x - other[0]) + abs(self.y - other[1])
        raise TypeError("Other must be State or tuple")
    
    def euclidean_distance(self, other):
        # Calculate Euclidean distance to another state (float).

        if isinstance(other, State):
            return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5
        elif isinstance(other, tuple):
            return ((self.x - other[0])**2 + (self.y - other[1])**2)**0.5
        raise TypeError("Other must be State or tuple")
