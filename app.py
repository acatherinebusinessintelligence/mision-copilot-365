"""
Misión Copilot 365 — Backend Flask
Admin: genera claves, envía correos y ve progreso.
Estudiantes: entran con clave y sincronizan avance.
"""

from __future__ import annotations

import json
import os
import secrets
import smtplib
import sqlite3
import string
import time
from datetime import datetime, timezone
from email.message import EmailMessage
from functools import wraps
from pathlib import Path

from dotenv import load_dotenv
from flask import (
    Flask,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    send_from_directory,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=None,
)
app.secret_key = os.getenv("FLASK_SECRET_KEY", secrets.token_hex(32))
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

DB_PATH = BASE_DIR / "data" / "mision.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Base de datos
# ---------------------------------------------------------------------------

def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE COLLATE NOCASE,
            access_key TEXT NOT NULL UNIQUE,
            key_hash TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL,
            last_login TEXT,
            email_sent_at TEXT
        );

        CREATE TABLE IF NOT EXISTS progress (
            student_id INTEGER PRIMARY KEY,
            payload TEXT NOT NULL DEFAULT '{}',
            percent INTEGER NOT NULL DEFAULT 0,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS presence (
            student_id INTEGER PRIMARY KEY,
            step TEXT,
            title TEXT,
            module TEXT,
            seen_at REAL NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS pulse_votes (
            student_id INTEGER NOT NULL,
            qid TEXT NOT NULL,
            answer INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            PRIMARY KEY (student_id, qid),
            FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS app_settings (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at REAL
        );

        CREATE TABLE IF NOT EXISTS access_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL COLLATE NOCASE,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL,
            resolved_at TEXT,
            note TEXT
        );
        """
    )
    db.commit()
    db.close()


init_db()


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def generate_access_key() -> str:
    alphabet = string.ascii_uppercase + string.digits
    part = lambda n: "".join(secrets.choice(alphabet) for _ in range(n))
    return f"MCP-{part(4)}-{part(4)}"


def admin_configured() -> bool:
    return bool(os.getenv("ADMIN_PASSWORD"))


def require_admin(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            if request.path.startswith("/api/"):
                return jsonify({"ok": False, "error": "No autorizado"}), 401
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)

    return wrapped


def require_student(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("student_id"):
            if request.path.startswith("/api/"):
                return jsonify({"ok": False, "error": "Sesión requerida"}), 401
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def require_login_any(view):
    """Participante o facilitadora con sesión (el modo /presentar usa la sesión de admin)."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not (session.get("student_id") or session.get("is_admin")):
            if request.path.startswith("/api/"):
                return jsonify({"ok": False, "error": "Sesión requerida"}), 401
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


CIERRE_IDEAS = dict([["i1", "Copilot propone; yo verifico, corrijo y decido."], ["i2", "Un buen prompt tiene estructura: PRISM."], ["i3", "Si un prompt es largo, lo divido en turnos."], ["i4", "Toda afirmación debe tener su fuente."], ["i5", "Lo que falta se marca «No especificado», no se inventa."], ["i6", "Una propuesta no es una decisión."], ["i7", "El mismo hecho se adapta a cada audiencia."], ["i8", "Las cifras se verifican en la fuente original."], ["i9", "Adjuntar archivos en lugar de pegarlos."], ["i10", "Cuaderno, agente o automatización: cuándo usar cada uno."], ["i11", "La automatización orquesta; la persona autoriza."], ["i12", "Proteger los datos sensibles antes de usar Copilot."]])
CIERRE_CAPS = [["comprender", "Comprender"], ["organizar", "Organizar"], ["analizar", "Analizar"], ["comunicar", "Comunicar"], ["planificar", "Planificar"], ["decidir", "Decidir"]]
ACTIVITY_KEYS = [
    "reto-r1", "reto-r2", "reto-r3", "reto-r4", "reto-r5", "reto-r6",
    "s2-f0", "s2-f1", "s2-f2", "s2-f3", "s2-f4", "s2-f5", "s2-f6", "s2-f7", "s2-f8",
    "lab-3-1", "lab-3-2", "lab-3-3", "lab-3-4",
    "proyecto-final",
]
QUIZ_TOTALS = {"s1": 5, "s2": 6, "lab": 6}

# Columnas del mapa de avance (mismo orden que ACTIVITY_GROUPS del frontend).
LIVE_COLUMNS = [
    ("s1", "Paso 1", [("reto-r1", "R1"), ("reto-r2", "R2"), ("reto-r3", "R3"), ("reto-r4", "R4"), ("reto-r5", "R5"), ("reto-r6", "R6"), ("quiz-s1", "Eval")]),
    ("desafio", "Entre pasos", [("desafio", "Mi oportunidad")]),
    ("s2", "Paso 2", [("s2-f0", "F0"), ("s2-f1", "F1"), ("s2-f2", "F2"), ("s2-f3", "F3"), ("s2-f4", "F4")]),
    ("s2b", "Paso 3", [("s2-f5", "F5"), ("s2-f6", "F6"), ("s2-f7", "F7"), ("s2-f8", "F8"), ("quiz-s2", "Eval")]),
    ("lab", "Paso 4 · Lab", [("lab-3-1", "3.1"), ("lab-3-2", "3.2"), ("lab-3-3", "3.3"), ("lab-3-4", "3.4"), ("quiz-lab", "Eval")]),
    ("cierre", "Cierre", [("cierre-reflexion", "Me llevo"), ("proyecto-final", "Mi plan")]),
]

# Votaciones en vivo (una por módulo). El orden de las opciones es el índice guardado.
PULSES = {
    "bienvenida": ("¿Cuánto tiempo a la semana dedicas a buscar información, resumir correos o preparar informes?",
                   ["Menos de 2 horas", "Entre 2 y 5 horas", "Entre 5 y 10 horas", "Más de 10 horas"]),
    "s1": ("¿Qué tarea te quita más tiempo hoy?",
           ["Leer y responder correos", "Preparar actas y resúmenes", "Organizar pendientes", "Redactar informes"]),
    "desafio": ("¿Qué tan claro tienes en qué tarea de tu trabajo usarías Copilot?",
                ["Muy claro", "Tengo una idea", "Aún no lo sé"]),
    "s2": ("¿Qué es lo más difícil al revisar un proyecto con muchos documentos?",
           ["Encontrar la información", "Detectar inconsistencias", "Priorizar los riesgos", "Explicarlo al comité"]),
    "s2b": ("¿Qué es lo más difícil al presentar ante un comité?",
            ["Resumir sin perder lo importante", "Respaldar cada cifra", "Pedir una decisión concreta", "Responder preguntas difíciles"]),
    "parada-biblioteca": ("¿Para qué usarías primero un prompt del kit?",
                          ["Correos", "Actas y compromisos", "Informes", "Riesgos y decisiones"]),
    "parada-escenarios": ("¿En qué área aplicarías primero Copilot?",
                          ["Operación y mantenimiento", "Gestión de proyectos (PMO)", "HSE", "Comunicaciones", "Finanzas"]),
    "lab": ("¿Qué te gustaría automatizar primero?",
            ["Reportes periódicos", "Seguimiento de compromisos", "Consultas sobre documentos", "Alertas y notificaciones"]),
    "herramientas": ("¿Qué técnica quieres probar primero?",
                     ["Pre-mortem", "Mesa de expertos", "Comité escéptico", "Ensayo de conversación difícil"]),
    "cierre": ("Después del curso, ¿qué tan seguro te sientes usando Copilot en tu trabajo?",
               ["Muy seguro", "Seguro", "Algo inseguro", "Necesito más práctica"]),
}
PULSE_TTL_S = 20 * 60  # una votación abierta se cierra sola a los 20 minutos
ONLINE_S = 90          # "conectado" si envió señal en el último minuto y medio


def cierre_reflexion_done(payload: dict) -> bool:
    c = payload.get("cierre") or {}
    conf = c.get("conf") or {}
    return bool(c.get("ideas")) and bool(str(c.get("sirvio") or "").strip()) and all(
        (conf.get(cid) or {}).get("hoy") for cid, _ in CIERRE_CAPS
    )


def activity_progress(payload: dict) -> tuple[float, int, int]:
    """(avance ponderado, actividades completas, total). Misma lógica que calcPercent() del frontend."""
    progress = payload.get("progress") or {}
    done = sum(1 for k in ACTIVITY_KEYS if progress.get(k))
    oportunidad = payload.get("oportunidad") or {}
    if any(str(v or "").strip() for v in oportunidad.values()):
        done += 1
    if cierre_reflexion_done(payload):
        done += 1
    complete = done
    quizzes = payload.get("quizzes") or {}
    for qid, n in QUIZ_TOTALS.items():
        st = payload.get("quiz") if qid == "s1" else quizzes.get(qid)
        answered = len((st or {}).get("answers") or {})
        done += min(n, answered) / n
        complete += 1 if answered >= n else 0
    total = len(ACTIVITY_KEYS) + 2 + len(QUIZ_TOTALS)  # + desafío + reflexión de cierre + 3 autoevaluaciones
    return done, complete, total


def activity_done_map(payload: dict) -> dict:
    """Estado de cada actividad del mapa: True (completa), fracción 0-1 (autoevaluación parcial) o False."""
    progress = payload.get("progress") or {}
    out: dict = {}
    for _, _, cols in LIVE_COLUMNS:
        for key, _ in cols:
            if key.startswith("quiz-"):
                qid = key[5:]
                st = payload.get("quiz") if qid == "s1" else (payload.get("quizzes") or {}).get(qid)
                answered = len((st or {}).get("answers") or {})
                n = QUIZ_TOTALS[qid]
                out[key] = True if answered >= n else (round(answered / n, 2) if answered else False)
            elif key == "desafio":
                out[key] = any(str(v or "").strip() for v in (payload.get("oportunidad") or {}).values())
            elif key == "cierre-reflexion":
                out[key] = cierre_reflexion_done(payload)
            else:
                out[key] = bool(progress.get(key))
    return out


def quiz_scores(payload: dict) -> dict:
    """Porcentaje de aciertos de cada autoevaluación completa (None si no la terminó)."""
    out = {}
    for qid, n in QUIZ_TOTALS.items():
        st = payload.get("quiz") if qid == "s1" else (payload.get("quizzes") or {}).get(qid)
        st = st or {}
        if len(st.get("answers") or {}) >= n:
            out[qid] = round(100 * int(st.get("score") or 0) / n)
        else:
            out[qid] = None
    return out


WORK_SECTIONS = [
    ("avance", "Paso 1 · notas y resultados"),
    ("oportunidad", "Entre pasos · Mi oportunidad Copilot"),
    ("s2Notes", "Pasos 2 y 3 · Proyecto Horizonte"),
    ("lab33", "Paso 4 · Copilot Lab · automatización"),
    ("proyecto", "Cierre · Mi plan"),
]


def student_work(payload: dict) -> list[dict]:
    """Textos escritos por el estudiante en la plataforma (no incluye sus conversaciones con Copilot)."""
    sections = []
    for key, label in WORK_SECTIONS:
        data = payload.get(key) or {}
        if not isinstance(data, dict):
            continue
        items = []
        for k, v in data.items():
            if isinstance(v, str) and v.strip():
                items.append({"campo": k.replace("_", " ").replace("-", " "), "texto": v.strip()[:2000]})
        if items:
            sections.append({"titulo": label, "items": items})
    c = cierre_summary(payload)
    cierre_items = []
    if c["ideas"]:
        cierre_items.append({"campo": "ideas que se lleva", "texto": " · ".join(c["ideas"])})
    for campo, k in (("qué le sirvió", "sirvio"), ("dudas", "dudas")):
        if c[k]:
            cierre_items.append({"campo": campo, "texto": c[k][:2000]})
    if cierre_items:
        sections.append({"titulo": "Cierre · Lo que me llevo", "items": cierre_items})
    return sections


def calc_percent_from_payload(payload: dict) -> int:
    """25 actividades evaluables (igual que el frontend)."""
    done, _, total = activity_progress(payload)
    return int(round((done / total) * 100))


def cierre_summary(payload: dict) -> dict:
    c = payload.get("cierre") or {}
    pf = payload.get("proyecto") or {}
    conf = c.get("conf") or {}
    return {
        "ideas": [CIERRE_IDEAS[i] for i in (c.get("ideas") or []) if i in CIERRE_IDEAS],
        "idea_ids": [i for i in (c.get("ideas") or []) if i in CIERRE_IDEAS],
        "sirvio": str(c.get("sirvio") or "").strip(),
        "dudas": str(c.get("dudas") or "").strip(),
        "problema": str(pf.get("problema") or "").strip(),
        "primer_paso": str(pf.get("primerpaso") or "").strip(),
        "apps": str(pf.get("apps") or "").strip(),
        "conf": {cid: conf.get(cid) or {} for cid, _ in CIERRE_CAPS},
    }


def send_access_email(to_email: str, name: str, access_key: str) -> tuple[bool, str]:
    smtp_email = os.getenv("SMTP_EMAIL", "analizamostunegocio@gmail.com")
    smtp_password = os.getenv("SMTP_APP_PASSWORD", "").replace(" ", "")
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    from_name = os.getenv("MAIL_FROM_NAME", "Misión Copilot 365")
    base_url = os.getenv("APP_BASE_URL", "http://127.0.0.1:5000").rstrip("/")

    if not smtp_password:
        return False, "Falta SMTP_APP_PASSWORD en .env (contraseña de aplicación de Gmail)."

    login_url = f"{base_url}/login"
    body = f"""Hola {name},

Te damos acceso a la experiencia formativa:

Misión Copilot 365
De la productividad individual a la gestión inteligente de proyectos

Tu clave de acceso (guárdala; la usarás cada vez que entres):
{access_key}

Enlace de ingreso:
{login_url}

Indicaciones:
1. Abre el enlace.
2. Ingresa tu correo y tu clave de acceso.
3. Tu progreso quedará guardado en el sistema.

Esta es una capacitación académica. No compartas tu clave con otras personas.

— {from_name}
"""

    msg = EmailMessage()
    msg["Subject"] = "Tu clave de acceso · Misión Copilot 365"
    msg["From"] = f"{from_name} <{smtp_email}>"
    msg["To"] = to_email
    msg.set_content(body)

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.send_message(msg)
        return True, "Correo enviado"
    except Exception as exc:  # noqa: BLE001 — devolver detalle útil al admin
        return False, f"Error SMTP: {exc}"


def _smtp_config() -> tuple[str, str, str, int]:
    email = os.getenv("SMTP_EMAIL", "analizamostunegocio@gmail.com")
    password = os.getenv("SMTP_APP_PASSWORD", "").replace(" ", "")
    host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT", "587"))
    return email, password, host, port



def _lab33_horizonte_email_content() -> tuple[str, str]:
    """Correo de prueba del Lab 3.3. El asunto incluye [HORIZONTE] y el cuerpo 'Criticidad: ALTA'."""
    subject = "[HORIZONTE] Hallazgo de prueba · Laboratorio 3.3"
    body = """Buenos días,

Este mensaje es un caso académico ficticio para probar el flujo de Power Automate del Laboratorio 3.3.

ID: H-LAB-33
PROYECTO: Horizonte
HALLAZGO: Caso de práctica para la automatización del laboratorio.
FUENTE: Correo de prueba del Laboratorio 3.3.
Criticidad: ALTA
ESTADO: Requiere revisión humana.
ACCIÓN REQUERIDA: Validar antes de comunicar.

No presenta el proyecto como aprobado. No autoriza envíos externos por sí solo.

Cordialmente,
Dirección de Infraestructura
Proyecto Horizonte · caso académico ficticio
"""
    return subject, body


# Las 3 pruebas del libro paso a paso del Lab 3.3 (ALTA aprobada, ALTA rechazada, normal).
LAB33_TEST_EMAILS = {
    "lab33-1": (
        "[HORIZONTE] Falla en cadena de frío – bodega norte",
        "Criticidad: ALTA\n\nTemperatura fuera de rango por más de 2 horas.\n\n"
        "Prueba 1 del Laboratorio 3.3 · responde la aprobación con Aprobar.\n",
    ),
    "lab33-2": (
        "[HORIZONTE] Retraso de proveedor – lote 45",
        "CRITICIDAD : Alta\n\nEl proveedor reporta 3 días de retraso.\n\n"
        "Prueba 2 del Laboratorio 3.3 · responde la aprobación con Rechazar.\n",
    ),
    "lab33-3": (
        "[HORIZONTE] Actualización de inventario",
        "Criticidad: BAJA\n\nConteo semanal sin novedades.\n\n"
        "Prueba 3 del Laboratorio 3.3 · no debe llegar ninguna aprobación.\n",
    ),
}


def _s2_horizonte_email_content() -> tuple[str, str]:
    subject = "SOLICITUD DE ANÁLISIS | Proyecto Horizonte"
    body = """Buenos días,

Solicitamos realizar la revisión inicial del Proyecto Horizonte, iniciativa orientada a la modernización de infraestructura energética urbana.

Para este análisis se adjuntan los siguientes documentos:

- Documento preliminar de alcance.
- Presupuesto y cronograma.
- Transcripción de la reunión inicial.
- Registro preliminar de riesgos.
- Comentarios de los interesados.

El comité requiere recibir:

1. Resumen ejecutivo.
2. Alcance consolidado.
3. Hallazgos presupuestales.
4. Riesgos prioritarios.
5. Compromisos identificados.
6. Información faltante.
7. Decisiones requeridas.
8. Presentación ejecutiva.

Por favor, no asuma que la iniciativa está aprobada. Diferencie claramente la información confirmada, las propuestas y los elementos pendientes de validación.

Cordialmente,

Laura Méndez
Dirección de Infraestructura
"""
    return subject, body


def _reto1_email_content(to_email: str, name: str, smtp_email: str) -> tuple[str, str]:
    subject = "URGENTE · Reprogramación intervención preventivo Circuito N-14"
    body = """Buenos días, equipo:

La intervención de mantenimiento preventivo del Circuito N-14 (Zona Norte), programada para el sábado 21/03/2026 de 07:00 a 15:00, debe moverse al sábado 28/03/2026 en el mismo horario. Motivo: no hay disponibilidad confirmada del personal especialista en protecciones para la fecha original.

Necesito confirmación de recepción de este mensaje antes del martes 17/03/2026 a las 12:00.

Responsable técnico designado: Andrés Quintero. La junta de acción comunal reportó, el 12/03, preocupación por ruido en jornada nocturna. Aún no hay decisión formal sobre si la ventana se mantiene diurna o se evalúa nocturna.

Quedo atenta.

Laura Méndez
Coordinación de Campo · Ext. 4412
"""
    return subject, body


def _first_name(name: str) -> str:
    parts = (name or "").strip().split()
    return parts[0] if parts else "colegas"


def get_reto_r2_parts() -> list[dict]:
    """Cuatro correos de la cadena ST-Urb-03 (uno por pestaña del Reto 2)."""
    # De / Para = cabecera del caso (operativa). El estudiante recibe una copia en su bandeja.
    return [
        {
            "id": "r2-1",
            "label": "01 mar",
            "date": "01/03/2026",
            "from_name": "Martha Ríos · Planeación de Mantenimiento",
            "to_line": "Comunicaciones Zona; Logística de Materiales; Seguridad Industrial",
            "subject": "Programación transformador auxiliar ST-Urb-03",
            "sig": "Martha Ríos\nPlaneación de Mantenimiento · Zona Norte",
            "body_tpl": (
                "Buenos días,\n\n"
                "Se confirma el mantenimiento del transformador auxiliar de la subestación ST-Urb-03 "
                "para el 12/03/2026, en la ventana 08:00–14:00.\n\n"
                "Compromiso operativo: notificar a usuarios con mínimo 72 horas de anticipación.\n"
                "Responsable del aviso: Comunicaciones Zona.\n\n"
                "Quedo pendiente de cualquier novedad de agenda.\n\n"
                "{sig}\n"
            ),
        },
        {
            "id": "r2-2",
            "label": "04 mar",
            "date": "04/03/2026",
            "from_name": "Julián Pardo · Logística de Materiales",
            "to_line": "Planeación de Mantenimiento; Comunicaciones Zona; Seguridad Industrial",
            "subject": "RE: adelanto de repuestos · ST-Urb-03",
            "sig": "Julián Pardo\nLogística de Materiales",
            "body_tpl": (
                "Buenos días,\n\n"
                "El proveedor confirma entrega anticipada de los repuestos del transformador auxiliar.\n"
                "Con ese adelanto, proponemos mover la ventana de intervención al 10/03/2026 "
                "(misma franja preliminar 08:00–14:00).\n\n"
                "Pendiente: validar disponibilidad de personal de seguridad industrial para esa fecha "
                "antes de comunicar el cambio a la comunidad.\n\n"
                "Gracias.\n\n"
                "{sig}\n"
            ),
        },
        {
            "id": "r2-3",
            "label": "06 mar",
            "date": "06/03/2026",
            "from_name": "Carolina Vélez · Seguridad Industrial",
            "to_line": "Logística de Materiales; Planeación de Mantenimiento; Comunicaciones Zona",
            "subject": "RE: personal 10/03 · ST-Urb-03",
            "sig": "Carolina Vélez\nSeguridad Industrial · Zona Norte",
            "body_tpl": (
                "Buenos días,\n\n"
                "Confirmamos personal de seguridad industrial para el 10/03/2026.\n"
                "Solicitamos ampliar el cierre de área hasta las 16:00 para cubrir el retiro de equipos "
                "y la inspección final.\n\n"
                "Riesgo señalado: señalización insuficiente si no se refuerza el perímetro antes de las 07:30.\n"
                "Agradecemos coordinación con Comunicaciones Zona para el aviso a vecinos.\n\n"
                "Quedo atenta.\n\n"
                "{sig}\n"
            ),
        },
        {
            "id": "r2-4",
            "label": "07 mar",
            "date": "07/03/2026",
            "from_name": "Diego Castaño · Gerencia de Zona Norte",
            "to_line": "Comunicaciones Zona; Planeación de Mantenimiento; Seguridad Industrial; Logística de Materiales",
            "subject": "Aprobación ventana 10/03 · ST-Urb-03",
            "sig": "Diego Castaño\nGerencia de Zona Norte",
            "body_tpl": (
                "Equipo,\n\n"
                "Se aprueba la intervención del transformador auxiliar ST-Urb-03 el 10/03/2026 "
                "con cierre de área hasta las 16:00.\n\n"
                "Solicito:\n"
                "1) Mensaje claro a la comunidad con al menos 72 horas de anticipación.\n"
                "2) Reporte ejecutivo al cierre de la jornada (alcance, novedades y estado final).\n\n"
                "Favor confirmar recepción.\n\n"
                "{sig}\n"
            ),
        },
    ]


def get_reto_email_content(reto_id: str, to_email: str, name: str, smtp_email: str) -> tuple[str, str, str]:
    """Contenido centralizado. Retorna (subject, body, from_display_name).

    Los cuerpos van sin marcas de 'simulación': deben leerse como correo operativo real.
    """
    reto_id = (reto_id or "r1").strip().lower().replace("_", "-")
    if reto_id in ("r1", "reto1", "reto-1"):
        subject, body = _reto1_email_content(to_email, name, smtp_email)
        return subject, body, "Laura Méndez · Coordinación de Campo"

    if reto_id in ("s2", "s2-horizonte", "horizonte", "sesion2"):
        subject, body = _s2_horizonte_email_content()
        return subject, body, "Laura Méndez · Dirección de Infraestructura"

    if reto_id in LAB33_TEST_EMAILS:
        subject, body = LAB33_TEST_EMAILS[reto_id]
        return subject, body, "Laboratorio 3.3 · Proyecto Horizonte"

    if reto_id in ("lab33", "lab-33", "powerautomate", "pa33"):
        subject, body = _lab33_horizonte_email_content()
        return subject, body, "Laboratorio 3.3 · Proyecto Horizonte"

    # r2-all se resuelve en send_reto_email (4 envíos independientes)
    if reto_id in ("r2", "reto2", "reto-2", "r2-all", "r2all"):
        return "", "", ""

    aliases = {
        "r21": "r2-1", "r22": "r2-2", "r23": "r2-3", "r24": "r2-4",
        "reto2-1": "r2-1", "reto2-2": "r2-2", "reto2-3": "r2-3", "reto2-4": "r2-4",
    }
    reto_id = aliases.get(reto_id, reto_id)

    for p in get_reto_r2_parts():
        if reto_id == p["id"]:
            body = p["body_tpl"].format(sig=p["sig"])
            return p["subject"], body, p["from_name"]

    return "", "", ""


def list_reto_email_ids() -> list[str]:
    return ["r1", "r2", "r2-all", "s2", "lab33", *LAB33_TEST_EMAILS] + [p["id"] for p in get_reto_r2_parts()]


def _send_email_smtp(to_email: str, subject: str, body: str, from_display: str) -> tuple[bool, str]:
    smtp_email, smtp_password, smtp_host, smtp_port = _smtp_config()
    if not smtp_password:
        return False, "Falta SMTP_APP_PASSWORD en .env"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_display
    msg["To"] = to_email
    msg["Reply-To"] = smtp_email
    msg.set_content(body)
    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.send_message(msg)
        return True, f"Enviado por SMTP a {to_email}"
    except OSError as exc:
        return False, (
            f"SMTP bloqueado o inaccesible ({exc}). "
            "En PythonAnywhere gratuito el puerto 587 suele estar cerrado. "
            "Usa EMAIL_WEBHOOK_URL (Google Apps Script) — ver scripts/gmail_reto1_webhook.gs"
        )
    except Exception as exc:  # noqa: BLE001
        return False, f"Error SMTP: {exc}"


def _send_email_webhook(
    to_email: str,
    name: str,
    subject: str,
    body: str,
    from_name: str = "Laura Méndez · Coordinación de Campo",
) -> tuple[bool, str]:
    """Envío por HTTPS. Re-POSTea redirects de Apps Script y exige JSON ok:true."""
    import json
    import urllib.error
    import urllib.request

    url = (os.getenv("EMAIL_WEBHOOK_URL") or "").strip()
    if not url:
        return False, "EMAIL_WEBHOOK_URL no configurada"
    if "/dev" in url:
        return False, "EMAIL_WEBHOOK_URL usa /dev (solo dueño). Despliega e usa la URL /exec."

    payload = json.dumps(
        {
            "to": to_email,
            "name": name,
            "subject": subject,
            "body": body,
            "fromName": from_name,
            "secret": (os.getenv("EMAIL_WEBHOOK_SECRET") or "").strip(),
        },
        ensure_ascii=False,
    ).encode("utf-8")

    class _NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
            return None

    opener = urllib.request.build_opener(_NoRedirect)

    def _post_once(target: str):
        req = urllib.request.Request(
            target,
            data=payload,
            headers={"Content-Type": "application/json", "User-Agent": "mision-copilot-365"},
            method="POST",
        )
        return opener.open(req, timeout=25)

    try:
        current = url
        raw = ""
        status = 0
        for _ in range(5):
            try:
                with _post_once(current) as resp:
                    status = getattr(resp, "status", 200) or 200
                    raw = resp.read().decode("utf-8", errors="replace")
                    break
            except urllib.error.HTTPError as exc:
                if exc.code in (301, 302, 303, 307, 308):
                    loc = exc.headers.get("Location") or ""
                    if not loc:
                        return False, f"Webhook redirect {exc.code} sin Location"
                    if loc.startswith("/"):
                        from urllib.parse import urljoin

                        loc = urljoin(current, loc)
                    current = loc
                    continue
                detail = exc.read().decode("utf-8", errors="replace")[:240]
                return False, f"Webhook HTTP {exc.code}: {detail}"
        else:
            return False, "Webhook: demasiados redirects"

        if status >= 400:
            return False, f"Webhook HTTP {status}: {raw[:200]}"

        text = (raw or "").strip()
        if not text:
            return False, (
                "Webhook respondió vacío. Revisa: app web publicada como "
                "'Cualquier persona', URL /exec, y secreto igual en .env y el .gs"
            )
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            snippet = text[:180].replace("\n", " ")
            return False, (
                f"Webhook no devolvió JSON (¿página de permiso?). Respuesta: {snippet}. "
                "Vuelve a Implementar la app web en script.google.com (acceso: Cualquiera)."
            )
        if not data.get("ok"):
            err = data.get("error") or data.get("message") or text[:160]
            return False, f"Webhook rechazó el envío: {err}"
        return True, f"Enviado por webhook HTTPS a {to_email}"
    except Exception as exc:  # noqa: BLE001
        return False, f"Webhook falló: {exc}"


def _send_email_resend(to_email: str, subject: str, body: str) -> tuple[bool, str]:
    import json
    import urllib.error
    import urllib.request

    api_key = (os.getenv("RESEND_API_KEY") or "").strip()
    if not api_key:
        return False, "RESEND_API_KEY no configurada"

    smtp_email, _, _, _ = _smtp_config()
    from_addr = os.getenv("RESEND_FROM", smtp_email)
    payload = json.dumps(
        {
            "from": f"Laura Méndez <{from_addr}>",
            "to": [to_email],
            "subject": subject,
            "text": body,
        },
        ensure_ascii=False,
    ).encode("utf-8")
    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            if resp.status >= 400:
                return False, f"Resend HTTP {resp.status}"
            return True, f"Enviado por Resend a {to_email}"
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:220]
        return False, f"Resend HTTP {exc.code}: {detail}"
    except Exception as exc:  # noqa: BLE001
        return False, f"Resend falló: {exc}"


def _deliver_reto_message(
    to_email: str, name: str, subject: str, body: str, from_name: str
) -> tuple[bool, str]:
    smtp_email, smtp_password, _, _ = _smtp_config()
    from_display = f"{from_name} <{smtp_email}>"
    errors: list[str] = []
    if (os.getenv("EMAIL_WEBHOOK_URL") or "").strip():
        ok, detail = _send_email_webhook(to_email, name, subject, body, from_name)
        if ok:
            return True, detail
        errors.append(detail)
    if (os.getenv("RESEND_API_KEY") or "").strip():
        ok, detail = _send_email_resend(to_email, subject, body)
        if ok:
            return True, detail
        errors.append(detail)
    if smtp_password:
        ok, detail = _send_email_smtp(to_email, subject, body, from_display)
        if ok:
            return True, detail
        errors.append(detail)
    else:
        errors.append("Falta SMTP_APP_PASSWORD en .env")
    return False, " · ".join(errors) if errors else "No hay método de envío configurado"


def send_reto_email(reto_id: str, to_email: str, name: str) -> tuple[bool, str]:
    smtp_email, _, _, _ = _smtp_config()
    reto_norm = (reto_id or "r1").strip().lower().replace("_", "-")

    # Cadena R2: cuatro correos independientes (no un resumen pedagógico)
    if reto_norm in ("r2", "reto2", "reto-2", "r2-all", "r2all"):
        sent = 0
        fails: list[str] = []
        for p in get_reto_r2_parts():
            subject, body, from_name = get_reto_email_content(p["id"], to_email, name, smtp_email)
            ok, detail = _deliver_reto_message(to_email, name, subject, body, from_name)
            if ok:
                sent += 1
            else:
                fails.append(f"{p['label']}: {detail}")
        if sent == 4:
            return True, f"Enviados 4 correos de la cadena ST-Urb-03 a {to_email}"
        if sent > 0:
            return False, f"Solo llegaron {sent}/4. " + " · ".join(fails)
        return False, " · ".join(fails) if fails else "No se pudo enviar la cadena"

    subject, body, from_name = get_reto_email_content(reto_norm, to_email, name, smtp_email)
    if not subject or not body:
        disponibles = ", ".join(list_reto_email_ids())
        return False, (
            f"No hay correo simulado configurado para el reto '{reto_id}'. "
            f"IDs válidos en este servidor: {disponibles}. "
            "Si esperabas r2-1/r2-all, ejecuta git pull + Web Reload en PythonAnywhere."
        )
    return _deliver_reto_message(to_email, name, subject, body, from_name)

def send_reto1_email(to_email: str, name: str) -> tuple[bool, str]:
    """Envía el correo operativo del Reto 1. Prioriza HTTPS (webhook/Resend) y luego SMTP."""
    return send_reto_email('r1', to_email, name)


def send_admin_notification(name: str, email: str) -> tuple[bool, str]:
    """Avisa al admin que hay una solicitud de clave pendiente."""
    smtp_email = os.getenv("SMTP_EMAIL", "analizamostunegocio@gmail.com")
    smtp_password = os.getenv("SMTP_APP_PASSWORD", "").replace(" ", "")
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    from_name = os.getenv("MAIL_FROM_NAME", "Misión Copilot 365")
    base_url = os.getenv("APP_BASE_URL", "http://127.0.0.1:5000").rstrip("/")
    admin_to = smtp_email

    if not smtp_password:
        return False, "Falta SMTP_APP_PASSWORD"

    body = f"""Nueva solicitud de acceso a Misión Copilot 365

Nombre: {name}
Correo: {email}

Revisa y aprueba en el panel:
{base_url}/admin

— Sistema {from_name}
"""
    msg = EmailMessage()
    msg["Subject"] = f"Solicitud de clave · {name}"
    msg["From"] = f"{from_name} <{smtp_email}>"
    msg["To"] = admin_to
    msg.set_content(body)
    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
            server.starttls()
            server.login(smtp_email, smtp_password)
            server.send_message(msg)
        return True, "ok"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


def create_student_record(db: sqlite3.Connection, name: str, email: str) -> tuple[int, str]:
    access_key = generate_access_key()
    cur = db.execute(
        """
        INSERT INTO students (name, email, access_key, key_hash, active, created_at)
        VALUES (?, ?, ?, ?, 1, ?)
        """,
        (name, email, access_key, generate_password_hash(access_key), utc_now()),
    )
    student_id = cur.lastrowid
    db.execute(
        "INSERT INTO progress (student_id, payload, percent, updated_at) VALUES (?, '{}', 0, ?)",
        (student_id, utc_now()),
    )
    db.commit()
    return student_id, access_key


def student_summary(row: sqlite3.Row, progress_row: sqlite3.Row | None) -> dict:
    payload = {}
    percent = 0
    updated_at = None
    if progress_row:
        try:
            payload = json.loads(progress_row["payload"] or "{}")
        except json.JSONDecodeError:
            payload = {}
        percent = progress_row["percent"] or 0
        updated_at = progress_row["updated_at"]

    progress = payload.get("progress") or {}
    return {
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
        "active": bool(row["active"]),
        "created_at": row["created_at"],
        "last_login": row["last_login"],
        "email_sent_at": row["email_sent_at"],
        "percent": percent,
        "updated_at": updated_at,
        "retos": sum(1 for k in ["reto-r1","reto-r2","reto-r3","reto-r4","reto-r5","reto-r6"] if progress.get(k)),
        "s1": bool(progress.get("s1-done")),
        "s2": bool(progress.get("s2-done")),
        "proyecto": bool(progress.get("proyecto-final")),
        "quiz": int((payload.get("quiz") or {}).get("score") or 0),
    }


# ---------------------------------------------------------------------------
# Archivos estáticos del front
# ---------------------------------------------------------------------------

# Nota de seguridad: no exponer BASE_DIR completo (contiene .env, data/mision.db y código).
# Solo se publican archivos concretos y la carpeta planillas/, siempre con sesión.
# material_privado/ no tiene ruta propia: solo se entrega por la lista cerrada de abajo.

PLANILLAS_SOLO_FACILITADORA = {"00_Guia_Instructor_Sesion2.docx"}


@app.get("/planillas/<path:filename>")
@require_login_any
def planillas(filename: str):
    if filename in PLANILLAS_SOLO_FACILITADORA and not session.get("is_admin"):
        return jsonify({"ok": False, "error": "Archivo no encontrado"}), 404
    resp = send_from_directory(BASE_DIR / "planillas", filename)
    resp.headers["Cache-Control"] = "private, no-store"
    return resp


PASO4_DIR = BASE_DIR / "material_privado" / "paso4"
PASO4_LIBRO = "Laboratorio_3.3_Libro_Power_Automate.html"
# Descargas del Paso 4: clave → nombre original del archivo.
PASO4_DESCARGAS = {
    "plantilla": "Horizonte_Trazabilidad.xlsx",
    "ejemplo": "Horizonte_Trazabilidad_Ejemplo.xlsx",
    "skill-analizar": "analizar-trazabilidad.zip",
    "skill-informe": "informe-comite.zip",
}


@app.get("/laboratorio-3-3/libro")
@require_login_any
def lab33_libro():
    resp = send_file(PASO4_DIR / PASO4_LIBRO, mimetype="text/html")
    resp.headers["Cache-Control"] = "private, no-store"
    return resp


@app.get("/material/paso4/<clave>")
@require_login_any
def paso4_descarga(clave: str):
    nombre = PASO4_DESCARGAS.get(clave)
    if not nombre:
        return jsonify({"ok": False, "error": "Archivo no encontrado"}), 404
    resp = send_file(PASO4_DIR / nombre, as_attachment=True, download_name=nombre)
    resp.headers["Cache-Control"] = "private, no-store"
    return resp


@app.get("/logo.png")
def logo():
    return send_from_directory(BASE_DIR, "logo.png")


@app.get("/fondo-corporativo.png")
def fondo():
    return send_from_directory(BASE_DIR, "fondo-corporativo.png")


# ---------------------------------------------------------------------------
# Auth estudiante
# ---------------------------------------------------------------------------

@app.get("/login")
def login():
    if session.get("student_id"):
        return redirect(url_for("mission"))
    if session.get("is_admin"):
        return redirect(url_for("admin_home"))
    return render_template("login.html")


@app.post("/login")
def login_post():
    email = (request.form.get("email") or "").strip().lower()
    access_key = (request.form.get("access_key") or "").strip().upper()

    if not email or not access_key:
        return render_template("login.html", error="Completa correo y clave de acceso."), 400

    db = get_db()
    row = db.execute(
        "SELECT * FROM students WHERE email = ? AND active = 1",
        (email,),
    ).fetchone()

    if not row or not check_password_hash(row["key_hash"], access_key):
        return render_template(
            "login.html",
            error="Correo o clave incorrectos. Si no tienes clave, solicítala abajo.",
        ), 401

    db.execute("UPDATE students SET last_login = ? WHERE id = ?", (utc_now(), row["id"]))
    db.commit()

    session.clear()
    session["student_id"] = row["id"]
    session["student_name"] = row["name"]
    session["student_email"] = row["email"]
    return redirect(url_for("mission"))


@app.get("/solicitar-clave")
def solicitar_clave():
    if session.get("student_id"):
        return redirect(url_for("mission"))
    return render_template("solicitar.html")


@app.post("/solicitar-clave")
def solicitar_clave_post():
    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip().lower()

    if not name or not email or "@" not in email:
        return render_template("solicitar.html", error="Nombre y correo válidos son obligatorios."), 400

    db = get_db()
    existing = db.execute(
        "SELECT id FROM students WHERE email = ? AND active = 1",
        (email,),
    ).fetchone()
    if existing:
        return render_template(
            "solicitar.html",
            error="Este correo ya tiene acceso. Revisa tu bandeja o pide reenvío al administrador.",
            info=None,
        ), 400

    pending = db.execute(
        "SELECT id FROM access_requests WHERE email = ? AND status = 'pending'",
        (email,),
    ).fetchone()
    if pending:
        return render_template(
            "solicitar.html",
            info="Ya tienes una solicitud pendiente. Te enviaremos la clave cuando sea aprobada.",
        )

    db.execute(
        """
        INSERT INTO access_requests (name, email, status, created_at)
        VALUES (?, ?, 'pending', ?)
        """,
        (name, email, utc_now()),
    )
    db.commit()
    send_admin_notification(name, email)

    return render_template(
        "solicitar.html",
        info="Solicitud enviada. Cuando se apruebe, recibirás tu clave en el correo indicado.",
    )


@app.post("/logout")
@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.get("/")
def root():
    if session.get("is_admin"):
        return redirect(url_for("admin_home"))
    if session.get("student_id"):
        return send_from_directory(BASE_DIR, "index.html")
    return redirect(url_for("login"))


@app.get("/mision")
@require_student
def mission():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/horizonte")
def horizonte_portal():
    """Portal público del caso Proyecto Horizonte (fuente web para Agente PMO)."""
    return send_from_directory(BASE_DIR, "horizonte.html")


# Página pública del caso (solo texto, documentos 02-06). Se genera con
# scripts/build_caso_horizonte.py. Un solo nivel, sin parámetros ni redirecciones,
# para que el Agente PMO pueda usarla como conocimiento web cuando Bing la indexe.
PUBLIC_PAGES = ["/caso-horizonte"]


def _public_base_url() -> str:
    """URL pública para robots/sitemap. En PythonAnywhere el proxy entrega http: se fuerza https."""
    env = (os.getenv("APP_BASE_URL") or "").strip().rstrip("/")
    if env.startswith("https://"):
        return env
    root = request.url_root.rstrip("/")
    if request.host.endswith(".pythonanywhere.com") and root.startswith("http://"):
        root = "https://" + root[len("http://"):]
    return root


@app.get("/caso-horizonte")
def caso_horizonte():
    resp = send_file(BASE_DIR / "caso-horizonte.html", mimetype="text/html")
    resp.headers["Cache-Control"] = "public, max-age=3600"
    resp.headers["X-Robots-Tag"] = "index, follow"
    return resp


@app.get("/robots.txt")
def robots_txt():
    base = _public_base_url()
    body = "\n".join([
        "User-agent: *",
        *[f"Allow: {p}" for p in PUBLIC_PAGES],
        "Disallow: /admin",
        "Disallow: /api/",
        "Disallow: /presentar",
        "Disallow: /mision",
        "Disallow: /planillas/",
        "Disallow: /material/",
        "Disallow: /laboratorio-3-3/",
        "",
        f"Sitemap: {base}/sitemap.xml",
        "",
    ])
    return app.response_class(body, mimetype="text/plain")


@app.get("/sitemap.xml")
def sitemap_xml():
    base = _public_base_url()
    lastmod = time.strftime("%Y-%m-%d", time.gmtime((BASE_DIR / "caso-horizonte.html").stat().st_mtime))
    urls = "".join(
        f"  <url><loc>{base}{p}</loc><lastmod>{lastmod}</lastmod></url>\n" for p in PUBLIC_PAGES
    )
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}</urlset>\n"
    )
    return app.response_class(body, mimetype="application/xml")


