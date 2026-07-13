import pygame
import sys
from collections import deque
import heapq

from start import generate_maze, index, rows, cols, total_cells

CELL_SIZE = 30
MARGIN_TOP = 60
WIDTH = cols * CELL_SIZE
HEIGHT = rows * CELL_SIZE + MARGIN_TOP

COLOR_BG = (255, 255, 255)
COLOR_WALL = (30, 30, 30)
COLOR_START = (46, 204, 113)
COLOR_GOAL = (231, 76, 60)
COLOR_BFS_VISITED = (174 , 214, 241)
COLOR_ASTAR_VISITED = (250, 215, 160)
COLOR_PATH = (241, 196, 15)
COLOR_TEXT = (20, 20, 20)

def cell_react(row, col):
    return pygame.Rect(col * CELL_SIZE, MARGIN_TOP + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)

def draw_maze(screen, maze):
    connected = set()
    for wall in maze:
        connected.add((wall.cell_a, wall.cell_b))
        connected.add((wall.cell_b, wall.cell_a))

    for row in range(rows):
        for col in range(cols):
            current = index(row, col, cols)
            x = col * CELL_SIZE
            y = MARGIN_TOP + row * CELL_SIZE

            if row == 0:
                pygame.draw.line(screen, COLOR_WALL, (x, y), (x + CELL_SIZE, y), 3)
            if col == 0:
                pygame.draw.line(screen, COLOR_WALL, (x, y), (x, y + CELL_SIZE), 3)

            right_neighbor = index(row, col + 1, cols) if col < cols - 1 else None
            if right_neighbor is None or (current, right_neighbor) not in connected:
                pygame.draw.line(screen, COLOR_WALL, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 3)

            bottom_neighbor = index(row + 1, col, cols) if row < rows - 1 else None
            if bottom_neighbor is None or (current, bottom_neighbor) not in connected:
                pygame.draw.line(screen, COLOR_WALL, (x , y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 3)

def solve_bfs_animated(maze, start, goal, total_cells):
    adjacency = {i: [] for i in range (total_cells)}
    for wall in maze:
        adjacency[wall.cell_a].append(wall.cell_b)
        adjacency[wall.cell_b].append(wall.cell_a)

    visited = {start}
    parents = {start: None}
    queue = deque([start])

    while queue:
        current = queue.popleft()
        yield ("visit", current)

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
    yield ("done", path)

def heuristic(a, b, cols):
    row_a, col_a = divmod(a, cols)
    row_b, col_b = divmod(b, cols)
    return abs(row_a - row_b) + abs(col_a - col_b)

def solve_astar_animated(maze, start, goal, total_cells, cols):
    adjacency = {i: [] for i in range(total_cells)}
    for wall in maze:
        adjacency[wall.cell_a].append(wall.cell_b)
        adjacency[wall.cell_b].append(wall.cell_a)

    g_score = {start: 0}
    parents = {start: None}
    counter = 0
    heap = [(heuristic(start, goal, cols), counter, start)]
    visited = set()

    while heap:
        f, _, current = heapq.heappop(heap)

        if current in visited:
            continue
        visited.add(current)
        yield ("visit", current)

        if current == goal:
            break

        for neighbor in adjacency[current]:
            new_g = g_score[current] + 1
            if neighbor not in g_score or new_g < g_score[neighbor]:
                g_score[neighbor] = new_g
                parents[neighbor] = current
                f_neighbor = new_g + heuristic(neighbor, goal, cols)
                counter +=1
                heapq.heappush(heap, (f_neighbor, counter, neighbor))

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
        yield ("done", path)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Kruskal's Maze")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    maze = generate_maze(rows, cols)
    start = index(0 , 0, cols)
    goal = index(rows - 1, cols - 1, cols)

    visited_cells = {}
    final_path = []
    active_gen = None
    active_algo = ""
    expanded_count = 0
    status_text = "SPACE = BFS  A = A*  R = new maze"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    maze = generate_maze(rows, cols)
                    visited_cells = {}
                    final_path = []
                    active_gen = None
                    status_text =  "SPACE = BFS  A = A*  R = new maze"
                elif event.key == pygame.K_SPACE:
                    visited_cells = {}
                    final_path = []
                    active_gen = solve_bfs_animated(maze, start, goal, total_cells)
                    active_algo = "BFS"
                    expanded_count = 0
                elif event.key == pygame.K_a:
                    visited_cells = {}
                    final_path = []
                    active_gen = solve_astar_animated(maze, start, goal, total_cells, cols)
                    active_algo = "A*"
                    expanded_count = 0
        if active_gen is not None:
            for _ in range(3):
                try:
                    kind, data = next(active_gen)
                except StopIteration:
                    active_gen = None
                    break
                if kind == "visit":
                    color = COLOR_BFS_VISITED if active_algo == "BFS" else COLOR_ASTAR_VISITED
                    visited_cells[data] = color
                    expanded_count += 1
                elif kind == "done":
                    final_path = data
                    active_gen = None
                    status_text = f"{active_algo}: {expanded_count} nodos expendidos, camino de {len(final_path)}"
                    break

        screen.fill(COLOR_BG)

        text_surface = font.render(status_text, True, COLOR_TEXT)
        screen.blit(text_surface, (10, 15))

        for cell, color in visited_cells.items():
            row, col = divmod(cell, cols)
            pygame.draw.rect(screen, COLOR_PATH, cell_react(row, col))

        draw_maze(screen, maze)

        start_row, start_col = divmod(start, cols)
        goal_row, goal_col = divmod(goal, cols)
        pygame.draw.rect(screen, COLOR_START, cell_react(start_row, start_col))
        pygame.draw.rect(screen, COLOR_GOAL, cell_react(goal_row, goal_col))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
