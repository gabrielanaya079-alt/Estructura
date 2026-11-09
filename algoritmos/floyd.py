"""Algoritmo de Floyd (Floyd-Warshall): caminos mas cortos entre todos los pares."""

INF = float("inf")


def floyd(matriz):
    """matriz: lista de listas con pesos (INF si no hay arista, 0 en la diagonal).
    Devuelve (D, siguiente) para consultar distancias y reconstruir caminos."""
    n = len(matriz)
    D = [fila[:] for fila in matriz]
    sig = [[j if matriz[i][j] != INF and i != j else None for j in range(n)]
           for i in range(n)]

    for k in range(n):              # nodo intermedio permitido
        for i in range(n):
            for j in range(n):
                if D[i][k] + D[k][j] < D[i][j]:
                    D[i][j] = D[i][k] + D[k][j]
                    sig[i][j] = sig[i][k]
    return D, sig


def camino(sig, i, j):
    if sig[i][j] is None:
        return []
    ruta = [i]
    while i != j:
        i = sig[i][j]
        ruta.append(i)
    return ruta


def imprimir(M, titulo):
    print(titulo)
    for fila in M:
        print("  " + " ".join(f"{'INF' if x == INF else x:>4}" for x in fila))


if __name__ == "__main__":
    M = [
        [0,   3,   INF, 7],
        [8,   0,   2,   INF],
        [5,   INF, 0,   1],
        [2,   INF, INF, 0],
    ]
    imprimir(M, "Matriz inicial:")
    D, sig = floyd(M)
    imprimir(D, "\nMatriz de distancias minimas (Floyd):")
    print("\nCamino 0 -> 3:", " -> ".join(map(str, camino(sig, 0, 3))))
