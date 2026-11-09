"""Algoritmo de Warshall: cerradura transitiva (alcanzabilidad) de un grafo."""


def warshall(adyacencia):
    """adyacencia: matriz de 0/1. Devuelve la matriz de alcanzabilidad."""
    n = len(adyacencia)
    R = [fila[:] for fila in adyacencia]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                R[i][j] = R[i][j] or (R[i][k] and R[k][j])
    return [[int(x) for x in fila] for fila in R]


def imprimir(M, titulo):
    print(titulo)
    for fila in M:
        print("  " + " ".join(map(str, fila)))


if __name__ == "__main__":
    A = [
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 0],
    ]
    imprimir(A, "Matriz de adyacencia:")
    R = warshall(A)
    imprimir(R, "\nCerradura transitiva (Warshall):")
    for i in range(len(R)):
        alc = [j for j in range(len(R)) if R[i][j]]
        print(f"  Desde {i} se llega a: {alc}")
