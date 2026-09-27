class ventasMensuales:

    MESES = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    DEPARTAMENTOS = ["Ropa", "Deportes", "Jugueteria"]

    def __init__(self):

        filas = len(self.MESES)
        columnas = len(self.DEPARTAMENTOS)
        self.ventas = [[0 for _ in range(columnas)] for _ in range(filas)]

    def _obtener_indice_mes(self, mes):
        mes = mes.strip().capitalize()
        if mes not in self.MESES:
            raise ValueError(f"El mes '{mes}' no es válido.")
        return self.MESES.index(mes)

    def _obtener_indice_departamento(self, departamento):
        depto_normalizado = (
            departamento.strip()
            .capitalize()
            .replace("í", "i")
        )
        deptos_normalizados = [d.replace("í", "i") for d in self.DEPARTAMENTOS]
        if depto_normalizado not in deptos_normalizados:
            raise ValueError(f"El departamento '{departamento}' no es válido.")
        return deptos_normalizados.index(depto_normalizado)

    # -------- 1. Insertar --------
    def insertar_venta(self, mes, departamento, monto):
        """Inserta o actualiza el monto de venta de un mes y departamento."""
        if monto < 0:
            raise ValueError("El monto de la venta no puede ser negativo.")
        fila = self._obtener_indice_mes(mes)
        columna = self._obtener_indice_departamento(departamento)
        self.ventas[fila][columna] = monto
        print(f"[OK] Venta insertada: {mes} - {departamento} = ${monto}")

    # -------- 2. Buscar --------
    def buscar_venta(self, mes, departamento):
        """Busca y retorna el monto de venta de un mes y departamento en particular."""
        fila = self._obtener_indice_mes(mes)
        columna = self._obtener_indice_departamento(departamento)
        monto = self.ventas[fila][columna]
        print(f"[BUSQUEDA] {mes} - {departamento}: ${monto}")
        return monto

    # -------- 3. Eliminar --------
    def eliminar_venta(self, mes, departamento):
        """Elimina (pone en 0) la venta de un mes y departamento en particular."""
        fila = self._obtener_indice_mes(mes)
        columna = self._obtener_indice_departamento(departamento)
        monto_anterior = self.ventas[fila][columna]
        self.ventas[fila][columna] = 0
        print(f"[OK] Venta eliminada: {mes} - {departamento} (era ${monto_anterior})")

    # -------- Utilidad extra: mostrar la tabla completa --------
    def mostrar_tabla(self):
        encabezado = f"{'':12}" + "".join(f"{depto:>12}" for depto in self.DEPARTAMENTOS)
        print(encabezado)
        print("-" * len(encabezado))
        for i, mes in enumerate(self.MESES):
            fila = f"{mes:12}" + "".join(f"{self.ventas[i][j]:>12}" for j in range(len(self.DEPARTAMENTOS)))
            print(fila)

if __name__ == "__main__":
    sistema = ventasMensuales()

    # 1. Insertar ventas
    sistema.insertar_venta("Enero", "Ropa", 1500)
    sistema.insertar_venta("Enero", "Deportes", 2300)
    sistema.insertar_venta("Enero", "Jugueteria", 800)
    sistema.insertar_venta("Febrero", "Ropa", 1750)
    sistema.insertar_venta("Diciembre", "Jugueteria", 5200)

    print("\n--- Tabla de ventas ---")
    sistema.mostrar_tabla()

    # 2. Buscar una venta
    print("\n--- Búsqueda ---")
    sistema.buscar_venta("Enero", "Deportes")

    # 3. Eliminar una venta
    print("\n--- Eliminación ---")
    sistema.eliminar_venta("Enero", "Ropa")

    print("\n--- Tabla después de eliminar ---")
    sistema.mostrar_tabla()