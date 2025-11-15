"""
Example Usage 2 - Interactive Algorithm Selection
Run individual algorithms and view their paths and explored states.
"""

from environment import Environment
from robot import Robot
from problem import PathfindingProblem
from search_algorithms import SearchAlgorithms
from visualizer import Visualizer
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving


def create_environment():
    """Create a customizable environment."""
    print("\n" + "="*70)
    print("ENVIRONMENT SETUP")
    print("="*70)
    
    print("\nChoose environment type:")
    print("  1. Simple 10x10 grid (recommended for testing)")
    print("  2. Medium 12x12 grid with obstacles")
    print("  3. Complex 15x15 maze")
    print("  4. Custom (you specify)")
    
    choice = input("\nEnter choice (1-4) [default: 1]: ").strip() or "1"
    
    if choice == "1":
        env = Environment(width=10, height=10, has_border=True)
        env.add_obstacle_rectangle(3, 3, 2, 4)
        env.add_obstacle(6, 5)
        env.add_obstacle(6, 6)
        env.set_initial_state(2, 2)
        env.set_goal_state(7, 7)
        print("✓ Created simple 10x10 environment")
        
    elif choice == "2":
        env = Environment(width=12, height=12, has_border=True)
        env.add_obstacle_rectangle(4, 4, 4, 1)
        env.add_obstacle_rectangle(4, 7, 4, 1)
        env.set_initial_state(2, 2)
        env.set_goal_state(9, 9)
        print("✓ Created medium 12x12 environment")
        
    elif choice == "3":
        env = Environment(width=15, height=15, has_border=True)
        env.add_obstacle_rectangle(2, 5, 5, 1)
        env.add_obstacle_rectangle(10, 5, 3, 1)
        env.add_obstacle_rectangle(5, 2, 1, 4)
        env.add_obstacle_rectangle(6, 8, 4, 1)
        env.set_initial_state(2, 2)
        env.set_goal_state(12, 12)
        print("✓ Created complex 15x15 maze")
        
    else:
        width = int(input("Enter width: ") or "10")
        height = int(input("Enter height: ") or "10")
        env = Environment(width=width, height=height, has_border=True)
        
        # Get start and goal
        start_x = int(input(f"Start X (0-{width-1}): ") or "2")
        start_y = int(input(f"Start Y (0-{height-1}): ") or "2")
        goal_x = int(input(f"Goal X (0-{width-1}): ") or str(width-3))
        goal_y = int(input(f"Goal Y (0-{height-1}): ") or str(height-3))
        
        env.set_initial_state(start_x, start_y)
        env.set_goal_state(goal_x, goal_y)
        print(f"✓ Created custom {width}x{height} environment")
    
    print(f"  Start: {env.initial_state}")
    print(f"  Goal: {env.goal_state}")
    
    return env


def choose_motion_model():
    """Choose robot motion model."""
    print("\n" + "="*70)
    print("MOTION MODEL SELECTION")
    print("="*70)
    
    print("\nChoose motion model:")
    print("  1. 4-directional (Up, Down, Left, Right)")
    print("  2. 8-directional (includes diagonals)")
    
    choice = input("\nEnter choice (1-2) [default: 1]: ").strip() or "1"
    
    robot = Robot()
    
    if choice == "2":
        robot.set_8_directional_model(straight_cost=1, diagonal_cost=1.414)
        print("✓ Using 8-directional motion model")
    else:
        robot.set_4_directional_model(cost=1)
        print("✓ Using 4-directional motion model")
    
    return robot


def choose_algorithm():
    """Choose which algorithm to run."""
    print("\n" + "="*70)
    print("ALGORITHM SELECTION")
    print("="*70)
    
    print("\nAvailable algorithms:")
    print("\n  TREE SEARCH (may revisit states):")
    print("    1. BFS-Tree   (Breadth-First Search)")
    print("    2. DFS-Tree   (Depth-First Search)")
    print("    3. UCS-Tree   (Uniform Cost Search)")
    print("    4. A*-Tree    (A Star Search)")
    
    print("\n  GRAPH SEARCH (never revisits states - recommended):")
    print("    5. BFS-Graph  (Breadth-First Search)")
    print("    6. DFS-Graph  (Depth-First Search)")
    print("    7. UCS-Graph  (Uniform Cost Search)")
    print("    8. A*-Graph   (A Star Search)")
    
    print("\n  OTHER OPTIONS:")
    print("    9. Run all algorithms (comparison)")
    print("    0. Exit")
    
    choice = input("\nEnter choice (0-9) [default: 5]: ").strip() or "5"
    return choice


