def mostrar_vector(vector):
    for num in vector:
        print(num)

def media(vector):
    suma = 0
    for num in vector:
        suma += num
    return suma / len(vector)


pares = [2, 4, 6, 8, 10]
impares = [1, 3, 5, 7, 9]

mostrar_vector(pares)
print("Media=", media(pares))

mostrar_vector(impares)
print("Media=", media(impares))