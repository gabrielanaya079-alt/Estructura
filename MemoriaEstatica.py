from tkinter import simpledialog, Tk

root = Tk()
root.withdraw()  

calificaciones = [0] * 5  
for i in range(5):
    calificaciones[i] = int(simpledialog.askstring("Entrada", "Captura la calificacion: "))