def run_single_algorithm(search, algorithm_choice):
    """Run a single algorithm and display results."""
    
    # Map choice to algorithm
    algorithm_map = {
        '1': ('bfs_tree', 'BFS-Tree', False),
        '2': ('dfs_tree', 'DFS-Tree', False),
        '3': ('ucs_tree', 'UCS-Tree', False),
        '4': ('astar_tree', 'A*-Tree', True),
        '5': ('bfs_graph', 'BFS-Graph', False),
        '6': ('dfs_graph', 'DFS-Graph', False),
        '7': ('ucs_graph', 'UCS-Graph', False),
        '8': ('astar_graph', 'A*-Graph', True),
    }
    
    if algorithm_choice not in algorithm_map:
        print("Invalid choice!")
        return None
    
    method_name, display_name, needs_heuristic = algorithm_map[algorithm_choice]
    
    print("\n" + "="*70)
    print(f"RUNNING: {display_name}")
    print("="*70)
    
    # Get heuristic for A*
    heuristic = 'euclidean'
    if needs_heuristic:
        print("\nChoose heuristic:")
        print("  1. Euclidean (straight-line distance)")
        print("  2. Manhattan (grid distance)")
        h_choice = input("Enter choice (1-2) [default: 1]: ").strip() or "1"
        heuristic = 'manhattan' if h_choice == '2' else 'euclidean'
        print(f"✓ Using {heuristic} heuristic")
    
    # Run the algorithm
    method = getattr(search, method_name)
    if needs_heuristic:
        result = method(heuristic=heuristic)
    else:
        result = method()
    
    # Display results
    print("\n" + "-"*70)
    print("RESULTS")
    print("-"*70)
    
    if result['success']:
        print(f"✓ Path found!")
        print(f"  Time elapsed:     {result['time']:.6f} seconds")
        print(f"  Path cost:        {result['cost']:.2f}")
        print(f"  Path length:      {result['path_length']} states")
        print(f"  Nodes expanded:   {result['nodes_expanded']}")
        print(f"  Max frontier:     {result['max_frontier_size']}")
        
        if 'explored' in result:
            print(f"  States explored:  {len(result['explored'])}")
        
        # Show path
        print(f"\n  Path (first 10 states):")
        for i, state in enumerate(result['path'][:10], 1):
            print(f"    {i}. {state}")
        if len(result['path']) > 10:
            print(f"    ... ({len(result['path']) - 10} more states)")
        
        # Show explored states (if graph search)
        if 'explored' in result and len(result['explored']) > 0:
            print(f"\n  Explored states (first 10):")
            for i, state in enumerate(list(result['explored'])[:10], 1):
                print(f"    {i}. {state}")
            if len(result['explored']) > 10:
                print(f"    ... ({len(result['explored']) - 10} more states)")
    else:
        print("✗ No path found!")
        print(f"  Time elapsed:     {result['time']:.6f} seconds")
        print(f"  Nodes expanded:   {result['nodes_expanded']}")
    
    print("-"*70)
    
    return result


def visualize_result(env, result, algorithm_name):
    """Create visualization for a single algorithm result."""
    
    if not result['success']:
        print("\n✗ Cannot visualize - no path found")
        return
    
    print("\n" + "="*70)
    print("CREATING VISUALIZATION")
    print("="*70)
    
    filename = f"{algorithm_name.lower().replace(' ', '_').replace('*', 'star')}_result.png"
    
    viz = Visualizer(env)
    viz.setup_plot(figsize=(10, 10))
    viz.draw_grid()
    
    # Draw explored states if available
    if 'explored' in result:
        viz.draw_explored(result['explored'], color='lightblue', alpha=0.3)
        print(f"✓ Drew {len(result['explored'])} explored states")
    
    viz.draw_start_goal()
    viz.draw_path(result['path'], color='blue', linewidth=3, label=algorithm_name)
    
    viz.save(filename, title=f"{algorithm_name} - Path Found")
    print(f"✓ Saved visualization to: {filename}")


def run_all_comparison(search, env):
    """Run all algorithms and create comparison."""
    
    print("\n" + "="*70)
    print("RUNNING ALL ALGORITHMS")
    print("="*70)
    
    results = search.run_all_algorithms(heuristic='euclidean')
    
    # Print summary
    search.print_results_summary()
    
    # Create comparison visualization
    print("\n✓ Creating comparison visualization...")
    comparison = search.get_comparison_data()
    
    if comparison['paths']:
        viz = Visualizer(env)
        viz.setup_plot(figsize=(14, 12))
        viz.draw_grid()
        viz.draw_start_goal()
        
        colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'cyan']
        for i, (name, path) in enumerate(comparison['paths'].items()):
            color = colors[i % len(colors)]
            viz.draw_path(path, color=color, linewidth=2, label=name)
        
        viz.save('all_algorithms_comparison.png', title='All Algorithms Comparison')
        print("✓ Saved comparison to: all_algorithms_comparison.png")
    
    return results


