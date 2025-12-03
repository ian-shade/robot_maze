"""UI screen components for setup and visualization"""

import streamlit as st
from environment import Environment
from robot import Robot
from problem import PathfindingProblem
from search_algorithms import SearchAlgorithms
from web.components.grid_visualizer import (
    create_grid_figure, show_final_result, show_step_by_step
)


def setup_screen():
    """First screen: Setup environment and algorithm"""
    st.title("🤖 Interactive Pathfinding Visualizer")
    st.markdown("---")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Environment Setup
        st.subheader("1️⃣ Environment")
        env_type = st.selectbox(
            "Environment Type",
            ["Simple 10x10", "Medium 12x12", "Complex 15x15", "Custom"]
        )
        
        # Create environment based on selection
        if env_type == "Simple 10x10":
            env = Environment(width=10, height=10, has_border=True)
            env.add_obstacle_rectangle(3, 3, 2, 4)
            env.add_obstacle(6, 5)
            env.add_obstacle(6, 6)
            env.set_initial_state(2, 2)
            env.set_goal_state(7, 7)
        
        elif env_type == "Medium 12x12":
            env = Environment(width=12, height=12, has_border=True)
            env.add_obstacle_rectangle(4, 4, 4, 1)
            env.add_obstacle_rectangle(4, 7, 4, 1)
            env.set_initial_state(2, 2)
            env.set_goal_state(9, 9)
        
        elif env_type == "Complex 15x15":
            env = Environment(width=15, height=15, has_border=True)
            env.add_obstacle_rectangle(2, 5, 5, 1)
            env.add_obstacle_rectangle(10, 5, 3, 1)
            env.add_obstacle_rectangle(5, 2, 1, 4)
            env.add_obstacle_rectangle(6, 8, 4, 1)
            env.set_initial_state(2, 2)
            env.set_goal_state(12, 12)
        
        else:  # Custom
            col1, col2 = st.columns(2)
            with col1:
                width = st.number_input("Width", 5, 20, 10)
            with col2:
                height = st.number_input("Height", 5, 20, 10)
            
            env = Environment(width=width, height=height, has_border=True)
            
            st.write("Start Position:")
            col1, col2 = st.columns(2)
            with col1:
                start_x = st.number_input("Start X", 0, width-1, 2)
            with col2:
                start_y = st.number_input("Start Y", 0, height-1, 2)
            
            st.write("Goal Position:")
            col1, col2 = st.columns(2)
            with col1:
                goal_x = st.number_input("Goal X", 0, width-1, width-3)
            with col2:
                goal_y = st.number_input("Goal Y", 0, height-1, height-3)
            
            env.set_initial_state(start_x, start_y)
            env.set_goal_state(goal_x, goal_y)
        
        # Motion Model
        st.subheader("2️⃣ Motion Model")
        motion = st.radio(
            "Choose movement type:",
            ["4-directional (Up, Down, Left, Right)", 
             "8-directional (includes diagonals)"]
        )
        
        robot = Robot()
        if "8-directional" in motion:
            robot.set_8_directional_model(straight_cost=1, diagonal_cost=1.414)
        else:
            robot.set_4_directional_model(cost=1)
        
        # Algorithm Selection
        st.subheader("3️⃣ Algorithm")
        algorithm_choice = st.selectbox(
            "Search Algorithm",
            ["BFS-Graph", "DFS-Graph", "UCS-Graph", "A*-Graph",
             "BFS-Tree", "DFS-Tree", "UCS-Tree", "A*-Tree"]
        )
        
        # Heuristic for A*
        heuristic = None
        if "A*" in algorithm_choice:
            heuristic = st.radio(
                "Heuristic:",
                ["Euclidean", "Manhattan"]
            ).lower()
        
        st.markdown("---")
        
        # Run button
        if st.button("🚀 Run Algorithm", type="primary"):
            try:
                problem = PathfindingProblem(env, robot)
                problem.validate_problem()
                
                search = SearchAlgorithms(problem)
                
                # Run selected algorithm
                algorithm_map = {
                    'BFS-Graph': search.bfs_graph,
                    'DFS-Graph': search.dfs_graph,
                    'UCS-Graph': search.ucs_graph,
                    'A*-Graph': lambda: search.astar_graph(heuristic=heuristic),
                    'BFS-Tree': search.bfs_tree,
                    'DFS-Tree': search.dfs_tree,
                    'UCS-Tree': search.ucs_tree,
                    'A*-Tree': lambda: search.astar_tree(heuristic=heuristic),
                }
                
                with st.spinner(f"Running {algorithm_choice}..."):
                    result = algorithm_map[algorithm_choice]()
                
                # Store in session state
                st.session_state.env = env
                st.session_state.robot = robot
                st.session_state.problem = problem
                st.session_state.result = result
                st.session_state.algorithm = algorithm_choice
                st.session_state.setup_complete = True
                
                st.success("✅ Algorithm completed!")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Main area - show environment preview
    st.header("📍 Environment Preview")
    if env:
        create_grid_figure(env, title="Environment Setup")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**Grid Size:** {env.width} × {env.height}")
        with col2:
            st.info(f"**Start:** {env.initial_state}")
        with col3:
            st.info(f"**Goal:** {env.goal_state}")


def visualization_screen():
    """Second screen: Show results with different visualization modes"""
    
    st.title("🎯 Results & Visualization")
    
    # Back button
    if st.sidebar.button("⬅️ Back to Setup"):
        st.session_state.setup_complete = False
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Display algorithm info
    st.sidebar.header("📊 Algorithm Info")
    st.sidebar.write(f"**Algorithm:** {st.session_state.algorithm}")
    
    result = st.session_state.result
    
    if result['success']:
        st.sidebar.success("✅ Path Found!")
    else:
        st.sidebar.error("❌ No Path Found")
    
    # Visualization mode selection
    st.sidebar.markdown("---")
    st.sidebar.header("🎬 Visualization Mode")
    
    viz_mode = st.sidebar.radio(
        "Choose display mode:",
        ["📸 Final Result", "🔍 Step-by-Step Exploration"],
        help="""
        - **Final Result**: Shows complete path and explored nodes
        - **Step-by-Step**: Shows exploration process node by node
        """
    )
    
    # Main content area
    if not result['success']:
        st.error("❌ No solution found!")
        st.write(f"**Nodes Expanded:** {result['nodes_expanded']}")
        st.write(f"**Time Elapsed:** {result['time']:.6f} seconds")
        return
    
    # Display metrics
    st.header(f"{st.session_state.algorithm} - {viz_mode}")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("⏱️ Time", f"{result['time']:.4f}s")
    with col2:
        st.metric("💰 Path Cost", f"{result['cost']:.2f}")
    with col3:
        st.metric("📏 Path Length", result['path_length'])
    with col4:
        st.metric("🔍 Nodes Expanded", result['nodes_expanded'])
    
    st.markdown("---")
    
    # Visualization based on mode
    if viz_mode == "📸 Final Result":
        show_final_result()
    else:  # Step-by-Step
        show_step_by_step()
