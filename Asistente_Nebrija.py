# ===============================================================
# Asistente Nebrija · Versión mejorada (FAQ + Incidencias)
# - FAQ (WiFi, horarios, enlaces, etc.)
# - Clasificación de incidencias (zero-shot)
# - Prioridad + umbral de confianza
# - Evaluación con incidencias.csv (pandas)
# - Registro de conversaciones (log CSV)
#
# Autor: Raúl Cid González
# ===============================================================

# Requisitos:
#   pip install transformers torch pandas
#
# Ejecución (consola):
#   python Asistente_Nebrija.py
#
# Archivos esperados:
#   - incidencias.csv
#   - log_chat.csv (se crea solo)

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import pandas as pd
from transformers import pipeline


# ---------- 1. Modelo PLN para clasificación de incidencias ----------

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

UMBRAL_CONFIANZA = 0.45


# ---------- 2. FAQ / Base de conocimiento rápida (respuestas + links) ----------

FAQ: List[Dict] = [
    {
        "intent": "wifi",
        "patterns": [r"\bwifi\b", r"\beduroam\b", r"\binternet\b", r"\bred\b"],
        "answer": (
            "Sí. En la universidad puedes conectarte a la red **eudoram-Nebrija**.\n"
            "Pasos típicos:\n"
            "1) Selecciona 'eduroam-Nebrija'\n"
            "2) Usuario: tu correo completo de Nebrija (ej. usuarioo@alumnos.nebrija.es)\n"
            "3) Contraseña: la misma que usas para entrar al Blackboard\n"
            "Si falla, prueba a olvidar la red y volver a conectarte."
        ),
        "links": [
            {"text": "Guía de eduroam (Nebrija)", "url": "https://campusvirtual.nebrija.es/?new_loc=%2Fultra%2Fcourses%2F_91881_1%2Foutline%2Ffile%2F_3633088_1%3FlinkContentId%3D_3633088_1M"}
        ],
    },
    {
        "intent": "horario",
        "patterns": [r"\bhorario\b", r"\bclases\b", r"\bcalendario\b", r"\b(a qué hora|a que hora)\b"],
        "answer": (
            "El horario depende de tu titulación y grupo. Normalmente se consulta en el portal del alumno.\n"
            "Si me dices tu grado y curso (por ejemplo: 'Informática 4º'), te indico qué dato necesitas buscar."
        ),
        "links": [
            {"text": "Portal del alumno (Nebrija)", "url": "https://app.unne.universitasxxi.com/ServiciosApp/;PortalJSESSION=QmVIMULsKmgO6cFuRLpjIaK92G1vyaVxE8r6QFcIAak5eChvJ4F0!1109235815"}
        ],
    },
    {
        "intent": "blackboard",
        "patterns": [r"\bblackboard\b", r"\baula virtual\b", r"\bcampus virtual\b"],
        "answer": (
            "Para acceder a Blackboard, comprueba primero:\n"
            "- usuario/correo correcto\n"
            "- contraseña actual\n"
            "- si el navegador tiene caché antigua (prueba modo incógnito)\n"
            "Si sigue fallando, dime el mensaje exacto de error."
        ),
        "links": [
            {"text": "Acceso Blackboard (Nebrija)", "url": "https://campusvirtual.nebrija.es/?new_loc=%2Fultra%2Fcourses%2F_91881_1%2Foutline%2Ffile%2F_3633088_1%3FlinkContentId%3D_3633088_1"}
        ],
    },
    {
        "intent": "equipos_y_servicios",
        "patterns": [r"\bteams\b", r"\bcorreo\b", r"\boutlook\b", r"\bmicrosoft 365\b", r"\bo365\b"],
        "answer": (
            "Si no puedes entrar a Teams o al correo institucional:\n"
            "1) Comprueba si tu contraseña ha cambiado recientemente\n"
            "2) Prueba desde un navegador (incógnito) o desde otro dispositivo\n"
            "3) Si te da error de credenciales, puede ser un problema de acceso o cuenta bloqueada\n"
            "4) Prueba cambiando la contraseña e intenta de nuevo."
        ),
        "links": [
            {"text": "Soporte Microsoft 365 (Nebrija)", "url": "https://www.nebrija.es/login/passwords/recuperacioninicial.php"}
        ],
    },
    {
        "intent": "soporte_tickets",
        "patterns": [r"\bticket\b", r"\bincidencia\b", r"\bsoporte\b", r"\bayuda\b", r"\bhelpdesk\b"],
        "answer": (
            "Para incidencias técnicas o administrativas, abrir un ticket ayuda a que se asigne rápido.\n"
            "Recomendación: añade descripción breve, capturas (si aplica) y tu usuario/correo."
        ),
        "links": [
            {"text": "Portal de soporte / tickets (Nebrija)", "url": "https://www.nebrija.com/vida_universitaria/servicios/secretaria/"}
        ],
    },
]


