import random
import shutil

NUM_ALUMNOS = 100
NUM_MATERIAS = 100

# Nombres de las materias: "Materia 1", "Materia 2", ..., "Materia 100"
MATERIAS = [f"Materia {n}" for n in range(1, NUM_MATERIAS + 1)]

# Anchos de columna calculados según el número más grande de cada uno
ANCHO_ALUMNO = len("Alumno ") + len(str(NUM_ALUMNOS)) + 2
ANCHO_MATERIA = len("Materia ") + len(str(NUM_MATERIAS)) + 1

# Cuántas materias caben en una tabla según el ancho de tu terminal
ancho_terminal = shutil.get_terminal_size(fallback=(120, 30)).columns - 1
MATERIAS_POR_TABLA = max(1, (ancho_terminal - ANCHO_ALUMNO) // ANCHO_MATERIA)

# Arreglo (matriz) de NUM_ALUMNOS filas x NUM_MATERIAS columnas
# Cada celda contiene una calificación entera de 1 a 10
calificaciones = [
    [random.randint(1, 10) for _ in MATERIAS]
    for _ in range(NUM_ALUMNOS)
]


# Mostrar los alumnos en tablas: cada tabla trae un grupo de materias
# y una fila por alumno (como cabe en tu terminal)
for desde in range(0, NUM_MATERIAS, MATERIAS_POR_TABLA):
    hasta = min(desde + MATERIAS_POR_TABLA, NUM_MATERIAS)
    ancho_tabla = ANCHO_ALUMNO + ANCHO_MATERIA * (hasta - desde)

    print(f"\nMaterias {desde + 1} a {hasta}")
    print(f"{'Alumno':<{ANCHO_ALUMNO}}" + "".join(f"{m:<{ANCHO_MATERIA}}" for m in MATERIAS[desde:hasta]))
    print("-" * ancho_tabla)
    for i in range(NUM_ALUMNOS):
        notas = calificaciones[i][desde:hasta]
        print(f"{'Alumno ' + str(i + 1):<{ANCHO_ALUMNO}}" + "".join(f"{c:<{ANCHO_MATERIA}}" for c in notas))

# ---------------- BÚSQUEDA DE UN ALUMNO Y UNA MATERIA ----------------
def buscar_calificacion():
    print("\n=== Búsqueda de calificación ===")

    # Pedir número de alumno
    try:
        alumno = int(input(f"Número de alumno (1-{NUM_ALUMNOS}): "))
    except ValueError:
        print("Debes escribir un número.")
        return
    if not 1 <= alumno <= NUM_ALUMNOS:
        print(f"El alumno debe estar entre 1 y {NUM_ALUMNOS}.")
        return

    # Pedir materia por número (acepta "5" o "Materia 5")
    entrada = input(f"Materia (1-{NUM_MATERIAS}): ").lower().replace("materia", "").strip()
    if not entrada.isdigit() or not 1 <= int(entrada) <= NUM_MATERIAS:
        print(f"La materia debe ser un número entre 1 y {NUM_MATERIAS}.")
        return
    j = int(entrada) - 1

    nota = calificaciones[alumno - 1][j]
    print(f"\nAlumno {alumno} - {MATERIAS[j]}: {nota}")


while True:
    buscar_calificacion()
    if input("\n¿Buscar otra? (s/n): ").strip().lower() != "s":
        break