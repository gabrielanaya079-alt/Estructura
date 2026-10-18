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


OPERADORES = {"+", "-", "*", "/", "^"}


def aplicar(op, a, b):
    """Aplica el operador 'op' a los operandos a y b (en ese orden)."""
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise ZeroDivisionError("División entre cero")
        return a / b
    if op == "^":
        return a ** b
    raise ValueError(f"Operador desconocido: {op}")


def evaluar_posfija(expresion):
    """Evalúa una expresión posfija. Ej: '3 4 + 2 *' -> 14"""
    pila = Pila()
    for token in expresion.split():
        if token in OPERADORES:
            if pila.tamanio() < 2:
                raise ValueError("Expresión inválida: faltan operandos")
            b = pila.desapilar()  # el primero en salir es el operando derecho
            a = pila.desapilar()
            pila.apilar(aplicar(token, a, b))
        else:
            pila.apilar(float(token))

    if pila.tamanio() != 1:
        raise ValueError("Expresión inválida: sobran operandos")
    return pila.desapilar()


def evaluar_prefija(expresion):
    """Evalúa una expresión prefija. Ej: '* + 3 4 2' -> 14
    Se recorre de derecha a izquierda."""
    pila = Pila()
    for token in reversed(expresion.split()):
        if token in OPERADORES:
            if pila.tamanio() < 2:
                raise ValueError("Expresión inválida: faltan operandos")
            a = pila.desapilar()  # aquí el primero en salir es el operando izquierdo
            b = pila.desapilar()
            pila.apilar(aplicar(token, a, b))
        else:
            pila.apilar(float(token))

    if pila.tamanio() != 1:
        raise ValueError("Expresión inválida: sobran operandos")
    return pila.desapilar()


def formatear(resultado):
    return int(resultado) if resultado == int(resultado) else resultado


def main():
    print("=== Evaluador de expresiones con pila ===")
    print("Escribe los tokens separados por espacios. Operadores: + - * / ^")
    print("Ejemplos:  posfija -> 3 4 + 2 *    |    prefija -> * + 3 4 2\n")

    while True:
        print("1) Evaluar expresión posfija")
        print("2) Evaluar expresión prefija")
        print("3) Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "3":
            print("¡Hasta luego!")
            break
        if opcion not in ("1", "2"):
            print("Opción no válida.\n")
            continue

        expresion = input("Expresión: ").strip()
        try:
            if opcion == "1":
                resultado = evaluar_posfija(expresion)
            else:
                resultado = evaluar_prefija(expresion)
            print(f"Resultado: {formatear(resultado)}\n")
        except (ValueError, ZeroDivisionError, IndexError) as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()