# ---------------------------------------------------------------------------
# API progreso estudiante
# ---------------------------------------------------------------------------

@app.get("/api/me")
def api_me():
    if session.get("is_admin") and not session.get("student_id"):
        return jsonify({"ok": True, "admin": True, "student": None})
    if not session.get("student_id"):
        return jsonify({"ok": False, "error": "Sesión requerida"}), 401
    return jsonify(
        {
            "ok": True,
            "student": {
                "id": session["student_id"],
                "name": session.get("student_name"),
                "email": session.get("student_email"),
            },
        }
    )



@app.post("/api/reto/send-email")
@require_student
def api_send_reto_email():
    """Envía el correo simulado del reto indicado al estudiante autenticado."""
    payload = request.get_json(silent=True) or {}
    reto_id = (payload.get("reto_id") or request.args.get("reto_id") or "r1").strip().lower()
    to_email = (session.get("student_email") or "").strip()
    name = (session.get("student_name") or "Participante").strip()
    if not to_email:
        return jsonify({"ok": False, "error": "No hay correo en la sesión. Vuelve a iniciar sesión."}), 400

    now = datetime.now(timezone.utc).timestamp()
    key = f"reto_email_at_{reto_id}"
    last = float(session.get(key) or 0)
    wait = 90 - int(now - last)
    if wait > 0:
        return jsonify({"ok": False, "error": f"Espera {wait} s antes de reenviar este reto."}), 429

    ok, detail = send_reto_email(reto_id, to_email, name)
    if not ok:
        return jsonify({"ok": False, "error": detail}), 502

    session[key] = now
    smtp_email = os.getenv("SMTP_EMAIL", "analizamostunegocio@gmail.com")
    subject, _, from_name = get_reto_email_content(reto_id, to_email, name, smtp_email)
    emails_sent = []
    rid = reto_id.replace("_", "-")
    if rid in ("r2", "reto2", "reto-2", "r2-all", "r2all"):
        subject = "4 correos ST-Urb-03 (Martha, Julián, Carolina, Diego)"
        for p in get_reto_r2_parts():
            emails_sent.append({
                "id": p["id"],
                "from": p["from_name"],
                "to": p["to_line"],
                "subject": p["subject"],
            })
    elif subject:
        emails_sent.append({
            "id": rid,
            "from": from_name,
            "to": to_email,
            "subject": subject,
        })
    self_send = to_email.lower() == smtp_email.lower()
    tip = ""
    if self_send:
        tip = (
            " Estás enviando a la misma cuenta Gmail de salida: puede no verse en Recibidos. "
            "Revisa Enviados / Todos / Spam, o inicia sesión con el correo del estudiante."
        )
    return jsonify({
        "ok": True,
        "message": detail + tip,
        "to": to_email,
        "from": from_name or smtp_email,
        "subject": subject,
        "reto_id": reto_id,
        "self_send": self_send,
        "emails": emails_sent,
        "note": (
            "Ignora correos viejos con asunto 'Cadena ST-Urb-03 · 4 correos del Reto 2 (resumen)' "
            "o texto 'Simulación Reto 2'. Ese formato ya no se usa."
        ),
    })


