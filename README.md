# Robot Maze Pathfinding

A pathfinding visualizer that implements and compares different search algorithms in a grid-based maze environment. Built this for a uni assignment on search algorithms.

## What it does

The app lets you create a maze, place a robot, and watch different pathfinding algorithms solve it. You can compare how BFS, DFS, UCS, and A* perform on the same maze - really helps to actually see the difference between them instead of just reading about it in a textbook.

## Algorithms

- **BFS** (Breadth-First Search) - explores level by level
- **DFS** (Depth-First Search) - goes deep first
- **UCS** (Uniform Cost Search) - finds the cheapest path
- **A*** - uses heuristics to search smarter

Each algorithm can run in tree search or graph search mode.

## Running it

Set up the environment:
```bash
python3 -m venv env/python
source env/python/bin/activate
python3 -m pip install -r requirements.txt
```

Run the visualizer:
```bash
python3 -m streamlit run app.py
```

The web interface should open in your browser. From there you can set up the maze, pick an algorithm, and watch it find the path.

## Project structure

- `robot.py` - robot movement logic
- `env.py` - maze environment
- `problem.py` - search problem definition
- `state.py` & `node.py` - state representation for search
- `app.py` - streamlit app entry point
- `web/` - UI components and visualization
