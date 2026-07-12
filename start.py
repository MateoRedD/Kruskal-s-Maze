import random
from collections import deque
import heapq

filas = 15
columnas = 15
total_celdas = filas * columnas

def indice(fila, columna, num_columnas):
    return (fila * num_columnas) + columna

class pared:
    def __init__(self, celda_a, celda_b):
        self.celda_a = celda_a
        self.celda_b = celda_b

paredes = []
for fila in range(filas):
    for columna in range(columnas):
        actual = indice(fila, columna, columnas)

        if columna < columnas - 1:
            vecino_derecha = indice(fila, columna + 1, columnas)
            paredes.append(pared(actual, vecino_derecha))

        if fila < filas - 1:
            vecino_abajo = indice(fila + 1, columna, columnas)
            paredes.append(pared(actual, vecino_abajo))

class UnionFind:
    def __init__(self, n):
        self.padres = list(range(n))

    def find(self, x):
        if self.padres[x] == x:
            return x
        self.padres[x] = self.find(self.padres[x])
        return self.padres[x]
    
    def union(self, x, y):
        raiz_x = self.find(x)
        raiz_y = self.find(y)
        if raiz_x != raiz_y:
            self.padres[raiz_x] = raiz_y

uf = UnionFind(total_celdas)
random.shuffle(paredes)
maze = []

for pared in paredes:
    if uf.find(pared.celda_a) != uf.find(pared.celda_b):
        uf.union(pared.celda_a, pared.celda_b)
        maze.append(pared)

print("aristas:", len(maze), "esperado:", total_celdas - 1)

def verificar_conectividad(maze, total_celdas):
    adyacencia = {i: [] for i in range(total_celdas)}
    for pared in maze:
        adyacencia[pared.celda_a].append(pared.celda_b)
        adyacencia[pared.celda_b].append(pared.celda_a)

    visitados = set()
    pila = [0]
    while pila:
        actual = pila.pop()
        if actual not in visitados:
            visitados.add(actual)
            for vecino in adyacencia[actual]:
                if vecino not in visitados:
                    pila.append(vecino)
    return len(visitados) == total_celdas

print("conectado:", verificar_conectividad(maze, total_celdas))

def imprimir_maze(maze, filas, columnas, inicio=None, meta=None):
    conectados = set()
    for pared in maze:
        conectados.add((pared.celda_a, pared.celda_b))
        conectados.add((pared.celda_b, pared.celda_a))
    
    pared_char = "▉" #■ #▉
    print(pared_char * (columnas * 2 + 1))

    for fila in range(filas):
        fila_str = pared_char
        for columna in range(columnas):
            actual = indice(fila, columna, columnas)
            if actual == inicio:
                fila_str += "A"
            elif actual == meta:
                fila_str += "B"
            else:
                fila_str += " "
            
            if columna < columnas - 1:
                vecino = indice(fila, columna + 1, columnas)
                fila_str += " " if (actual, vecino) in conectados else pared_char
            else:
                fila_str += pared_char
        print(fila_str)

        piso_str = pared_char
        for columna in range(columnas):
            actual = indice(fila, columna, columnas)
            if fila < filas - 1:
                vecino = indice(fila + 1, columna, columnas)
                piso_str += " " if (actual, vecino) in conectados else pared_char
            else:
                piso_str += pared_char
            piso_str += pared_char
        print(piso_str)

imprimir_maze(maze, filas, columnas, inicio=indice(0, 0, columnas), meta=indice(filas - 1, columnas - 1, columnas))

