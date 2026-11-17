def ordenar_insercion(numeros):
    arreglo = list(numeros)

    # El primer elemento ya forma una sección ordenada de tamaño uno.
    for indice in range(1, len(arreglo)):
        valor = arreglo[indice]
        posicion = indice

        while posicion > 0 and arreglo[posicion - 1] > valor:
            arreglo[posicion] = arreglo[posicion - 1]
            posicion -= 1

        arreglo[posicion] = valor
        print(f"Pasada {indice} | valor {valor}: {arreglo}")

    return arreglo


if __name__ == "__main__":
    datos = [54, 26, 93, 17, 77, 31, 44, 55, 20]
    print("Lista original:", datos)
    print("Lista ordenada:", ordenar_insercion(datos))