@app.post("/api/reto1/send-email")
@require_student
def api_send_reto1_email():
    """Envía el correo del Reto 1 a la bandeja del estudiante autenticado."""
    to_email = (session.get("student_email") or "").strip()
    name = (session.get("student_name") or "Participante").strip()
    if not to_email:
        return jsonify({"ok": False, "error": "No hay correo en la sesión. Vuelve a iniciar sesión."}), 400

    # Anti-spam: máximo 1 envío cada 90 segundos por sesión
    now = datetime.now(timezone.utc).timestamp()
    last = float(session.get("reto1_email_at") or 0)
    wait = 90 - int(now - last)
    if wait > 0:
        return jsonify({
            "ok": False,
            "error": f"Espera {wait} s antes de reenviar el correo del reto.",
        }), 429

    ok, detail = send_reto1_email(to_email, name)
    if not ok:
        return jsonify({"ok": False, "error": detail}), 502

    session["reto1_email_at"] = now
    return jsonify({
        "ok": True,
        "message": detail,
        "to": to_email,
        "from": os.getenv("SMTP_EMAIL", "analizamostunegocio@gmail.com"),
        "subject": "URGENTE · Reprogramación intervención preventivo Circuito N-14",
    })


@app.get("/api/reto1/email-status")
@require_student
def api_reto1_email_status():
    """Diagnóstico de envío para el estudiante autenticado."""
    _, smtp_password, _, _ = _smtp_config()
    return jsonify({
        "ok": True,
        "student_email": session.get("student_email"),
        "smtp_configured": bool(smtp_password),
        "webhook_configured": bool((os.getenv("EMAIL_WEBHOOK_URL") or "").strip()),
        "resend_configured": bool((os.getenv("RESEND_API_KEY") or "").strip()),
        "endpoint": "/api/reto1/send-email",
    })


