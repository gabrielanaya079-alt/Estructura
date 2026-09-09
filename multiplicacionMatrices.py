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

    def multiplicar(self, otra_matriz):
        if self.columnas != otra_matriz.filas:
            raise ValueError(
                "El número de columnas de la primera matriz debe ser igual "
                "al número de filas de la segunda para poder multiplicarlas."
            )

        resultado = Matriz(self.filas, otra_matriz.columnas)
        resultado.datos = []
        for i in range(self.filas):
            fila_resultado = []
            for j in range(otra_matriz.columnas):
                suma = 0
                for k in range(self.columnas):
                    suma += self.datos[i][k] * otra_matriz.datos[k][j]
                fila_resultado.append(suma)
            resultado.datos.append(fila_resultado)
        return resultado

    def mostrar(self, titulo="Matriz"):
        print(f"\n{titulo}:")
        for fila in self.datos:
            print("  ", [f"{valor:.1f}" for valor in fila])


def main():
    print("=== Multiplicación de Matrices ===")

    filas_a = int(input("¿Cuántas filas tiene la matriz A? "))
    columnas_a = int(input("¿Cuántas columnas tiene la matriz A? "))
    matriz_a = Matriz(filas_a, columnas_a)
    matriz_a.capturar_datos("A")

    print("\nPara poder multiplicar, la matriz B debe tener "
          f"{columnas_a} filas (igual a las columnas de A).")
    columnas_b = int(input("¿Cuántas columnas tendrá la matriz B? "))
    matriz_b = Matriz(columnas_a, columnas_b)
    matriz_b.capturar_datos("B")

    matriz_a.mostrar("Matriz A")
    matriz_b.mostrar("Matriz B")

    resultado = matriz_a.multiplicar(matriz_b)
    resultado.mostrar("Resultado (A x B)")


if __name__ == "__main__":
    main()