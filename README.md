Para crear un arreglo bidimensional en Python, creamos dos listas: una llamada "Meses" y la otra "Departamentos", ya que en Python no existen los arrays a excepción con Java.

Posteriormente, creamos un método constructor el cual será el encargado de crear una matriz vacía de 12 filas(meses) x 3 columnas(departamentos). En "filas = len(self.MESES)" y "columnas = len(self.DEPARTAMENTOS)" la función len, sirve para contar los elementos que tiene cada lista.

"self.ventas = [[0 for _ in range(columnas)] for _ in range(filas)]"

0 for _ in range(columnas) Esto es una comprensión de lista (list comprehension): una forma compacta de escribir un bucle for que construye una lista. Se lee así: "por cada elemento en range(columnas), produce el valor 0". El _ es una variable de bucle "descartable": Python exige poner un nombre de variable en el for, pero como no nos importa su valor (solo queremos repetir 3 veces), se usa _ por convención, para indicar que esta variable no se usa. El resultado de [0 for _ in range(columnas)] es una lista: [0, 0, 0] (una fila con 3 ceros, uno por departamento).

La capa exterior, [ ... for _ in range(filas)], sigue la misma lógica que la interior, pero en vez de repetir el número 0, repite la lista completa [0, 0, 0] que ya construimos, y lo hace filas veces (12 veces, una por mes). Se lee: "por cada elemento en range(filas), produce una lista nueva [0, 0, 0]". La palabra clave es "nueva": en cada vuelta del bucle, Python ejecuta de cero la comprensión interna y crea una lista [0, 0, 0] independiente, en lugar de reutilizar siempre la misma. Por eso el resultado son 12 filas separadas en memoria, que se ven iguales al inicio pero pueden modificarse una sin afectar a las demás.

Métodos

-Obtener índice del mes:
mes = mes.strip().capitalize()

.strip() quita espacios sobrantes (para que " enero " funcione igual que "Enero").
.capitalize() pone la primera letra en mayúscula y el resto en minúscula (para que "ENERO" o "enero" también funcionen)

Se crea un "if" para buscar si el mes que se escribió se encuentra en la lista de meses, si esto no es así, lanza la excepción "ValueError", y si sí, retorna self.MESES.index(mes) ".index(…)" Busca dentro de la lista el primer elemento que sea igual al valor que le pasas, y devuelve su posición (un número entero, empezando en 0). Esta línea toma el nombre del mes ya validado, encuentra en qué posición de la lista MESES está ubicado, y devuelve ese número como resultado del método _obtener_indice_mes. Ese número es justamente la "fila" que después se usa para acceder a self.ventas[fila][columna].

-Obtener índice departamento:
Hace lo mismo que el método anterior, pero con un paso extra: .replace("í", "i"), tanto en el texto ingresado como en la lista DEPARTAMENTOS. Esto es para que "Jugueteria" (sin tilde) y "Juguetería" (con tilde) se reconozcan como lo mismo, evitando errores por acentos.

-Insertar venta:

Este método comienza con `def insertar_venta(self, mes, departamento, monto):`, que define una función dentro de la clase con tres parámetros además de `self`: el mes, el departamento y el monto a insertar. Luego viene una validación: `if monto < 0: raise ValueError(...)`, que comprueba si el monto es negativo y, de ser así, detiene la ejecución lanzando un error. Después, `fila = self._obtener_indice_mes(mes)` llama al método auxiliar que ya vimos, el cual valida y traduce el nombre del mes a su posición numérica en la lista `MESES`; de forma análoga, `columna = self._obtener_indice_departamento(departamento)` hace lo mismo pero con el departamento, devolviendo su posición en `DEPARTAMENTOS`.

Con esas dos coordenadas ya calculadas, `self.ventas[fila][columna] = monto` accede directamente a esa celda específica de la matriz bidimensional y le **asigna** el nuevo valor (sobreescribiendo lo que hubiera antes, por eso el método sirve tanto para insertar como para actualizar). Finalmente, `print(f"[OK] Venta insertada: {mes} - {departamento} = ${monto}")` usa un f-string (una cadena con variables incrustadas entre llaves `{}`) para mostrar en pantalla un mensaje de confirmación legible, insertando los valores originales de `mes`, `departamento` y `monto` tal como los recibió el método (sin normalizar), para que el usuario vea exactamente lo que escribió.

