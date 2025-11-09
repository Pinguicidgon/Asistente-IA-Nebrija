# ===============================================================
# Asistente Nebrija · Clasificación automática de incidencias
# Autor: Raúl Cid González
# ===============================================================

# Importamos un pipeline preentrenado de análisis de texto
from transformers import pipeline

# Cargamos el modelo de clasificación zero-shot
# Este modelo permite clasificar frases en categorías sin entrenamiento previo
clasificador = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Definimos las posibles categorías de incidencias
categorias = [
    "problema de acceso",
    "error de matrícula",
    "cuenta bloqueada",
    "problema técnico",
    "consulta administrativa",
    "otro tipo de incidencia"
]

# Entrada de ejemplo del usuario
texto_usuario = input("Introduce tu incidencia: ")

# Aplicamos la clasificación
resultado = clasificador(texto_usuario, categorias)

# Mostramos la categoría con mayor puntuación
print("\nClasificación automática:")
print(f"Texto analizado: {texto_usuario}")
print(f"Categoría más probable: {resultado['labels'][0]}")
print("\nDetalles:")
for etiqueta, puntuacion in zip(resultado['labels'], resultado['scores']):
    print(f"{etiqueta}: {puntuacion:.2f}")