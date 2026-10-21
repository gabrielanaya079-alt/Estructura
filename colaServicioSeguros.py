class Cola:
    def __init__(self):
        self.items = []

    def encolar(self, elemento):
        self.items.append(elemento)

    def desencolar(self):
        return self.items.pop(0)

    def esta_vacia(self):
        return len(self.items) == 0

    def tamano(self):
        return len(self.items)


SERVICIOS = {
    1: "Siniestros",
    2: "Contratación de pólizas",
    3: "Pagos y cobranzas",
    4: "Consultas generales",
}


class SistemaAtencion:
    def __init__(self, servicios):
        self.nombres = servicios
        self.colas = {num: Cola() for num in servicios}
        # Último número entregado en cada servicio
        self.ultimo_numero = {num: 0 for num in servicios}

    def llegada_cliente(self, servicio):
        self.ultimo_numero[servicio] += 1
        numero = self.ultimo_numero[servicio]
        self.colas[servicio].encolar(numero)
        return numero

    def atender_cliente(self, servicio):
        if self.colas[servicio].esta_vacia():
            return None
        return self.colas[servicio].desencolar()

    def mostrar_estado(self):
        print("\n--- Estado de las colas ---")
        for num, nombre in self.nombres.items():
            print(f"Servicio {num} ({nombre}): {self.colas[num].tamano()} en espera")


def interpretar_comando(texto):
    texto = texto.strip().upper().replace(" ", "")
    if len(texto) < 2 or texto[0] not in ("C", "A") or not texto[1:].isdigit():
        return None
    return texto[0], int(texto[1:])


def main():
    sistema = SistemaAtencion(SERVICIOS)

    print("=== Sistema de atención - Compañía de seguros ===")
    print("Servicios disponibles:")
    for num, nombre in SERVICIOS.items():
        print(f"  {num} - {nombre}")
    print("\nComandos:")
    print("  C <n°>  -> llega un cliente al servicio (ej: C 1)")
    print("  A <n°>  -> atender al siguiente cliente del servicio (ej: A 1)")
    print("  E       -> ver estado de las colas")
    print("  S       -> salir")

    while True:
        entrada = input("\n> ").strip()

        if entrada.upper() == "S":
            print("Fin del programa.")
            break
        if entrada.upper() == "E":
            sistema.mostrar_estado()
            continue

        comando = interpretar_comando(entrada)
        if comando is None:
            print("Comando no válido. Use C o A seguido del número de servicio.")
            continue

        letra, servicio = comando
        if servicio not in SERVICIOS:
            print(f"El servicio {servicio} no existe.")
            continue

        if letra == "C":
            numero = sistema.llegada_cliente(servicio)
            print(f"Su número de atención es: {numero} "
                  f"(Servicio {servicio} - {SERVICIOS[servicio]})")
        else:
            numero = sistema.atender_cliente(servicio)
            if numero is None:
                print(f"No hay clientes en espera en el servicio {servicio}.")
            else:
                print(f"Llamando al número {numero} "
                      f"(Servicio {servicio} - {SERVICIOS[servicio]})")


if __name__ == "__main__":
    main()