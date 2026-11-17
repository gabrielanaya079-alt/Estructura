from itertools import permutations
from statistics import mean


def ordenar_burbuja(numeros):
    arreglo = list(numeros)
    intercambios = 0

    for limite in range(len(arreglo) - 1, 0, -1):
        for posicion in range(limite):
            if arreglo[posicion] > arreglo[posicion + 1]:
                arreglo[posicion], arreglo[posicion + 1] = (
                    arreglo[posicion + 1], arreglo[posicion]
                )
                intercambios += 1

    return arreglo, intercambios


if __name__ == "__main__":
    datos = [3, 2, 4, 1]
    ordenados, intercambios = ordenar_burbuja(datos)
    print("Lista original:", datos)
    print("Lista ordenada:", ordenados)
    print("Intercambios del ejemplo:", intercambios)

    # Cada permutación aparece una vez, así que todas pesan lo mismo.
    conteos = [
        ordenar_burbuja(orden)[1] for orden in permutations(ordenados)
    ]
    print(f"Mejor caso: {min(conteos)} intercambios")
    print(f"Peor caso: {max(conteos)} intercambios")
    print(f"Promedio de las {len(conteos)} permutaciones: {mean(conteos)}")
