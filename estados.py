import heapq
import math
import random
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

MAX_NODOS_RECOMENDADO = 13       # el espacio de estados crece como n * 2^n
LIMITE_BUSQUEDA_LARGA = 3_000_000  # tope de pasos de la búsqueda exhaustiva


# ----------------------------------------------------------------------------
# Modelo del grafo
# ----------------------------------------------------------------------------
class Grafo:
    def __init__(self):
        self.pos = {}      # nombre -> (x, y)
        self.aristas = {}  # frozenset({a, b}) -> costo

    def agregar_nodo(self, nombre, x, y):
        self.pos[nombre] = (x, y)

    def eliminar_nodo(self, nombre):
        self.pos.pop(nombre, None)
        self.aristas = {k: v for k, v in self.aristas.items() if nombre not in k}

    def agregar_arista(self, a, b, costo):
        self.aristas[frozenset((a, b))] = costo

    def eliminar_arista(self, a, b):
        return self.aristas.pop(frozenset((a, b)), None) is not None

    def costo(self, a, b):
        return self.aristas.get(frozenset((a, b)))

    def vecinos(self, nombre):
        res = []
        for k, c in self.aristas.items():
            if nombre in k:
                (otro,) = tuple(k - {nombre})
                res.append((otro, c))
        return sorted(res)


def grafo_inicial():
    """7 estados del sureste/golfo con sus colindancias y costos aproximados (MXN)."""
    g = Grafo()
    nodos = {
        "Yucatán": (660, 140),
        "Quintana Roo": (800, 270),
        "Campeche": (540, 250),
        "Tabasco": (400, 300),
        "Chiapas": (320, 470),
        "Oaxaca": (150, 400),
        "Veracruz": (170, 190),
    }
    for n, (x, y) in nodos.items():
        g.agregar_nodo(n, x, y)
    conexiones = [
        ("Yucatán", "Campeche", 350),
        ("Yucatán", "Quintana Roo", 650),
        ("Campeche", "Quintana Roo", 700),
        ("Campeche", "Tabasco", 600),
        ("Tabasco", "Chiapas", 500),
        ("Tabasco", "Veracruz", 950),
        ("Tabasco", "Oaxaca", 1000),
        ("Chiapas", "Oaxaca", 850),
        ("Chiapas", "Veracruz", 1200),
        ("Veracruz", "Oaxaca", 700),
    ]
    for a, b, c in conexiones:
        g.agregar_arista(a, b, c)
    return g


# ----------------------------------------------------------------------------
# Algoritmos
# ----------------------------------------------------------------------------
def recorrido_mas_corto(grafo, repetir, inicio=None):
    """
    Recorrido de MENOR costo que visita todos los estados.
    repetir=False -> sin repetir ninguno.  repetir=True -> repitiendo al menos uno.
    Devuelve (costo, [estados], aproximado=False) o None si no existe.
    """
    nodos = list(grafo.pos)
    n = len(nodos)
    if n == 0:
        return None
    idx = {nombre: i for i, nombre in enumerate(nodos)}
    adj = [[] for _ in range(n)]
    for k, c in grafo.aristas.items():
        a, b = tuple(k)
        adj[idx[a]].append((idx[b], c))
        adj[idx[b]].append((idx[a], c))

    lleno = (1 << n) - 1
    meta_rep = 1 if repetir else 0
    inicios = [idx[inicio]] if inicio else range(n)

    heap = []
    for s in inicios:
        heapq.heappush(heap, (0, s, 1 << s, 0, (s,)))

    mejor = {}
    while heap:
        costo, u, mask, rep, camino = heapq.heappop(heap)
        clave = (u, mask, rep)
        if clave in mejor:
            continue
        mejor[clave] = costo
        if mask == lleno and rep == meta_rep:
            return costo, [nodos[i] for i in camino], False
        for v, w in adj[u]:
            bit = 1 << v
            if mask & bit:
                if not repetir:
                    continue
                nrep = 1
            else:
                nrep = rep
            nmask = mask | bit
            if (v, nmask, nrep) not in mejor:
                heapq.heappush(heap, (costo + w, v, nmask, nrep, camino + (v,)))
    return None


