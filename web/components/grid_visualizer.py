"""Grid visualization components for displaying pathfinding results"""

import streamlit as st
import time


def create_html_grid(env, path=None, explored=None, current_pos=None, 
                      show_explored=True, show_path=True, title="Grid"):
    """Create an HTML/CSS grid visualization"""
    
    cell_size = 40  # pixels per cell
    grid_width = env.width * cell_size
    grid_height = env.height * cell_size
    
    html_content = f"""
    <div style="text-align: center;">
        <h3 style="color: #2c3e50; margin-bottom: 20px;">{title}</h3>
        <div style="display: inline-block; border: 2px solid #34495e; background-color: white; border-radius: 8px; padding: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            <svg width="{grid_width}" height="{grid_height}" style="background-color: #ecf0f1; display: block;">
    """
    
    # Draw grid lines
    for x in range(env.width + 1):
        x_pos = x * cell_size
        html_content += f'<line x1="{x_pos}" y1="0" x2="{x_pos}" y2="{grid_height}" stroke="#bdc3c7" stroke-width="1"/>\n'
    
    for y in range(env.height + 1):
        y_pos = y * cell_size
        html_content += f'<line x1="0" y1="{y_pos}" x2="{grid_width}" y2="{y_pos}" stroke="#bdc3c7" stroke-width="1"/>\n'
    
    # Draw explored nodes
    if explored and show_explored:
        for state in explored:
            if state != env.initial_state and state != env.goal_state:
                x, y = state
                x_pos = x * cell_size
                y_pos = y * cell_size
                html_content += f'<rect x="{x_pos}" y="{y_pos}" width="{cell_size}" height="{cell_size}" fill="#3498db" opacity="0.3"/>\n'
    
    # Draw obstacles
    for y in range(env.height):
        for x in range(env.width):
            if env.grid[y, x] == 1:
                x_pos = x * cell_size
                y_pos = y * cell_size
                html_content += f'<rect x="{x_pos}" y="{y_pos}" width="{cell_size}" height="{cell_size}" fill="#2c3e50"/>\n'
    
    # Draw path
    if path and show_path and len(path) > 1:
        points = " ".join([f"{s[0] * cell_size + cell_size//2},{s[1] * cell_size + cell_size//2}" for s in path])
        html_content += f'<polyline points="{points}" stroke="#2980b9" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>\n'
        
        # Draw path markers
        for i, (x, y) in enumerate(path[1:-1], 1):
            x_pos = x * cell_size + cell_size//2
            y_pos = y * cell_size + cell_size//2
            html_content += f'<circle cx="{x_pos}" cy="{y_pos}" r="3" fill="#2980b9"/>\n'
    
    # Draw start
    if env.initial_state:
        x, y = env.initial_state
        x_pos = x * cell_size
        y_pos = y * cell_size
        html_content += f'<rect x="{x_pos}" y="{y_pos}" width="{cell_size}" height="{cell_size}" fill="#e74c3c"/>\n'
        html_content += f'<text x="{x_pos + cell_size//2}" y="{y_pos + cell_size//2 + 6}" text-anchor="middle" font-size="20" fill="white">S</text>\n'
    
    # Draw goal
    if env.goal_state:
        x, y = env.goal_state
        x_pos = x * cell_size
        y_pos = y * cell_size
        html_content += f'<rect x="{x_pos}" y="{y_pos}" width="{cell_size}" height="{cell_size}" fill="#27ae60"/>\n'
        html_content += f'<text x="{x_pos + cell_size//2}" y="{y_pos + cell_size//2 + 6}" text-anchor="middle" font-size="20" fill="white">G</text>\n'
    
    # Draw current position (robot)
    if current_pos:
        x, y = current_pos
        x_pos = x * cell_size + cell_size//2
        y_pos = y * cell_size + cell_size//2
        html_content += f'<text x="{x_pos}" y="{y_pos + 10}" text-anchor="middle" font-size="28">🤖</text>\n'
    
    # Close SVG and add legend
    html_content += '</svg>\n'
    html_content += '</div>\n'
    html_content += '<div style="margin-top: 15px; font-size: 12px; color: #7f8c8d;">\n'
    html_content += '<span style="display: inline-block; margin: 0 15px;">\n'
    html_content += '<span style="display: inline-block; width: 20px; height: 20px; background-color: #e74c3c; border-radius: 2px; vertical-align: middle;"></span> Start\n'
    html_content += '</span>\n'
    html_content += '<span style="display: inline-block; margin: 0 15px;">\n'
    html_content += '<span style="display: inline-block; width: 20px; height: 20px; background-color: #27ae60; border-radius: 2px; vertical-align: middle;"></span> Goal\n'
    html_content += '</span>\n'
    html_content += '<span style="display: inline-block; margin: 0 15px;">\n'
    html_content += '<span style="display: inline-block; width: 20px; height: 20px; background-color: #2c3e50; border-radius: 2px; vertical-align: middle;"></span> Obstacle\n'
    html_content += '</span>\n'
    html_content += '<span style="display: inline-block; margin: 0 15px;">\n'
    html_content += '<span style="display: inline-block; width: 20px; height: 20px; background-color: #3498db; opacity: 0.3; border-radius: 2px; vertical-align: middle;"></span> Explored\n'
    html_content += '</span>\n'
    html_content += '</div>\n'
    html_content += '</div>\n'
    
    return html_content