def resolver_bfs(maze, inicio, meta, total_celdas):
    adyacencia = {i: [] for i in range(total_celdas)}
    for pared in maze:
        adyacencia[pared.celda_a].append(pared.celda_b)
        adyacencia[pared.celda_b].append(pared.celda_a)

    visitados = {inicio}
    padres = {inicio: None}
    cola = deque([inicio])
    nodos_expandidos = 0

    while cola:
        actual = cola.popleft()
        nodos_expandidos += 1

        if actual == meta:
            break

        for vecino in adyacencia[actual]:
            if vecino not in visitados:
                visitados.add(vecino)
                padres[vecino] = actual
                cola.append(vecino)

    camino = []
    nodo = meta
    while nodo is not None:
        camino.append(nodo)
        nodo = padres.get(nodo)
    camino.reverse()

    return camino, nodos_expandidos
inicio = indice(0 , 0, columnas)
meta = indice(filas - 1, columna - 1, columnas)
camino, nodos = resolver_bfs(maze, inicio, meta, total_celdas)
print("largo del camino:", len(camino))
print("nodos expandidos", nodos)

def heuristica(a, b, columnas):
    fila_a, col_a = divmod(a , columnas)
    fila_b, col_b = divmod(b, columnas)
    return abs(fila_a - fila_b) + abs(total_celdas)

def resolver_astar(maze, inicio, meta, total_celdas, columnas):
    adyacencia = {i: [] for i in range(total_celdas)}
    for pared in maze:
        adyacencia[pared.celda_a].append(pared.celda_b)
        adyacencia[pared.celda_b].append(pared.celda_a)
    
    g_score = {inicio: 0}
    padres = {inicio: None}
    contador = 0
    heap = [(heuristica(inicio, meta, columnas), contador, inicio)]
    visitados = set()
    nodos_expandidos = 0
    while heap:
        f, _, actual = heapq.heappop(heap)

        if actual in visitados:
            continue
        visitados.add(actual)
        nodos_expandidos += 1

        if actual == meta:
            break

        for vecino in adyacencia[actual]:
            nuevo_g = g_score[actual] + 1
            if vecino not in g_score or nuevo_g < g_score[vecino]:
                g_score[vecino] = nuevo_g
                padres[vecino] = actual
                f_vecino = nuevo_g + heuristica(vecino, meta, columnas)
                contador += 1
                heapq.heappush(heap, (f_vecino, contador, vecino))
    camino = []
    nodo = meta
    while nodo is not None:
        camino.append(nodo)
        nodo = padres.get(nodo)
    camino.reverse()

    return camino, nodos_expandidos
camino_astar, nodo_astar = resolver_astar(maze, inicio, meta, total_celdas, columnas)
print("largo del camino:", len(camino_astar))
print("nodos expandidos:", nodo_astar)

def generar_maze(filas, columnas):
    total = filas * columnas
    paredes = []
    for fila in range (filas):
        for columna in range(columnas):
            actual = indice(fila, columna, columnas)
            if columna < columnas - 1:
                paredes.append(pared(actual, indice(fila, columna + 1, columnas)))
            if fila < filas - 1:
                paredes.append(pared(actual, indice(fila + 1, columna, columnas)))
            
    uf = UnionFind(total)
    random.shuffle(paredes)
    maze_generado = []
    for p in paredes:
        if uf.find(pared.celda_a) != uf.find(pared.celda_b):
            uf.union(pared.celda_a, pared.celda_b)
            maze_generado.append(pared)
            return maze_generado

N_TRIALS = 30
reducciones = []
for _ in range(N_TRIALS):
    maze_prueba = generar_maze(filas, columnas)
    inicio = indice(0, 0, columnas)
    meta = indice(filas - 1, columnas - 1, columnas)
    _, nodos_bfs = resolver_bfs(maze_prueba, inicio, meta, total_celdas)
    _, nodo_astar = resolver_astar(maze_prueba, inicio, meta, total_celdas, columnas)

    reduccion = (nodos_bfs - nodo_astar) / nodos_bfs * 100
    reducciones.append(reduccion)

promedio = sum(reducciones) / len(reducciones)
print(f"reduccion promedio de A* sobre BFS: {promedio:.1f}%")
print(f"Minimo: {min(reducciones):.1f}% Maximo: {max(reducciones):.1f}%")