@app.get("/api/progress")
@require_student
def api_get_progress():
    db = get_db()
    row = db.execute(
        "SELECT payload, percent, updated_at FROM progress WHERE student_id = ?",
        (session["student_id"],),
    ).fetchone()
    if not row:
        return jsonify({"ok": True, "payload": {}, "percent": 0, "updated_at": None})
    try:
        payload = json.loads(row["payload"] or "{}")
    except json.JSONDecodeError:
        payload = {}
    return jsonify(
        {
            "ok": True,
            "payload": payload,
            "percent": row["percent"],
            "updated_at": row["updated_at"],
        }
    )


@app.post("/api/progress")
@require_student
def api_save_progress():
    data = request.get_json(silent=True) or {}
    payload = data.get("payload")
    if not isinstance(payload, dict):
        return jsonify({"ok": False, "error": "payload inválido"}), 400

    percent = calc_percent_from_payload(payload)
    now = utc_now()
    db = get_db()
    db.execute(
        """
        INSERT INTO progress (student_id, payload, percent, updated_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(student_id) DO UPDATE SET
            payload = excluded.payload,
            percent = excluded.percent,
            updated_at = excluded.updated_at
        """,
        (session["student_id"], json.dumps(payload, ensure_ascii=False), percent, now),
    )
    db.commit()
    return jsonify({"ok": True, "percent": percent, "updated_at": now})


