class Matriz:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.datos = []

    def capturar_datos(self, nombre):
        print(f"\nCaptura los valores de la matriz {nombre} ({self.filas}x{self.columnas}):")
        self.datos = []
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                valor = float(input(f"  {nombre}[{i}][{j}] = "))
                fila.append(valor)
            self.datos.append(fila)

    def sumar(self, otra_matriz):
        if self.filas != otra_matriz.filas or self.columnas != otra_matriz.columnas:
            raise ValueError("Las matrices deben tener las mismas dimensiones para sumarse.")

        resultado = Matriz(self.filas, self.columnas)
        resultado.datos = []
        for i in range(self.filas):
            fila_resultado = []
            for j in range(self.columnas):
                suma = self.datos[i][j] + otra_matriz.datos[i][j]
                fila_resultado.append(suma)
            resultado.datos.append(fila_resultado)
        return resultado

    def mostrar(self, titulo="Matriz"):
        print(f"\n{titulo}:")
        for fila in self.datos:
            print("  ", [f"{valor:.1f}" for valor in fila])


def main():
    print("=== Suma de Matrices ===")

    filas = int(input("¿Cuántas filas tendrán las matrices? "))
    columnas = int(input("¿Cuántas columnas tendrán las matrices? "))

    matriz_a = Matriz(filas, columnas)
    matriz_a.capturar_datos("A")

    matriz_b = Matriz(filas, columnas)
    matriz_b.capturar_datos("B")

    matriz_a.mostrar("Matriz A")
    matriz_b.mostrar("Matriz B")

    resultado = matriz_a.sumar(matriz_b)
    resultado.mostrar("Resultado (A + B)")


if __name__ == "__main__":
    main()