def recorrido_mas_largo(grafo, repetir, inicio=None, limite=LIMITE_BUSQUEDA_LARGA):
    """
    Recorrido de MAYOR costo que visita todos los estados.
    repetir=False -> camino hamiltoniano de mayor costo.
    repetir=True  -> pasa por todos, repite al menos un estado y no usa dos veces
                     la misma conexión (si no, el costo sería ilimitado).
    Devuelve (costo, [estados], aproximado) o None. 'aproximado' es True si la
    búsqueda llegó al tope de pasos y puede haber una ruta aún mayor.
    """
    nodos = list(grafo.pos)
    n = len(nodos)
    if n == 0:
        return None
    adj = {u: [] for u in nodos}
    for k, c in grafo.aristas.items():
        a, b = tuple(k)
        adj[a].append((b, c))
        adj[b].append((a, c))

    mejor = {"costo": None, "camino": None}
    pasos = [0]
    truncado = [False]

    def dfs(u, visitados, usadas, camino, costo, repeticiones):
        pasos[0] += 1
        if pasos[0] > limite:
            truncado[0] = True
            return
        if len(visitados) == n and (repeticiones >= 1 or not repetir):
            if mejor["costo"] is None or costo > mejor["costo"]:
                mejor["costo"] = costo
                mejor["camino"] = list(camino)
        for v, c in adj[u]:
            if truncado[0]:
                return
            if repetir:
                k = frozenset((u, v))
                if k in usadas:
                    continue
                usadas.add(k)
                camino.append(v)
                if v in visitados:
                    dfs(v, visitados, usadas, camino, costo + c, repeticiones + 1)
                else:
                    visitados.add(v)
                    dfs(v, visitados, usadas, camino, costo + c, repeticiones)
                    visitados.discard(v)
                camino.pop()
                usadas.discard(k)
            else:
                if v in visitados:
                    continue
                visitados.add(v)
                camino.append(v)
                dfs(v, visitados, usadas, camino, costo + c, repeticiones)
                camino.pop()
                visitados.discard(v)

    for s in ([inicio] if inicio else nodos):
        dfs(s, {s}, set(), [s], 0, 0)

    if mejor["costo"] is None:
        return None
    return mejor["costo"], mejor["camino"], truncado[0]


def mejor_recorrido(grafo, repetir, inicio=None, largo=False):
    """Atajo: elige el algoritmo según el criterio (corto u largo)."""
    if largo:
        return recorrido_mas_largo(grafo, repetir, inicio)
    return recorrido_mas_corto(grafo, repetir, inicio)


def distancia_a_segmento(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)
    t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))