def detectar_faq(texto: str) -> Optional[Dict]:
    texto_min = texto.lower()
    for item in FAQ:
        if any(re.search(p, texto_min) for p in item["patterns"]):
            return item
    return None


# ---------- 3. Clasificación + prioridad + solicitud de info ----------

def estimar_prioridad(texto: str) -> str:
    texto_min = texto.lower()

    disparadores_alta = [
        "no puedo acceder",
        "no puedo entrar",
        "no tengo acceso",
        "cuenta bloqueada",
        "bloqueado",
        "examen",
        "entrega hoy",
        "plazo termina",
        "plazo acaba",
        "urgente",
        "hoy"
    ]

    return "alta" if any(d in texto_min for d in disparadores_alta) else "normal"


def preguntas_seguimiento(categoria: str) -> List[str]:
    if categoria == "problema de acceso":
        return [
            "¿Te falla en Blackboard, Teams, correo o en todos?",
            "¿Te aparece algún mensaje de error? (cópialo si puedes)",
            "¿Has probado en modo incógnito o en otro dispositivo?"
        ]
    if categoria == "error de matrícula":
        return [
            "¿En qué paso exacto te da el error (confirmación, pago, asignaturas)?",
            "¿Qué mensaje aparece?",
            "¿Puedes adjuntar una captura si vas a abrir ticket?"
        ]
    if categoria == "cuenta bloqueada":
        return [
            "¿Te indica explícitamente 'cuenta bloqueada' o es un error de credenciales?",
            "¿Has intentado restablecer la contraseña?",
            "¿Te ocurre también en Teams/correo?"
        ]
    if categoria == "problema técnico":
        return [
            "¿Qué aplicación o sistema falla exactamente?",
            "¿Desde cuándo ocurre?",
            "¿En qué dispositivo/navegador lo estás usando?"
        ]
    if categoria == "consulta administrativa":
        return [
            "¿A qué trámite te refieres exactamente (cambio de grupo, títulos, tasas, etc.)?",
            "¿De qué facultad o grado eres?",
            "¿Es una consulta urgente por algún plazo?"
        ]
    return [
        "¿Puedes darme un poco más de detalle para clasificarlo mejor?",
        "¿Qué estabas intentando hacer exactamente?"
    ]


def clasificacion_por_reglas(texto: str) -> Optional[str]:
    t = texto.lower()

    if any(k in t for k in ["matrícula", "matricula", "tasas", "pagar", "pago de tasas", "confirmar la matrícula", "confirmar la matricula"]):
        return "error de matrícula"

    if any(k in t for k in ["plazos", "solicitar el título", "solicitar el titulo", "título", "titulo", "trámite", "tramite", "cambio de grupo", "secretaría", "secretaria"]):
        return "consulta administrativa"

    if any(k in t for k in ["correo", "outlook", "mensajes", "mail"]) and any(k in t for k in ["falla", "no recibo", "no llegan", "no me llegan", "error", "no funciona"]):
        return "problema técnico"

    return None