-Buscar Venta

Este método comienza con `def buscar_venta(self, mes, departamento):`, que define la función con dos parámetros: el mes y el departamento que se quieren consultar. 

La diferencia clave frente a `insertar_venta` está en la siguiente línea: `monto = self.ventas[fila][columna]` **lee** el valor que ya existe en esa celda (en vez de asignarle uno nuevo) y lo guarda en la variable local `monto`. Después, `print(f"[BUSQUEDA] {mes} - {departamento}: ${monto}")` muestra en pantalla un mensaje informativo con ese valor encontrado. Por último, `return monto` es lo que hace que este método sea distinto a los demás: además de imprimir el resultado, **lo devuelve** como valor de salida, para que quien llame a `buscar_venta(...)` pueda guardar ese número en una variable y usarlo después en el programa (por ejemplo, para hacer cálculos), en vez de solo verlo impreso en consola.

-Eliminar Venta
Este método comienza con def eliminar_venta(self, mes, departamento):; y las siguientes líneas hacen exactamente lo mismo que los dos métodos anteriores, sin embargo, cambian en la siguiente linea:
monto_anterior = self.ventas[fila][columna] el cual lee y guarda el valor que había en esa celda antes de modificarlo (esto es solo para poder mostrarlo después en el mensaje; es un paso informativo, no necesario para la eliminación en sí). Justo después, self.ventas[fila][columna] = 0 hace el trabajo real: sobreescribe esa celda con 0, que es la forma en que este programa representa "no hay venta ahí". Ojo, la fila y la columna en sí no desaparecen de la matriz (eso rompería sus dimensiones fijas de 12×3); solo se resetea el valor a cero. Finalmente, print(f"[OK] Venta eliminada: {mes} - {departamento} (era ${monto_anterior})") imprime un mensaje de confirmación que incluye, entre paréntesis, cuál era el monto justo antes de eliminarlo, usando la variable guardada en el paso anterior.

-Mostrar tabla
El método `mostrar_tabla(self)` no recibe parámetros extra porque usa los datos que ya tiene el objeto. Primero arma el encabezado: `f"{'':12}"` deja un espacio en blanco de 12 caracteres para la esquina superior izquierda, y se le suma `"".join(f"{depto:>12}" for depto in self.DEPARTAMENTOS)`, que recorre `DEPARTAMENTOS` y alinea cada nombre a la derecha en 12 caracteres, uniendo todo en una sola línea. Luego `print(encabezado)` lo muestra, y `print("-" * len(encabezado))` imprime una línea de guiones del mismo largo como separador.

Después viene el cuerpo de la tabla: `for i, mes in enumerate(self.MESES)` recorre los meses obteniendo a la vez su índice `i` (para acceder a la matriz) y su nombre. En cada vuelta, `f"{mes:12}"` alinea el nombre del mes a la izquierda en 12 caracteres, y se le suma `"".join(f"{self.ventas[i][j]:>12}" for j in range(len(self.DEPARTAMENTOS)))`, que recorre las 3 columnas (`j`), toma el valor `self.ventas[i][j]` de esa celda y lo alinea a la derecha en 12 caracteres. `print(fila)` imprime esa línea completa, y al repetirse por cada mes, se construye la tabla entera fila por fila.

Uso

`if __name__ == "__main__":` hace que este bloque solo se ejecute cuando corres el archivo directamente (no si lo importas desde otro lado).

`sistema = ventasMensuales()` crea un objeto de la clase, ejecutando el constructor que arma la matriz vacía, y lo guarda en la variable `sistema` para usarla en las siguientes líneas.

Las cinco líneas de `sistema.insertar_venta(...)` llaman al método varias veces con distintos valores, guardando cada monto en su celda correspondiente de la matriz.

`print("\n--- Tabla de ventas ---")` imprime un título, y `sistema.mostrar_tabla()` muestra la matriz completa ya con los datos insertados.

`sistema.buscar_venta("Enero", "Deportes")` busca esa celda e imprime el resultado (el valor que devuelve no se guarda en ninguna variable aquí, solo se ve impreso).

`sistema.eliminar_venta("Enero", "Ropa")` pone esa celda en cero, mostrando el valor que tenía antes.

Finalmente, otro `sistema.mostrar_tabla()` vuelve a imprimir la matriz completa, para comparar y confirmar que la celda "Enero-Ropa" ahora es `0`.
