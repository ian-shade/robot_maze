"""
Environment Class for Mobile Robot Pathfinding
Represents the 2D grid environment with square obstacles.
Grid size is always 1 (each cell is 1x1).
"""

import numpy as np

class Environment:
    
    def __init__(self, width=10, height=10, has_border=True):

        self.width = width
        self.height = height
        self.has_border = has_border
        
        # Initialize grid with all free space
        self.grid = np.zeros((height, width), dtype=int)
        
        # Add borders if requested
        if has_border:
            self._add_borders()
        
        # States will be set later
        self.initial_state = None
        self.goal_state = None
    
    def _add_borders(self):
        # Add obstacle borders around the environment.

        self.grid[0, :] = 1   # Top border
        self.grid[-1, :] = 1  # Bottom border
        self.grid[:, 0] = 1   # Left border
        self.grid[:, -1] = 1  # Right border
    
    def add_obstacle(self, x, y):

        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = 1
    
    def add_obstacle_rectangle(self, x_start, y_start, width, height):

        for y in range(y_start, min(y_start + height, self.height)):
            for x in range(x_start, min(x_start + width, self.width)):
                self.grid[y, x] = 1
    
    def remove_obstacle(self, x, y):

        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = 0
    
    def is_free(self, x, y):
        
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y, x] == 0
        return False
    
    def is_valid(self, x, y):
        # Check if a position is within bounds and free.

        return self.is_free(x, y)
    
    def set_initial_state(self, x, y):
        # Set the initial (start) state.
       
        if self.is_free(x, y):
            self.initial_state = (x, y)
        else:
            raise ValueError(f"Initial state ({x}, {y}) is not free!")
    
    def set_goal_state(self, x, y):
        # Set the goal state.

        if self.is_free(x, y):
            self.goal_state = (x, y)
        else:
            raise ValueError(f"Goal state ({x}, {y}) is not free!")
    
    def get_neighbors(self, state, motion_model):
        # Get valid neighboring states based on motion model.

        x, y = state
        neighbors = []

        for action in motion_model:
            dx, dy, cost = action
            next_x, next_y = x + dx, y + dy

            # Check if destination is valid
            if not self.is_valid(next_x, next_y):
                continue

            # For diagonal moves (both dx and dy are non-zero),
            # check that the robot can't squeeze through diagonal obstacles
            if dx != 0 and dy != 0:
                # Check the two adjacent cells that form the "corridor" for this diagonal move
                # The robot can only move diagonally if at least one of these cells is free
                adjacent1_free = self.is_free(x + dx, y)  # Move horizontally first
                adjacent2_free = self.is_free(x, y + dy)  # Move vertically first

                # Allow diagonal move only if at least one path is clear
                if not (adjacent1_free or adjacent2_free):
                    continue

            neighbors.append(((next_x, next_y), action, cost))

        return neighbors
    
    def clear_obstacles(self):
        # Clear all obstacles (except borders if enabled).
        self.grid = np.zeros((self.height, self.width), dtype=int)
        if self.has_border:
            self._add_borders()
    
    def get_grid_copy(self):

        # Get a copy of the current grid.

        return np.copy(self.grid)
    
    def __repr__(self):
        # String representation of the environment.
        return f"Environment({self.width}x{self.height}, obstacles={np.sum(self.grid)})"
