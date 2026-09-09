class Calculadora:

    def factorial(self, n):
        if n == 0:
            return 1
        else:
            return n * self.factorial(n - 1)

calculadora = Calculadora()

a = 996

print(calculadora.factorial(a))
