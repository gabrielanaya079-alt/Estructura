class Pila:


    def __init__(self):
        self._items = []

    def apilar(self, elemento):
        self._items.append(elemento)

    def desapilar(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        return self._items.pop()

    def tope(self):
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        return self._items[-1]

    def esta_vacia(self):
        return len(self._items) == 0

    def tamanio(self):
        return len(self._items)

    def limpiar(self):
        self._items.clear()

    def elementos(self):
        """Devuelve una copia de los elementos (del fondo al tope)."""
        return list(self._items)


class Navegador:
    """
    Usa dos pilas:
      - atras:     sitios visitados anteriormente
      - adelante:  sitios a los que se puede volver tras retroceder
    La página actual se guarda aparte.
    """

    def __init__(self):
        self.actual = None
        self.atras = Pila()
        self.adelante = Pila()

    def visitar(self, url):
        if self.actual is not None:
            self.atras.apilar(self.actual)
        self.actual = url
        # Al visitar un sitio nuevo, el historial "adelante" se pierde
        self.adelante.limpiar()
        print(f"Visitando: {url}")

    def retroceder(self):
        if self.atras.esta_vacia():
            print("No hay páginas anteriores.")
            return
        self.adelante.apilar(self.actual)
        self.actual = self.atras.desapilar()
        print(f"Retrocediste a: {self.actual}")

    def avanzar(self):
        if self.adelante.esta_vacia():
            print("No hay páginas siguientes.")
            return
        self.atras.apilar(self.actual)
        self.actual = self.adelante.desapilar()
        print(f"Avanzaste a: {self.actual}")

    def mostrar_historial(self):G
        print("\n--- Historial ---")
        if self.actual is None:
            print("(vacío)\n")
            return
        print("Anteriores (más reciente primero):")
        for url in reversed(self.atras.elementos()):
            print(f"   {url}")
        print(f"Página actual:\n > {self.actual}")
        print("Siguientes (más cercana primero):")
        for url in reversed(self.adelante.elementos()):
            print(f"   {url}")
        print()


def main():
    nav = Navegador()
    print("=== Navegador web simulado ===")

    while True:
        print("1) Visitar sitio")
        print("2) Retroceder")
        print("3) Avanzar")
        print("4) Ver historial")
        print("5) Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            url = input("URL: ").strip()
            if url:
                nav.visitar(url)
            else:
                print("La URL no puede estar vacía.")
        elif opcion == "2":
            nav.retroceder()
        elif opcion == "3":
            nav.avanzar()
        elif opcion == "4":
            nav.mostrar_historial()
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")
        print()


if __name__ == "__main__":
    main()