def clasificar_incidencia(texto: str) -> Tuple[str, Dict[str, float], str, float]:
    por_reglas = clasificacion_por_reglas(texto)
    if por_reglas:
        prioridad = estimar_prioridad(texto)
        return por_reglas, {}, prioridad, 1.0

    resultado = clasificador(
        texto,
        categorias,
        hypothesis_template="Esta incidencia trata sobre {}."
    )

    etiqueta_top = resultado["labels"][0]
    score_top = float(resultado["scores"][0])
    scores = dict(zip(resultado["labels"], resultado["scores"]))

    prioridad = estimar_prioridad(texto)

    if score_top < UMBRAL_CONFIANZA:
        etiqueta_top = "otro tipo de incidencia"

    return etiqueta_top, scores, prioridad, score_top


# ---------- 4. Evaluación con CSV (incidencias.csv) ----------

def evaluar_sobre_csv(ruta_csv: str) -> Tuple[pd.DataFrame, float]:
    df = pd.read_csv(ruta_csv)

    predicciones = []
    prioridades = []
    confianzas = []
    aciertos = 0

    print("🧪 Evaluación del asistente Nebrija sobre el dataset de ejemplo\n")

    for i, fila in df.iterrows():
        texto = str(fila["texto"])
        esperado = str(fila["tipo_esperado"])

        pred, scores, prioridad, conf = clasificar_incidencia(texto)

        predicciones.append(pred)
        prioridades.append(prioridad)
        confianzas.append(conf)

        coincide = (pred == esperado)
        if coincide:
            aciertos += 1

        print(f"Incidencia {i+1}:")
        print(f"  Texto: {texto}")
        print(f"  Etiqueta esperada: {esperado}")
        print(f"  Predicción modelo: {pred} (confianza: {conf:.2f})")
        print(f"  Prioridad estimada: {prioridad}")
        print(f"  ¿Coincide?: {'✅' if coincide else '❌'}")
        print()

    df["prediccion"] = predicciones
    df["prioridad"] = prioridades
    df["confianza_top"] = confianzas

    precision = aciertos / len(df) if len(df) else 0.0
    print(f"Precisión aproximada del modelo en este dataset: {precision:.2%}\n")

    return df, precision


# ---------- 5. Registro de chat (log) ----------

LOG_PATH = Path("log_chat.csv")

def registrar_log(texto_usuario: str, tipo: str, prioridad: str, confianza: float, respuesta: str) -> None:
    fila = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "texto_usuario": texto_usuario,
        "tipo_detectado": tipo,
        "prioridad": prioridad,
        "confianza_top": round(confianza, 4),
        "respuesta_resumen": respuesta.replace("\n", " ").strip()[:250]
    }

    existe = LOG_PATH.exists()
    df = pd.DataFrame([fila])
    df.to_csv(LOG_PATH, mode="a", index=False, header=not existe, encoding="utf-8")


# ---------- 6. Registro de feedback (SI / NO) ----------

FEEDBACK_PATH = Path("feedback_chat.csv")

def registrar_feedback(texto_usuario: str, tipo: str, prioridad: str, confianza: float, respuesta: str, feedback: str) -> None:
    fila = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "texto_usuario": texto_usuario,
        "tipo_detectado": tipo,
        "prioridad": prioridad,
        "confianza_top": round(confianza, 4),
        "respuesta_resumen": respuesta.replace("\n", " ").strip()[:250],
        "feedback": feedback
    }

    existe = FEEDBACK_PATH.exists()
    df = pd.DataFrame([fila])
    df.to_csv(FEEDBACK_PATH, mode="a", index=False, header=not existe, encoding="utf-8")


# ---------- 7. Chat interactivo ----------

