import json
import os

ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "postres.json")


class Nodo:
    def __init__(self, ingrediente):
        self.ingrediente = ingrediente
        self.sig = None


class ListaIngredientes:
    def __init__(self):
        self.cabeza = None

    def esta_vacia(self):
        return self.cabeza is None

    def __len__(self):
        n, act = 0, self.cabeza
        while act:
            n, act = n + 1, act.sig
        return n

    def a_lista(self):
        res, act = [], self.cabeza
        while act:
            res.append(act.ingrediente)
            act = act.sig
        return res

    def buscar(self, ingrediente):
        clave = ingrediente.lower()
        act = self.cabeza
        while act:
            if act.ingrediente.lower() == clave:
                return act
            act = act.sig
        return None

    def insertar_final(self, ingrediente):
        if self.buscar(ingrediente):
            return False
        nuevo = Nodo(ingrediente)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            act = self.cabeza
            while act.sig:
                act = act.sig
            act.sig = nuevo
        return True

    def eliminar(self, ingrediente):
        clave = ingrediente.lower()
        ant, act = None, self.cabeza
        while act and act.ingrediente.lower() != clave:
            ant, act = act, act.sig
        if act is None:
            return False
        if ant is None:
            self.cabeza = act.sig
        else:
            ant.sig = act.sig
        act.sig = None
        return True

    def vaciar(self):
        act = self.cabeza
        while act:
            sig = act.sig
            act.sig = None
            act = sig
        self.cabeza = None


class Postre:
    def __init__(self, nombre):
        self.nombre = nombre
        self.ingredientes = ListaIngredientes()


POSTRES = []


def clave(texto):
    return texto.strip().lower()


def buscar_postre(nombre):
    k = clave(nombre)
    ini, fin = 0, len(POSTRES) - 1
    while ini <= fin:
        mid = (ini + fin) // 2
        km = clave(POSTRES[mid].nombre)
        if km == k:
            return True, mid
        if km < k:
            ini = mid + 1
        else:
            fin = mid - 1
    return False, ini


def pedir_texto(mensaje):
    txt = input(mensaje).strip()
    if not txt:
        print("  [Error] La entrada no puede estar vacía.")
        return None
    return txt


def pedir_ingredientes(mensaje):
    crudo = input(mensaje).split(",")
    vistos, res = set(), []
    for ing in crudo:
        ing = ing.strip()
        if ing and ing.lower() not in vistos:
            vistos.add(ing.lower())
            res.append(ing)
    return res


def listar_ingredientes(nombre):
    if not POSTRES:
        print("  [Error] El arreglo POSTRES está vacío.")
        return
    ok, i = buscar_postre(nombre)
    if not ok:
        print(f"  [Error] El postre '{nombre}' no existe.")
        return
    ings = POSTRES[i].ingredientes.a_lista()
    if not ings:
        print(f"  '{POSTRES[i].nombre}' no tiene ingredientes registrados.")
    else:
        print(f"  Ingredientes de {POSTRES[i].nombre}:")
        for n, ing in enumerate(ings, 1):
            print(f"    {n}. {ing}")


def insertar_ingredientes(nombre, nuevos):
    ok, i = buscar_postre(nombre)
    if not ok:
        print(f"  [Error] El postre '{nombre}' no existe.")
        return
    if not nuevos:
        print("  [Error] No se proporcionó ningún ingrediente válido.")
        return
    for ing in nuevos:
        if POSTRES[i].ingredientes.insertar_final(ing):
            print(f"  + '{ing}' agregado.")
        else:
            print(f"  [Aviso] '{ing}' ya estaba en la lista; no se duplicó.")


def eliminar_ingrediente(nombre, ingrediente):
    ok, i = buscar_postre(nombre)
    if not ok:
        print(f"  [Error] El postre '{nombre}' no existe.")
        return
    lista = POSTRES[i].ingredientes
    if lista.esta_vacia():
        print("  [Error] El postre no tiene ingredientes que eliminar.")
    elif lista.eliminar(ingrediente):
        print(f"  - '{ingrediente}' eliminado.")
        if lista.esta_vacia():
            print("  [Aviso] El postre se quedó sin ingredientes.")
    else:
        print(f"  [Error] '{ingrediente}' no está en la lista de {POSTRES[i].nombre}.")


def alta_postre(nombre, ingredientes):
    ok, pos = buscar_postre(nombre)
    if ok:
        print(f"  [Error] El postre '{nombre}' ya existe (no se permiten repetidos).")
        return
    p = Postre(nombre.strip())
    for ing in ingredientes:
        p.ingredientes.insertar_final(ing)
    POSTRES.insert(pos, p)
    print(f"  Postre '{p.nombre}' dado de alta con {len(p.ingredientes)} ingrediente(s).")
    if not ingredientes:
        print("  [Aviso] Se registró sin ingredientes.")


def baja_postre(nombre):
    if not POSTRES:
        print("  [Error] El arreglo POSTRES está vacío.")
        return
    ok, i = buscar_postre(nombre)
    if not ok:
        print(f"  [Error] El postre '{nombre}' no existe.")
        return
    POSTRES[i].ingredientes.vaciar()
    borrado = POSTRES.pop(i)
    print(f"  Postre '{borrado.nombre}' y todos sus ingredientes eliminados.")


def mostrar_todo():
    if not POSTRES:
        print("  (POSTRES vacío)")
        return
    for i, p in enumerate(POSTRES):
        print(f"  [{i}] {p.nombre} -> " +
              (" -> ".join(p.ingredientes.a_lista()) + " -> NIL"
               if not p.ingredientes.esta_vacia() else "NIL"))


