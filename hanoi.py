#!/usr/bin/env python3
"""
Torre de Hanoi - versión gráfica (tkinter, sin instalar nada extra)

  * Jugar tú: clic en una torre para levantar su disco superior y clic en
    otra torre para soltarlo.
  * Resolver solo: la computadora resuelve con animación (velocidad ajustable).
  * Medir tiempos: ventana que mide 5, 10, 30 y 64 discos.
"""

import colorsys
import queue
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

# ----------------------------------------------------------------------------
# Constantes de dibujo
# ----------------------------------------------------------------------------
CANVAS_W, CANVAS_H = 780, 370
PEG_X = [140, 390, 640]
BASE_Y = 320
PEG_H = 240
MAX_W, MIN_W = 210, 36
NOMBRES = "ABC"
MAX_DISCOS = 10

BG = "#1e2230"
FG = "#e8eaf0"


# ----------------------------------------------------------------------------
# Lógica del juego
# ----------------------------------------------------------------------------
def crear_torres(n):
    return [list(range(n, 0, -1)), [], []]


def generar_movimientos(n, origen, destino, auxiliar):
    """Generador de movimientos (origen, destino) para animar."""
    if n == 0:
        return
    yield from generar_movimientos(n - 1, origen, auxiliar, destino)
    yield (origen, destino)
    yield from generar_movimientos(n - 1, auxiliar, destino, origen)


class Cancelado(Exception):
    pass


def resolver_rapido(n, origen, destino, auxiliar, torres, contador, cancelar):
    """Mueve discos de verdad (sin dibujar). Se puede cancelar desde otro hilo."""
    if n == 0:
        return
    if n >= 15 and cancelar.is_set():
        raise Cancelado
    resolver_rapido(n - 1, origen, auxiliar, destino, torres, contador, cancelar)
    torres[destino].append(torres[origen].pop())
    contador[0] += 1
    resolver_rapido(n - 1, auxiliar, destino, origen, torres, contador, cancelar)


def formatear_tiempo(seg):
    if seg < 1e-3:
        return f"{seg * 1e6:.1f} µs"
    if seg < 1:
        return f"{seg * 1e3:.2f} ms"
    if seg < 60:
        return f"{seg:.2f} s"
    if seg < 3600:
        return f"{seg / 60:.2f} min"
    if seg < 86400:
        return f"{seg / 3600:.2f} horas"
    if seg < 86400 * 365.25:
        return f"{seg / 86400:.2f} días"
    anios = seg / (86400 * 365.25)
    if anios < 1e6:
        return f"{anios:,.0f} años"
    return f"{anios:.3e} años"


def color_disco(d, n):
    h = (d - 1) / max(n, 1) * 0.82
    r, g, b = colorsys.hsv_to_rgb(h, 0.62, 0.95)
    return "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))


def oscurecer(hex_color, f=0.65):
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % (int(r * f), int(g * f), int(b * f))


