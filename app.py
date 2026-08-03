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


def calc_percent_from_payload(payload: dict) -> int:
    """Misma lógica aproximada que el frontend para el panel admin."""
    progress = payload.get("progress") or {}
    keys = [
        "reto-r1", "reto-r2", "reto-r3", "reto-r4", "reto-r5", "reto-r6",
        "s1-done", "s2-done", "proyecto-final",
        "fase-1", "fase-2", "fase-3", "fase-4", "fase-5", "fase-6", "fase-7", "fase-8",
    ]
    done = sum(1 for k in keys if progress.get(k))
    quiz_score = min(5, int((payload.get("quiz") or {}).get("score") or 0))
    favs = min(3, len(payload.get("favorites") or [])) * 0.5
    path_done = sum(1 for v in (payload.get("path") or {}).values() if v)
    path_pts = min(4, path_done * 0.5)
    total_weight = len(keys) + 5 + 1.5 + 4
    score = done + quiz_score + min(1.5, favs) + path_pts
    return int(round((score / total_weight) * 100))


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
    return ["r1", "r2", "r2-all"] + [p["id"] for p in get_reto_r2_parts()]


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

@app.get("/assets/<path:filename>")
def assets(filename: str):
    return send_from_directory(BASE_DIR, filename)


@app.get("/planillas/<path:filename>")
def planillas(filename: str):
    return send_from_directory(BASE_DIR / "planillas", filename)


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


# ---------------------------------------------------------------------------
# API progreso estudiante
# ---------------------------------------------------------------------------

@app.get("/api/me")
@require_student
def api_me():
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
    flash = session.pop("flash", None)
    return render_template(
        "admin.html",
        students=rows,
        stats=stats,
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
# Health
# ---------------------------------------------------------------------------

APP_CODE_VERSION = "2026-08-03-r6-html-priorizacion-v1"


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
