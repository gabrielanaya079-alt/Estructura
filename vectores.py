class Vectores:
    def __init__(self, datos):
        self.datos = datos

    def mostrar_vector(self):
        for elemento in self.datos:
            print(elemento)

    def media(self):
        n = len(self.datos)
        suma = 0
        for elemento in self.datos:
            suma += elemento
        return suma / n
    
if __name__ == "__main__":
    pares = Vectores([2, 4, 6, 8, 10])
    impares = Vectores([1, 3, 5, 7, 9])

    pares.mostrar_vector()
    print("Media=", pares.media())

    impares.mostrar_vector()
    print("Media=", impares.media())