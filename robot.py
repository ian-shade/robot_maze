"""
Robot Class for Mobile Robot Pathfinding
Defines robot properties including motion model.
Robot is always square occupying one grid cell.
"""

class Robot:
    """
    Represents a mobile robot with motion capabilities.
    Robot is always square-shaped and occupies exactly one grid cell.
    
    Attributes:
        motion_model: List of possible actions as tuples (dx, dy, cost)
        position: Current position as tuple (x, y)
    """
    
    def __init__(self, motion_model=None):
        """
        Initialize a robot.
        
        Args:
            motion_model: List of tuples (dx, dy, cost) representing possible moves
                         If None, uses default 4-directional model
        """
        self.position = None  # Will be set when starting pathfinding
        
        # Default motion model: 4-directional (up, down, left, right)
        if motion_model is None:
            self.motion_model = [
                (0, 1, 1),   # Up
                (0, -1, 1),  # Down
                (-1, 0, 1),  # Left
                (1, 0, 1)    # Right
            ]
        else:
            self.motion_model = motion_model
    
    def set_motion_model(self, motion_model):
        """
        Set a custom motion model.
        
        Args:
            motion_model: List of tuples (dx, dy, cost)
        """
        self.motion_model = motion_model
    
    def set_4_directional_model(self, cost=1):
        """
        Set 4-directional motion model (up, down, left, right).
        
        Args:
            cost: Cost for each move (default: 1)
        """
        self.motion_model = [
            (0, 1, cost),   # Up
            (0, -1, cost),  # Down
            (-1, 0, cost),  # Left
            (1, 0, cost)    # Right
        ]
    
    def set_8_directional_model(self, straight_cost=1, diagonal_cost=1.414):
        """
        Set 8-directional motion model (includes diagonals).
        
        Args:
            straight_cost: Cost for straight moves (default: 1)
            diagonal_cost: Cost for diagonal moves (default: sqrt(2) ≈ 1.414)
        """
        self.motion_model = [
            (0, 1, straight_cost),      # Up
            (0, -1, straight_cost),     # Down
            (-1, 0, straight_cost),     # Left
            (1, 0, straight_cost),      # Right
            (1, 1, diagonal_cost),      # Up-Right
            (-1, 1, diagonal_cost),     # Up-Left
            (1, -1, diagonal_cost),     # Down-Right
            (-1, -1, diagonal_cost)     # Down-Left
        ]
    
    def get_possible_actions(self):
        """
        Get all possible actions from the motion model.
        
        Returns:
            List of tuples (dx, dy, cost)
        """
        return self.motion_model
    
    def __repr__(self):
        """String representation of the robot."""
        return f"Robot(motions={len(self.motion_model)})"
