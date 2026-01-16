# ---------------------------------------------------------
# Autor: Raúl Cid (base adaptada)
# Utilidades para registrar y leer feedback SI/NO
# ---------------------------------------------------------

from __future__ import annotations

from pathlib import Path
from datetime import datetime
import pandas as pd


FEEDBACK_PATH = Path("feedback_chat.csv")


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia nombres de columnas (quita espacios) y asegura tipos básicos."""
    df.columns = df.columns.astype(str).str.strip()
    return df


def ensure_feedback_csv_exists() -> None:
    """
    Crea el CSV con cabecera correcta si no existe.
    Si existe, no lo toca.
    """
    if FEEDBACK_PATH.exists():
        return

    cols = [
        "timestamp",
        "question_id",
        "texto_usuario",
        "tipo_detectado",
        "prioridad",
        "confianza_top",
        "respuesta_resumen",
        "feedback",
    ]
    pd.DataFrame(columns=cols).to_csv(FEEDBACK_PATH, index=False, encoding="utf-8")


def build_question_id(texto_usuario: str) -> str:
    """
    Genera un id estable para una "pregunta".
    """
    return str(abs(hash(texto_usuario.strip())))


def feedback_already_exists(question_id: str) -> bool:
    """
    Devuelve True si ya hay feedback registrado para ese question_id.
    Esto bloquea duplicados incluso si se recarga la página.
    """
    if not FEEDBACK_PATH.exists():
        return False

    df = pd.read_csv(FEEDBACK_PATH)
    df = _normalize_columns(df)

    if "question_id" not in df.columns:
        # CSV antiguo: no podemos comprobar con id
        return False

    return (df["question_id"].astype(str) == str(question_id)).any()


def registrar_feedback(
    texto_usuario: str,
    tipo: str,
    prioridad: str,
    confianza: float,
    respuesta: str,
    feedback: str,
) -> bool:
    """
    Registra una fila de feedback. Devuelve:
      - True si se ha guardado
      - False si ya existía feedback para esa pregunta (duplicado)
    """
    ensure_feedback_csv_exists()

    question_id = build_question_id(texto_usuario)

    # Bloqueo anti-duplicados (persistente)
    if feedback_already_exists(question_id):
        return False

    fila = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "question_id": question_id,
        "texto_usuario": texto_usuario,
        "tipo_detectado": tipo,
        "prioridad": prioridad,
        "confianza_top": round(float(confianza), 4),
        "respuesta_resumen": str(respuesta).replace("\n", " ").strip()[:250],
        "feedback": str(feedback).strip().upper(),  # SI / NO
    }

    existe = FEEDBACK_PATH.exists()
    df = pd.DataFrame([fila])
    df.to_csv(FEEDBACK_PATH, mode="a", index=False, header=not existe, encoding="utf-8")
    return True


def read_feedback_df() -> pd.DataFrame:
    """
    Lee el CSV y lo normaliza para que nunca reviente con KeyError.
    Si faltan columnas, las crea vacías.
    """
    ensure_feedback_csv_exists()
    df = pd.read_csv(FEEDBACK_PATH)
    df = _normalize_columns(df)

    # Aseguro columnas mínimas para que no haya KeyError
    needed = [
        "timestamp",
        "question_id",
        "texto_usuario",
        "tipo_detectado",
        "prioridad",
        "confianza_top",
        "respuesta_resumen",
        "feedback",
    ]
    for col in needed:
        if col not in df.columns:
            df[col] = ""

    return df


def compute_feedback_stats(df: pd.DataFrame) -> dict:
    """
    Calcula estadísticas: total, si, no, porcentaje_si.
    """
    df = _normalize_columns(df)

    # Por seguridad
    if "feedback" not in df.columns:
        return {"total": 0, "si": 0, "no": 0, "porcentaje_si": 0.0}

    fb = df["feedback"].astype(str).str.strip().str.upper()
    si = int((fb == "SI").sum())
    no = int((fb == "NO").sum())
    total = int(si + no)
    porcentaje_si = round((si / total) * 100, 2) if total > 0 else 0.0

    return {"total": total, "si": si, "no": no, "porcentaje_si": porcentaje_si}