def create_grid_figure(env, path=None, explored=None, current_pos=None, 
                        show_explored=True, show_path=True, title="Grid"):
    """Create a grid visualization (wrapper for HTML grid)"""
    html = create_html_grid(env, path=path, explored=explored, current_pos=current_pos,
                            show_explored=show_explored, show_path=show_path, title=title)
    st.markdown(html, unsafe_allow_html=True)


def show_final_result():
    """Mode 1: Show final result with path and explored nodes"""
    result = st.session_state.result
    env = st.session_state.env
    
    # Options
    col1, col2 = st.columns(2)
    with col1:
        show_explored = st.checkbox("Show Explored Nodes", value=True)
    with col2:
        show_path = st.checkbox("Show Path", value=True)
    
    # Create and display figure
    explored = result.get('explored', set()) if show_explored else None
    path = result['path'] if show_path else None
    
    create_grid_figure(
        env, 
        path=path, 
        explored=explored,
        show_explored=show_explored,
        show_path=show_path,
        title=f"{st.session_state.algorithm} - Final Result"
    )
    
    # Additional info
    with st.expander("📋 Path Details"):
        st.write("**Path Coordinates:**")
        path_text = " → ".join([f"({x}, {y})" for x, y in result['path']])
        st.code(path_text)
        
        if 'explored' in result:
            st.write(f"**Total Explored States:** {len(result['explored'])}")


def show_step_by_step():
    """Mode 3: Step through the exploration process"""
    result = st.session_state.result
    env = st.session_state.env
    
    st.write("🔍 **Step-by-Step Exploration**")
    st.write("*Note: This shows the final path and explored states. For live exploration, the algorithm would need to be modified to track exploration order.*")
    
    # For now, show slices of explored states
    if 'explored' in result:
        explored_list = list(result['explored'])
        
        step = st.slider(
            "Exploration Progress",
            0,
            len(explored_list),
            len(explored_list),
            help="Slide to see exploration progress"
        )
        
        # Show explored states up to current step
        explored_subset = set(explored_list[:step])
        
        create_grid_figure(
            env,
            path=result['path'],
            explored=explored_subset,
            title=f"Explored: {step}/{len(explored_list)} nodes"
        )
        
        # Show statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Nodes Explored", step)
        with col2:
            st.metric("Remaining", len(explored_list) - step)
        with col3:
            progress_pct = (step / len(explored_list) * 100) if explored_list else 0
            st.metric("Progress", f"{progress_pct:.1f}%")
    else:
        st.info("This algorithm doesn't track explored states (Tree Search)")
        create_grid_figure(
            env,
            path=result['path'],
            title=f"{st.session_state.algorithm} - Path Only"
        )


def show_path_animation():
    """Mode 2: Animate the robot moving along the path"""
    result = st.session_state.result
    env = st.session_state.env
    path = result['path']
    
    st.write("🎥 **Animated Path Playback**")
    
    # Animation controls
    col1, col2 = st.columns([1, 4])
    with col1:
        speed = st.select_slider(
            "Speed",
            options=[0.1, 0.2, 0.5, 1.0, 2.0],
            value=0.5,
            help="Animation speed in seconds per step"
        )
    with col2:
        if st.button("▶️ Play Animation", type="primary"):
            play_animation(env, path, speed)


def play_animation(env, path, speed):
    """Play the path animation"""
    # Create containers for chart and progress
    chart_container = st.container()
    progress_container = st.container()
    
    for i, pos in enumerate(path):
        # Show current progress
        progress = (i + 1) / len(path)
        
        with progress_container:
            st.progress(progress, text=f"Step {i+1}/{len(path)}")
        
        # Create figure with current position
        create_grid_figure(
            env,
            path=path[:i+2],  # Show path up to current position
            current_pos=pos,
            show_explored=False,
            title=f"Step {i+1}/{len(path)} - Position: {pos}"
        )
        
        time.sleep(speed)
    
    st.success("✅ Animation complete!")
