# ===============================================================
# Interfaz Web (Streamlit) · Asistente Nebrija
# Usa el módulo Asistente_Nebrija.py
# Autor: Raúl Cid González
# ===============================================================

# Compilar versión web
# python -m streamlit run app.py

import os
import streamlit as st
import pandas as pd
from pandas.errors import EmptyDataError

from Asistente_Nebrija import (
    detectar_faq,
    clasificar_incidencia,
    preguntas_seguimiento,
    evaluar_sobre_csv,
    registrar_log,
    registrar_feedback,
)

st.set_page_config(
    page_title="Asistente Nebrija",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Tony, el asistente de la Nebrija (Prototipo)")
st.caption("Interfaz visual para las incidencias de los alumnos de Nebrija.")

# ---------- Utilidades locales (para evitar duplicados y lecturas rotas) ----------
FEEDBACK_PATH = "feedback_chat.csv"
FEEDBACK_COLUMNS = [
    "timestamp",
    "texto_usuario",
    "tipo_detectado",
    "prioridad",
    "confianza_top",
    "respuesta_resumen",
    "feedback",
    # columna extra para bloquear duplicados (la gestionamos desde app.py)
    "question_id",
]


def _ensure_feedback_file_has_header() -> None:
    """
    Si feedback_chat.csv no existe o está vacío (0 bytes), crea el archivo con cabecera.
    Esto evita EmptyDataError de pandas.
    """
    if (not os.path.exists(FEEDBACK_PATH)) or (os.path.getsize(FEEDBACK_PATH) == 0):
        df = pd.DataFrame(columns=FEEDBACK_COLUMNS)
        df.to_csv(FEEDBACK_PATH, index=False, encoding="utf-8")


def _safe_read_csv(path: str) -> pd.DataFrame:
    """
    Lee CSV de forma robusta:
    - Si no existe o está vacío: devuelve DF vacío (con columnas).
    - Si pandas lanza EmptyDataError: devuelve DF vacío.
    - Limpia nombres de columnas.
    """
    if (not os.path.exists(path)) or (os.path.getsize(path) == 0):
        return pd.DataFrame(columns=FEEDBACK_COLUMNS)

    try:
        df = pd.read_csv(path)
    except EmptyDataError:
        return pd.DataFrame(columns=FEEDBACK_COLUMNS)
    except Exception:
        # Si hay cualquier problema raro, no rompemos la app
        return pd.DataFrame(columns=FEEDBACK_COLUMNS)

    if df is None or df.empty:
        return pd.DataFrame(columns=FEEDBACK_COLUMNS)

    df.columns = df.columns.astype(str).str.strip()
    return df


def _build_question_id(texto_usuario: str, respuesta: str) -> str:
    """
    Id estable para una pregunta+respuesta.
    """
    base = (texto_usuario or "").strip() + "||" + (respuesta or "").strip()
    return str(abs(hash(base)))


def _feedback_already_recorded(question_id: str) -> bool:
    """
    Bloqueo persistente: si el CSV ya tiene una fila con ese question_id, no deja volver a votar.
    Importante: soporta archivo vacío y falta de columnas.
    """
    # Si no existe o está vacío, no hay registros
    if (not os.path.exists(FEEDBACK_PATH)) or (os.path.getsize(FEEDBACK_PATH) == 0):
        return False

    df = _safe_read_csv(FEEDBACK_PATH)
    if df.empty:
        return False

    # si el CSV todavía no tiene la columna question_id, no podemos bloquear persistente
    if "question_id" not in df.columns:
        return False

    return (df["question_id"].astype(str) == str(question_id)).any()


def _append_question_id_to_last_row(question_id: str) -> None:
    """
    Tu registrar_feedback de Asistente_Nebrija escribe una fila nueva.
    Aquí añadimos/actualizamos question_id en la última fila para bloqueo persistente.
    """
    _ensure_feedback_file_has_header()

    df = _safe_read_csv(FEEDBACK_PATH)
    if df.empty:
        return

    if "question_id" not in df.columns:
        df["question_id"] = ""

    df.loc[df.index.max(), "question_id"] = str(question_id)
    df.to_csv(FEEDBACK_PATH, index=False, encoding="utf-8")


def _safe_feedback_stats() -> tuple[int, int, int, float, pd.DataFrame]:
    """
    Devuelve (total_validos, si, no, ratio_si, df_fb)
    - No revienta si falta feedback o si CSV vacío.
    - total_validos cuenta solo SI/NO.
    """
    df_fb = _safe_read_csv(FEEDBACK_PATH)

    if df_fb.empty:
        return 0, 0, 0, 0.0, df_fb

    # Asegura columna feedback
    if "feedback" not in df_fb.columns:
        df_fb["feedback"] = ""

    fb = df_fb["feedback"].astype(str).str.strip().str.upper()
    si = int((fb == "SI").sum())
    no = int((fb == "NO").sum())
    total = int(si + no)
    ratio = (si / total) if total else 0.0
    return total, si, no, ratio, df_fb


# ---------------- Layout principal ----------------
col_chat, col_eval = st.columns([1.3, 1])

# ====================== COLUMNA CHAT ======================
with col_chat:
    st.subheader("💬 Chat")

    if "historial" not in st.session_state:
        st.session_state.historial = []

    if "ultima_interaccion" not in st.session_state:
        st.session_state.ultima_interaccion = None

    # Bloqueo en sesión (para que no puedas clickar mil veces sin recargar)
    if "feedback_done" not in st.session_state:
        st.session_state.feedback_done = {}  # question_id -> "SI"/"NO"

    for msg in st.session_state.historial:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_text = st.chat_input("Escribe tu consulta o incidencia…")

    if user_text:
        st.session_state.historial.append({"role": "user", "content": user_text})
        with st.chat_message("user"):
            st.markdown(user_text)

        faq = detectar_faq(user_text)
        if faq:
            answer = faq["answer"]

            links = faq.get("links", [])
            if links:
                answer += "\n\n**🔗 Enlaces útiles:**\n"
                for l in links:
                    answer += f"- [{l['text']}]({l['url']})\n"

            st.session_state.historial.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)

            registrar_log(user_text, f"FAQ:{faq['intent']}", "n/a", 1.0, answer)

            st.session_state.ultima_interaccion = {
                "texto_usuario": user_text,
                "tipo": f"FAQ:{faq['intent']}",
                "prioridad": "n/a",
                "confianza": 1.0,
                "respuesta": answer
            }

        else:
            categoria, scores, prioridad, conf = clasificar_incidencia(user_text)

            respuesta = (
                f"**Clasificación:** {categoria}\n\n"
                f"**Prioridad estimada:** {prioridad.upper()}  \n"
                f"**Confianza:** {conf:.2f}\n\n"
            )

            if categoria == "problema de acceso":
                respuesta += "Te recomiendo probar: modo incógnito, revisar credenciales y restablecer contraseña si es necesario."
            elif categoria == "error de matrícula":
                respuesta += "Indica en qué paso ocurre (confirmación/pago/asignaturas) y el mensaje de error. Si procede, abre ticket con captura."
            elif categoria == "cuenta bloqueada":
                respuesta += "Prueba restablecer la contraseña. Si sigue igual, solicita desbloqueo a Soporte."
            elif categoria == "consulta administrativa":
                respuesta += "Suele resolverse consultando portal del alumno/normativa. Si me dices el trámite concreto, te digo dónde mirarlo."
            elif categoria == "problema técnico":
                respuesta += "Dime qué aplicación falla, desde cuándo y dispositivo/navegador para orientar mejor el ticket."
            else:
                respuesta += "No estoy seguro al 100%. Si me das más detalle (sistema, error, contexto), lo clasificaré mejor."

            if categoria == "otro tipo de incidencia" or conf < 0.55:
                respuesta += "\n\n**Para afinar, dime por favor:**\n"
                for q in preguntas_seguimiento(categoria):
                    respuesta += f"- {q}\n"

            st.session_state.historial.append({"role": "assistant", "content": respuesta})
            with st.chat_message("assistant"):
                st.markdown(respuesta)

            registrar_log(user_text, categoria, prioridad, conf, respuesta)

            st.session_state.ultima_interaccion = {
                "texto_usuario": user_text,
                "tipo": categoria,
                "prioridad": prioridad,
                "confianza": conf,
                "respuesta": respuesta
            }

    st.divider()
    st.subheader("✅ ¿Te ha servido la respuesta?")

    if st.session_state.ultima_interaccion is None:
        st.info("Aún no hay una respuesta para valorar. Haz una pregunta en el chat.")
    else:
        u = st.session_state.ultima_interaccion
        qid = _build_question_id(u["texto_usuario"], u["respuesta"])

        # Bloqueo: sesión + CSV
        ya_en_sesion = qid in st.session_state.feedback_done
        ya_en_csv = _feedback_already_recorded(qid)

        if ya_en_sesion or ya_en_csv:
            voto = st.session_state.feedback_done.get(qid, "registrado")
            st.info(f"Ya has valorado esta respuesta: **{voto}**")
        else:
            c1, c2 = st.columns(2)

            with c1:
                if st.button("✅ Sí", key=f"btn_si_{qid}"):
                    _ensure_feedback_file_has_header()
                    registrar_feedback(
                        u["texto_usuario"], u["tipo"], u["prioridad"],
                        u["confianza"], u["respuesta"], "SI"
                    )
                    st.session_state.feedback_done[qid] = "SI"
                    _append_question_id_to_last_row(qid)
                    st.success("Feedback guardado: SI ✅")

            with c2:
                if st.button("❌ No", key=f"btn_no_{qid}"):
                    _ensure_feedback_file_has_header()
                    registrar_feedback(
                        u["texto_usuario"], u["tipo"], u["prioridad"],
                        u["confianza"], u["respuesta"], "NO"
                    )
                    st.session_state.feedback_done[qid] = "NO"
                    _append_question_id_to_last_row(qid)
                    st.warning("Feedback guardado: NO ❌")