# ---------------------------------------------------------------------------
# Admin
# ---------------------------------------------------------------------------

@app.get("/admin/login")
def admin_login():
    if session.get("is_admin"):
        return redirect(url_for("admin_home"))
    return render_template("admin_login.html")


@app.post("/admin/login")
def admin_login_post():
    password = request.form.get("password") or ""
    expected = os.getenv("ADMIN_PASSWORD", "")
    if not expected:
        return render_template(
            "admin_login.html",
            error="Configura ADMIN_PASSWORD en el archivo .env",
        ), 500
    if password != expected:
        return render_template("admin_login.html", error="Contraseña incorrecta."), 401
    session.clear()
    session["is_admin"] = True
    return redirect(url_for("admin_home"))


@app.get("/admin")
@require_admin
def admin_home():
    db = get_db()
    students = db.execute(
        """
        SELECT s.*, p.payload, p.percent, p.updated_at
        FROM students s
        LEFT JOIN progress p ON p.student_id = s.id
        ORDER BY s.created_at DESC
        """
    ).fetchall()

    rows = []
    for s in students:
        summary = {
            "id": s["id"],
            "name": s["name"],
            "email": s["email"],
            "active": bool(s["active"]),
            "created_at": s["created_at"],
            "last_login": s["last_login"],
            "email_sent_at": s["email_sent_at"],
            "percent": s["percent"] or 0,
            "updated_at": s["updated_at"],
            "retos": 0,
            "actividades": 0,
            "cierre": None,
            "s1": False,
            "s2": False,
            "proyecto": False,
            "quiz": 0,
        }
        if s["payload"]:
            try:
                payload = json.loads(s["payload"])
            except json.JSONDecodeError:
                payload = {}
            progress = payload.get("progress") or {}
            summary["retos"] = sum(
                1
                for k in ["reto-r1", "reto-r2", "reto-r3", "reto-r4", "reto-r5", "reto-r6"]
                if progress.get(k)
            )
            summary["s1"] = bool(progress.get("s1-done"))
            summary["s2"] = bool(progress.get("s2-done"))
            summary["proyecto"] = bool(progress.get("proyecto-final"))
            summary["quiz"] = int((payload.get("quiz") or {}).get("score") or 0)
            summary["actividades"] = activity_progress(payload)[1]
            summary["cierre"] = cierre_summary(payload)
        rows.append(summary)

    requests_pending = db.execute(
        """
        SELECT * FROM access_requests
        WHERE status = 'pending'
        ORDER BY created_at ASC
        """
    ).fetchall()

    stats = {
        "total": len(rows),
        "activos": sum(1 for r in rows if r["active"]),
        "con_avance": sum(1 for r in rows if r["percent"] > 0),
        "promedio": int(round(sum(r["percent"] for r in rows) / len(rows), 0)) if rows else 0,
        "solicitudes": len(requests_pending),
    }
    # Lo que se llevan y lo que van a hacer (cierre del curso)
    cierres = [r for r in rows if r.get("cierre") and (r["cierre"]["ideas"] or r["cierre"]["primer_paso"] or r["cierre"]["dudas"])]
    idea_counts: dict[str, int] = {}
    for r in cierres:
        for i in r["cierre"]["idea_ids"]:
            idea_counts[i] = idea_counts.get(i, 0) + 1
    top_ideas = sorted(((CIERRE_IDEAS[i], n) for i, n in idea_counts.items()), key=lambda x: -x[1])
    conf_avg = []
    for cid, label in CIERRE_CAPS:
        pares = [r["cierre"]["conf"].get(cid) for r in cierres if r["cierre"]["conf"].get(cid, {}).get("antes") and r["cierre"]["conf"].get(cid, {}).get("hoy")]
        if pares:
            antes = sum(p["antes"] for p in pares) / len(pares)
            hoy = sum(p["hoy"] for p in pares) / len(pares)
            conf_avg.append({"label": label, "antes": round(antes, 1), "hoy": round(hoy, 1), "delta": round(hoy - antes, 1), "n": len(pares)})
    flash = session.pop("flash", None)
    return render_template(
        "admin.html",
        students=rows,
        stats=stats,
        cierres=cierres,
        top_ideas=top_ideas,
        conf_avg=conf_avg,
        activity_total=activity_progress({})[2],
        flash=flash,
        requests=requests_pending,
    )