def eliminar_repetidos(fusionar=False):
    reporte = []
    if len(POSTRES) < 2:
        return reporte
    escritura = 0
    for lectura in range(1, len(POSTRES)):
        actual, base = POSTRES[lectura], POSTRES[escritura]
        if clave(actual.nombre) == clave(base.nombre):
            ings = actual.ingredientes.a_lista()
            if fusionar:
                nuevos = [x for x in ings if base.ingredientes.insertar_final(x)]
                reporte.append((actual.nombre, ings, f"fusionados {nuevos}"))
            else:
                reporte.append((actual.nombre, ings, "descartada"))
            actual.ingredientes.vaciar()
        else:
            escritura += 1
            POSTRES[escritura] = actual
    del POSTRES[escritura + 1:]
    return reporte


def demo_repetidos():
    global POSTRES
    respaldo = POSTRES
    POSTRES = []
    datos = [("Flan", ["huevo", "leche", "azúcar"]),
             ("Flan", ["huevo", "vainilla"]),
             ("Gelatina", ["grenetina", "agua"]),
             ("Pastel", ["harina", "huevo"]),
             ("pastel", ["chocolate"]),
             ("Pastel", [])]
    for nom, ings in datos:
        p = Postre(nom)
        for ing in ings:
            p.ingredientes.insertar_final(ing)
        POSTRES.append(p)
    POSTRES.sort(key=lambda p: clave(p.nombre))
    print("ANTES:")
    mostrar_todo()
    rep = eliminar_repetidos(fusionar=False)
    print("\nDuplicados eliminados:")
    for nom, ings, destino in rep:
        print(f"  '{nom}': lista {ings or '(vacía)'} -> {destino}")
    print("\nDESPUÉS:")
    mostrar_todo()
    POSTRES = respaldo
    print("\n(La demostración no modificó tus postres guardados.)")


def guardar():
    datos = [{"nombre": p.nombre, "ingredientes": p.ingredientes.a_lista()} for p in POSTRES]
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def cargar():
    global POSTRES
    POSTRES = []
    if not os.path.exists(ARCHIVO):
        return
    try:
        with open(ARCHIVO, encoding="utf-8") as f:
            datos = json.load(f)
        for d in datos:
            p = Postre(d["nombre"])
            for ing in d["ingredientes"]:
                p.ingredientes.insertar_final(ing)
            POSTRES.append(p)
        POSTRES.sort(key=lambda p: clave(p.nombre))
    except (ValueError, KeyError, OSError):
        print("  [Aviso] No se pudo leer postres.json; se inicia con POSTRES vacío.")


def alta_forzada(nombre, ingredientes):
    if not nombre.strip():
        print("  [Error] El nombre no puede estar vacío.")
        return
    _, pos = buscar_postre(nombre)
    while pos < len(POSTRES) and clave(POSTRES[pos].nombre) <= clave(nombre):
        pos += 1
    p = Postre(nombre.strip())
    for ing in ingredientes:
        p.ingredientes.insertar_final(ing)
    POSTRES.insert(pos, p)
    print(f"  Postre '{p.nombre}' registrado (duplicado permitido para pruebas).")


def ejecutar_eliminar_repetidos():
    antes = len(POSTRES)
    if antes < 2:
        print("  No hay suficientes postres para buscar repetidos.")
        return
    f = input("¿Fusionar los ingredientes del duplicado en el que se conserva? (s/n): ").strip().lower()
    rep = eliminar_repetidos(fusionar=(f == "s"))
    if not rep:
        print("  No se encontraron postres repetidos.")
        return
    print("  Duplicados eliminados:")
    for nom, ings, destino in rep:
        print(f"    '{nom}': lista {ings or '(vacía)'} -> {destino}")
    print(f"  Elementos: {antes} -> {len(POSTRES)}")


def menu():
    opciones = """
=== POSTRES ===
1. Ver ingredientes de un postre
2. Insertar ingredientes a un postre
3. Eliminar un ingrediente de un postre
4. Alta de postre
5. Baja de postre
6. Mostrar toda la estructura
7. Eliminar postres repetidos (ejercicio 3)
8. Alta FORZADA (permite repetidos, para probar la opción 7)
9. Demostración del ejercicio 3 (no modifica tus datos)
0. Salir"""
    cargar()
    while True:
        print(opciones)
        op = input("Opción: ").strip()
        if op == "0":
            break
        elif op in ("1", "2", "3", "4", "5", "8"):
            nom = pedir_texto("Nombre del postre: ")
            if nom is None:
                continue
            if op == "1":
                listar_ingredientes(nom)
            elif op == "2":
                insertar_ingredientes(nom, pedir_ingredientes("Ingredientes (separados por coma): "))
            elif op == "3":
                ing = pedir_texto("Ingrediente a eliminar: ")
                if ing:
                    eliminar_ingrediente(nom, ing)
            elif op == "4":
                existe, _ = buscar_postre(nom)
                if existe:
                    r = input(f"  '{nom}' ya existe. ¿Registrarlo de todos modos como repetido? (s/n): ").strip().lower()
                    if r == "s":
                        alta_forzada(nom, pedir_ingredientes("Ingredientes (separados por coma): "))
                    else:
                        print("  Alta cancelada.")
                else:
                    ings = pedir_ingredientes("Ingredientes (separados por coma): ")
                    alta_postre(nom, ings)
            elif op == "5":
                baja_postre(nom)
            else:
                alta_forzada(nom, pedir_ingredientes("Ingredientes (separados por coma): "))
            guardar()
        elif op == "6":
            mostrar_todo()
        elif op == "7":
            ejecutar_eliminar_repetidos()
            guardar()
        elif op == "9":
            demo_repetidos()
        else:
            print("  [Error] Opción inválida.")


if __name__ == "__main__":
    menu()