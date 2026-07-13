import pygame
import sys
from collections import deque
import heapq

from start import generate_maze, index, rows, cols, total_cells

CELL_SIZE = 30
MARGIN_TOP = 70
WIDTH = cols * CELL_SIZE
HEIGHT = rows * CELL_SIZE + MARGIN_TOP

COLOR_BG = (255, 255, 255)
COLOR_WALL = (30, 30, 30)
COLOR_START = (46, 204, 113)
COLOR_GOAL = (231, 76, 60)
COLOR_BFS_LINE = (52, 152, 219)
COLOR_ASTAR_LINE = (192, 57, 43)
COLOR_PATH = (241, 196, 15)
COLOR_TEXT = (20, 20, 20)
COLOR_DIVIDER = (210, 210, 210)

CONTROLS_TEXT = "SPACE = BFS   A = A*   R = nuevo maze"
EXPLORE_WIDTH = 3
PATH_WIDTH = 5


def cell_rect(row, col):
    return pygame.Rect(col * CELL_SIZE, MARGIN_TOP + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)


def cell_center(cell):
    row, col = divmod(cell, cols)
    return cell_rect(row, col).center


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
                pygame.draw.line(screen, COLOR_WALL, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 3)


def draw_exploration(screen, edges, color):
    for parent, current in edges:
        p_center = cell_center(parent)
        c_center = cell_center(current)
        pygame.draw.line(screen, color, p_center, c_center, EXPLORE_WIDTH)
        pygame.draw.circle(screen, color, c_center, EXPLORE_WIDTH // 2)


def draw_path(screen, final_path):
    if len(final_path) < 2:
        return
    points = [cell_center(cell) for cell in final_path]
    pygame.draw.lines(screen, COLOR_PATH, False, points, PATH_WIDTH)
    for point in points:
        pygame.draw.circle(screen, COLOR_PATH, point, PATH_WIDTH // 2)


def solve_bfs_animated(maze, start, goal, total_cells):
    adjacency = {i: [] for i in range(total_cells)}
    for wall in maze:
        adjacency[wall.cell_a].append(wall.cell_b)
        adjacency[wall.cell_b].append(wall.cell_a)

    visited = {start}
    parents = {start: None}
    queue = deque([start])

    while queue:
        current = queue.popleft()
        yield ("visit", current, parents.get(current))

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
    yield ("done", path, None)


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
        yield ("visit", current, parents.get(current))

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
    yield ("done", path, None)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Kruskal's Maze")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    maze = generate_maze(rows, cols)
    start = index(0, 0, cols)
    goal = index(rows - 1, cols - 1, cols)

    exploration_edges = []
    final_path = []
    active_gen = None
    active_algo = ""
    active_color = COLOR_BFS_LINE
    expanded_count = 0
    result_text = ""

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    maze = generate_maze(rows, cols)
                    exploration_edges = []
                    final_path = []
                    active_gen = None
                    result_text = ""
                elif event.key == pygame.K_SPACE:
                    exploration_edges = []
                    final_path = []
                    active_gen = solve_bfs_animated(maze, start, goal, total_cells)
                    active_algo = "BFS"
                    active_color = COLOR_BFS_LINE
                    expanded_count = 0
                    result_text = ""
                elif event.key == pygame.K_a:
                    exploration_edges = []
                    final_path = []
                    active_gen = solve_astar_animated(maze, start, goal, total_cells, cols)
                    active_algo = "A*"
                    active_color = COLOR_ASTAR_LINE
                    expanded_count = 0
                    result_text = ""

        if active_gen is not None:
            for _ in range(3):
                try:
                    kind, a, b = next(active_gen)
                except StopIteration:
                    active_gen = None
                    break
                if kind == "visit":
                    current, parent = a, b
                    if parent is not None:
                        exploration_edges.append((parent, current))
                    expanded_count += 1
                elif kind == "done":
                    final_path = a
                    active_gen = None
                    result_text = f"{active_algo}: {expanded_count} nodos expandidos, camino de {len(final_path)}"
                    break

        screen.fill(COLOR_BG)

        controls_surface = font.render(CONTROLS_TEXT, True, COLOR_TEXT)
        screen.blit(controls_surface, (10, 12))

        if result_text:
            result_surface = font.render(result_text, True, COLOR_TEXT)
            screen.blit(result_surface, (10, 38))

        pygame.draw.line(screen, COLOR_DIVIDER, (0, MARGIN_TOP - 1), (WIDTH, MARGIN_TOP - 1), 1)

        draw_exploration(screen, exploration_edges, active_color)
        draw_path(screen, final_path)
        draw_maze(screen, maze)

        start_row, start_col = divmod(start, cols)
        goal_row, goal_col = divmod(goal, cols)
        pygame.draw.rect(screen, COLOR_START, cell_rect(start_row, start_col))
        pygame.draw.rect(screen, COLOR_GOAL, cell_rect(goal_row, goal_col))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()