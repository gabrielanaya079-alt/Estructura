"""Árbol binario de búsqueda de enteros. Ejecuta con --demo para cargar el ejemplo."""
#Pegar en la terminal y darle enter para cargar el ejemplo: py arbol_binario.py --demo  


import argparse
from collections import deque


class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.izquierdo = None
        self.derecho = None


class Arbol:
    def __init__(self):
        self.raiz = None

    def es_vacio(self):
        return self.raiz is None

    def regresa_raiz(self):
        return self.raiz

    def insertar_nodo(self, dato):
        """Devuelve False si el valor ya está en el árbol."""
        if self.es_vacio():
            self.raiz = Nodo(dato)
            return True

        nodo = self.raiz
        while nodo.dato != dato:
            if dato < nodo.dato:
                if nodo.izquierdo is None:
                    nodo.izquierdo = Nodo(dato)
                    return True
                nodo = nodo.izquierdo
            else:
                if nodo.derecho is None:
                    nodo.derecho = Nodo(dato)
                    return True
                nodo = nodo.derecho
        return False

    def busqueda(self, dato):
        nodo = self.raiz
        while nodo is not None and nodo.dato != dato:
            if dato < nodo.dato:
                nodo = nodo.izquierdo
            else:
                nodo = nodo.derecho
        return nodo

    def busca_menor(self):
        return self._extremo(self.raiz, "izquierdo")

    def busca_mayor(self):
        return self._extremo(self.raiz, "derecho")

    def _extremo(self, nodo, lado):
        if nodo is None:
            return None
        while getattr(nodo, lado) is not None:
            nodo = getattr(nodo, lado)
        return nodo

    def eliminar_predecesor(self, dato):
        return self._eliminar(dato, "izquierdo", "derecho")

    def eliminar_sucesor(self, dato):
        return self._eliminar(dato, "derecho", "izquierdo")

    def _eliminar(self, dato, rama, extremo):
        def eliminar(nodo, valor):
            if nodo is None:
                return None, False

            if valor < nodo.dato:
                nodo.izquierdo, eliminado = eliminar(nodo.izquierdo, valor)
                return nodo, eliminado
            if valor > nodo.dato:
                nodo.derecho, eliminado = eliminar(nodo.derecho, valor)
                return nodo, eliminado

            # Cero o un hijo: el hijo existente (o None) toma el lugar del nodo.
            if nodo.izquierdo is None:
                return nodo.derecho, True
            if nodo.derecho is None:
                return nodo.izquierdo, True

            # Dos hijos: copiar el valor de reemplazo y quitarlo de su rama.
            subarbol = getattr(nodo, rama)
            reemplazo = self._extremo(subarbol, extremo)
            nodo.dato = reemplazo.dato
            subarbol, _ = eliminar(subarbol, reemplazo.dato)
            setattr(nodo, rama, subarbol)
            return nodo, True

        self.raiz, eliminado = eliminar(self.raiz, dato)
        return eliminado

    def podar_arbol(self):
        # Al quitar la referencia a la raíz, Python administra la memoria.
        self.raiz = None

    def preorden(self):
        return self._recorrido(("dato", "izquierdo", "derecho"))

    def inorden(self):
        return self._recorrido(("izquierdo", "dato", "derecho"))

    def postorden(self):
        return self._recorrido(("izquierdo", "derecho", "dato"))

    def _recorrido(self, orden):
        datos = []

        def visitar(nodo):
            if nodo is None:
                return
            for parte in orden:
                if parte == "dato":
                    datos.append(nodo.dato)
                else:
                    visitar(getattr(nodo, parte))

        visitar(self.raiz)
        return datos

    def recorrido_niveles(self):
        if self.es_vacio():
            return []
        datos = []
        cola = deque([self.raiz])
        while cola:
            nodo = cola.popleft()
            datos.append(nodo.dato)
            for hijo in (nodo.izquierdo, nodo.derecho):
                if hijo is not None:
                    cola.append(hijo)
        return datos

    def altura(self):
        def medir(nodo):
            if nodo is None:
                return 0
            return 1 + max(medir(nodo.izquierdo), medir(nodo.derecho))

        return medir(self.raiz)

    def contar_hojas(self):
        def contar(nodo):
            if nodo is None:
                return 0
            if nodo.izquierdo is None and nodo.derecho is None:
                return 1
            return contar(nodo.izquierdo) + contar(nodo.derecho)

        return contar(self.raiz)

    def contar_nodos(self):
        def contar(nodo):
            if nodo is None:
                return 0
            return 1 + contar(nodo.izquierdo) + contar(nodo.derecho)

        return contar(self.raiz)

    def es_lleno(self):
        def verificar(nodo):
            if nodo is None:
                return True
            if (nodo.izquierdo is None) != (nodo.derecho is None):
                return False
            return verificar(nodo.izquierdo) and verificar(nodo.derecho)

        return verificar(self.raiz)

    def es_completo(self):
        cola = deque([self.raiz])
        hay_hueco = False
        while cola:
            nodo = cola.popleft()
            if nodo is None:
                hay_hueco = True
            elif hay_hueco:
                return False
            else:
                cola.extend((nodo.izquierdo, nodo.derecho))
        return True

    def muestra_acostado(self):
        lineas = []

        def dibujar(nodo, nivel):
            if nodo is None:
                return
            dibujar(nodo.derecho, nivel + 1)
            lineas.append("    " * nivel + str(nodo.dato))
            dibujar(nodo.izquierdo, nivel + 1)

        dibujar(self.raiz, 0)
        return "\n".join(lineas) or "El árbol está vacío."

    def graficar_arbol(self):
        """Dibuja la raíz arriba y los enlaces en la consola."""
        if self.es_vacio():
            return "El árbol está vacío."

        # Inorden asigna una columna a cada nodo. Así, los hijos conservan su lado.
        paso = max(len(str(self.busca_menor().dato)),
                   len(str(self.busca_mayor().dato))) + 2
        posiciones = {}

        def ubicar(nodo, nivel):
            if nodo is None:
                return
            ubicar(nodo.izquierdo, nivel + 1)
            posiciones[nodo] = (len(posiciones) * paso + paso // 2, nivel)
            ubicar(nodo.derecho, nivel + 1)

        ubicar(self.raiz, 0)
        filas = [[" "] * (len(posiciones) * paso)
                 for _ in range(2 * self.altura() - 1)]
        for nodo, (columna, nivel) in posiciones.items():
            etiqueta = str(nodo.dato)
            inicio = columna - len(etiqueta) // 2
            filas[2 * nivel][inicio:inicio + len(etiqueta)] = etiqueta
            for hijo in (nodo.izquierdo, nodo.derecho):
                if hijo is not None:
                    columna_hijo, _ = posiciones[hijo]
                    enlace = filas[2 * nivel + 1]
                    desde = min(columna, columna_hijo)
                    hasta = max(columna, columna_hijo)
                    enlace[desde:hasta + 1] = "-" * (hasta - desde + 1)
                    enlace[columna] = "+"
                    enlace[columna_hijo] = "+"

        return "\n".join("".join(fila).rstrip() for fila in filas)


MENU = """
ÁRBOL BINARIO DE BÚSQUEDA
 1. Insertar un número           10. Recorrer por niveles
 2. Mostrar el árbol acostado    11. Mostrar la altura
 3. Dibujar el árbol             12. Contar las hojas
 4. Buscar un número             13. Contar los nodos
 5. Mostrar preorden             14. Mostrar mínimo y máximo
 6. Mostrar inorden              15. Verificar si es completo
 7. Mostrar postorden            16. Verificar si es lleno
 8. Eliminar con el predecesor   17. Vaciar el árbol
 9. Eliminar con el sucesor       0. Salir
"""


def menu(arbol):
    recorridos = {
        "5": ("Preorden", arbol.preorden),
        "6": ("Inorden", arbol.inorden),
        "7": ("Postorden", arbol.postorden),
        "10": ("Por niveles", arbol.recorrido_niveles),
    }
    print(MENU)
    while True:
        opcion = input("\nOpción (M para ver el menú): ").strip().lower()
        if opcion == "0":
            return
        if opcion == "m":
            print(MENU)
        elif opcion in ("1", "4", "8", "9"):
            try:
                dato = int(input("Número entero: "))
            except ValueError:
                print("Escribe un número entero.")
                continue

            if opcion == "1":
                print("Número insertado." if arbol.insertar_nodo(dato)
                      else "Ese número ya está en el árbol.")
            elif opcion == "4":
                print("Número encontrado." if arbol.busqueda(dato) is not None
                      else "Número no encontrado.")
            else:
                eliminar = arbol.eliminar_predecesor if opcion == "8" else arbol.eliminar_sucesor
                print("Número eliminado." if eliminar(dato) else "Número no encontrado.")
        elif opcion in recorridos:
            nombre, recorrer = recorridos[opcion]
            datos = recorrer()
            if datos:
                print(f"{nombre}: " + " → ".join(map(str, datos)))
            else:
                print("El árbol está vacío.")
        elif opcion == "2":
            print(arbol.muestra_acostado())
        elif opcion == "3":
            print(arbol.graficar_arbol())
        elif opcion == "11":
            print(f"Altura: {arbol.altura()} niveles")
        elif opcion == "12":
            print(f"Hojas: {arbol.contar_hojas()}")
        elif opcion == "13":
            print(f"Nodos: {arbol.contar_nodos()}")
        elif opcion == "14":
            if arbol.es_vacio():
                print("El árbol está vacío.")
            else:
                print(f"Mínimo: {arbol.busca_menor().dato} | Máximo: {arbol.busca_mayor().dato}")
        elif opcion == "15":
            print("¿Es completo?", "Sí" if arbol.es_completo() else "No")
        elif opcion == "16":
            print("¿Es lleno?", "Sí" if arbol.es_lleno() else "No")
        elif opcion == "17":
            arbol.podar_arbol()
            print("El árbol se vació.")
        else:
            print("Opción inválida. Escribe M para ver el menú.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="Carga los números de ejemplo.")
    argumentos = parser.parse_args()
    arbol = Arbol()
    if argumentos.demo:
        valores = (8, 3, 20, 1, 5, 10, 7, 4)
        for valor in valores:
            arbol.insertar_nodo(valor)
        print("Ejemplo cargado:", *valores)
    try:
        menu(arbol)
    except (EOFError, KeyboardInterrupt):
        print("\nPrograma terminado.")
