from functools import lru_cache

def fibonacci_iterativo(cantidad):
    """Devuelve una lista con los primeros 'cantidad' términos (rápido y eficiente)."""
    serie = []
    a, b = 0, 1
    for _ in range(cantidad):
        serie.append(a)
        a, b = b, a + b
    return serie


def fibonacci_hasta_valor(limite):
    """Devuelve los términos de la serie cuyo valor sea <= limite."""
    serie = []
    a, b = 0, 1
    while a <= limite:
        serie.append(a)
        a, b = b, a + b
    return serie


@lru_cache(maxsize=None)
def fibonacci_recursivo(n):
    """Versión recursiva con memoria (sin lru_cache sería lentísima para n grande)."""
    if n < 2:
        return n
    return fibonacci_recursivo(n - 1) + fibonacci_recursivo(n - 2)


def mostrar(serie):
    for posicion, valor in enumerate(serie, start=1):
        print(f"{posicion:>3}: {valor}")


if __name__ == "__main__":
    print("SERIE DE FIBONACCI")
    print("1. Mostrar los primeros 500 términos")
    print("2. Mostrar los términos hasta el valor 500")
    print("3. Mostrar los primeros 500 términos (versión recursiva)")
    opcion = input("Elige una opción (1/2/3): ").strip()

    if opcion == "1":
        mostrar(fibonacci_iterativo(500))
    elif opcion == "2":
        mostrar(fibonacci_hasta_valor(500))
    elif opcion == "3":
        # Se calcula en orden ascendente para no exceder el límite de recursión
        mostrar([fibonacci_recursivo(n) for n in range(500)])
    else:
        print("Opción no válida.")