# ====================== COLUMNA EVALUACIÓN ======================
with col_eval:
    st.subheader("🧪 Evaluación con incidencias.csv")

    ruta_csv = st.text_input("Ruta del CSV", value="incidencias.csv")

    if st.button("Evaluar dataset"):
        try:
            df_res, precision = evaluar_sobre_csv(ruta_csv)
            st.success(f"Precisión aproximada en este dataset: {precision:.2%}")

            st.write("**Resultados:**")
            st.dataframe(df_res, use_container_width=True)

            df_res.to_csv("resultados_evaluacion.csv", index=False, encoding="utf-8")

            st.download_button(
                label="⬇️ Descargar resultados_evaluacion.csv",
                data=open("resultados_evaluacion.csv", "rb").read(),
                file_name="resultados_evaluacion.csv",
                mime="text/csv"
            )

        except FileNotFoundError:
            st.error("No se encontró el archivo. Asegúrate de que 'incidencias.csv' está en la misma carpeta.")
        except Exception as e:
            st.error(f"Error durante la evaluación: {e}")

    st.divider()
    st.subheader("📊 Feedback (éxito percibido)")

    if st.button("📈 Calcular porcentaje feedback"):
        total, si, no, ratio, df_fb = _safe_feedback_stats()

        if total == 0:
            st.warning("Aún no hay feedback válido (SI/NO) guardado.")
        else:
            st.success(f"Éxito percibido: {ratio:.2%}")
            st.write(f"Total valoraciones: {total} | SI: {si} | NO: {no}")

        with st.expander("Ver últimas 20 filas (debug)"):
            st.write("Columnas detectadas:", list(df_fb.columns))
            st.dataframe(df_fb.tail(20), use_container_width=True)

    if os.path.exists(FEEDBACK_PATH) and os.path.getsize(FEEDBACK_PATH) > 0:
        st.download_button(
            label="⬇️ Descargar feedback_chat.csv",
            data=open(FEEDBACK_PATH, "rb").read(),
            file_name="feedback_chat.csv",
            mime="text/csv"
        )

    st.divider()
    st.subheader("📄 Logs")

    try:
        df_log = pd.read_csv("log_chat.csv")
        st.dataframe(df_log.tail(50), use_container_width=True)
        st.download_button(
            label="⬇️ Descargar log_chat.csv",
            data=open("log_chat.csv", "rb").read(),
            file_name="log_chat.csv",
            mime="text/csv"
        )
    except Exception:
        st.info("Aún no hay logs. Habla con el asistente y se generará 'log_chat.csv'.")