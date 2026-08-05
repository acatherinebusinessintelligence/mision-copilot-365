# -*- coding: utf-8 -*-
"""Regenera s2_prism_data.json y reinyecta S2_PRISM en index.html."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

# Import data
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2_prism_data import S2_PRISM  # noqa: E402

JSON_PATH = Path(__file__).with_name("s2_prism_data.json")
JSON_PATH.write_text(json.dumps(S2_PRISM, ensure_ascii=False, indent=2), encoding="utf-8")

t = INDEX.read_text(encoding="utf-8")
prism_json = json.dumps(S2_PRISM, ensure_ascii=False)

# Replace const S2_PRISM = {...};
a = t.find("  const S2_PRISM = ")
if a < 0:
    raise SystemExit("S2_PRISM not found")
# Find end: next line starting with "  function escHtml" or ";\n\n  function"
b = t.find(";\n\n  function escHtml", a)
if b < 0:
    b = t.find(";\n  function escHtml", a)
if b < 0:
    raise SystemExit("end of S2_PRISM not found")
t = t[:a] + "  const S2_PRISM = " + prism_json + t[b:]

# Do NOT overwrite initS2F1SourceGuard if already present (gate + Paso 0 live in index.html).
if "initS2F1SourceGuard" not in t:
    raise SystemExit("initS2F1SourceGuard missing in index.html — abort")

if "initS2F1SourceGuard();" not in t:
    t = t.replace(
        "    initS2PrismEngine();\n",
        "    initS2PrismEngine();\n    initS2F1SourceGuard();\n",
        1,
    )

VERSION = "2026-08-05-s2-f1-multifile-v1"
app = (ROOT / "app.py").read_text(encoding="utf-8")
app = re.sub(
    r'APP_CODE_VERSION = "[^"]+"',
    f'APP_CODE_VERSION = "{VERSION}"',
    app,
    count=1,
)
(ROOT / "app.py").write_text(app, encoding="utf-8")
INDEX.write_text(t, encoding="utf-8")

# Verify expert prompt content (documentary multi-file analysis)
expert = S2_PRISM["f1"]["levels"]["4"]["text"]
pro = S2_PRISM["f1"]["levels"]["3"]["text"]
html = INDEX.read_text(encoding="utf-8")
s1 = html[html.find('id="sesion1"'): html.find('id="desafio"')]
checks = {
    "f1 title": S2_PRISM["f1"]["title"].startswith("Análisis documental"),
    "Mencionado/Seleccionado/Analizado": "Mencionado" in pro and "Seleccionado" in pro and "Analizado" in pro,
    "per-file analysis": "02_Alcance" in pro and "Transcripción" in pro and "riesgos" in pro.lower(),
    "no fake from email name": "solo porque su nombre aparece" in pro or "MENCIONADO SIN ACCESO" in expert,
    "Word/PDF": "Word" in expert and "PDF" in expert,
    "html paso0": "Paso 0 · Verificar que Copilot reconoce los archivos" in html,
    "html warn content": "reconocer el nombre de un archivo sin haber accedido" in html,
    "continue analysis": "s2f1ContinueAnalysis" in html,
    "rec checks": "data-s2f1-rec" in html,
    "prism mount": 'data-prism-mount="f1"' in html,
    "html warn correo": "Verifica que seleccionaste el correo" in html,
    "checklist src": "s2f1-src1" in html,
    "S1 intact": "Circuito N-14" in s1,
    "version": VERSION in (ROOT / "app.py").read_text(encoding="utf-8"),
}
for k, v in checks.items():
    print(("OK" if v else "FAIL"), k)
if not all(checks.values()):
    raise SystemExit(1)
print("OK reembed")
