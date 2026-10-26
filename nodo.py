class Nodo:
    """Nodo con campos INFO y LIGA (como en el Algoritmo 5.1)."""
    def __init__(self, info):
        self.info = info
        self.liga = None          # LIGA <- NIL


class ListaEnlazada:
    def __init__(self):
        self.p = None             # P apunta al inicio de la lista

    # ---------- Recorrido seguro ----------
    def _recorrer(self):
        """Recorre desde P y se detiene al llegar a NIL o a un nodo ya visitado
        (así no se cicla si la lista tiene un ciclo)."""
        visitados = set()
        actual = self.p
        while actual is not None and id(actual) not in visitados:
            visitados.add(id(actual))
            yield actual
            actual = actual.liga

    def longitud(self):
        """Cuenta los nodos a los que se llega desde P."""
        contador = 0
        for _ in self._recorrer():
            contador += 1
        return contador

    def tiene_ciclo(self):
        ultimo = None
        for nodo in self._recorrer():
            ultimo = nodo
        return ultimo is not None and ultimo.liga is not None

    def _nodo_en(self, posicion):
        """Devuelve el nodo que está en 'posicion' (1 = primero)."""
        contador = 1
        for nodo in self._recorrer():
            if contador == posicion:
                return nodo
            contador += 1
        return None

    # ---------- Inserciones ----------
    def agregar_inicio(self, info):
        q = Nodo(info)
        q.liga = self.p           # Hacer Q^.LIGA <- P
        self.p = q                # P <- Q

    def agregar_final(self, info):
        """Devuelve False si no se pudo (la lista tiene un ciclo)."""
        if self.tiene_ciclo():    # con ciclo no existe "último nodo"
            return False
        q = Nodo(info)
        if self.p is None:        # lista vacía
            self.p = q
            return True
        actual = self.p
        while actual.liga is not None:   # recorrer hasta el último nodo
            actual = actual.liga
        actual.liga = q
        return True

    def agregar_medio(self, info, posicion):
        """Inserta el nodo para que quede en 'posicion' (1 = primer nodo)."""
        if posicion <= 1 or self.p is None:
            self.agregar_inicio(info)
            return
        q = Nodo(info)
        actual = self.p
        contador = 1
        # Avanzar hasta el nodo anterior a la posición deseada
        while actual.liga is not None and contador < posicion - 1:
            actual = actual.liga
            contador += 1
        q.liga = actual.liga
        actual.liga = q

    # ---------- Eliminaciones ----------
    def eliminar_por_posicion(self, posicion):
        """Elimina el nodo en 'posicion' (1 = primero). Devuelve True si lo logró."""
        if self.p is None or posicion < 1 or posicion > self.longitud():
            return False

        if posicion == 1:                 # eliminar el primer nodo
            self.p = self.p.liga          # P <- P^.LIGA
            return True

        anterior = self.p
        contador = 1
        # Avanzar hasta el nodo anterior al que se va a eliminar
        while contador < posicion - 1:
            anterior = anterior.liga
            contador += 1
        anterior.liga = anterior.liga.liga   # saltarse el nodo eliminado
        return True

    def eliminar_por_dato(self, dato):
        """Elimina la primera aparición de 'dato'. Devuelve True si lo encontró.
        (Con un ciclo en la lista no se usa: el menú lo avisa antes.)"""
        if self.p is None or self.tiene_ciclo():
            return False

        if self.p.info == dato:           # el dato está en el primer nodo
            self.p = self.p.liga
            return True

        anterior = self.p
        actual = self.p.liga
        while actual is not None and actual.info != dato:
            anterior = actual
            actual = actual.liga

        if actual is None:                # llegó a NIL sin encontrarlo
            return False

        anterior.liga = actual.liga       # saltarse el nodo encontrado
        return True

    # ---------- Búsqueda ----------
    def buscar(self, dato):
        """Busca la primera aparición de 'dato'.
        Devuelve su posición (1 = primer nodo) o None si no está en la lista."""
        posicion = 1
        for nodo in self._recorrer():     # recorrido seguro (también con ciclos)
            if nodo.info == dato:
                return posicion
            posicion += 1
        return None

    # ---------- Dos nodos apuntando a un mismo nodo ----------
    def apuntar_mismo_nodo(self, pos_a, pos_b, pos_destino):
        """Hace que el nodo en pos_a y el nodo en pos_b apunten (LIGA) al nodo
        en pos_destino. Devuelve (nodo_a, nodo_b, nodo_destino) o None si las
        posiciones no son válidas."""
        n = self.longitud()
        posiciones = (pos_a, pos_b, pos_destino)

        if any(pos < 1 or pos > n for pos in posiciones):
            return None
        if len(set(posiciones)) < 3:      # las tres posiciones deben ser distintas
            return None

        # Primero se localizan los tres nodos (antes de modificar cualquier LIGA)
        nodo_a = self._nodo_en(pos_a)
        nodo_b = self._nodo_en(pos_b)
        destino = self._nodo_en(pos_destino)

        nodo_a.liga = destino             # A^.LIGA <- D
        nodo_b.liga = destino             # B^.LIGA <- D
        return nodo_a, nodo_b, destino

    # ---------- Mostrar ----------
    def mostrar(self):
        if self.p is None:
            print("La lista está vacía.")
            return
        partes = []
        ultimo = None
        for nodo in self._recorrer():
            partes.append(str(nodo.info))
            ultimo = nodo
        if ultimo.liga is None:
            final = "NIL"
        else:
            final = f"(regresa a {ultimo.liga.info})"
        print(" -> ".join(partes) + " -> " + final)


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
    if lista.p is None:
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
    if lista.p is None:
        print("\nLa lista está vacía, no hay nada que buscar.")
        return

    dato = input("\nDato a buscar: ")
    posicion = lista.buscar(dato)
    if posicion is None:
        print(f"El dato '{dato}' no se encontró en la lista.")
    else:
        print(f"El dato '{dato}' se encontró en la posición {posicion}.")


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
        print("  0. Salir")
        opcion = pedir_entero("Opción: ", 0, 5)

        if opcion == 1:
            menu_agregar(lista)
        elif opcion == 2:
            menu_eliminar(lista)
        elif opcion == 3:
            menu_buscar(lista)
        elif opcion == 5:
            menu_apuntar(lista)

        if opcion in (1, 2, 4, 5):
            print("Lista actual:")
            lista.mostrar()

    print("\nLista final:")
    lista.mostrar()


if __name__ == "__main__":
    main()