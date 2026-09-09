import random


class Vectores:
    def __init__(self, datos):
        """Constructor: recibe una lista de números"""
        self.datos = datos

    def mostrar_vector(self):
        """Muestra todos los elementos del vector"""
        for elemento in self.datos:
            print(elemento)

    def media(self):
        """Calcula el promedio (suma de todos entre la cantidad)"""
        suma = 0
        for elemento in self.datos:
            suma += elemento
        return suma / len(self.datos)

    def mediana(self):
        """Calcula el valor central al ordenar los datos"""
        ordenado = sorted(self.datos)
        n = len(ordenado)
        mitad = n // 2

        if n % 2 == 0:
            # Cantidad par: promedio de los dos valores centrales
            return (ordenado[mitad - 1] + ordenado[mitad]) / 2
        else:
            # Cantidad impar: el valor central
            return ordenado[mitad]

    def moda(self):
        """Calcula el/los valor(es) que más se repite(n)"""
        frecuencias = {}
        for elemento in self.datos:
            if elemento in frecuencias:
                frecuencias[elemento] += 1
            else:
                frecuencias[elemento] = 1

        max_frecuencia = max(frecuencias.values())
        modas = [valor for valor, frecuencia in frecuencias.items()
                 if frecuencia == max_frecuencia]

        return modas, max_frecuencia

    def varianza(self, poblacional=True):
        """Calcula qué tan dispersos están los datos respecto a la media"""
        m = self.media()
        suma_cuadrados = 0
        for elemento in self.datos:
            suma_cuadrados += (elemento - m) ** 2

        n = len(self.datos)
        if poblacional:
            return suma_cuadrados / n
        else:
            return suma_cuadrados / (n - 1)

    def desviacion_estandar(self, poblacional=True):
        """Raíz cuadrada de la varianza"""
        return self.varianza(poblacional) ** 0.5


# ---------- Programa principal ----------
if __name__ == "__main__":
    # Generar 50 números aleatorios entre 1 y 100
    datos = [random.randint(150, 250) for _ in range(50)]

    vector = Vectores(datos)

    print("Lista de datos:")
    print(vector.datos)
    print()

    print("Media:", vector.media())
    print("Mediana:", vector.mediana())

    modas, frecuencia = vector.moda()
    print(f"Moda: {modas} (aparece {frecuencia} veces)")

    print("Varianza (poblacional):", vector.varianza(poblacional=True))
    print("Varianza (muestral):", vector.varianza(poblacional=False))
    print("Desviación estándar (poblacional):", vector.desviacion_estandar(poblacional=True))
    print("Desviación estándar (muestral):", vector.desviacion_estandar(poblacional=False))