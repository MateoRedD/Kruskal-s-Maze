# Kruskal's Maze

A maze generator and solver built to visualize, in real time, the difference between **Breadth-First Search (BFS)** and **A\*** — two classic pathfinding algorithms with very different strategies for exploring a graph.

![Python](https://img.shields.io/badge/python-3.x-blue) ![Pygame](https://img.shields.io/badge/pygame--ce-visualization-orange)

## What is BFS?

Breadth-First Search is an **uninformed** search algorithm. It explores a graph level by level, expanding outward from the start node in every direction equally, with no notion of where the goal is. It's guaranteed to find the shortest path (when all edges cost the same), but it pays for that guarantee by visiting far more nodes than necessary.

## What is A*?

A* is an **informed** search algorithm. It uses a heuristic — in this project, Manhattan distance — to estimate how far each node is from the goal, and prioritizes exploring nodes that seem closer to it. As long as the heuristic never overestimates the real distance (an "admissible" heuristic), A* still guarantees the shortest path, but typically expands far fewer nodes than BFS to get there.

## Why compare them here?

Because the maze is generated as a **perfect maze** (a spanning tree, via Kruskal's algorithm), there is always exactly **one possible path** between any two cells — no shortcuts, no alternate routes. That means both algorithms always agree on path length; the real, measurable difference is in **how many nodes each one had to expand** to find it. That's the metric this project tracks, instead of wall-clock time, which is too noisy to be a fair comparison at this scale.

## Features

- **Maze generation** — Kruskal's algorithm using a Union-Find (Disjoint Set Union) structure with path compression, guaranteeing a valid spanning tree (no cycles, fully connected).
- **BFS solver** — classic FIFO queue-based search, tracking expanded node count.
- **A\* solver** — min-heap based search with Manhattan distance heuristic and tie-breaking counter.
- **Correctness checks** — edge count validation (`V - 1`) and full connectivity check (DFS) after every generation.
- **Real-time animated visualization** (pygame) — watch BFS and A* explore the maze live, with the exploration tree drawn as thin branching lines and the final path highlighted separately.
- **Statistical comparison** — runs both algorithms across many randomly generated mazes and reports the average, minimum, and maximum reduction in expanded nodes that A* achieves over BFS.

## Project structure

```
start.py       # Core logic: maze generation, BFS/A* solvers, ASCII output, statistical comparison
visualize.py   # Pygame-based real-time visualization
```

## Installation

```bash
pip install pygame-ce
```

> Note: this project uses `pygame-ce` (Community Edition) instead of the original `pygame` package, since `pygame-ce` maintains up-to-date support for recent Python versions. The API is identical — `import pygame` works the same either way.

## Usage

**Console mode** — generates a maze, prints it as ASCII art, runs both solvers once, and runs a 30-trial statistical comparison:

```bash
python start.py
```

**Visual mode** — opens an interactive pygame window:

```bash
python visualize.py
```

| Key | Action |
|-----|--------|
| `SPACE` | Run BFS on the current maze |
| `A` | Run A* on the current maze |
| `R` | Generate a new random maze |

## Example results

Across 30 randomly generated 15×15 mazes, A* consistently expands fewer nodes than BFS to find the same (only possible) path:

```
average A* reduction over BFS: 40.3%
min: 12.7%   max: 66.9%
```

The variance between trials reflects how much a given maze's shape favors a heuristic-guided search — mazes with long, direct corridors tend to favor A* more than mazes with dense, short branching.

## How it works, briefly

- **Grid → graph**: each cell is a node, indexed as `row * num_cols + col`.
- **Kruskal's algorithm** shuffles all candidate walls and, for each one, uses Union-Find to check whether the two cells it connects are already in the same group. If not, the wall is knocked down and the groups are merged. This guarantees a spanning tree with no cycles.
- **BFS** expands nodes in the order they were discovered, using a FIFO queue.
- **A\*** expands nodes based on `f(n) = g(n) + h(n)`, where `g(n)` is the real cost so far and `h(n)` is the Manhattan distance estimate to the goal — using a min-heap so the most promising node is always expanded next.

## Author

Built as a personal algorithms project to practice graph theory, search algorithms, and complexity analysis from the ground up.