# ----------------------------------------------------------------------------
# Ventana principal
# ----------------------------------------------------------------------------
class HanoiApp:
    def __init__(self, root):
        self.root = root
        root.title("Torre de Hanoi")
        root.configure(bg=BG)
        root.resizable(False, False)

        self.n = 4
        self.torres = []
        self.movs = 0
        self.seleccion = None
        self.modo_auto = False
        self.auto_job = None
        self.gen = None
        self.t_inicio = None
        self.terminado = False

        self._construir_ui()
        self.nuevo_juego()
        self._tick()

    # ---------------------------------------------------------------- UI
    def _construir_ui(self):
        estilo = ttk.Style()
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass

        barra = tk.Frame(self.root, bg=BG)
        barra.pack(fill="x", padx=12, pady=(12, 4))

        tk.Label(barra, text="Discos:", bg=BG, fg=FG).pack(side="left")
        self.var_discos = tk.StringVar(value=str(self.n))
        self.spin = tk.Spinbox(barra, from_=1, to=MAX_DISCOS, width=3,
                               textvariable=self.var_discos, command=self.nuevo_juego)
        self.spin.pack(side="left", padx=(4, 10))
        self.spin.bind("<Return>", lambda e: self.nuevo_juego())

        ttk.Button(barra, text="Nuevo juego", command=self.nuevo_juego).pack(side="left", padx=3)
        self.btn_auto = ttk.Button(barra, text="▶ Resolver solo", command=self.resolver_solo)
        self.btn_auto.pack(side="left", padx=3)
        self.btn_stop = ttk.Button(barra, text="⏹ Detener", command=self.detener_auto,
                                   state="disabled")
        self.btn_stop.pack(side="left", padx=3)

        tk.Label(barra, text="  Velocidad:", bg=BG, fg=FG).pack(side="left")
        self.vel = tk.Scale(barra, from_=1, to=10, orient="horizontal", length=120,
                            bg=BG, fg=FG, highlightthickness=0, troughcolor="#3a4058")
        self.vel.set(5)
        self.vel.pack(side="left", padx=4)

        ttk.Button(barra, text="⏱ Medir tiempos", command=self.abrir_benchmark).pack(side="right")

        self.canvas = tk.Canvas(self.root, width=CANVAS_W, height=CANVAS_H,
                                bg="#262b3d", highlightthickness=0)
        self.canvas.pack(padx=12, pady=6)
        self.canvas.bind("<Button-1>", self.on_click)

        info = tk.Frame(self.root, bg=BG)
        info.pack(fill="x", padx=12)
        self.lbl_movs = tk.Label(info, bg=BG, fg=FG, font=("Helvetica", 11, "bold"))
        self.lbl_movs.pack(side="left")
        self.lbl_min = tk.Label(info, bg=BG, fg="#9aa3c0", font=("Helvetica", 11))
        self.lbl_min.pack(side="left", padx=18)
        self.lbl_tiempo = tk.Label(info, bg=BG, fg=FG, font=("Helvetica", 11, "bold"))
        self.lbl_tiempo.pack(side="right")

        self.lbl_msg = tk.Label(self.root, bg=BG, fg="#9aa3c0", font=("Helvetica", 11),
                                wraplength=CANVAS_W, justify="left")
        self.lbl_msg.pack(fill="x", padx=12, pady=(4, 12))

    # ------------------------------------------------------------ estado
    def _leer_n(self):
        try:
            n = int(self.var_discos.get())
        except ValueError:
            n = self.n
        n = max(1, min(MAX_DISCOS, n))
        self.var_discos.set(str(n))
        return n

    def nuevo_juego(self):
        self.detener_auto(silencioso=True)
        self.n = self._leer_n()
        self.torres = crear_torres(self.n)
        self.movs = 0
        self.seleccion = None
        self.t_inicio = None
        self.terminado = False
        self.lbl_tiempo.config(text="Tiempo: 0.00 s")
        self.mensaje("Haz clic en una torre para levantar su disco superior y luego "
                     "en la torre destino. Meta: llevar todo a la torre C.")
        self.actualizar_info()
        self.dibujar()

    def mensaje(self, texto, error=False):
        self.lbl_msg.config(text=texto, fg="#ff7a7a" if error else "#9aa3c0")

    def actualizar_info(self):
        self.lbl_movs.config(text=f"Movimientos: {self.movs}")
        self.lbl_min.config(text=f"Mínimo posible: {2 ** self.n - 1:,}")

    def _tick(self):
        if self.t_inicio is not None and not self.terminado:
            self.lbl_tiempo.config(
                text=f"Tiempo: {formatear_tiempo(time.perf_counter() - self.t_inicio)}")
        self.root.after(100, self._tick)

    # ---------------------------------------------------------- dibujo
    def alto_disco(self):
        return min(26, (PEG_H - 10) // self.n)

    def dibujar(self):
        c = self.canvas
        c.delete("all")
        c.create_rectangle(20, BASE_Y, CANVAS_W - 20, BASE_Y + 14, fill="#5b4636", outline="")

        for i, x in enumerate(PEG_X):
            activa = self.seleccion == i
            c.create_rectangle(x - 5, BASE_Y - PEG_H, x + 5, BASE_Y,
                               fill="#f0c53d" if activa else "#8a6d4b", outline="")
            c.create_text(x, BASE_Y + 34, text=NOMBRES[i], fill=FG,
                          font=("Helvetica", 15, "bold"))

        h = self.alto_disco()
        for i, torre in enumerate(self.torres):
            for nivel, d in enumerate(torre):
                y_base = BASE_Y - nivel * h
                if self.seleccion == i and nivel == len(torre) - 1:
                    y_base = BASE_Y - PEG_H - 6  # disco levantado
                self._disco(PEG_X[i], d, y_base, h)

    def _disco(self, x, d, y_base, h):
        w = MIN_W + (MAX_W - MIN_W) * d / self.n
        col = color_disco(d, self.n)
        self.canvas.create_rectangle(x - w / 2, y_base - h + 2, x + w / 2, y_base - 1,
                                     fill=col, outline=oscurecer(col), width=2)
        self.canvas.create_text(x, y_base - h / 2 + 0.5, text=str(d),
                                fill=oscurecer(col, 0.4), font=("Helvetica", 9, "bold"))

    # -------------------------------------------------- modo jugador
    def on_click(self, event):
        if self.modo_auto or self.terminado:
            return
        idx = min(range(3), key=lambda i: abs(event.x - PEG_X[i]))
        if abs(event.x - PEG_X[idx]) > 125:
            return

        if self.seleccion is None:
            if not self.torres[idx]:
                self.mensaje("Esa torre está vacía.", error=True)
                return
            self.seleccion = idx
            self.mensaje(f"Disco {self.torres[idx][-1]} levantado. Elige la torre destino.")
        elif idx == self.seleccion:
            self.seleccion = None
            self.mensaje("Disco soltado en su lugar.")
        else:
            origen, self.seleccion = self.seleccion, None
            self.intentar_mover(origen, idx)
        self.dibujar()

    def intentar_mover(self, origen, destino):
        disco = self.torres[origen][-1]
        if self.torres[destino] and self.torres[destino][-1] < disco:
            self.mensaje("⚠ No puedes poner un disco grande sobre uno más pequeño.", error=True)
            return
        if self.t_inicio is None:
            self.t_inicio = time.perf_counter()
        self.torres[destino].append(self.torres[origen].pop())
        self.movs += 1
        self.mensaje(f"Moviste el disco {disco}: {NOMBRES[origen]} → {NOMBRES[destino]}")
        self.actualizar_info()

        if len(self.torres[2]) == self.n:
            self.terminado = True
            t = time.perf_counter() - self.t_inicio
            self.lbl_tiempo.config(text=f"Tiempo: {formatear_tiempo(t)}")
            minimo = 2 ** self.n - 1
            extra = ("¡Perfecto, lo resolviste con el mínimo de movimientos!"
                     if self.movs == minimo else f"El mínimo posible era {minimo}.")
            self.mensaje(f"🎉 ¡Ganaste en {self.movs} movimientos y {formatear_tiempo(t)}! {extra}")
            self.dibujar()
            messagebox.showinfo("¡Ganaste!", f"Resuelto en {self.movs} movimientos.\n{extra}")

    # --------------------------------------------- modo automático
    def resolver_solo(self):
        if self.modo_auto:
            return
        self.nuevo_juego()
        self.modo_auto = True
        self.gen = generar_movimientos(self.n, 0, 2, 1)
        self.t_inicio = time.perf_counter()
        self.btn_auto.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.mensaje("La computadora está resolviendo...")
        self._paso_auto()

    def _paso_auto(self):
        if not self.modo_auto:
            return
        try:
            origen, destino = next(self.gen)
        except StopIteration:
            t = time.perf_counter() - self.t_inicio
            self.modo_auto = False
            self.terminado = True
            self.btn_auto.config(state="normal")
            self.btn_stop.config(state="disabled")
            self.lbl_tiempo.config(text=f"Tiempo: {formatear_tiempo(t)}")
            self.mensaje(f"✅ Resuelto en {self.movs} movimientos "
                         f"({formatear_tiempo(t)}, incluye las pausas de la animación). "
                         "Usa «Medir tiempos» para ver la velocidad real sin animación.")
            return
        self.torres[destino].append(self.torres[origen].pop())
        self.movs += 1
        self.actualizar_info()
        self.dibujar()
        retraso = max(1, int(900 / (2 ** (self.vel.get() - 1))))
        self.auto_job = self.root.after(retraso, self._paso_auto)

    def detener_auto(self, silencioso=False):
        if self.auto_job is not None:
            self.root.after_cancel(self.auto_job)
            self.auto_job = None
        if self.modo_auto:
            self.modo_auto = False
            if not silencioso:
                self.mensaje("Detenido. Puedes continuar jugando desde esta posición.")
        self.gen = None
        self.btn_auto.config(state="normal")
        self.btn_stop.config(state="disabled")

    # ------------------------------------------------- benchmark
    def abrir_benchmark(self):
        VentanaBenchmark(self.root)


# ----------------------------------------------------------------------------
# Ventana de medición de tiempos
# ----------------------------------------------------------------------------
class VentanaBenchmark:
    DISCOS = (5, 10, 30, 64)

    def __init__(self, root):
        self.win = tk.Toplevel(root)
        self.win.title("Medición de tiempos")
        self.win.configure(bg=BG)
        self.win.resizable(False, False)
        self.win.protocol("WM_DELETE_WINDOW", self.cerrar)

        self.q = queue.Queue()
        self.cancelar = threading.Event()
        self.hilo = None
        self.cont = [0]
        self.total = 1
        self.corriendo = False

        tk.Label(self.win, text="La computadora resuelve sola, sin animación",
                 bg=BG, fg=FG, font=("Helvetica", 13, "bold")).pack(padx=14, pady=(14, 6))

        cols = ("discos", "movs", "tiempo", "tipo")
        self.tree = ttk.Treeview(self.win, columns=cols, show="headings", height=4)
        for col, txt, w in (("discos", "Discos", 70), ("movs", "Movimientos", 230),
                            ("tiempo", "Tiempo", 160), ("tipo", "Tipo", 90)):
            self.tree.heading(col, text=txt)
            self.tree.column(col, width=w, anchor="center")
        self.tree.pack(padx=14, pady=6)
        self._reiniciar_filas()

        self.var_real30 = tk.BooleanVar(value=False)
        tk.Checkbutton(self.win, bg=BG, fg=FG, selectcolor="#3a4058",
                       activebackground=BG, activeforeground=FG,
                       text="Ejecutar 30 discos de verdad (más de mil millones de "
                            "movimientos, puede tardar muchos minutos)",
                       variable=self.var_real30).pack(padx=14, anchor="w")

        self.barra = ttk.Progressbar(self.win, length=520, maximum=100)
        self.barra.pack(padx=14, pady=(10, 2))
        self.lbl_estado = tk.Label(self.win, text="Listo para iniciar.", bg=BG, fg="#9aa3c0")
        self.lbl_estado.pack(padx=14)

        botones = tk.Frame(self.win, bg=BG)
        botones.pack(pady=10)
        self.btn_ini = ttk.Button(botones, text="▶ Iniciar", command=self.iniciar)
        self.btn_ini.pack(side="left", padx=4)
        self.btn_can = ttk.Button(botones, text="Cancelar", command=self.cancelar.set,
                                  state="disabled")
        self.btn_can.pack(side="left", padx=4)

        self.lbl_nota = tk.Label(
            self.win, bg=BG, fg="#9aa3c0", wraplength=520, justify="left",
            text="Resolver n discos requiere 2ⁿ − 1 movimientos. Los valores "
                 "«estimado» se calculan con la velocidad medida en tu equipo.")
        self.lbl_nota.pack(padx=14, pady=(0, 14))

    def _reiniciar_filas(self):
        for fila in self.tree.get_children():
            self.tree.delete(fila)
        for n in self.DISCOS:
            self.tree.insert("", "end", iid=str(n),
                             values=(n, f"{2 ** n - 1:,}", "—", "pendiente"))

    # ---- control
    def iniciar(self):
        if self.corriendo:
            return
        self.corriendo = True
        self.cancelar.clear()
        self._reiniciar_filas()
        self.btn_ini.config(state="disabled")
        self.btn_can.config(state="normal")
        real30 = self.var_real30.get()
        self.hilo = threading.Thread(target=self._trabajo, args=(real30,), daemon=True)
        self.hilo.start()
        self._sondear()

    def cerrar(self):
        self.cancelar.set()
        self.win.destroy()

    # ---- hilo de trabajo
    def _ejecutar(self, n):
        torres = crear_torres(n)
        self.cont = [0]
        self.total = 2 ** n - 1
        t0 = time.perf_counter()
        resolver_rapido(n, 0, 2, 1, torres, self.cont, self.cancelar)
        seg = time.perf_counter() - t0
        return self.cont[0], seg

    def _trabajo(self, real30):
        try:
            for n in (5, 10):
                self.q.put(("estado", f"Ejecutando {n} discos..."))
                movs, seg = self._ejecutar(n)
                self.q.put(("fila", n, movs, seg, "medido"))

            self.q.put(("estado", "Calibrando velocidad con 20 discos..."))
            movs, seg = self._ejecutar(20)
            vel = movs / seg
            self.q.put(("estado", f"Velocidad medida: {vel:,.0f} movimientos/s"))

            movs30 = 2 ** 30 - 1
            if real30:
                self.q.put(("estado", "Ejecutando 30 discos de verdad..."))
                try:
                    movs, seg = self._ejecutar(30)
                    self.q.put(("fila", 30, movs, seg, "medido"))
                except Cancelado:
                    self.q.put(("fila", 30, movs30, movs30 / vel, "estimado"))
                    self.q.put(("estado", "30 discos cancelado: se usa la estimación."))
            else:
                self.q.put(("fila", 30, movs30, movs30 / vel, "estimado"))

            movs64 = 2 ** 64 - 1
            self.q.put(("fila", 64, movs64, movs64 / vel, "estimado"))
            self.q.put(("nota", movs64))
        except Cancelado:
            self.q.put(("estado", "Cancelado."))
        finally:
            self.q.put(("fin",))

    # ---- sondeo desde el hilo principal de la GUI
    def _sondear(self):
        if not self.win.winfo_exists():
            return
        try:
            while True:
                msg = self.q.get_nowait()
                if msg[0] == "fila":
                    _, n, movs, seg, tipo = msg
                    self.tree.item(str(n), values=(n, f"{movs:,}", formatear_tiempo(seg), tipo))
                elif msg[0] == "estado":
                    self.lbl_estado.config(text=msg[1])
                elif msg[0] == "nota":
                    self.lbl_nota.config(
                        text="Resolver n discos requiere 2ⁿ − 1 movimientos. Con 64 discos, "
                             f"incluso a 1 movimiento por segundo (como en la leyenda) "
                             f"tomaría {formatear_tiempo(msg[1])}.")
                elif msg[0] == "fin":
                    self.corriendo = False
                    self.btn_ini.config(state="normal")
                    self.btn_can.config(state="disabled")
                    self.barra["value"] = 100
                    if self.lbl_estado.cget("text") != "Cancelado.":
                        self.lbl_estado.config(text="Medición terminada.")
                    return
        except queue.Empty:
            pass

        self.barra["value"] = 100 * self.cont[0] / max(self.total, 1)
        self.win.after(100, self._sondear)


def main():
    root = tk.Tk()
    HanoiApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()