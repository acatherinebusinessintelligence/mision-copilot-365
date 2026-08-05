# -*- coding: utf-8 -*-
"""Regenera s2_prism_data.json y reinyecta S2_PRISM en index.html."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2_prism_data import F7_PPTX_PROMPT, S2_PRISM  # noqa: E402

JSON_PATH = Path(__file__).with_name("s2_prism_data.json")
JSON_PATH.write_text(json.dumps(S2_PRISM, ensure_ascii=False, indent=2), encoding="utf-8")

t = INDEX.read_text(encoding="utf-8")
prism_json = json.dumps(S2_PRISM, ensure_ascii=False)

a = t.find("  const S2_PRISM = ")
if a < 0:
    raise SystemExit("S2_PRISM not found")
b = t.find(";\n\n  function escHtml", a)
if b < 0:
    b = t.find(";\n  function escHtml", a)
if b < 0:
    raise SystemExit("end of S2_PRISM not found")
t = t[:a] + "  const S2_PRISM = " + prism_json + t[b:]

if "initS2F1SourceGuard" not in t:
    raise SystemExit("initS2F1SourceGuard missing in index.html — abort")

VERSION = "2026-08-05-s2-f7-pptx-v1"
app = (ROOT / "app.py").read_text(encoding="utf-8")
app = re.sub(
    r'APP_CODE_VERSION = "[^"]+"',
    f'APP_CODE_VERSION = "{VERSION}"',
    app,
    count=1,
)
(ROOT / "app.py").write_text(app, encoding="utf-8")
INDEX.write_text(t, encoding="utf-8")

html = INDEX.read_text(encoding="utf-8")
f7 = S2_PRISM["f7"]
expert = f7["levels"]["4"]["text"]
pro = f7["levels"]["3"]["text"]
s1 = html[html.find('id="sesion1"'): html.find('id="desafio"')]
checks = {
    "f7 title": "Comité" in f7["title"] or "PowerPoint" in f7["title"],
    "f7 expert is PPTX prompt": expert.strip() == F7_PPTX_PROMPT.strip(),
    "f7 no Word format block": "Tabla de Contenido" not in expert and "documento ejecutivo completo" not in expert,
    "f7 pro no Word format": "Tabla de Contenido" not in pro,
    "f7 demands pptx": "Presentacion_Comite_Proyecto_Horizonte.pptx" in expert,
    "f7 template": "07_Plantilla_Comite_Horizonte.pptx" in expert,
    "html official": 'id="s2f7Official"' in html,
    "html prompt": "Presentacion_Comite_Proyecto_Horizonte.pptx" in html,
    "html no ruta B guion": "Si la generación del archivo no está disponible" not in html,
    "protect f7": 'box.id === "s2f7-pp"' in html,
    "prism mount f7": 'data-prism-mount="f7"' in html,
    "S1 intact": "Circuito N-14" in s1,
    "version": VERSION in (ROOT / "app.py").read_text(encoding="utf-8"),
}
for k, v in checks.items():
    print(("OK" if v else "FAIL"), k)
if not all(checks.values()):
    raise SystemExit(1)
print("OK reembed")
