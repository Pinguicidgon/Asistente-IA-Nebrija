# ===============================================================
# Asistente Nebrija · Versión ampliada
# Clasificación de incidencias + prioridad + evaluación con CSV
# Autor: Raúl Cid González
# ===============================================================

# pip install transformers torch pandas

# python Asistente_Nebrija.py


from transformers import pipeline
import pandas as pd

# ---------- 1. Modelo NLP para clasificación de incidencias ----------

clasificador = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

categorias = [
    "problema de acceso",
    "error de matrícula",
    "cuenta bloqueada",
    "problema técnico",
    "consulta administrativa",
    "otro tipo de incidencia"
]


def clasificar_incidencia(texto: str):
    """
    Recibe el texto de una incidencia y devuelve:
    - categoría más probable
    - diccionario etiqueta -> score
    - prioridad estimada (alta / normal)
    """

    resultado = clasificador(texto, categorias)

    categoria_principal = resultado["labels"][0]
    scores = dict(zip(resultado["labels"], resultado["scores"]))

    # ---------- 2. Lógica sencilla de prioridad ----------
    texto_min = texto.lower()

    prioridad = "normal"

    disparadores_alta = [
        "no puedo acceder",
        "no puedo entrar",
        "no tengo acceso",
        "cuenta bloqueada",
        "examen",
        "entrega hoy",
        "plazo termina"
    ]

    if any(disparador in texto_min for disparador in disparadores_alta):
        prioridad = "alta"

    return categoria_principal, scores, prioridad


# ---------- 3. Evaluación con un CSV de ejemplos ----------

def evaluar_sobre_csv(ruta_csv: str):
    """
    Lee un fichero incidencias.csv con columnas:
    - texto
    - tipo_esperado

    Clasifica cada fila y calcula la precisión aproximada.
    """

    df = pd.read_csv(ruta_csv)

    predicciones = []
    aciertos = 0

    print("🧪 Evaluación del asistente Nebrija sobre el dataset de ejemplo\n")

    for i, fila in df.iterrows():
        texto = fila["texto"]
        esperado = fila["tipo_esperado"]

        pred, scores, prioridad = clasificar_incidencia(texto)
        predicciones.append(pred)

        coincide = (pred == esperado)
        if coincide:
            aciertos += 1

        print(f"Incidencia {i+1}:")
        print(f"  Texto: {texto}")
        print(f"  Etiqueta esperada: {esperado}")
        print(f"  Predicción modelo: {pred}")
        print(f"  Prioridad estimada: {prioridad}")
        print(f"  ¿Coincide?: {'✅' if coincide else '❌'}")
        print()

    df["prediccion"] = predicciones
    precision = aciertos / len(df)

    print(f"Precisión aproximada del modelo en este dataset: {precision:.2%}")
    return df, precision


# ---------- 4. Pequeña simulación tipo chat ----------

def chat_simulado():
    """
    Simula brevemente una conversación con el asistente
    a partir de lo que escribe el usuario.
    """

    print("\n💬 Chat simulado con el asistente Nebrija")
    print("Escribe 'salir' para terminar.\n")

    while True:
        texto = input("👩‍🎓 Usuario: ")
        if texto.lower().strip() == "salir":
            print("🤖 Asistente: Gracias, hasta pronto.")
            break

        categoria, scores, prioridad = clasificar_incidencia(texto)

        print(f"🤖 Asistente: He detectado que tu incidencia parece un '{categoria}'.")
        print(f"   Prioridad estimada: {prioridad.upper()}")

        if categoria == "problema de acceso":
            print("   Te recomiendo probar primero a restablecer la contraseña "
                  "en el portal de identidad de la universidad.")
        elif categoria == "error de matrícula":
            print("   Este tipo de problemas suele resolverse contactando con Secretaria "
                  "Académica. Si el error persiste, abre un ticket adjuntando captura.")
        elif categoria == "cuenta bloqueada":
            print("   Es posible que se haya bloqueado por varios intentos fallidos. "
                  "Solicita el desbloqueo a Soporte IT o restablece la contraseña.")
        elif categoria == "consulta administrativa":
            print("   Puedes consultar el calendario académico y la normativa "
                  "en la web institucional. Si sigues con dudas, contacta con Secretaría.")
        else:
            print("   Tu incidencia será derivada al equipo correspondiente "
                  "para una revisión más detallada.")

        print()


# ---------- 5. Punto de entrada ----------

if __name__ == "__main__":
    print("=== Asistente Nebrija · Versión ampliada ===\n")

    # 1) Evaluación sobre el CSV
    try:
        df_resultados, precision = evaluar_sobre_csv("incidencias.csv")
    except FileNotFoundError:
        print("No se ha encontrado 'incidencias.csv'. "
              "Crea el archivo en la misma carpeta para ejecutar la evaluación.\n")

    # 2) Chat interactivo en consola
    chat_simulado()