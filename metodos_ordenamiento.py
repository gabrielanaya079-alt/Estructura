


def shell_sort(numeros):
    """Ordena con inserciones separadas por saltos cada vez menores."""
    salto = len(numeros) // 2
    while salto > 0:
        for indice in range(salto, len(numeros)):
            valor = numeros[indice]
            posicion = indice
            while posicion >= salto and numeros[posicion - salto] > valor:
                numeros[posicion] = numeros[posicion - salto]
                posicion -= salto
            numeros[posicion] = valor
        salto //= 2


def particionar(numeros, inicio, fin):
    """Coloca el último elemento como pivote en su posición final."""
    pivote = numeros[fin]
    frontera = inicio
    for indice in range(inicio, fin):
        if numeros[indice] < pivote:
            numeros[frontera], numeros[indice] = numeros[indice], numeros[frontera]
            frontera += 1
    numeros[frontera], numeros[fin] = numeros[fin], numeros[frontera]
    return frontera


def quick_sort(numeros):
    """Ordena los rangos mediante una pila de particiones pendientes."""
    pendientes = [(0, len(numeros) - 1)]
    while pendientes:
        inicio, fin = pendientes.pop()
        if inicio < fin:
            pivote = particionar(numeros, inicio, fin)
            if inicio < pivote - 1:
                pendientes.append((inicio, pivote - 1))
            if pivote + 1 < fin:
                pendientes.append((pivote + 1, fin))


def hundir(numeros, raiz, limite):
    """Restaura el montículo máximo en el rango anterior a limite."""
    while 2 * raiz + 1 < limite:
        mayor = 2 * raiz + 1
        derecho = mayor + 1
        if derecho < limite and numeros[derecho] > numeros[mayor]:
            mayor = derecho
        if numeros[raiz] >= numeros[mayor]:
            break
        numeros[raiz], numeros[mayor] = numeros[mayor], numeros[raiz]
        raiz = mayor


def heap_sort(numeros):
    """Construye un montículo máximo y coloca cada máximo al final."""
    cantidad = len(numeros)
    for raiz in range(cantidad // 2 - 1, -1, -1):
        hundir(numeros, raiz, cantidad)

    for fin in range(cantidad - 1, 0, -1):
        numeros[0], numeros[fin] = numeros[fin], numeros[0]
        hundir(numeros, 0, fin)


def radix_sort(numeros):
    """Ordena por dígitos y aplica un desplazamiento para admitir negativos."""
    if not numeros:
        return

    desplazamiento = max(0, -min(numeros))
    maximo = max(numeros) + desplazamiento
    posicion_decimal = 1
    while maximo // posicion_decimal > 0:
        grupos = [[] for _ in range(10)]
        for numero in numeros:
            digito = ((numero + desplazamiento) // posicion_decimal) % 10
            grupos[digito].append(numero)

        # Conservamos el orden de llegada dentro de cada grupo.
        numeros[:] = [numero for grupo in grupos for numero in grupo]
        posicion_decimal *= 10


def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Entrada inválida. Escribe un número entero.")


def main():
    metodos = {
        "1": ("ShellSort", shell_sort),
        "2": ("Quicksort", quick_sort),
        "3": ("Heapsort", heap_sort),
        "4": ("Radix Sort", radix_sort),
    }

    while True:
        print("\n=== MENÚ DE ORDENAMIENTO ===")
        for opcion, (nombre, _) in metodos.items():
            print(f"{opcion}. {nombre}")
        print("5. Salir")

        opcion = input("Elige una opción: ").strip()
        if opcion == "5":
            print("Programa finalizado.")
            break
        if opcion not in metodos:
            print("Opción inválida. Elige del 1 al 5.")
            continue

        cantidad = leer_entero("¿Cuántos números quieres ordenar? ")
        while cantidad <= 0:
            print("La cantidad debe ser mayor que cero.")
            cantidad = leer_entero("¿Cuántos números quieres ordenar? ")

        numeros = []
        for indice in range(cantidad):
            numeros.append(leer_entero(f"Número {indice + 1}: "))

        nombre, ordenar = metodos[opcion]
        print(f"Lista original: {numeros}")
        ordenar(numeros)
        print(f"Lista ordenada con {nombre}: {numeros}")


if __name__ == "__main__":
    main()
