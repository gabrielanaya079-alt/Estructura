from MyLinkedList import ListaEnlazada


def pedir_entero(mensaje, minimo, maximo):
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print(f"Ingresa un número entre {minimo} y {maximo}.")
        except ValueError:
            print("Entrada no válida, ingresa un número entero.")


def menu_agregar(lista):
    info = input("\nDato a almacenar en el nodo: ")

    print("¿Dónde quieres agregar el nodo?")
    print("  1. Al inicio")
    print("  2. En medio")
    print("  3. Al final")
    opcion = pedir_entero("Opción: ", 1, 3)

    if opcion == 1:
        lista.agregar_inicio(info)
    elif opcion == 3:
        if not lista.agregar_final(info):
            print("No se puede agregar al final: la lista tiene un ciclo "
                  "y no existe un último nodo.")
            return
    else:
        n = lista.longitud()
        if n < 2:
            print("Para insertar en medio se necesitan al menos 2 nodos. "
                  "Se agregará al inicio.")
            lista.agregar_inicio(info)
        else:
            pos = pedir_entero(f"Posición (2 a {n}): ", 2, n)
            lista.agregar_medio(info, pos)
    print("Nodo agregado.")


def menu_eliminar(lista):
    if lista.esta_vacia():
        print("\nLa lista está vacía, no hay nada que eliminar.")
        return

    print("\n¿Cómo quieres eliminar el nodo?")
    print("  1. Por posición")
    print("  2. Por dato")
    opcion = pedir_entero("Opción: ", 1, 2)

    if opcion == 1:
        n = lista.longitud()
        pos = pedir_entero(f"Posición a eliminar (1 a {n}): ", 1, n)
        lista.eliminar_por_posicion(pos)
        print(f"Se eliminó el nodo en la posición {pos}.")
    else:
        if lista.tiene_ciclo():
            print("No se puede eliminar por dato mientras la lista tenga un ciclo. "
                  "Usa la eliminación por posición.")
            return
        dato = input("Dato a eliminar: ")
        if lista.eliminar_por_dato(dato):
            print(f"Se eliminó el nodo con el dato '{dato}'.")
        else:
            print(f"El dato '{dato}' no se encontró en la lista.")


def menu_buscar(lista):
    if lista.esta_vacia():
        print("\nLa lista está vacía, no hay nada que buscar.")
        return

    dato = input("\nDato a buscar: ")
    posicion = lista.buscar(dato)
    if posicion is None:
        print(f"El dato '{dato}' no se encontró en la lista.")
    else:
        print(f"El dato '{dato}' se encontró en la posición {posicion}.")


def pedir_archivo():
    nombre = input("Nombre del archivo (Enter para 'lista.txt'): ").strip()
    return nombre if nombre else "lista.txt"


def menu_guardar(lista):
    if lista.esta_vacia():
        print("\nLa lista está vacía, no hay nada que guardar.")
        return
    archivo = pedir_archivo()
    try:
        total = lista.guardar(archivo)
        print(f"Se guardaron {total} nodo(s) en '{archivo}'.")
    except OSError as error:
        print(f"No se pudo guardar el archivo: {error}")


def menu_cargar(lista):
    archivo = pedir_archivo()
    if not lista.esta_vacia():
        print("Esto reemplazará la lista actual.")
        if pedir_entero("¿Continuar? Sí: 1, No: 0: ", 0, 1) == 0:
            print("Operación cancelada.")
            return
    try:
        total = lista.cargar(archivo)
        print(f"Se cargaron {total} nodo(s) desde '{archivo}'.")
    except FileNotFoundError:
        print(f"El archivo '{archivo}' no existe.")
    except OSError as error:
        print(f"No se pudo leer el archivo: {error}")


def menu_apuntar(lista):
    n = lista.longitud()
    if n < 3:
        print("\nSe necesitan al menos 3 nodos para hacer esta operación.")
        return

    print(f"\nLa lista tiene {n} nodos (posiciones 1 a {n}).")
    a = pedir_entero("Posición del primer nodo que va a apuntar: ", 1, n)

    b = pedir_entero("Posición del segundo nodo que va a apuntar: ", 1, n)
    while b == a:
        print("Debe ser un nodo distinto al primero.")
        b = pedir_entero("Posición del segundo nodo que va a apuntar: ", 1, n)

    d = pedir_entero("Posición del nodo al que ambos van a apuntar: ", 1, n)
    while d in (a, b):
        print("El nodo destino debe ser distinto a los otros dos.")
        d = pedir_entero("Posición del nodo al que ambos van a apuntar: ", 1, n)

    nodo_a, nodo_b, destino = lista.apuntar_mismo_nodo(a, b, d)
    print(f"Ahora '{nodo_a.info}' y '{nodo_b.info}' apuntan a '{destino.info}'.")

    perdidos = n - lista.longitud()
    if perdidos > 0:
        print(f"Aviso: {perdidos} nodo(s) quedaron fuera de la lista "
              "(ya no se llega a ellos desde P).")
    if lista.tiene_ciclo():
        print("Aviso: la lista ahora tiene un ciclo (no termina en NIL).")


def main():
    lista = ListaEnlazada()
    opcion = -1

    while opcion != 0:
        print("\n===== LISTA ENLAZADA =====")
        print("  1. Agregar nodo (inserción)")
        print("  2. Eliminar nodo (borrado)")
        print("  3. Buscar un dato (búsqueda)")
        print("  4. Recorrer y mostrar la lista (recorrido)")
        print("  5. Hacer que dos nodos apunten a un mismo nodo")
        print("  6. Guardar la lista en un archivo")
        print("  7. Cargar la lista desde un archivo")
        print("  0. Salir")
        opcion = pedir_entero("Opción: ", 0, 7)

        if opcion == 1:
            menu_agregar(lista)
        elif opcion == 2:
            menu_eliminar(lista)
        elif opcion == 3:
            menu_buscar(lista)
        elif opcion == 5:
            menu_apuntar(lista)
        elif opcion == 6:
            menu_guardar(lista)
        elif opcion == 7:
            menu_cargar(lista)

        if opcion in (1, 2, 4, 5, 7):
            print("Lista actual:")
            lista.mostrar()

    print("\nLista final:")
    lista.mostrar()


if __name__ == "__main__":
    main()