import random

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
