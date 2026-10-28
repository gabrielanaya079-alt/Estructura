# ¿Qué sucedió con las listas?

Al eliminar automáticamente los elementos repetidos del arreglo `POSTRES` (función `eliminar_repetidos()` en `postres.py`), cada elemento del arreglo tiene asociada una lista ligada de ingredientes. Esto fue lo que ocurrió con esas listas.

## ¿Mandó mensaje de error?

**No.** El programa no mostró ningún error. En Python, cuando se elimina un elemento del arreglo, los nodos de su lista que ya no tienen ninguna referencia son liberados automáticamente por el recolector de basura.

## ¿Qué pasó con las listas?

Se probó con dos postres repetidos:

| Elemento | Lista de ingredientes |
|----------|-----------------------|
| `Flan` (primero, se conserva) | huevo -> leche -> NIL |
| `Flan` (repetido, se elimina) | huevo -> vainilla -> NIL |

- **Al descartar el repetido:** se elimina el elemento del arreglo y también su lista completa. Queda `Flan -> huevo -> leche -> NIL` y **se pierde la vainilla**.
- **Al fusionar:** los ingredientes del repetido que no estaban en la lista conservada se pasan a ella. Queda `Flan -> huevo -> leche -> vainilla -> NIL` y **no se pierde información**.

El programa imprime un reporte con la lista de cada elemento repetido y lo que se hizo con ella (descartada o fusionada).

## Conclusiones

Al eliminar los elementos repetidos de `POSTRES` se comprobó que borrar un elemento del arreglo no es suficiente, porque cada uno tiene asociada una lista ligada de ingredientes y hay que decidir qué se hace con ella: descartarla, fusionarla con la del elemento que se conserva o liberarla. Si se descarta, se puede perder información sin que el programa avise, ya que los repetidos pueden tener ingredientes distintos y al quedarse solo con el primero los demás desaparecen; por eso conviene fusionar las listas o, al menos, reportar lo que se descartó. En Python no se produce ningún error porque el recolector de basura libera los nodos que se quedan sin referencias, pero en lenguajes con manejo manual de memoria como C o Pascal el resultado sería distinto: si solo se borra el elemento del arreglo sin liberar los nodos de su lista, estos quedan en memoria sin ningún puntero que los alcance (fuga de memoria), y si se libera la memoria y después se sigue usando el puntero, se produce un puntero colgante y un error de ejecución. Por esta razón el programa vacía la lista antes de quitar el elemento, recorriendo y desenlazando cada nodo, de modo que el procedimiento también sería correcto en un lenguaje sin recolector de basura. Finalmente, el hecho de que `POSTRES` esté ordenado alfabéticamente facilita el proceso, ya que los repetidos quedan contiguos y pueden eliminarse en un solo recorrido del arreglo.
