import tkinter as tk

CAPACIDAD = 6
ALTO = 50
ANCHO = 140
X = 80
BASE = 340

pila = []


def dibujar():
    canvas.delete("all")
    # Pared de la pila (forma de U)
    canvas.create_line(X - 5, BASE - CAPACIDAD * ALTO, X - 5, BASE + 5,
                       X + ANCHO + 5, BASE + 5,
                       X + ANCHO + 5, BASE - CAPACIDAD * ALTO, width=4)
    # Elementos
    for i, valor in enumerate(pila):
        y2 = BASE - i * ALTO
        y1 = y2 - ALTO
        canvas.create_rectangle(X, y1, X + ANCHO, y2, fill="#4C9BE8", outline="white", width=2)
        canvas.create_text(X + ANCHO / 2, (y1 + y2) / 2, text=valor,
                           font=("Arial", 16, "bold"), fill="white")
    # Flecha de la cima
    if pila:
        y = BASE - (len(pila) - 1) * ALTO - ALTO / 2
        canvas.create_text(X + ANCHO + 20, y, text="◄ CIMA", anchor="w",
                           font=("Arial", 12, "bold"), fill="red")


def push():
    if len(pila) >= CAPACIDAD:
        mensaje.config(text="¡Pila llena!", fg="red")
        return
    valor = entrada.get().strip() or str(len(pila) + 1)
    pila.append(valor)
    entrada.delete(0, tk.END)
    mensaje.config(text="Push: se apiló '%s'" % valor, fg="green")
    dibujar()


def pop():
    if not pila:
        mensaje.config(text="¡Pila vacía!", fg="red")
        return
    valor = pila.pop()
    mensaje.config(text="Pop: se sacó '%s'" % valor, fg="green")
    dibujar()


ventana = tk.Tk()
ventana.title("Pila (Stack)")

canvas = tk.Canvas(ventana, width=320, height=370, bg="white")
canvas.pack(padx=10, pady=10)

entrada = tk.Entry(ventana, font=("Arial", 14), width=12, justify="center")
entrada.pack()
entrada.bind("<Return>", lambda e: push())

botones = tk.Frame(ventana)
botones.pack(pady=8)
tk.Button(botones, text="Push", width=10, command=push).pack(side="left", padx=5)
tk.Button(botones, text="Pop", width=10, command=pop).pack(side="left", padx=5)

mensaje = tk.Label(ventana, text="Escribe un valor y pulsa Push", font=("Arial", 11))
mensaje.pack(pady=(0, 10))

dibujar()
ventana.mainloop()