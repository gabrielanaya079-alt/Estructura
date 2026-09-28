import re

# Simulamos una base de datos o un archivo de configuración complejo.
# Nota cómo las variables hacen referencia a otras variables.
base_de_datos = {
    "mensaje_bienvenida": "[saludo] El evento será en [ubicacion_completa].",
    "saludo": "Hola [titulo] [apellido].",
    "titulo": "[profesion] Senior",
    "profesion": "Ingeniero",
    "apellido": "López",
    "ubicacion_completa": "el salón [salon] del edificio [edificio]",
    "salon": "Principal",
    "edificio": "Central"
}

def renderizar_plantilla(texto):
    """
    Busca etiquetas [variable] en un texto y las reemplaza por su valor real.
    Si el valor tiene más etiquetas, las resuelve usando recursividad anidada.
    """
    # Buscamos si hay alguna etiqueta en formato [texto]
    coincidencia = re.search(r'\[(.*?)\]', texto)
    
    # CASO BASE: Si ya no hay corchetes en el texto, devolvemos el texto limpio
    if not coincidencia:
        return texto
        
    # Extraemos el nombre de la etiqueta (ej. "saludo")
    etiqueta = coincidencia.group(1)
    
    # Buscamos qué significa esa etiqueta en nuestra base de datos
    valor_crudo = base_de_datos.get(etiqueta, f"[{etiqueta}]")
    
    # RECURSIVIDAD ANIDADA:
    # 1. renderizar_plantilla(valor_crudo): Resuelve las variables ocultas DENTRO del valor encontrado.
    # 2. texto.replace(...): Inserta ese valor ya resuelto en nuestro texto principal.
    # 3. renderizar_plantilla(...): Vuelve a evaluar todo el texto nuevo por si quedaron otras etiquetas diferentes.
    #
    # Estructura visual: funcion( texto.reemplazar( funcion(valor) ) )
    
    texto_actualizado = texto.replace(f"[{etiqueta}]", renderizar_plantilla(valor_crudo), 1)
    
    return renderizar_plantilla(texto_actualizado)

# ==========================================
# Ejecución del programa
# ==========================================
texto_inicial = "[mensaje_bienvenida]"

print("TEXTO CRUDO:")
print(texto_inicial)
print("\nTEXTO FINAL PROCESADO:")
print(renderizar_plantilla(texto_inicial))