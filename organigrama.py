"""
Organigrama de empresa con recursividad anidada.

Caso real: un director tiene gerentes, cada gerente tiene supervisores,
y cada supervisor tiene empleados. No sabemos cuántos niveles hay,
así que la recursividad recorre toda la jerarquía.
"""

empresa = {
    "nombre": "Laura Méndez",
    "puesto": "Directora General",
    "sueldo": 90000,
    "equipo": [
        {
            "nombre": "Carlos Ruiz",
            "puesto": "Gerente de Ventas",
            "sueldo": 55000,
            "equipo": [
                {
                    "nombre": "Ana Torres",
                    "puesto": "Supervisora de Ventas",
                    "sueldo": 32000,
                    "equipo": [
                        {"nombre": "Luis Pech", "puesto": "Vendedor", "sueldo": 15000, "equipo": []},
                        {"nombre": "María Canul", "puesto": "Vendedora", "sueldo": 15000, "equipo": []},
                    ],
                },
                {"nombre": "Pedro Chan", "puesto": "Ejecutivo de Cuentas", "sueldo": 28000, "equipo": []},
            ],
        },
        {
            "nombre": "Sofía Herrera",
            "puesto": "Gerente de Tecnología",
            "sueldo": 60000,
            "equipo": [
                {
                    "nombre": "Diego Castro",
                    "puesto": "Líder de Desarrollo",
                    "sueldo": 42000,
                    "equipo": [
                        {"nombre": "Valeria Dzul", "puesto": "Programadora", "sueldo": 25000, "equipo": []},
                        {"nombre": "Jorge Uc", "puesto": "Programador", "sueldo": 25000, "equipo": []},
                        {"nombre": "Camila Ek", "puesto": "Diseñadora UX", "sueldo": 23000, "equipo": []},
                    ],
                },
            ],
        },
    ],
}


def mostrar_organigrama(persona, nivel=0):
    """Imprime la jerarquía con sangría según el nivel."""
    sangria = "    " * nivel
    print(f"{sangria}👤 {persona['nombre']} - {persona['puesto']}")
    for empleado in persona["equipo"]:
        mostrar_organigrama(empleado, nivel + 1)


def costo_nomina(persona):
    """Costo mensual de una persona más todo su equipo (directo e indirecto)."""
    total = persona["sueldo"]
    for empleado in persona["equipo"]:
        total += costo_nomina(empleado)
    return total


def contar_subordinados(persona):
    """Cuántas personas dependen de esta, directa o indirectamente."""
    total = len(persona["equipo"])
    for empleado in persona["equipo"]:
        total += contar_subordinados(empleado)
    return total


def cadena_de_mando(persona, buscado, camino=None):
    """Devuelve la lista de jefes desde la cima hasta la persona buscada."""
    camino = (camino or []) + [persona["nombre"]]
    if persona["nombre"] == buscado:
        return camino
    for empleado in persona["equipo"]:
        resultado = cadena_de_mando(empleado, buscado, camino)
        if resultado:
            return resultado
    return None


def dar_aumento(persona, porcentaje):
    """Aplica un aumento porcentual a toda la jerarquía hacia abajo."""
    persona["sueldo"] = round(persona["sueldo"] * (1 + porcentaje / 100))
    for empleado in persona["equipo"]:
        dar_aumento(empleado, porcentaje)


def buscar_por_puesto(persona, palabra):
    """Lista todas las personas cuyo puesto contenga la palabra dada."""
    encontrados = []
    if palabra.lower() in persona["puesto"].lower():
        encontrados.append(persona["nombre"])
    for empleado in persona["equipo"]:
        encontrados += buscar_por_puesto(empleado, palabra)
    return encontrados


if __name__ == "__main__":
    print("=== ORGANIGRAMA ===")
    mostrar_organigrama(empresa)

    print("\n=== ESTADÍSTICAS ===")
    print(f"Nómina total mensual: ${costo_nomina(empresa):,}")
    print(f"Personas en la empresa (sin contar a la directora): {contar_subordinados(empresa)}")

    gerente_ventas = empresa["equipo"][0]
    print(f"Nómina del área de Ventas: ${costo_nomina(gerente_ventas):,}")

    print("\n=== CADENA DE MANDO ===")
    ruta = cadena_de_mando(empresa, "Jorge Uc")
    print(" -> ".join(ruta))

    print("\n=== BÚSQUEDA POR PUESTO ===")
    print("Programadores:", buscar_por_puesto(empresa, "programador"))

    print("\n=== AUMENTO DEL 10% AL ÁREA DE TECNOLOGÍA ===")
    gerente_tec = empresa["equipo"][1]
    antes = costo_nomina(gerente_tec)
    dar_aumento(gerente_tec, 10)
    despues = costo_nomina(gerente_tec)
    print(f"Antes: ${antes:,}  |  Después: ${despues:,}")