# ----------------------------------------------------------------------------
# Interfaz gráfica
# ----------------------------------------------------------------------------
class App(tk.Tk):
    RADIO = 32

    def __init__(self):
        super().__init__()
        self.title("Grafo de estados de México - Recorridos óptimos")
        self.geometry("1300x800")
        self.minsize(1100, 700)

        self.g = grafo_inicial()
        self.ruta = []          # recorrido actual (lista de nombres)
        self.ruta_mostrada = 0  # cuántos nodos de la ruta se dibujan (animación)
        self.anim_id = None
        self.arrastrando = None

        self._crear_widgets()
        self._refrescar_todo()

    # ---------------------------- construcción ----------------------------
    def _crear_widgets(self):
        self.canvas = tk.Canvas(self, bg="#f7f9fc", highlightthickness=1,
                                highlightbackground="#bbb")
        self.canvas.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        self.canvas.bind("<ButtonPress-1>", self._click)
        self.canvas.bind("<B1-Motion>", self._mover)
        self.canvas.bind("<ButtonRelease-1>", lambda e: setattr(self, "arrastrando", None))
        self.canvas.bind("<Double-Button-1>", self._doble_click)
        self.canvas.bind("<Configure>", lambda e: self._dibujar())

        panel = ttk.Frame(self, padding=6)
        panel.pack(side="right", fill="y")

        # --- Estados
        f1 = ttk.LabelFrame(panel, text="Estados (nodos)", padding=6)
        f1.pack(fill="x", pady=3)
        self.var_nombre = tk.StringVar()
        ttk.Entry(f1, textvariable=self.var_nombre, width=22).grid(row=0, column=0, padx=2)
        ttk.Button(f1, text="Agregar estado", command=self.agregar_estado).grid(row=0, column=1, padx=2)
        ttk.Button(f1, text="Eliminar estado (Origen)", command=self.eliminar_estado)\
            .grid(row=1, column=0, columnspan=2, sticky="ew", pady=3)

        # --- Conexiones
        f2 = ttk.LabelFrame(panel, text="Conexiones y costos", padding=6)
        f2.pack(fill="x", pady=3)
        self.var_o = tk.StringVar()
        self.var_d = tk.StringVar()
        self.var_c = tk.StringVar(value="500")
        ttk.Label(f2, text="Origen").grid(row=0, column=0, sticky="w")
        self.cb_o = ttk.Combobox(f2, textvariable=self.var_o, state="readonly", width=18)
        self.cb_o.grid(row=0, column=1, padx=2, pady=1)
        ttk.Label(f2, text="Destino").grid(row=1, column=0, sticky="w")
        self.cb_d = ttk.Combobox(f2, textvariable=self.var_d, state="readonly", width=18)
        self.cb_d.grid(row=1, column=1, padx=2, pady=1)
        ttk.Label(f2, text="Costo (MXN)").grid(row=2, column=0, sticky="w")
        ttk.Entry(f2, textvariable=self.var_c, width=20).grid(row=2, column=1, padx=2, pady=1)
        ttk.Button(f2, text="Cambiar costo de esta conexión", command=self.cambiar_costo)\
            .grid(row=3, column=0, columnspan=2, sticky="ew", pady=2)
        ttk.Button(f2, text="Agregar conexión nueva", command=self.agregar_conexion)\
            .grid(row=4, column=0, columnspan=2, sticky="ew")
        ttk.Button(f2, text="Eliminar conexión", command=self.eliminar_conexion)\
            .grid(row=5, column=0, columnspan=2, sticky="ew", pady=2)
        ttk.Label(f2, foreground="#555", wraplength=300,
                  text="También: doble clic en una arista del dibujo o en una fila de "
                       "la pestaña 'Conexiones' para editar su costo.")\
            .grid(row=6, column=0, columnspan=2, sticky="w")

        # --- Recorridos
        f3 = ttk.LabelFrame(panel, text="Recorridos", padding=6)
        f3.pack(fill="x", pady=3)
        self.var_inicio = tk.StringVar(value="Cualquiera")
        self.var_criterio = tk.StringVar(value="corto")
        ttk.Label(f3, text="Inicio").grid(row=0, column=0, sticky="w")
        self.cb_inicio = ttk.Combobox(f3, textvariable=self.var_inicio, state="readonly", width=18)
        self.cb_inicio.grid(row=0, column=1, padx=2, pady=1)
        ttk.Label(f3, text="Criterio").grid(row=1, column=0, sticky="w")
        crit = ttk.Frame(f3)
        crit.grid(row=1, column=1, sticky="w")
        ttk.Radiobutton(crit, text="Más corta (óptima)", variable=self.var_criterio,
                        value="corto").pack(anchor="w")
        ttk.Radiobutton(crit, text="Más larga", variable=self.var_criterio,
                        value="largo").pack(anchor="w")
        ttk.Button(f3, text="a) Todos SIN repetir ninguno", command=lambda: self.calcular(False))\
            .grid(row=2, column=0, columnspan=2, sticky="ew", pady=2)
        ttk.Button(f3, text="b) Todos repitiendo al menos uno", command=lambda: self.calcular(True))\
            .grid(row=3, column=0, columnspan=2, sticky="ew")
        ttk.Button(f3, text="Limpiar recorrido", command=self.limpiar_ruta)\
            .grid(row=4, column=0, columnspan=2, sticky="ew", pady=2)

        # --- Resultado
        f4 = ttk.LabelFrame(panel, text="Resultado y costo total", padding=4)
        f4.pack(fill="both", pady=3)
        self.txt = tk.Text(f4, width=48, height=10, wrap="word", font=("Consolas", 9))
        self.txt.pack(fill="both")

        # --- Relaciones / conexiones (pestañas)
        nb = ttk.Notebook(panel)
        nb.pack(fill="both", expand=True, pady=3)

        t1 = ttk.Frame(nb)
        nb.add(t1, text="Estados y relaciones")
        self.tree = ttk.Treeview(t1, columns=("estado", "rel"), show="headings", height=6)
        self.tree.heading("estado", text="Estado")
        self.tree.heading("rel", text="Conectado con (costo MXN)")
        self.tree.column("estado", width=95, anchor="w")
        self.tree.column("rel", width=290, anchor="w")
        self.tree.pack(fill="both", expand=True)

        t2 = ttk.Frame(nb)
        nb.add(t2, text="Conexiones")
        self.tree_c = ttk.Treeview(t2, columns=("a", "b", "c"), show="headings", height=6)
        for col, txt, w in (("a", "Origen", 120), ("b", "Destino", 120), ("c", "Costo (MXN)", 90)):
            self.tree_c.heading(col, text=txt)
            self.tree_c.column(col, width=w, anchor="w")
        self.tree_c.pack(fill="both", expand=True)
        self.tree_c.bind("<<TreeviewSelect>>", self._seleccion_conexion)
        self.tree_c.bind("<Double-Button-1>", self._doble_click_tabla)

        ttk.Label(panel, foreground="#555",
                  text="Tip: arrastra los nodos con el mouse para acomodarlos.").pack(pady=2)

    # ----------------------------- utilidades -----------------------------
    def _escribir(self, texto):
        self.txt.config(state="normal")
        self.txt.delete("1.0", "end")
        self.txt.insert("end", texto)
        self.txt.config(state="disabled")

    def _refrescar_todo(self):
        nombres = sorted(self.g.pos)
        for cb in (self.cb_o, self.cb_d):
            cb["values"] = nombres
        self.cb_inicio["values"] = ["Cualquiera"] + nombres
        if self.var_o.get() not in nombres:
            self.var_o.set(nombres[0] if nombres else "")
        if self.var_d.get() not in nombres:
            self.var_d.set(nombres[1] if len(nombres) > 1 else "")
        if self.var_inicio.get() not in ["Cualquiera"] + nombres:
            self.var_inicio.set("Cualquiera")

        self.tree.delete(*self.tree.get_children())
        for n in nombres:
            vec = self.g.vecinos(n)
            texto = ", ".join(f"{m} (${c:,.0f})" for m, c in vec) if vec else "— sin conexiones —"
            self.tree.insert("", "end", values=(n, texto))

        self.tree_c.delete(*self.tree_c.get_children())
        for k, c in sorted(self.g.aristas.items(), key=lambda kv: sorted(kv[0])):
            a, b = sorted(k)
            self.tree_c.insert("", "end", values=(a, b, f"{c:,.0f}"))
        self._dibujar()

    # ------------------------------ edición -------------------------------
    def agregar_estado(self):
        nombre = self.var_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Falta nombre", "Escribe el nombre del estado.")
            return
        if nombre in self.g.pos:
            messagebox.showwarning("Duplicado", f"'{nombre}' ya existe.")
            return
        w = max(self.canvas.winfo_width(), 600)
        h = max(self.canvas.winfo_height(), 400)
        for _ in range(200):  # busca un hueco libre
            x = random.randint(60, w - 60)
            y = random.randint(60, h - 60)
            if all(math.hypot(x - px, y - py) > 2 * self.RADIO + 10 for px, py in self.g.pos.values()):
                break
        self.g.agregar_nodo(nombre, x, y)
        self.var_nombre.set("")
        self.limpiar_ruta(refrescar=False)
        if len(self.g.pos) > MAX_NODOS_RECOMENDADO:
            messagebox.showinfo("Aviso", f"Con más de {MAX_NODOS_RECOMENDADO} estados el cálculo "
                                         "óptimo puede tardar bastante.")
        self._refrescar_todo()

    def eliminar_estado(self):
        n = self.var_o.get()
        if n not in self.g.pos:
            messagebox.showwarning("Selecciona", "Elige el estado a eliminar en 'Origen'.")
            return
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{n}' y todas sus conexiones?"):
            self.g.eliminar_nodo(n)
            self.limpiar_ruta(refrescar=False)
            self._refrescar_todo()

    def _leer_costo(self):
        try:
            c = float(self.var_c.get())
            if c <= 0:
                raise ValueError
            return c
        except ValueError:
            messagebox.showwarning("Costo inválido", "El costo debe ser un número positivo.")
            return None

    def agregar_conexion(self):
        a, b = self.var_o.get(), self.var_d.get()
        if a not in self.g.pos or b not in self.g.pos:
            messagebox.showwarning("Selecciona", "Elige origen y destino.")
            return
        if a == b:
            messagebox.showwarning("Inválido", "Origen y destino deben ser distintos.")
            return
        c = self._leer_costo()
        if c is None:
            return
        self.g.agregar_arista(a, b, c)
        self.limpiar_ruta(refrescar=False)
        self._refrescar_todo()

    def cambiar_costo(self):
        a, b = self.var_o.get(), self.var_d.get()
        if self.g.costo(a, b) is None:
            messagebox.showinfo("Sin conexión", "Esa conexión no existe todavía.\n"
                                                "Usa 'Agregar conexión nueva'.")
            return
        c = self._leer_costo()
        if c is None:
            return
        self.g.agregar_arista(a, b, c)
        self.limpiar_ruta(refrescar=False)
        self._refrescar_todo()

    def editar_costo_dialogo(self, a, b):
        actual = self.g.costo(a, b)
        nuevo = simpledialog.askfloat("Cambiar costo", f"Nuevo costo (MXN) de {a} ↔ {b}:",
                                      initialvalue=actual, minvalue=0.01, parent=self)
        if nuevo is not None:
            self.g.agregar_arista(a, b, nuevo)
            self.var_o.set(a)
            self.var_d.set(b)
            self.var_c.set(f"{nuevo:g}")
            self.limpiar_ruta(refrescar=False)
            self._refrescar_todo()

    def eliminar_conexion(self):
        a, b = self.var_o.get(), self.var_d.get()
        if self.g.eliminar_arista(a, b):
            self.limpiar_ruta(refrescar=False)
            self._refrescar_todo()
        else:
            messagebox.showinfo("Sin conexión", "Esa conexión no existe.")

    def _seleccion_conexion(self, _e=None):
        sel = self.tree_c.selection()
        if not sel:
            return
        a, b, _c = self.tree_c.item(sel[0], "values")
        self.var_o.set(a)
        self.var_d.set(b)
        costo = self.g.costo(a, b)
        if costo is not None:
            self.var_c.set(f"{costo:g}")

    def _doble_click_tabla(self, _e=None):
        sel = self.tree_c.selection()
        if sel:
            a, b, _c = self.tree_c.item(sel[0], "values")
            self.editar_costo_dialogo(a, b)

    # ------------------------------ cálculo -------------------------------
    def calcular(self, repetir):
        self.limpiar_ruta(refrescar=False)
        largo = self.var_criterio.get() == "largo"
        titulo = ("b) Todos repitiendo al menos uno" if repetir else "a) Todos SIN repetir")
        titulo += " — ruta MÁS LARGA" if largo else " — ruta MÁS CORTA (óptima)"
        if len(self.g.pos) == 0:
            self._escribir("No hay estados en el grafo.")
            return
        inicio = self.var_inicio.get()
        inicio = None if inicio == "Cualquiera" else inicio
        self.config(cursor="watch")
        self.update_idletasks()
        res = mejor_recorrido(self.g, repetir, inicio, largo)
        self.config(cursor="")

        if res is None:
            extra = ("No existe un camino que pase por todos los estados sin repetir.\n"
                     "Agrega conexiones o prueba otro estado inicial."
                     if not repetir else
                     "No existe un recorrido que visite todos y repita alguno\n"
                     "(el grafo está desconectado o tiene un solo estado)."
                     + ("\nPara la ruta más larga no se reutilizan conexiones." if largo else ""))
            self._escribir(f"{titulo}\n\n{extra}")
            self._dibujar()
            return

        costo, ruta, aproximado = res
        lineas = [titulo, "", "Ruta:", " → ".join(ruta), ""]
        for i in range(len(ruta) - 1):
            c = self.g.costo(ruta[i], ruta[i + 1])
            lineas.append(f"{i + 1}. {ruta[i]} → {ruta[i + 1]}: ${c:,.0f}")
        repetidos = sorted({n for n in ruta if ruta.count(n) > 1})
        lineas.append("")
        if repetidos:
            lineas.append("Estados repetidos: " + ", ".join(repetidos))
        lineas.append(f"COSTO TOTAL: ${costo:,.0f} MXN")
        if aproximado:
            lineas.append("(Búsqueda cortada por tamaño: puede existir una ruta aún más larga.)")
        self._escribir("\n".join(lineas))

        self.ruta = ruta
        self.ruta_mostrada = 1
        self._animar()

    def _animar(self):
        self._dibujar()
        if self.ruta_mostrada < len(self.ruta):
            self.ruta_mostrada += 1
            self.anim_id = self.after(600, self._animar)
        else:
            self.anim_id = None

    def limpiar_ruta(self, refrescar=True):
        if self.anim_id:
            self.after_cancel(self.anim_id)
            self.anim_id = None
        self.ruta = []
        self.ruta_mostrada = 0
        if refrescar:
            self._escribir("")
            self._dibujar()

    # ------------------------------ dibujo --------------------------------
    def _dibujar(self):
        c = self.canvas
        c.delete("all")
        R = self.RADIO
        parcial = self.ruta[:self.ruta_mostrada] if self.ruta else []

        pasos = {}
        for i in range(len(parcial) - 1):
            pasos.setdefault(frozenset((parcial[i], parcial[i + 1])), []).append(i + 1)

        # aristas
        for k, costo in self.g.aristas.items():
            a, b = tuple(k)
            x1, y1 = self.g.pos[a]
            x2, y2 = self.g.pos[b]
            activa = k in pasos
            c.create_line(x1, y1, x2, y2, width=5 if activa else 2,
                          fill="#e53935" if activa else "#90a4ae")
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            etiqueta = f"${costo:,.0f}"
            if activa:
                etiqueta += "  [" + ",".join(map(str, pasos[k])) + "]"
            t = c.create_text(mx, my, text=etiqueta, font=("Arial", 9, "bold"),
                              fill="#b71c1c" if activa else "#263238")
            bb = c.bbox(t)
            r = c.create_rectangle(bb[0] - 3, bb[1] - 1, bb[2] + 3, bb[3] + 1,
                                   fill="#fff8e1" if activa else "white", outline="#cfd8dc")
            c.tag_raise(t, r)

        # nodos
        for nombre, (x, y) in self.g.pos.items():
            fill, outline, ancho = "#bbdefb", "#1565c0", 2
            if parcial:
                if nombre == parcial[0]:
                    fill, outline = "#a5d6a7", "#2e7d32"
                elif nombre in parcial:
                    fill, outline = "#fff59d", "#f9a825"
                if nombre == parcial[-1] and len(parcial) > 1:
                    fill, outline = "#ffcc80", "#e65100"
                if parcial.count(nombre) > 1:
                    outline, ancho = "#8e24aa", 4
            c.create_oval(x - R, y - R, x + R, y + R, fill=fill, outline=outline, width=ancho)
            c.create_text(x, y, text=nombre, width=2 * R - 8, justify="center",
                          font=("Arial", 9, "bold"))

        # leyenda
        if parcial:
            c.create_text(10, 10, anchor="nw", font=("Arial", 9),
                          text="Verde: inicio | Naranja: fin | Amarillo: visitado | "
                               "Borde morado: repetido | [n]: orden del tramo")
        else:
            c.create_text(10, 10, anchor="nw", font=("Arial", 9), fill="#555",
                          text="Doble clic sobre una arista para cambiar su costo.")

    # ------------------------------ mouse ---------------------------------
    def _nodo_en(self, x, y):
        for nombre, (nx, ny) in self.g.pos.items():
            if math.hypot(x - nx, y - ny) <= self.RADIO:
                return nombre
        return None

    def _click(self, e):
        self.arrastrando = self._nodo_en(e.x, e.y)

    def _mover(self, e):
        if self.arrastrando:
            self.g.pos[self.arrastrando] = (e.x, e.y)
            self._dibujar()

    def _doble_click(self, e):
        if self._nodo_en(e.x, e.y):
            return
        mejor, dmin = None, 14
        for k in self.g.aristas:
            a, b = tuple(k)
            x1, y1 = self.g.pos[a]
            x2, y2 = self.g.pos[b]
            d = distancia_a_segmento(e.x, e.y, x1, y1, x2, y2)
            if d < dmin:
                mejor, dmin = (a, b), d
        if mejor:
            self.editar_costo_dialogo(*mejor)


if __name__ == "__main__":
    App().mainloop()