@app.post("/admin/students")
@require_admin
def admin_create_student():
    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip().lower()
    send_mail = request.form.get("send_email") == "on"

    if not name or not email or "@" not in email:
        session["flash"] = {"type": "error", "msg": "Nombre y correo válidos son obligatorios."}
        return redirect(url_for("admin_home"))

    db = get_db()
    try:
        student_id, access_key = create_student_record(db, name, email)
    except sqlite3.IntegrityError:
        session["flash"] = {"type": "error", "msg": f"Ya existe un estudiante con el correo {email}."}
        return redirect(url_for("admin_home"))

    mail_note = ""
    if send_mail:
        ok, detail = send_access_email(email, name, access_key)
        if ok:
            db.execute("UPDATE students SET email_sent_at = ? WHERE id = ?", (utc_now(), student_id))
            db.commit()
            mail_note = " Correo enviado."
        else:
            mail_note = f" Correo NO enviado: {detail}"

    session["flash"] = {
        "type": "ok",
        "msg": f"Estudiante creado. Clave: {access_key}.{mail_note}",
        "key": access_key,
    }
    return redirect(url_for("admin_home"))


@app.post("/admin/requests/<int:request_id>/approve")
@require_admin
def admin_approve_request(request_id: int):
    db = get_db()
    req = db.execute("SELECT * FROM access_requests WHERE id = ?", (request_id,)).fetchone()
    if not req or req["status"] != "pending":
        session["flash"] = {"type": "error", "msg": "Solicitud no encontrada o ya resuelta."}
        return redirect(url_for("admin_home"))

    existing = db.execute(
        "SELECT id, access_key, name FROM students WHERE email = ?",
        (req["email"],),
    ).fetchone()

    if existing:
        access_key = existing["access_key"]
        student_id = existing["id"]
        name = existing["name"] or req["name"]
        db.execute("UPDATE students SET active = 1 WHERE id = ?", (student_id,))
    else:
        student_id, access_key = create_student_record(db, req["name"], req["email"])
        name = req["name"]

    ok, detail = send_access_email(req["email"], name, access_key)
    db.execute(
        "UPDATE access_requests SET status = 'approved', resolved_at = ?, note = ? WHERE id = ?",
        (utc_now(), detail if not ok else "clave enviada", request_id),
    )
    if ok:
        db.execute("UPDATE students SET email_sent_at = ? WHERE id = ?", (utc_now(), student_id))
    db.commit()

    if ok:
        session["flash"] = {
            "type": "ok",
            "msg": f"Solicitud aprobada. Clave enviada a {req['email']}.",
            "key": access_key,
        }
    else:
        session["flash"] = {
            "type": "error",
            "msg": f"Estudiante creado, pero el correo falló: {detail}. Clave: {access_key}",
            "key": access_key,
        }
    return redirect(url_for("admin_home"))


