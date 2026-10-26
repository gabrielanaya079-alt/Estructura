__all__ = ["Nodo", "ListaEnlazada"]


class Nodo:
    def __init__(self, info):
        self.info = info
        self.liga = None         


class ListaEnlazada:
    def __init__(self):
        self.p = None            

    # ---------- Recorrido seguro ----------
    def _recorrer(self):
        visitados = set()
        actual = self.p
        while actual is not None and id(actual) not in visitados:
            visitados.add(id(actual))
            yield actual
            actual = actual.liga

    def longitud(self):
        contador = 0
        for _ in self._recorrer():
            contador += 1
        return contador

    def esta_vacia(self):
        return self.p is None

    def __len__(self):
        return self.longitud()

    def tiene_ciclo(self):
        ultimo = None
        for nodo in self._recorrer():
            ultimo = nodo
        return ultimo is not None and ultimo.liga is not None

    def _nodo_en(self, posicion):
        contador = 1
        for nodo in self._recorrer():
            if contador == posicion:
                return nodo
            contador += 1
        return None

    # ---------- Inserciones ----------
    def agregar_inicio(self, info):
        q = Nodo(info)
        q.liga = self.p          
        self.p = q            

    def agregar_final(self, info):
        if self.tiene_ciclo():    
            return False
        q = Nodo(info)
        if self.p is None:        
            self.p = q
            return True
        actual = self.p
        while actual.liga is not None:   
            actual = actual.liga
        actual.liga = q
        return True

    def agregar_medio(self, info, posicion):
        if posicion <= 1 or self.p is None:
            self.agregar_inicio(info)
            return
        q = Nodo(info)
        actual = self.p
        contador = 1
        while actual.liga is not None and contador < posicion - 1:
            actual = actual.liga
            contador += 1
        q.liga = actual.liga
        actual.liga = q

    # ---------- Eliminaciones ----------
    def eliminar_por_posicion(self, posicion):
        if self.p is None or posicion < 1 or posicion > self.longitud():
            return False

        if posicion == 1:                
            self.p = self.p.liga          
            return True

        anterior = self.p
        contador = 1
        while contador < posicion - 1:
            anterior = anterior.liga
            contador += 1
        anterior.liga = anterior.liga.liga   
        return True

    def eliminar_por_dato(self, dato):
        if self.p is None or self.tiene_ciclo():
            return False

        if self.p.info == dato:         
            self.p = self.p.liga
            return True

        anterior = self.p
        actual = self.p.liga
        while actual is not None and actual.info != dato:
            anterior = actual
            actual = actual.liga

        if actual is None:             
            return False

        anterior.liga = actual.liga      
        return True

    # ---------- Búsqueda ----------
    def buscar(self, dato):
        posicion = 1
        for nodo in self._recorrer():     
            if nodo.info == dato:
                return posicion
            posicion += 1
        return None

    # ---------- Dos nodos apuntando a un mismo nodo ----------
    def apuntar_mismo_nodo(self, pos_a, pos_b, pos_destino):
        n = self.longitud()
        posiciones = (pos_a, pos_b, pos_destino)

        if any(pos < 1 or pos > n for pos in posiciones):
            return None
        if len(set(posiciones)) < 3:     
            return None

        nodo_a = self._nodo_en(pos_a)
        nodo_b = self._nodo_en(pos_b)
        destino = self._nodo_en(pos_destino)

        nodo_a.liga = destino             # A^.LIGA <- D
        nodo_b.liga = destino             # B^.LIGA <- D
        return nodo_a, nodo_b, destino

    # ---------- Guardar y cargar ----------
    def guardar(self, archivo):
        total = 0
        with open(archivo, "w", encoding="utf-8") as f:
            for nodo in self._recorrer():
                f.write(str(nodo.info) + "\n")
                total += 1
        return total

    def cargar(self, archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            datos = [linea.rstrip("\n") for linea in f]

        self.p = None                  
        ultimo = None
        for dato in datos:
            q = Nodo(dato)
            if self.p is None:
                self.p = q               
            else:
                ultimo.liga = q           
            ultimo = q
        return len(datos)

    # ---------- Recorrido / Mostrar ----------
    def __str__(self):
        if self.p is None:
            return "La lista está vacía."
        partes = []
        ultimo = None
        for nodo in self._recorrer():
            partes.append(str(nodo.info))
            ultimo = nodo
        if ultimo.liga is None:
            final = "NIL"
        else:
            final = f"(regresa a {ultimo.liga.info})"
        return " -> ".join(partes) + " -> " + final

    def mostrar(self):
        print(self)