def main_interactive():
    """Main interactive function."""
    
    print("\n" + "="*70)
    print("🤖 INTERACTIVE SEARCH ALGORITHM TESTER")
    print("="*70)
    
    # Setup environment
    env = create_environment()
    
    # Choose motion model
    robot = choose_motion_model()
    
    # Create problem
    problem = PathfindingProblem(env, robot)
    problem.validate_problem()
    print("\n✓ Problem validated successfully")
    
    # Visualize environment
    print("\n✓ Creating environment visualization...")
    viz_env = Visualizer(env)
    viz_env.setup_plot(figsize=(10, 10))
    viz_env.draw_grid()
    viz_env.draw_start_goal()
    viz_env.save('current_environment.png', title='Environment Setup')
    print("✓ Saved environment to: current_environment.png")
    
    # Create search instance
    search = SearchAlgorithms(problem)
    
    # Main loop
    while True:
        # Choose algorithm
        choice = choose_algorithm()
        
        if choice == '0':
            print("\n" + "="*70)
            print("👋 Goodbye!")
            print("="*70)
            break
        
        elif choice == '9':
            # Run all algorithms
            run_all_comparison(search, env)
            
            # Ask if want to continue
            cont = input("\nRun another algorithm? (y/n) [default: y]: ").strip().lower()
            if cont == 'n':
                break
        
        else:
            # Run single algorithm
            result = run_single_algorithm(search, choice)
            
            if result:
                # Ask if want visualization
                viz_choice = input("\nCreate visualization? (y/n) [default: y]: ").strip().lower()
                if viz_choice != 'n':
                    algorithm_name = {
                        '1': 'BFS-Tree', '2': 'DFS-Tree', '3': 'UCS-Tree', '4': 'A*-Tree',
                        '5': 'BFS-Graph', '6': 'DFS-Graph', '7': 'UCS-Graph', '8': 'A*-Graph'
                    }[choice]
                    visualize_result(env, result, algorithm_name)
            
            # Ask if want to continue
            cont = input("\nRun another algorithm? (y/n) [default: y]: ").strip().lower()
            if cont == 'n':
                break
    
    print("\n" + "="*70)
    print("📊 SESSION SUMMARY")
    print("="*70)
    print(f"Algorithms run: {len(search.results)}")
    if search.results:
        print("\nResults stored in:")
        for name in search.results.keys():
            print(f"  - {name}")
    print("\n✓ All visualizations saved in current directory")
    print("="*70)


def quick_demo():
    """Quick demo without interaction (for testing)."""
    
    print("\n" + "="*70)
    print("🚀 QUICK DEMO MODE")
    print("="*70)
    
    # Create simple environment
    env = Environment(width=10, height=10, has_border=True)
    env.add_obstacle_rectangle(3, 3, 2, 4)
    env.set_initial_state(2, 2)
    env.set_goal_state(7, 7)
    print("✓ Environment created: 10x10 grid")
    
    # Create robot and problem
    robot = Robot()
    robot.set_4_directional_model(cost=1)
    problem = PathfindingProblem(env, robot)
    print("✓ Robot: 4-directional movement")
    
    # Create search instance
    search = SearchAlgorithms(problem)
    
    # Run BFS-Graph
    print("\n" + "="*70)
    print("Running BFS-Graph...")
    print("="*70)
    result = search.bfs_graph()
    
    print(f"\n✓ Path found!")
    print(f"  Time:           {result['time']:.6f}s")
    print(f"  Cost:           {result['cost']}")
    print(f"  Path length:    {result['path_length']}")
    print(f"  Nodes expanded: {result['nodes_expanded']}")
    print(f"\n  Path: {result['path']}")
    
    if 'explored' in result:
        print(f"\n  Explored states ({len(result['explored'])} total):")
        print(f"  {list(result['explored'])[:10]}...")
    
    # Visualize
    print("\n✓ Creating visualization...")
    viz = Visualizer(env)
    viz.setup_plot(figsize=(10, 10))
    viz.draw_grid()
    viz.draw_explored(result['explored'], color='lightblue', alpha=0.3)
    viz.draw_start_goal()
    viz.draw_path(result['path'], color='blue', linewidth=3, label='BFS-Graph')
    viz.save('demo_bfs_graph.png', title='BFS Graph Search Demo')
    print("✓ Saved to: demo_bfs_graph.png")
    
    print("\n" + "="*70)
    print("✅ DEMO COMPLETED!")
    print("="*70)


if __name__ == "__main__":
    import sys
    
    # Check if running in interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        # Quick demo mode
        quick_demo()
    else:
        # Interactive mode
        try:
            main_interactive()
        except KeyboardInterrupt:
            print("\n\n" + "="*70)
            print("⚠️  Interrupted by user")
            print("="*70)
        except EOFError:
            print("\n\n" + "="*70)
            print("⚠️  Running in non-interactive mode")
            print("💡 Use --demo flag for automatic demo: python example_usage_2.py --demo")
            print("="*70)
