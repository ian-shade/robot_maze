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

## Deployment

### Deploy to Render

1. Fork/push this repository to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" and select "Web Service"
4. Connect your GitHub repository
5. Render will automatically detect the `render.yaml` configuration
6. Click "Create Web Service"

Your app will be live at `https://robot-maze-pathfinding.onrender.com` (or your custom URL)

### Deploy to Streamlit Community Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository and set:
   - Main file path: `app.py`
   - Python version: 3.11
6. Click "Deploy"

### Deploy to Cloudflare Pages (with Workers)

For Cloudflare, you'll need to set up a Python worker or use a compatible framework adapter. This is more complex for Streamlit apps - Render or Streamlit Cloud are recommended.

## Project structure

- `robot.py` - robot movement logic
- `env.py` - maze environment
- `problem.py` - search problem definition
- `state.py` & `node.py` - state representation for search
- `app.py` - streamlit app entry point
- `web/` - UI components and visualization
