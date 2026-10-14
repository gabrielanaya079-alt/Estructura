# Torre de Hanoi en Python 

Programa en Python con interfaz gráfica (`tkinter`) que permite **jugar** la Torre de Hanoi o dejar que **la computadora la resuelva sola**, y que además **mide el tiempo** que tarda en resolver 5, 10, 30 y 64 discos.

## Funcionalidades

- **Jugar tú:** clic en una torre para levantar su disco superior y clic en otra para soltarlo.
- **Resolver solo:** la computadora resuelve con animación y velocidad ajustable.
- **Medir tiempos:** ventana que resuelve (o estima) 5, 10, 30 y 64 discos.


## Estructura del código

El programa maneja **30 elementos** entre funciones y métodos:

- **7 funciones** a nivel de módulo
- **23 métodos** repartidos en **2 clases** (`HanoiApp` con 16 y `VentanaBenchmark` con 7)
- 1 clase de excepción auxiliar (`Cancelado`)

### Funciones del módulo (7)

| Función | Explicación breve |
|---|---|
| `crear_torres(n)` | Crea las 3 torres; la primera con `n` discos (el más grande abajo). |
| `generar_movimientos(n, o, d, a)` | Generador recursivo que va entregando cada movimiento `(origen, destino)`; se usa para la animación. |
| `resolver_rapido(...)` | Resuelve moviendo discos de verdad, sin dibujar; sirve para medir tiempos y se puede cancelar. |
| `formatear_tiempo(seg)` | Convierte segundos a µs, ms, s, min, horas, días o años. |
| `color_disco(d, n)` | Asigna un color distinto a cada disco. |
| `oscurecer(color, f)` | Oscurece un color para el borde y el número del disco. |
| `main()` | Crea la ventana y arranca la aplicación. |

### Clase `HanoiApp` – ventana principal (16 métodos)

| Método | Explicación breve |
|---|---|
| `__init__` | Inicializa el estado del juego y construye la interfaz. |
| `_construir_ui` | Crea botones, selector de discos, velocidad, lienzo y etiquetas. |
| `_leer_n` | Lee y valida la cantidad de discos (1 a 10). |
| `nuevo_juego` | Reinicia torres, contador y tiempo. |
| `mensaje` | Muestra mensajes y errores al usuario. |
| `actualizar_info` | Actualiza movimientos realizados y mínimo posible. |
| `_tick` | Actualiza el cronómetro cada 100 ms. |
| `alto_disco` | Calcula el alto de cada disco según la cantidad. |
| `dibujar` | Redibuja base, torres y discos. |
| `_disco` | Dibuja un disco individual. |
| `on_click` | Maneja los clics del jugador (elegir origen y destino). |
| `intentar_mover` | Valida la regla (no poner grande sobre pequeño), mueve y detecta la victoria. |
| `resolver_solo` | Inicia la resolución automática animada. |
| `_paso_auto` | Ejecuta un movimiento de la animación y programa el siguiente. |
| `detener_auto` | Pausa la resolución automática. |
| `abrir_benchmark` | Abre la ventana de medición de tiempos. |

### Clase `VentanaBenchmark` – medición de tiempos (7 métodos)

| Método | Explicación breve |
|---|---|
| `__init__` | Construye la ventana con la tabla, barra de progreso y botones. |
| `_reiniciar_filas` | Deja la tabla en estado «pendiente». |
| `iniciar` | Lanza la medición en un hilo aparte para no congelar la ventana. |
| `cerrar` | Cancela la medición y cierra la ventana. |
| `_ejecutar` | Resuelve `n` discos de verdad y devuelve movimientos y tiempo. |
| `_trabajo` | Hilo que mide 5 y 10, calibra con 20, y mide o estima 30 y 64. |
| `_sondear` | Lee los resultados del hilo y actualiza tabla y progreso. |

---

## Resultados de tiempo

Resolver `n` discos requiere **2ⁿ − 1 movimientos**. Se hicieron dos ejecuciones en la misma computadora:

### Ejecución 1: 30 discos ejecutados de verdad

| Discos | Movimientos | Tiempo | Tipo |
|:---:|---:|---:|:---:|
| 5 | 31 | 45.6 µs | medido |
| 10 | 1,023 | 1.22 ms | medido |
| 30 | 1,073,741,823 | 10.10 min | medido |
| 64 | 18,446,744,073,709,551,615 | 385,430 años | estimado |

### Ejecución 2: 30 discos estimado (sin ejecutarlo)

| Discos | Movimientos | Tiempo | Tipo |
|:---:|---:|---:|:---:|
| 5 | 31 | 47.1 µs | medido |
| 10 | 1,023 | 736.3 µs | medido |
| 30 | 1,073,741,823 | 8.54 min | estimado |
| 64 | 18,446,744,073,709,551,615 | 279,013 años | estimado |



## Conclusiones

### 1. Crecimiento exponencial
Cada disco extra **duplica** el número de movimientos (2ⁿ − 1). Pasar de 5 a 10 discos multiplica el trabajo por ~33; de 10 a 30, por más de un millón. Por eso el tiempo pasa de **microsegundos** (5 discos) a **minutos** (30 discos) y a **cientos de miles de años** (64 discos). Con 64 discos, incluso a 1 movimiento por segundo (como en la leyenda) tomaría unos 585 mil millones de años. Es un problema correcto pero **no resoluble en la práctica**.

### 2. Cada torre es una pila (LIFO)
Cada torre funciona como una **pila (stack)** con la regla **LIFO** (*Last In, First Out*: el último en entrar es el primero en salir):

| Concepto de la pila | En la Torre de Hanoi | En el código |
|---|---|---|
| `push` (apilar) | Colocar un disco en una torre | `torres[destino].append(disco)` |
| `pop` (desapilar) | Quitar el disco de arriba | `torres[origen].pop()` |
| `top` (cima) | Único disco accesible | `torres[i][-1]` |

**Es como una pila de platos, ya que solo puedes tomar el de arriba, y para llegar al de abajo primero debes mover todos los de encima. Justo por eso el disco más grande solo se mueve cuando los demás ya están en las otras torres.** 

La regla es que nunca se puede poner un disco grande sobre uno pequeño. puesto que es una pila **ordenada**: lo que se apila debe ser menor que la cima actual. Se verifica en `intentar_mover` comparando con `torres[destino][-1]`.

### 3. La recursión también usa una pila
`resolver_rapido` es recursiva y Python guarda cada llamada pendiente en la **pila de llamadas** (*call stack*), que también es LIFO: la última llamada abierta es la primera en terminar. Esto da una conclusión interesante:

- **Tiempo:** crece como O(2ⁿ) (explosivo).
- **Memoria de la recursión:** crece solo como O(n), porque la pila tiene profundidad máxima `n`. Con 64 discos solo habría ~64 llamadas anidadas.

El problema es **barato en memoria pero carísimo en tiempo**.
