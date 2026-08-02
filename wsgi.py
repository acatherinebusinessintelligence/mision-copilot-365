# Archivo WSGI para PythonAnywhere — usuario: acatherinem
# Copia este contenido en: Web > WSGI configuration file
# (reemplaza el contenido por defecto)

import sys
from pathlib import Path

project_home = "/home/acatherinem/Clases_Enel"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Cargar variables de entorno desde .env
try:
    from dotenv import load_dotenv
    load_dotenv(Path(project_home) / ".env")
except Exception:
    pass

from app import app as application  # noqa: E402
