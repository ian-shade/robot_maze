"""
Example Usage of the Pathfinding Framework
Demonstrates how to set up the environment, robot, and problem with visualization.
"""

import numpy as np
from environment import Environment
from robot import Robot
from problem import PathfindingProblem
from visualizer import visualize_environment, visualize_path

def create_simple_example():
    
    env = Environment(width=10, height=10, has_border=True)

    env.add_obstacle_rectangle(x_start=3, y_start=3, width=2, height=4)
    
    # Add individual obstacles
    env.add_obstacle(6, 5)
    env.add_obstacle(6, 6)
    
    # 3. Set initial and goal states
    env.set_initial_state(2, 2)
    env.set_goal_state(7, 7)

    
    # 4. Create robot
    robot = Robot()  # Simplified - always square, grid size = 1
    robot.set_4_directional_model(cost=1)

    
    # 5. Create problem
    problem = PathfindingProblem(env, robot)
    problem.validate_problem()
    
    # 6. Visualize the environment
    visualize_environment(env, title='Simple Example Environment', show=False)
    
    return env, robot, problem


def create_complex_example():
    """Create a more complex example with 8-directional movement."""
    
    # 1. Create larger environment
    env = Environment(width=15, height=15, has_border=True)
    print(f"✓ Environment created: {env}")
    
    # 2. Add rectangular obstacles to create a maze-like structure
    env.add_obstacle_rectangle(2, 5, 5, 1)  # Horizontal wall
    env.add_obstacle_rectangle(10, 5, 3, 1)  # Another horizontal wall
    env.add_obstacle_rectangle(5, 2, 1, 4)  # Vertical wall
    env.add_obstacle_rectangle(6, 6, 3, 3)  # Square obstacle in middle
    print("✓ Added maze-like obstacles")
    
    # 3. Set states
    env.set_initial_state(2, 2)
    env.set_goal_state(12, 12)
    print(f"✓ Initial state: {env.initial_state}")
    print(f"✓ Goal state: {env.goal_state}")
    
    # 4. Create robot with 8-directional movement
    robot = Robot()
    robot.set_8_directional_model(straight_cost=1, diagonal_cost=1.414)
    print(f"✓ Robot created: {robot}")
    print(f"  Motion model: {len(robot.motion_model)} actions (8-directional)")
    
    # 5. Create problem
    problem = PathfindingProblem(env, robot)
    problem.validate_problem()
    print(f"✓ Problem created and validated")
    
    # 6. Test heuristics
    test_state = (5, 5)
    manhattan = problem.heuristic_manhattan(test_state)
    euclidean = problem.heuristic_euclidean(test_state)
    print(f"\n✓ Heuristic test from {test_state} to {env.goal_state}:")
    print(f"  Manhattan distance: {manhattan}")
    print(f"  Euclidean distance: {euclidean:.2f}")
    
    # 7. Visualize
    print("\n✓ Creating visualization...")
    visualize_environment(env, title='Complex Example Environment', show=False)
    
    return env, robot, problem


def test_successor_generation():
    """Test successor generation for a given problem."""
    # Create simple environment
    env = Environment(width=5, height=5, has_border=False)
    env.set_initial_state(2, 2)
    env.set_goal_state(4, 4)
    
    robot = Robot()
    robot.set_4_directional_model(cost=1)
    
    problem = PathfindingProblem(env, robot)
    
    # Get initial node
    initial_node = problem.get_initial_node()
    print(f"Initial node: {initial_node}")
    
    # Get successors
    successors = problem.get_successors(initial_node)
    print(f"\nSuccessors of initial state {initial_node.state}:")
    for i, succ in enumerate(successors, 1):
        print(f"  {i}. State: {succ.state}, Action: {succ.action}, Cost: {succ.path_cost}")
    
    print(f"\n✓ Generated {len(successors)} successors")


def demo_visualization():
    
    # Create environment
    env = Environment(width=12, height=12, has_border=True)
    env.add_obstacle_rectangle(4, 4, 4, 1)
    env.add_obstacle_rectangle(4, 7, 4, 1)
    env.set_initial_state(2, 2)
    env.set_goal_state(9, 9)
    
    # Create a sample path (manually for demonstration)
    sample_path = [
        (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2),
        (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (9, 9)
    ]
    
    # Sample explored states
    explored = {
        (2, 2), (3, 2), (2, 3), (4, 2), (3, 3),
        (5, 2), (4, 3), (6, 2), (5, 3), (7, 2),
        (8, 2), (8, 3), (8, 4), (8, 5), (8, 6),
        (8, 7), (8, 8), (8, 9), (9, 9), (9, 8)
    }
    
    visualize_path(env, sample_path, explored, 
        title='Sample Path Visualization', show=False)


if __name__ == "__main__":
    # Run examples
    env1, robot1, problem1 = create_simple_example()
    env2, robot2, problem2 = create_complex_example()
    test_successor_generation()
    demo_visualization()
    
    import matplotlib.pyplot as plt
    plt.show()  # Show all plots at once