@app.post("/admin/requests/<int:request_id>/reject")
@require_admin
def admin_reject_request(request_id: int):
    db = get_db()
    db.execute(
        "UPDATE access_requests SET status = 'rejected', resolved_at = ? WHERE id = ? AND status = 'pending'",
        (utc_now(), request_id),
    )
    db.commit()
    session["flash"] = {"type": "ok", "msg": "Solicitud rechazada."}
    return redirect(url_for("admin_home"))


@app.post("/admin/students/<int:student_id>/resend")
@require_admin
def admin_resend(student_id: int):
    db = get_db()
    row = db.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    if not row:
        session["flash"] = {"type": "error", "msg": "Estudiante no encontrado."}
        return redirect(url_for("admin_home"))

    # La clave en texto se guarda para reenvío administrativo controlado
    access_key = row["access_key"]
    ok, detail = send_access_email(row["email"], row["name"], access_key)
    if ok:
        db.execute("UPDATE students SET email_sent_at = ? WHERE id = ?", (utc_now(), student_id))
        db.commit()
        session["flash"] = {"type": "ok", "msg": f"Clave reenviada a {row['email']}."}
    else:
        session["flash"] = {"type": "error", "msg": detail}
    return redirect(url_for("admin_home"))


@app.post("/admin/students/<int:student_id>/toggle")
@require_admin
def admin_toggle(student_id: int):
    db = get_db()
    row = db.execute("SELECT active FROM students WHERE id = ?", (student_id,)).fetchone()
    if not row:
        session["flash"] = {"type": "error", "msg": "Estudiante no encontrado."}
        return redirect(url_for("admin_home"))
    new_val = 0 if row["active"] else 1
    db.execute("UPDATE students SET active = ? WHERE id = ?", (new_val, student_id))
    db.commit()
    session["flash"] = {"type": "ok", "msg": "Estado de acceso actualizado."}
    return redirect(url_for("admin_home"))


@app.post("/admin/students/<int:student_id>/reset-progress")
@require_admin
def admin_reset_progress(student_id: int):
    db = get_db()
    db.execute(
        "UPDATE progress SET payload = '{}', percent = 0, updated_at = ? WHERE student_id = ?",
        (utc_now(), student_id),
    )
    db.commit()
    session["flash"] = {"type": "ok", "msg": "Progreso reiniciado."}
    return redirect(url_for("admin_home"))


@app.get("/api/admin/students")
@require_admin
def api_admin_students():
    """JSON para refrescar el panel sin recargar (opcional)."""
    db = get_db()
    students = db.execute(
        """
        SELECT s.*, p.payload, p.percent, p.updated_at
        FROM students s
        LEFT JOIN progress p ON p.student_id = s.id
        ORDER BY s.created_at DESC
        """
    ).fetchall()
    out = []
    for s in students:
        payload = {}
        if s["payload"]:
            try:
                payload = json.loads(s["payload"])
            except json.JSONDecodeError:
                payload = {}
        progress = payload.get("progress") or {}
        out.append(
            {
                "id": s["id"],
                "name": s["name"],
                "email": s["email"],
                "active": bool(s["active"]),
                "percent": s["percent"] or 0,
                "last_login": s["last_login"],
                "updated_at": s["updated_at"],
                "retos": sum(1 for k in ["reto-r1","reto-r2","reto-r3","reto-r4","reto-r5","reto-r6"] if progress.get(k)),
                "s1": bool(progress.get("s1-done")),
                "s2": bool(progress.get("s2-done")),
                "proyecto": bool(progress.get("proyecto-final")),
                "quiz": int((payload.get("quiz") or {}).get("score") or 0),
            }
        )
    return jsonify({"ok": True, "students": out})


# ---------------------------------------------------------------------------
# Clase en vivo: presencia, votaciones y panel de la instructora
# ---------------------------------------------------------------------------

def _active_pulse(db) -> str | None:
    row = db.execute("SELECT value, updated_at FROM app_settings WHERE key = 'active_pulse'").fetchone()
    if not row or not row["value"] or row["value"] not in PULSES:
        return None
    if time.time() - (row["updated_at"] or 0) > PULSE_TTL_S:
        return None
    return row["value"]


def _pulse_results(db, qid: str) -> dict:
    question, options = PULSES[qid]
    counts = [0] * len(options)
    for r in db.execute("SELECT answer, COUNT(*) AS n FROM pulse_votes WHERE qid = ? GROUP BY answer", (qid,)):
        if 0 <= r["answer"] < len(options):
            counts[r["answer"]] = r["n"]
    return {"qid": qid, "question": question, "options": options, "counts": counts, "total": sum(counts)}


@app.post("/api/live/ping")
@require_student
def api_live_ping():
    """Señal de presencia del estudiante (paso actual) y consulta de votación abierta."""
    data = request.get_json(silent=True) or {}
    clip = lambda v, n: str(v or "")[:n]
    db = get_db()
    db.execute(
        """
        INSERT INTO presence (student_id, step, title, module, seen_at) VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(student_id) DO UPDATE SET step = excluded.step, title = excluded.title,
            module = excluded.module, seen_at = excluded.seen_at
        """,
        (session["student_id"], clip(data.get("step"), 80), clip(data.get("title"), 160), clip(data.get("module"), 80), time.time()),
    )
    db.commit()
    qid = _active_pulse(db)
    pulse = None
    if qid:
        mine = db.execute("SELECT answer FROM pulse_votes WHERE student_id = ? AND qid = ?", (session["student_id"], qid)).fetchone()
        question, options = PULSES[qid]
        pulse = {"qid": qid, "question": question, "options": options, "mine": mine["answer"] if mine else None}
    return jsonify({"ok": True, "pulse": pulse})


