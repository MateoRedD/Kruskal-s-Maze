import random
from collections import deque
import heapq

rows = 15
cols = 15
total_cells = rows * cols

def index(row, col, num_cols):
    return (row * num_cols) + col

class Wall:
    def __init__(self, cell_a, cell_b):
        self.cell_a = cell_a
        self.cell_b = cell_b

walls = []
for row in range(rows):
    for col in range(cols):
        current = index(row, col, cols)

        if col < cols - 1:
         right_neighbor = index(row, col + 1, cols)
         walls.append(Wall(current, right_neighbor))

        if row < rows - 1:
         down_neighbor = index(row + 1, col, cols)
         walls.append(Wall(current,down_neighbor))

print("candidatas generadas:", len(walls))

class UnionFind:
    def __init__(self, n):
        self.parents = list(range(n))

    def find(self, x):
        if self.parents[x] == x:
            return x
        self.parents[x] = self.find(self.parents[x])
        return self.parents[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parents[root_x] = root_y      

uf = UnionFind(total_cells)
random.shuffle(walls)
maze = []

for wall in walls:
    if uf.find(wall.cell_a) != uf.find(wall.cell_b):
        uf.union(wall.cell_a, wall.cell_b)
        maze.append(wall)

print("edges:", len(maze), "expected:", total_cells -1)

def check_connectivity(maze, total_cells):
    adjacency = {i: [] for i in range(total_cells)}
    for wall in maze:
        adjacency[wall.cell_a].append(wall.cell_b)
        adjacency[wall.cell_b].append(wall.cell_a)

    visited = set()
    stack = [0]
    while stack:
        current = stack.pop()
        if current not in visited:
            visited.add(current)
            for neighbor in adjacency[current]:
                if neighbor not in visited:
                    stack.append(neighbor)
    return len(visited) == total_cells

print("connected:", check_connectivity(maze, total_cells))

def print_maze(maze, rows, cols, start=None, goal=None):
    connected = set()
    for wall in maze:
        connected.add((wall.cell_a, wall.cell_b))
        connected.add((wall.cell_b, wall.cell_a))

    wall_char = "█" #█ #■ 
    print(wall_char * (cols * 2 + 1))

    for row in range(rows):
        row_str = wall_char
        for col in range(cols):
            current = index(row, col, cols)
            if current == start:
                row_str += "A"
            elif current == goal:
                row_str += "B"
            else:
                row_str += " "
            
            if col < cols - 1:
                neighbor = index(row, col + 1, cols)
                row_str += " " if (current, neighbor) in connected else wall_char
            else:
                row_str += wall_char
        print(row_str)

        floor_str = wall_char
        for col in range(cols):
            current = index(row, col, cols)
            if row < rows - 1:
                neighbor = index(row + 1, col, cols)
                floor_str += " " if (current, neighbor) in connected else wall_char
            else:
                floor_str += wall_char
            floor_str += wall_char
        print(floor_str)

print_maze(maze, rows, cols, start=index(0, 0, cols), goal=index(rows - 1, cols - 1, cols))

def solve_bfs(maze, start, goal, total_cells):
    adjacency = {i: [] for i in range(total_cells)}
    for wall in maze:
        adjacency[wall.cell_a].append(wall.cell_b)
        adjacency[wall.cell_b].append(wall.cell_a)

    visited = {start}
    parents = {start: None}
    queue = deque([start])
    expanded_nodes = 0

    while queue:
        current = queue.popleft()
        expanded_nodes += 1

        if current == goal:
            break

        for neighbor in adjacency[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                parents[neighbor] = current
                queue.append(neighbor)

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parents.get(node)
    path.reverse()

    return path, expanded_nodes
start = index(0, 0, cols)
goal = index(rows - 1, cols - 1, cols)
path, nodes = solve_bfs(maze, start, goal, total_cells)
print("path length:", len(path))
print("expanded nodes:", nodes)

def heuristic(a, b, cols):
    row_a, col_a = divmod(a, cols)
    row_b, col_b = divmod(b, cols)
    return abs(row_a - row_b) + abs(col_a - col_b)

def solve_astar(maze, start, goal, total_cells, cols):
    adjacency = {i: [] for i in range(total_cells)}
    for wall in maze:
        adjacency[wall.cell_a].append(wall.cell_b)
        adjacency[wall.cell_b].append(wall.cell_a)

    g_score = {start: 0}
    parents = {start: None}
    counter = 0
    heap = [(heuristic(start, goal, cols), counter, start)]
    visited = set()
    expanded_nodes = 0


    while heap:
        f, _, current = heapq.heappop(heap)

        if current in visited:
            continue
        visited.add(current)
        expanded_nodes += 1

        if current == goal:
            break

        for neighbor in adjacency[current]:
            new_g = g_score[current] + 1
            if neighbor not in g_score or new_g < g_score[neighbor]:
                g_score[neighbor] = new_g
                parents[neighbor] = current
                f_neighbor = new_g + heuristic(neighbor, goal, cols)
                counter += 1
                heapq.heappush(heap, (f_neighbor, counter, neighbor))

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parents.get(node)
    path.reverse()

    return path, expanded_nodes

path_astar, nodes_astar = solve_astar(maze, start, goal, total_cells, cols)
print("path length:", len(path_astar))
print("expanded nodes:", nodes_astar)

def generate_maze(rows,cols):
    total = rows * cols
    walls = []
    for row in range(rows):
        for col in range(cols):
            current = index(row, col, cols)
            if col < cols - 1:
                walls.append(Wall(current, index(row, col + 1, cols)))
            if row < rows - 1:
                walls.append(Wall(current, index(row + 1, col, cols)))
    
    uf = UnionFind(total)
    random.shuffle(walls)
    generated_maze = []
    for w in walls:
        if uf.find(w.cell_a) != uf.find(w.cell_b):
            uf.union(w.cell_a, w.cell_b)
            generated_maze.append(w)
    return generated_maze
N_TRIALS = 30
reductions = []
for _ in range(N_TRIALS):
    test_maze = generate_maze(rows, cols)
    start_t = index(0, 0, cols)
    goal_t = index(rows - 1, cols - 1, cols)
    _, nodes_bfs = solve_bfs(test_maze, start_t, goal_t, total_cells)
    _, nodes_astar_t = solve_astar(test_maze, start_t, goal_t, total_cells, cols)

    reduction = (nodes_bfs - nodes_astar_t) / nodes_bfs * 100
    reductions.append(reduction)
average = sum(reductions) / len(reductions)
print(f"average A* reduction over BFS: {average:.1f}%")
print(f"min: {min(reductions):.1f}% Max: {max(reductions):.1f}%" )
print("connected:", check_connectivity(maze, total_cells))



