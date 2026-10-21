class Cola:
    def __init__(self):
        self.items = []

    def encolar(self, elemento):
        self.items.append(elemento)

    def desencolar(self):
        return self.items.pop(0)

    def esta_vacia(self):
        return len(self.items) == 0

    def tamano(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


def sumar_colas(cola_a, cola_b):
    resultado = Cola()

    for _ in range(cola_a.tamano()):
        a = cola_a.desencolar()
        b = cola_b.desencolar()
        resultado.encolar(a + b)
        cola_a.encolar(a)
        cola_b.encolar(b)

    return resultado


cola_a = Cola()
cola_b = Cola()

for n in [8, 5, 7, 9, 10]:
    cola_a.encolar(n)
for n in [6, 2, 9, 11, 3]:
    cola_b.encolar(n)

cola_resultado = sumar_colas(cola_a, cola_b)

print("Cola A:", cola_a)              
print("Cola B:", cola_b)              
print("Cola Resultado:", cola_resultado)  