def ordenar_seleccion(numeros):
    arreglo = list(numeros)

    for inicio in range(len(arreglo) - 1):
        posicion_menor = inicio
        for posicion in range(inicio + 1, len(arreglo)):
            if arreglo[posicion] < arreglo[posicion_menor]:
                posicion_menor = posicion

        menor = arreglo[posicion_menor]
        if posicion_menor != inicio:
            arreglo[inicio], arreglo[posicion_menor] = menor, arreglo[inicio]

        print(f"Pasada {inicio + 1} | mínimo {menor}: {arreglo}")

    return arreglo


if __name__ == "__main__":
    datos = [64, 25, 12, 22, 11]
    print("Lista original:", datos)
    print("Lista ordenada:", ordenar_seleccion(datos))
