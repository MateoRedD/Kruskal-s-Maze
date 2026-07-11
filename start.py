import random

def indice(fila, columna, num_columnas):
    return (fila*num_columnas) + columna

class Pared:
    def __init__(self, celda_a, celda_b):
        self.celda_a = celda_a
        self.celda_b = celda_b



paredes = []
for fila in range(5):
    for columna in range(5):
        actual = indice(fila, columna, 5)

        if columna < 4:
            vecino_derecha = indice(fila, columna + 1, 5)
            paredes.append(Pared(actual, vecino_derecha))

        if fila < 4:
            vecino_abajo = indice(fila + 1, columna, 5)
            paredes.append(Pared(actual, vecino_abajo))
print(len(paredes))


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

uf = UnionFind(25)
random.shuffle(paredes)
maze = []

for pared in paredes:
    if uf.find(pared.celda_a) != uf.find(pared.celda_b):
        uf.union(pared.celda_a, pared.celda_b)
        maze.append(pared)

print(len(maze))

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
print(verificar_conectividad(maze, 25))

def imprimir_maze(maze, filas, columnas, inicio=None, meta=None):
    conectados = set()
    for pared in maze:
        conectados.add((pared.celda_a, pared.celda_b))
        conectados.add((pared.celda_b, pared.celda_a))
    
    pared = "#" ##■

    print(pared * (columnas * 2 + 1))

    for fila in range(filas):
        fila_str = pared
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
                fila_str += " " if (actual, vecino) in conectados else pared
            else:
                fila_str += pared
        print(fila_str)

        piso_str = pared
        for columba in range(columnas):
            actual = indice(fila, columna, columnas)
            if fila < filas - 1:
                vecino = indice(fila + 1, columna, columnas)
                piso_str += " " if (actual, vecino) in conectados else pared
            else:
                piso_str += pared
            piso_str += pared
        print(piso_str)

imprimir_maze(maze, 5, 5, inicio=indice(0, 0, 5), meta=indice(4, 4, 5))

    