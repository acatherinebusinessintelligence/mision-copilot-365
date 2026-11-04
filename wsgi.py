# Archivo WSGI para PythonAnywhere — cuenta: dracorazonia
# Copia este contenido en: Web > WSGI configuration file
# (/var/www/dracorazonia_pythonanywhere_com_wsgi.py) reemplazando el contenido por defecto.
#
# La carpeta del proyecto se detecta sola dentro de /home/<usuario>/:
#   - mision-copilot-365  (nombre por defecto de `git clone`)
#   - Clases_Enel         (nombre usado en despliegues anteriores)
# Si usas otra carpeta, cambia PROJECT_DIR_NAME.

import sys
from pathlib import Path

PROJECT_DIR_NAME = None  # p. ej. "mision-copilot-365"; None = detección automática

home = Path.home()
candidates = [PROJECT_DIR_NAME] if PROJECT_DIR_NAME else ["mision-copilot-365", "Clases_Enel"]
project_home = next((home / c for c in candidates if (home / c / "app.py").exists()), home / candidates[0])

if str(project_home) not in sys.path:
    sys.path.insert(0, str(project_home))

# Cargar variables de entorno desde .env
try:
    from dotenv import load_dotenv
    load_dotenv(project_home / ".env")
except Exception:
    pass

from app import app as application  # noqa: E402
