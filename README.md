# Robot Maze Pathfinding

A pathfinding visualizer that implements and compares different search algorithms in a grid-based maze environment. Built this for a uni assignment on search algorithms.

## What it does

The app lets you create a maze, place a robot, and watch different pathfinding algorithms solve it. You can compare how BFS, DFS, UCS, and A* perform on the same maze - really helps to actually see the difference between them instead of just reading about it in a textbook.

## Algorithms

- **BFS** (Breadth-First Search) - explores level by level
- **DFS** (Depth-First Search) - goes deep first
- **UCS** (Uniform Cost Search) - finds the cheapest path
- **A*** - uses heuristics to search smarter

## Live Demo

Check out the live app at [https://robotmaze.ianshade.com/](https://robotmaze.ianshade.com/)


## Running it

### macOS/Linux

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

### Windows

Set up the environment:
```bash
python -m venv env/python
env\python\Scripts\activate
python -m pip install -r requirements.txt
```

Run the visualizer:
```bash
python -m streamlit run app.py
```

The web interface should open in your browser automatically. From there you can set up the maze, pick an algorithm, and watch it find the path.



## Project structure

- `robot.py` - robot movement logic
- `environment.py` - maze environment setup
- `problem.py` - search problem definition
- `search_algorithms.py` - implementation of BFS, DFS, UCS, and A* algorithms
- `state.py` & `node.py` - state representation for search
- `app.py` - Streamlit app entry point
- `web/` - UI components and visualization

## Contributors

- Zaema Dar
- Karyme Nahle Acosta
- Ihsan Abourshaid
