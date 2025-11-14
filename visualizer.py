"""
Visualization Module for Robot Pathfinding
Uses matplotlib to visualize the grid environment and paths.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class Visualizer:

    def __init__(self, environment):
        self.environment = environment
        self.fig = None
        self.ax = None
    
    def setup_plot(self, figsize=(10, 10)):

        self.fig, self.ax = plt.subplots(1, 1, figsize=figsize)
        self.ax.set_aspect('equal')
        self.ax.set_xlim(-0.5, self.environment.width - 0.5)
        self.ax.set_ylim(-0.5, self.environment.height - 0.5)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.grid(True, alpha=0.3)
        
        # Set integer ticks
        self.ax.set_xticks(range(self.environment.width))
        self.ax.set_yticks(range(self.environment.height))
    
    def draw_grid(self):
        # Draw the grid with obstacles.
        if self.fig is None:
            self.setup_plot()
        
        # Draw each cell
        for y in range(self.environment.height):
            for x in range(self.environment.width):
                if self.environment.grid[y, x] == 1:
                    # Obstacle - draw as gray square
                    rect = patches.Rectangle(
                        (x - 0.5, y - 0.5), 1, 1,
                        linewidth=1, edgecolor='black',
                        facecolor='gray', alpha=0.7
                    )
                    self.ax.add_patch(rect)
                else:
                    # Free space - draw as white square
                    rect = patches.Rectangle(
                        (x - 0.5, y - 0.5), 1, 1,
                        linewidth=0.5, edgecolor='lightgray',
                        facecolor='white', alpha=1.0
                    )
                    self.ax.add_patch(rect)
    
    def draw_start_goal(self):
        # Draw the initial and goal states.
        if self.environment.initial_state is not None:
            x, y = self.environment.initial_state
            rect = patches.Rectangle(
                (x - 0.5, y - 0.5), 1, 1,
                linewidth=2, edgecolor='darkred',
                facecolor='red', alpha=0.6
            )
            self.ax.add_patch(rect)
            self.ax.text(x, y, 'START', ha='center', va='center',
                        fontsize=8, fontweight='bold', color='white')
        
        if self.environment.goal_state is not None:
            x, y = self.environment.goal_state
            rect = patches.Rectangle(
                (x - 0.5, y - 0.5), 1, 1,
                linewidth=2, edgecolor='darkgreen',
                facecolor='green', alpha=0.6
            )
            self.ax.add_patch(rect)
            self.ax.text(x, y, 'GOAL', ha='center', va='center',
                        fontsize=8, fontweight='bold', color='white')
    
    def draw_path(self, path, color='blue', linewidth=2, label='Path'):
        # Draw a path on the grid.

        if len(path) < 2:
            return
        
        x_coords = [state[0] for state in path]
        y_coords = [state[1] for state in path]
        
        self.ax.plot(x_coords, y_coords, color=color, linewidth=linewidth,
                    marker='o', markersize=4, label=label, alpha=0.7)
    
    def draw_explored(self, explored_states, color='cyan', alpha=0.3):
        # Draw explored states. 
        for state in explored_states:
            if state != self.environment.initial_state and \
               state != self.environment.goal_state:
                x, y = state
                rect = patches.Rectangle(
                    (x - 0.5, y - 0.5), 1, 1,
                    linewidth=0, facecolor=color, alpha=alpha
                )
                self.ax.add_patch(rect)
    
    def show(self, title='Robot Pathfinding'):
        # Display the plot.
  
        self.ax.set_title(title, fontsize=14, fontweight='bold')
        self.ax.legend(loc='upper right')
        plt.tight_layout()
        plt.show()
    
    def save(self, filename, title='Robot Pathfinding'): 
        # Save the plot to a file.

        self.ax.set_title(title, fontsize=14, fontweight='bold')
        self.ax.legend(loc='upper right')
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"✓ Saved visualization to {filename}")
    
    def clear(self):
        # Clear the current plot.
        if self.ax is not None:
            self.ax.clear()
            self.setup_plot()


def visualize_environment(environment, title='Environment', show=True):
    # Quick function to visualize just the environment.

    viz = Visualizer(environment)
    viz.setup_plot()
    viz.draw_grid()
    viz.draw_start_goal()
    
    if show:
        viz.show(title)
    
    return viz


def visualize_path(environment, path, explored=None, title='Path Found', show=True):
    # Quick function to visualize environment with a path.

    viz = Visualizer(environment)
    viz.setup_plot()
    viz.draw_grid()
    
    if explored is not None:
        viz.draw_explored(explored, color='lightblue', alpha=0.4)
    
    viz.draw_start_goal()
    viz.draw_path(path, color='blue', linewidth=3, label='Path')
    
    if show:
        viz.show(title)
    
    return viz


def compare_paths(environment, paths_dict, explored_dict=None, title='Path Comparison'):
    # Visualize multiple paths on the same plot for comparison.

    viz = Visualizer(environment)
    viz.setup_plot(figsize=(12, 10))
    viz.draw_grid()
    viz.draw_start_goal()
    
    # Color palette for different algorithms
    colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'cyan']
    
    for i, (name, path) in enumerate(paths_dict.items()):
        color = colors[i % len(colors)]
        viz.draw_path(path, color=color, linewidth=2, label=name)
    
    viz.show(title)
    return viz
