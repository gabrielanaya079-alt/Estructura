"""Algoritmo de Dijkstra: caminos mas cortos desde un origen (pesos no negativos)."""
import heapq

INF = float("inf")


def dijkstra(grafo, origen):
    """grafo: dict {nodo: [(vecino, peso), ...]}. Devuelve (distancias, previos)."""
    dist = {n: INF for n in grafo}
    previo = {n: None for n in grafo}
    dist[origen] = 0
    cola = [(0, origen)]  # cola de prioridad (distancia, nodo)

    while cola:
        d, u = heapq.heappop(cola)
        if d > dist[u]:          # entrada obsoleta
            continue
        for v, peso in grafo[u]:
            nueva = d + peso     # relajacion de la arista (u, v)
            if nueva < dist[v]:
                dist[v] = nueva
                previo[v] = u
                heapq.heappush(cola, (nueva, v))
    return dist, previo


def reconstruir_camino(previo, destino):
    camino = []
    while destino is not None:
        camino.append(destino)
        destino = previo[destino]
    return camino[::-1]


if __name__ == "__main__":
    grafo = {
        "A": [("B", 4), ("C", 2)],
        "B": [("C", 5), ("D", 10)],
        "C": [("E", 3)],
        "D": [("F", 11)],
        "E": [("D", 4)],
        "F": [],
    }
    origen = "A"
    dist, previo = dijkstra(grafo, origen)
    print(f"Distancias minimas desde {origen}:")
    for nodo in grafo:
        camino = " -> ".join(reconstruir_camino(previo, nodo))
        print(f"  {nodo}: {dist[nodo]:>3}   camino: {camino}")
