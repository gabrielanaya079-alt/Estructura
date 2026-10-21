
import tkinter as tk
from tkinter import ttk, messagebox

EPS = 1e-9

def fmt(x):
    x = round(float(x), 6)
    return str(int(x)) if x == int(x) else str(x)

def esquina_noroeste(costos, oferta, demanda):

    m, n = len(oferta), len(demanda)
    filas = [f"Origen {i + 1}" for i in range(m)]
    cols = [f"Destino {j + 1}" for j in range(n)]
    costos = [r[:] for r in costos]
    oferta = oferta[:]
    demanda = demanda[:]

    total_of, total_de = sum(oferta), sum(demanda)
    notas = [f"Oferta total = {fmt(total_of)}   |   Demanda total = {fmt(total_de)}"]

    # --- Balanceo ---
    if abs(total_of - total_de) < EPS:
        notas.append("El problema está BALANCEADO (oferta = demanda). "
                     "No se agrega ningún origen/destino ficticio.")
    elif total_of > total_de:
        dif = total_of - total_de
        notas.append(f"El problema NO está balanceado: sobra oferta ({fmt(dif)} unidades).")
        notas.append(f"Se agrega un DESTINO FICTICIO con demanda {fmt(dif)} y costos 0.")
        for r in costos:
            r.append(0)
        demanda.append(dif)
        cols.append("Ficticio")
        n += 1
    else:
        dif = total_de - total_of
        notas.append(f"El problema NO está balanceado: falta oferta ({fmt(dif)} unidades).")
        notas.append(f"Se agrega un ORIGEN FICTICIO con oferta {fmt(dif)} y costos 0.")
        costos.append([0] * n)
        oferta.append(dif)
        filas.append("Ficticio")
        m += 1

    oferta0, demanda0 = oferta[:], demanda[:]
    asign = [[None] * n for _ in range(m)]
    rows_done, cols_done = set(), set()

    pasos = [{
        "texto": "\n".join(notas) + "\n\nTabla inicial (lista para aplicar la esquina noroeste). "
                 "Presiona «Siguiente» para avanzar.",
        "asign": [r[:] for r in asign],
        "of": oferta[:], "de": demanda[:],
        "actual": None, "rd": set(), "cd": set(),
    }]

    i = j = 0
    k = 1
    while i < m and j < n:
        q = min(oferta[i], demanda[j])
        asign[i][j] = q
        oferta[i] -= q
        demanda[j] -= q
        txt = (f"Paso {k}: esquina noroeste = celda ({filas[i]}, {cols[j]}).\n"
               f"Se asigna min(oferta {fmt(oferta[i] + q)}, demanda {fmt(demanda[j] + q)}) = {fmt(q)}.\n"
               f"Quedan: oferta {fmt(oferta[i])}  |  demanda {fmt(demanda[j])}.")
        actual = (i, j)

        if oferta[i] < EPS and demanda[j] < EPS:
            if i == m - 1 and j == n - 1:
                rows_done.add(i)
                cols_done.add(j)
                txt += "\nSe agotaron oferta y demanda: fin del método."
                i += 1
            elif j < n - 1:
                rows_done.add(i)
                txt += (f"\nOferta y demanda se agotan a la vez (DEGENERACIÓN). "
                        f"Se tacha {filas[i]} y la siguiente celda a la derecha "
                        f"se asigna con 0 para mantener m+n-1 celdas básicas.")
                cols_done.add(j)
                j += 1
            else:
                rows_done.add(i)
                txt += "\nOferta y demanda se agotan a la vez (DEGENERACIÓN)."
                i += 1
        elif oferta[i] < EPS:
            rows_done.add(i)
            txt += f"\n{filas[i]} se agotó: se tacha la fila y se baja."
            i += 1
        else:
            cols_done.add(j)
            txt += f"\n{cols[j]} quedó satisfecho: se tacha la columna y se mueve a la derecha."
            j += 1

        pasos.append({
            "texto": txt,
            "asign": [r[:] for r in asign],
            "of": oferta[:], "de": demanda[:],
            "actual": actual, "rd": set(rows_done), "cd": set(cols_done),
        })
        k += 1

    # --- Costo total ---
    partes, total = [], 0
    for a in range(m):
        for b in range(n):
            if asign[a][b] is not None and asign[a][b] > EPS:
                c = costos[a][b]
                total += c * asign[a][b]
                partes.append(f"{fmt(asign[a][b])}×{fmt(c)}")
    basicas = sum(1 for r in asign for v in r if v is not None)

    return {
        "filas": filas, "cols": cols, "costos": costos,
        "oferta0": oferta0, "demanda0": demanda0,
        "pasos": pasos, "asign": asign, "total": total,
        "partes": partes, "basicas": basicas, "m": m, "n": n, "notas": notas,
    }

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modelo de Transporte - Método de la Esquina Noroeste")
        self.geometry("1050x760")
        self.minsize(900, 650)
        self.res = None
        self.paso_actual = 0


        top = ttk.LabelFrame(self, text=" 1. Tamaño del problema ")
        top.pack(fill="x", padx=10, pady=(10, 4))
        ttk.Label(top, text="Orígenes (filas):").pack(side="left", padx=(10, 4), pady=8)
        self.sp_m = ttk.Spinbox(top, from_=1, to=12, width=5)
        self.sp_m.set(3)
        self.sp_m.pack(side="left")
        ttk.Label(top, text="Destinos (columnas):").pack(side="left", padx=(15, 4))
        self.sp_n = ttk.Spinbox(top, from_=1, to=12, width=5)
        self.sp_n.set(4)
        self.sp_n.pack(side="left")
        ttk.Button(top, text="Crear tabla", command=self.crear_tabla).pack(side="left", padx=15)
        ttk.Button(top, text="Ejemplo balanceado",
                   command=lambda: self.cargar_ejemplo(True)).pack(side="left", padx=4)
        ttk.Button(top, text="Ejemplo no balanceado",
                   command=lambda: self.cargar_ejemplo(False)).pack(side="left", padx=4)

        # ---- Datos ----
        self.f_datos = ttk.LabelFrame(
            self, text=" 2. Costos unitarios, oferta y demanda ")
        self.f_datos.pack(fill="x", padx=10, pady=4)
        self.f_grid = ttk.Frame(self.f_datos)
        self.f_grid.pack(padx=10, pady=8)

        bt = ttk.Frame(self.f_datos)
        bt.pack(pady=(0, 8))
        ttk.Button(bt, text="RESOLVER", command=self.resolver).pack(side="left", padx=6)
        ttk.Button(bt, text="Limpiar valores", command=self.limpiar).pack(side="left", padx=6)

        # ---- Resultados ----
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=10, pady=(4, 10))

        self.tab_pasos = ttk.Frame(self.nb)
        self.tab_final = ttk.Frame(self.nb)
        self.nb.add(self.tab_pasos, text="Paso a paso")
        self.nb.add(self.tab_final, text="Resultado final")

        nav = ttk.Frame(self.tab_pasos)
        nav.pack(fill="x", pady=6, padx=6)
        self.b_ant = ttk.Button(nav, text="◀ Anterior", command=lambda: self.ir_paso(-1))
        self.b_ant.pack(side="left")
        self.b_sig = ttk.Button(nav, text="Siguiente ▶", command=lambda: self.ir_paso(1))
        self.b_sig.pack(side="left", padx=6)
        ttk.Button(nav, text="Ir al final", command=self.ir_final).pack(side="left")
        self.lbl_paso = ttk.Label(nav, text="")
        self.lbl_paso.pack(side="right")

        self.txt_paso = tk.Label(self.tab_pasos, text="", justify="left", anchor="w",
                                 font=("Segoe UI", 10), wraplength=980)
        self.txt_paso.pack(fill="x", padx=10)
        self.f_tabla_paso = ttk.Frame(self.tab_pasos)
        self.f_tabla_paso.pack(padx=10, pady=8, anchor="w")

        self.f_tabla_final = ttk.Frame(self.tab_final)
        self.f_tabla_final.pack(padx=10, pady=10, anchor="w")
        self.txt_final = tk.Text(self.tab_final, height=9, font=("Consolas", 10),
                                 wrap="word", state="disabled")
        self.txt_final.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.crear_tabla()
        self.cargar_ejemplo(True)

    # ---------- Tabla de entrada ----------
    def crear_tabla(self):
        try:
            m, n = int(self.sp_m.get()), int(self.sp_n.get())
            if not (1 <= m <= 12 and 1 <= n <= 12):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingresa tamaños enteros entre 1 y 12.")
            return
        for w in self.f_grid.winfo_children():
            w.destroy()
        self.m, self.n = m, n
        ttk.Label(self.f_grid, text="").grid(row=0, column=0)
        for j in range(n):
            ttk.Label(self.f_grid, text=f"Destino {j + 1}",
                      font=("Segoe UI", 9, "bold")).grid(row=0, column=j + 1, padx=3)
        ttk.Label(self.f_grid, text="OFERTA",
                  font=("Segoe UI", 9, "bold")).grid(row=0, column=n + 1, padx=8)
        self.e_cost = []
        for i in range(m):
            ttk.Label(self.f_grid, text=f"Origen {i + 1}",
                      font=("Segoe UI", 9, "bold")).grid(row=i + 1, column=0, padx=5, pady=2)
            fila = []
            for j in range(n):
                e = ttk.Entry(self.f_grid, width=8, justify="center")
                e.grid(row=i + 1, column=j + 1, padx=2, pady=2)
                fila.append(e)
            self.e_cost.append(fila)
        self.e_of = []
        for i in range(m):
            e = ttk.Entry(self.f_grid, width=8, justify="center")
            e.grid(row=i + 1, column=n + 1, padx=8)
            self.e_of.append(e)
        ttk.Label(self.f_grid, text="DEMANDA",
                  font=("Segoe UI", 9, "bold")).grid(row=m + 1, column=0, pady=(8, 0))
        self.e_de = []
        for j in range(n):
            e = ttk.Entry(self.f_grid, width=8, justify="center")
            e.grid(row=m + 1, column=j + 1, padx=2, pady=(8, 0))
            self.e_de.append(e)

    def limpiar(self):
        for e in [x for r in self.e_cost for x in r] + self.e_of + self.e_de:
            e.delete(0, "end")

    def cargar_ejemplo(self, balanceado):
        if balanceado:
            costos = [[8, 6, 10, 9], [9, 12, 13, 7], [14, 9, 16, 5]]
            of, de = [35, 50, 40], [45, 20, 30, 30]
        else:
            costos = [[8, 6, 10, 9], [9, 12, 13, 7], [14, 9, 16, 5]]
            of, de = [40, 50, 45], [30, 20, 25, 25]
        self.sp_m.set(3)
        self.sp_n.set(4)
        self.crear_tabla()
        for i in range(3):
            for j in range(4):
                self.e_cost[i][j].insert(0, str(costos[i][j]))
            self.e_of[i].insert(0, str(of[i]))
        for j in range(4):
            self.e_de[j].insert(0, str(de[j]))

    # ---------- Lectura y resolución ----------
    @staticmethod
    def _num(e, nombre):
        s = e.get().strip().replace(",", ".")
        if s == "":
            raise ValueError(f"Falta el valor de {nombre}.")
        try:
            v = float(s)
        except ValueError:
            raise ValueError(f"'{s}' no es un número válido ({nombre}).")
        if v < 0:
            raise ValueError(f"No se permiten valores negativos ({nombre}).")
        return v

    def resolver(self):
        try:
            costos = [[self._num(self.e_cost[i][j], f"costo ({i + 1},{j + 1})")
                       for j in range(self.n)] for i in range(self.m)]
            oferta = [self._num(self.e_of[i], f"oferta del origen {i + 1}") for i in range(self.m)]
            demanda = [self._num(self.e_de[j], f"demanda del destino {j + 1}") for j in range(self.n)]
        except ValueError as ex:
            messagebox.showwarning("Datos incompletos", str(ex))
            return
        if sum(oferta) < EPS and sum(demanda) < EPS:
            messagebox.showwarning("Datos", "La oferta y la demanda no pueden ser todas cero.")
            return

        self.res = esquina_noroeste(costos, oferta, demanda)
        self.paso_actual = 0
        self.mostrar_paso()
        self.mostrar_final()
        self.nb.select(self.tab_pasos)

    # ---------- Dibujo de tablas ----------
    def dibujar_tabla(self, parent, r, asign, of_rest, de_rest, actual, rd, cd):
        for w in parent.winfo_children():
            w.destroy()
        m, n = r["m"], r["n"]

        def celda(txt, row, col, bg="#ffffff", bold=False, fg="#000000"):
            tk.Label(parent, text=txt, bg=bg, fg=fg, width=13, height=2,
                     font=("Segoe UI", 10, "bold" if bold else "normal"),
                     relief="solid", bd=1).grid(row=row, column=col, sticky="nsew")

        celda("", 0, 0, "#d9d9d9")
        for j in range(n):
            celda(r["cols"][j], 0, j + 1, "#c9d7ee", True,
                  "#888888" if j in cd else "#000000")
        celda("Oferta (resta)", 0, n + 1, "#c9d7ee", True)

        for i in range(m):
            celda(r["filas"][i], i + 1, 0, "#c9d7ee", True,
                  "#888888" if i in rd else "#000000")
            for j in range(n):
                a = asign[i][j]
                bg = "#ffffff"
                if i in rd or j in cd:
                    bg = "#ececec"
                if a is not None:
                    bg = "#d5f0d5"
                if actual == (i, j):
                    bg = "#ffe680"
                txt = f"c = {fmt(r['costos'][i][j])}"
                if a is not None:
                    txt += f"\n[ {fmt(a)} ]"
                tk.Label(parent, text=txt, bg=bg, width=13, height=2,
                         font=("Segoe UI", 10, "bold" if a is not None else "normal"),
                         relief="solid", bd=1).grid(row=i + 1, column=j + 1, sticky="nsew")
            celda(f"{fmt(r['oferta0'][i])}  ({fmt(of_rest[i])})", i + 1, n + 1, "#f4f4f4")

        celda("Demanda (resta)", m + 1, 0, "#c9d7ee", True)
        for j in range(n):
            celda(f"{fmt(r['demanda0'][j])}  ({fmt(de_rest[j])})", m + 1, j + 1, "#f4f4f4")
        celda(fmt(sum(r["oferta0"])), m + 1, n + 1, "#d9d9d9", True)

    def mostrar_paso(self):
        r = self.res
        p = r["pasos"][self.paso_actual]
        self.txt_paso.config(text=p["texto"])
        self.dibujar_tabla(self.f_tabla_paso, r, p["asign"], p["of"], p["de"],
                           p["actual"], p["rd"], p["cd"])
        self.lbl_paso.config(text=f"Paso {self.paso_actual} de {len(r['pasos']) - 1}")
        self.b_ant.config(state="normal" if self.paso_actual > 0 else "disabled")
        self.b_sig.config(state="normal" if self.paso_actual < len(r["pasos"]) - 1 else "disabled")

    def ir_paso(self, d):
        if not self.res:
            return
        self.paso_actual = max(0, min(len(self.res["pasos"]) - 1, self.paso_actual + d))
        self.mostrar_paso()

    def ir_final(self):
        if not self.res:
            return
        self.paso_actual = len(self.res["pasos"]) - 1
        self.mostrar_paso()

    def mostrar_final(self):
        r = self.res
        ult = r["pasos"][-1]
        self.dibujar_tabla(self.f_tabla_final, r, r["asign"], ult["of"], ult["de"],
                           None, set(), set())
        lines = list(r["notas"])
        lines.append("")
        lines.append(f"Celdas básicas (asignadas): {r['basicas']}  "
                     f"(m + n - 1 = {r['m'] + r['n'] - 1})")
        if r["basicas"] < r["m"] + r["n"] - 1:
            lines.append("Aviso: solución degenerada (menos de m+n-1 celdas básicas).")
        lines.append("")
        lines.append("ASIGNACIONES:")
        for a in range(r["m"]):
            for b in range(r["n"]):
                v = r["asign"][a][b]
                if v is not None and v > EPS:
                    lines.append(f"  {r['filas'][a]} → {r['cols'][b]}: {fmt(v)} unidades "
                                 f"(costo unitario {fmt(r['costos'][a][b])})")
        lines.append("")
        lines.append("COSTO TOTAL = " + " + ".join(r["partes"]))
        lines.append(f"COSTO TOTAL = {fmt(r['total'])}")
        if "Ficticio" in r["filas"] + r["cols"]:
            lines.append("(Las asignaciones al origen/destino ficticio no tienen costo; "
                         "representan demanda no satisfecha u oferta no utilizada.)")
        self.txt_final.config(state="normal")
        self.txt_final.delete("1.0", "end")
        self.txt_final.insert("1.0", "\n".join(lines))
        self.txt_final.config(state="disabled")


if __name__ == "__main__":
    App().mainloop()