def formatear_links(links: List[Dict[str, str]]) -> str:
    if not links:
        return ""
    out = ["🔗 Enlaces útiles:"]
    for l in links:
        out.append(f" - {l['text']}: {l['url']}")
    return "\n".join(out)


def chat_simulado() -> None:
    print("\n💬 Chat con el asistente Nebrija (FAQ + Incidencias)")
    print("Escribe 'salir' para terminar.\n")

    while True:
        texto = input("👩‍🎓 Usuario: ").strip()
        if texto.lower() == "salir":
            print("🤖 Asistente: Gracias, hasta pronto.")
            break

        faq = detectar_faq(texto)
        if faq:
            respuesta = faq["answer"]
            print(f"🤖 Asistente: {respuesta}")
            links_txt = formatear_links(faq.get("links", []))
            if links_txt:
                print(links_txt)
            print()
            registrar_log(texto, f"FAQ:{faq['intent']}", "n/a", 1.0, respuesta)
            continue

        categoria, scores, prioridad, conf = clasificar_incidencia(texto)

        print(f"🤖 Asistente: He detectado que tu incidencia parece un '{categoria}'.")
        print(f"   Prioridad estimada: {prioridad.upper()} (confianza: {conf:.2f})")

        if categoria == "problema de acceso":
            respuesta = (
                "Te recomiendo probar primero:\n"
                "1) Comprobar usuario/contraseña\n"
                "2) Probar modo incógnito\n"
                "3) Restablecer contraseña si es necesario\n"
                "Si me dices el mensaje de error, lo afinamos."
            )
        elif categoria == "error de matrícula":
            respuesta = (
                "En errores de matrícula suele ayudar:\n"
                "1) Revisar en qué paso ocurre (confirmación/pago/asignaturas)\n"
                "2) Hacer captura del error\n"
                "3) Abrir ticket a Secretaría/Soporte con esa información"
            )
        elif categoria == "cuenta bloqueada":
            respuesta = (
                "Es posible que la cuenta se haya bloqueado por intentos fallidos.\n"
                "Prueba a restablecer la contraseña y, si sigue igual, solicita desbloqueo a Soporte."
            )
        elif categoria == "consulta administrativa":
            respuesta = (
                "Para consultas administrativas, normalmente encontrarás la info en el portal del alumno "
                "o normativa/calendario académico. Si me das más detalle, te digo el paso exacto."
            )
        elif categoria == "problema técnico":
            respuesta = (
                "Para problemas técnicos:\n"
                "- indica qué aplicación/sistema falla\n"
                "- desde cuándo\n"
                "- dispositivo/navegador\n"
                "Con eso se puede abrir un ticket más completo."
            )
        else:
            respuesta = (
                "No estoy 100% seguro del tipo de incidencia. "
                "Si me das más detalle (qué sistema, qué estabas intentando hacer y qué error sale), "
                "puedo clasificarlo mejor o derivarlo."
            )

        print("   " + respuesta.replace("\n", "\n   "))

        if categoria == "otro tipo de incidencia" or conf < 0.55:
            qs = preguntas_seguimiento(categoria)
            print("\n   Para ayudarte mejor, dime por favor:")
            for q in qs:
                print(f"   - {q}")

        print()
        registrar_log(texto, categoria, prioridad, conf, respuesta)


# ---------- 8. Punto de entrada ----------

if __name__ == "__main__":
    print("=== Asistente Nebrija · Versión mejorada ===\n")

    try:
        df_resultados, precision = evaluar_sobre_csv("incidencias.csv")
        df_resultados.to_csv("resultados_evaluacion.csv", index=False, encoding="utf-8")
        print("✅ Se ha guardado 'resultados_evaluacion.csv' con predicciones y confianza.\n")
    except FileNotFoundError:
        print("No se ha encontrado 'incidencias.csv'. "
              "Crea el archivo en la misma carpeta para ejecutar la evaluación.\n")

    chat_simulado()