@app.post("/api/pulse")
@require_student
def api_pulse_vote():
    data = request.get_json(silent=True) or {}
    qid = str(data.get("qid") or "")
    try:
        answer = int(data.get("answer"))
    except (TypeError, ValueError):
        answer = -1
    if qid not in PULSES or not 0 <= answer < len(PULSES[qid][1]):
        return jsonify({"ok": False, "error": "Votación no válida"}), 400
    db = get_db()
    db.execute(
        """
        INSERT INTO pulse_votes (student_id, qid, answer, created_at) VALUES (?, ?, ?, ?)
        ON CONFLICT(student_id, qid) DO UPDATE SET answer = excluded.answer, created_at = excluded.created_at
        """,
        (session["student_id"], qid, answer, utc_now()),
    )
    db.commit()
    return jsonify({"ok": True, **_pulse_results(db, qid), "mine": answer})


@app.get("/api/pulse/<qid>")
def api_pulse_results(qid: str):
    if not (session.get("is_admin") or session.get("student_id")):
        return jsonify({"ok": False, "error": "Sesión requerida"}), 401
    if qid not in PULSES:
        return jsonify({"ok": False, "error": "No existe"}), 404
    db = get_db()
    out = _pulse_results(db, qid)
    out["active"] = _active_pulse(db) == qid
    if session.get("student_id"):
        mine = db.execute("SELECT answer FROM pulse_votes WHERE student_id = ? AND qid = ?", (session["student_id"], qid)).fetchone()
        out["mine"] = mine["answer"] if mine else None
    return jsonify({"ok": True, **out})


@app.post("/api/admin/pulse/active")
@require_admin
def api_admin_pulse_active():
    """Abre (qid) o cierra (qid vacío) la votación que ven los estudiantes en su pantalla."""
    qid = str((request.get_json(silent=True) or {}).get("qid") or "")
    if qid and qid not in PULSES:
        return jsonify({"ok": False, "error": "No existe"}), 404
    db = get_db()
    db.execute(
        "INSERT INTO app_settings (key, value, updated_at) VALUES ('active_pulse', ?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at",
        (qid, time.time()),
    )
    db.commit()
    return jsonify({"ok": True, "active": qid or None})


@app.post("/api/admin/pulse/<qid>/reset")
@require_admin
def api_admin_pulse_reset(qid: str):
    if qid not in PULSES:
        return jsonify({"ok": False, "error": "No existe"}), 404
    db = get_db()
    db.execute("DELETE FROM pulse_votes WHERE qid = ?", (qid,))
    db.commit()
    return jsonify({"ok": True, **_pulse_results(db, qid)})


@app.get("/presentar")
@require_admin
def admin_course():
    """El curso completo en modo instructora (presentaciones y votaciones, sin guardar avance)."""
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/admin/en-vivo")
@require_admin
def admin_live():
    return render_template("live.html", columns=LIVE_COLUMNS)


@app.get("/admin/resultados")
@require_admin
def admin_results():
    return render_template("results.html")


def _live_rows(db) -> list[dict]:
    now = time.time()
    rows = db.execute(
        """
        SELECT s.id, s.name, s.email, s.active, p.payload, p.percent, p.updated_at,
               pr.step, pr.title AS step_title, pr.module, pr.seen_at
        FROM students s
        LEFT JOIN progress p ON p.student_id = s.id
        LEFT JOIN presence pr ON pr.student_id = s.id
        WHERE s.active = 1
        ORDER BY s.name COLLATE NOCASE
        """
    ).fetchall()
    out = []
    for r in rows:
        try:
            payload = json.loads(r["payload"] or "{}")
        except json.JSONDecodeError:
            payload = {}
        ago = int(now - r["seen_at"]) if r["seen_at"] else None
        out.append({
            "id": r["id"],
            "name": r["name"],
            "percent": r["percent"] or 0,
            "done": activity_done_map(payload),
            "complete": activity_progress(payload)[1],
            "quiz": quiz_scores(payload),
            "cierre": cierre_summary(payload),
            "sorpresa": sum(1 for v in (payload.get("sorpresa") or {}).values() if v),
            "step": r["step"],
            "step_title": r["step_title"],
            "module": r["module"],
            "seen_ago": ago,
            "online": ago is not None and ago <= ONLINE_S,
        })
    return out


@app.get("/api/admin/live")
@require_admin
def api_admin_live():
    db = get_db()
    students = _live_rows(db)
    for s in students:
        s.pop("cierre", None)
    columns = [{"id": gid, "title": title, "cols": [{"key": k, "label": lab} for k, lab in cols]} for gid, title, cols in LIVE_COLUMNS]
    active = _active_pulse(db)
    return jsonify({
        "ok": True,
        "columns": columns,
        "students": students,
        "total_activities": activity_progress({})[2],
        "pulse": _pulse_results(db, active) if active else None,
    })


@app.get("/api/admin/student/<int:student_id>/work")
@require_admin
def api_admin_student_work(student_id: int):
    db = get_db()
    row = db.execute(
        "SELECT s.name, p.payload FROM students s LEFT JOIN progress p ON p.student_id = s.id WHERE s.id = ?",
        (student_id,),
    ).fetchone()
    if not row:
        return jsonify({"ok": False, "error": "No existe"}), 404
    try:
        payload = json.loads(row["payload"] or "{}")
    except json.JSONDecodeError:
        payload = {}
    return jsonify({"ok": True, "name": row["name"], "sections": student_work(payload)})


@app.get("/api/admin/results")
@require_admin
def api_admin_results():
    db = get_db()
    rows = _live_rows(db)
    started = [r for r in rows if r["percent"] > 0]
    n = len(started)

    def avg(vals):
        vals = [v for v in vals if v is not None]
        return round(sum(vals) / len(vals)) if vals else None

    modules = []
    for gid, title, cols in LIVE_COLUMNS:
        keys = [k for k, _ in cols]
        if n:
            frac = sum(
                sum(1 if r["done"][k] is True else (r["done"][k] or 0) for k in keys) / len(keys)
                for r in started
            ) / n
        else:
            frac = 0
        modules.append({"id": gid, "label": title, "value": round(100 * frac)})

    activities = []
    for gid, title, cols in LIVE_COLUMNS:
        for k, lab in cols:
            activities.append({"key": k, "label": f"{title} · {lab}", "done": sum(1 for r in started if r["done"][k] is True)})

    quizzes = [{"id": q, "label": {"s1": "Paso 1", "s2": "Proyecto Horizonte", "lab": "Copilot Lab"}[q],
                "value": avg([r["quiz"][q] for r in started]),
                "n": sum(1 for r in started if r["quiz"][q] is not None)} for q in QUIZ_TOTALS]

    conf = []
    for cid, label in CIERRE_CAPS:
        pares = [r["cierre"]["conf"].get(cid) for r in started
                 if (r["cierre"]["conf"].get(cid) or {}).get("antes") and (r["cierre"]["conf"].get(cid) or {}).get("hoy")]
        if pares:
            conf.append({"label": label,
                         "antes": round(sum(p["antes"] for p in pares) / len(pares), 1),
                         "hoy": round(sum(p["hoy"] for p in pares) / len(pares), 1),
                         "n": len(pares)})

    idea_counts: dict[str, int] = {}
    for r in started:
        for i in r["cierre"]["idea_ids"]:
            idea_counts[i] = idea_counts.get(i, 0) + 1
    ideas = sorted(({"label": CIERRE_IDEAS[i], "value": v} for i, v in idea_counts.items()), key=lambda x: -x["value"])[:6]

    pasos = [{"texto": r["cierre"]["primer_paso"]}
             for r in started if r["cierre"]["primer_paso"]]

    return jsonify({
        "ok": True,
        "participants": n,
        "enrolled": len(rows),
        "avg_percent": avg([r["percent"] for r in started]) or 0,
        "activities_done": sum(r["complete"] for r in started),
        "techniques": sum(r["sorpresa"] for r in started),
        "modules": modules,
        "activities": activities,
        "quizzes": quizzes,
        "confidence": conf,
        "ideas": ideas,
        "pulses": [_pulse_results(db, q) for q in PULSES],
        "first_steps": pasos[:12],
    })


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

APP_CODE_VERSION = "2026-11-11-paso4-faseA-v2"


@app.get("/health")
def health():
    _, smtp_password, _, _ = _smtp_config()
    webhook_url = (os.getenv("EMAIL_WEBHOOK_URL") or "").strip()
    return jsonify({
        "ok": True,
        "service": "mision-copilot-365",
        "version": APP_CODE_VERSION,
        "reto_emails": list_reto_email_ids(),
        "mail": {
            "webhook_configured": bool(webhook_url),
            "webhook_is_exec": ("/exec" in webhook_url) if webhook_url else False,
            "smtp_configured": bool(smtp_password),
            "resend_configured": bool((os.getenv("RESEND_API_KEY") or "").strip()),
            "smtp_email": os.getenv("SMTP_EMAIL", "analizamostunegocio@gmail.com"),
        },
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
