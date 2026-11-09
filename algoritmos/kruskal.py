"""Algoritmo de Kruskal: arbol de expansion minima con Union-Find."""


class UnionFind:
    def __init__(self, nodos):
        self.padre = {n: n for n in nodos}
        self.rango = {n: 0 for n in nodos}

    def encontrar(self, x):
        if self.padre[x] != x:
            self.padre[x] = self.encontrar(self.padre[x])  # compresion de caminos
        return self.padre[x]

    def unir(self, a, b):
        ra, rb = self.encontrar(a), self.encontrar(b)
        if ra == rb:
            return False                # ya estan conectados: formaria ciclo
        if self.rango[ra] < self.rango[rb]:
            ra, rb = rb, ra
        self.padre[rb] = ra
        if self.rango[ra] == self.rango[rb]:
            self.rango[ra] += 1
        return True


def kruskal(nodos, aristas):
    """aristas: lista de (peso, u, v). Devuelve (arbol, peso_total)."""
    uf = UnionFind(nodos)
    arbol, total = [], 0
    for peso, u, v in sorted(aristas):          # orden ascendente por peso
        if uf.unir(u, v):
            arbol.append((u, v, peso))
            total += peso
    return arbol, total


if __name__ == "__main__":
    nodos = ["A", "B", "C", "D", "E", "F"]
    aristas = [
        (4, "A", "B"), (2, "A", "C"), (5, "B", "C"), (10, "B", "D"),
        (3, "C", "E"), (4, "E", "D"), (11, "D", "F"), (6, "E", "F"),
    ]
    arbol, total = kruskal(nodos, aristas)
    print("Aristas del arbol de expansion minima:")
    for u, v, p in arbol:
        print(f"  {u} - {v}  (peso {p})")
    print("Peso total:", total)
