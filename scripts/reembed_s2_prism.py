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

# Button handlers near initS2PrismEngine or S2 prompt lab
BTN_JS = r'''
  function initS2F1SourceGuard() {
    const showBtn = document.getElementById("s2f1ShowWrongSource");
    const contBtn = document.getElementById("s2f1ContinueCorrect");
    const details = document.getElementById("s2f1WrongSourceExample");
    const anchor = document.getElementById("s2f1PromptsAnchor");
    if (showBtn && details && !showBtn.dataset.bound) {
      showBtn.dataset.bound = "1";
      showBtn.addEventListener("click", () => {
        details.open = true;
        showBtn.setAttribute("aria-expanded", "true");
        details.scrollIntoView({ behavior: "smooth", block: "nearest" });
        if (window.lucide) lucide.createIcons({ nodes: [details] });
      });
    }
    if (contBtn && !contBtn.dataset.bound) {
      contBtn.dataset.bound = "1";
      contBtn.addEventListener("click", () => {
        if (details) details.open = false;
        if (showBtn) showBtn.setAttribute("aria-expanded", "false");
        const target = anchor || document.querySelector('[data-reto="s2-f1"] .prism-host');
        if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
        toast("Selecciona en Outlook: SOLICITUD DE ANÁLISIS | Proyecto Horizonte", "mail-check");
      });
    }
  }

'''

if "initS2F1SourceGuard" not in t:
    t = t.replace(
        "  function initS2PrismEngine()",
        BTN_JS + "  function initS2PrismEngine()",
        1,
    )
    t = t.replace(
        "    initS2PrismEngine();\n",
        "    initS2PrismEngine();\n    initS2F1SourceGuard();\n",
        1,
    )

app = (ROOT / "app.py").read_text(encoding="utf-8")
app = re.sub(
    r'APP_CODE_VERSION = "[^"]+"',
    'APP_CODE_VERSION = "2026-08-05-s2-word-ready-doc-v1"',
    app,
    count=1,
)
(ROOT / "app.py").write_text(app, encoding="utf-8")
INDEX.write_text(t, encoding="utf-8")

# Verify expert prompt content
expert = S2_PRISM["f1"]["levels"]["4"]["text"]
checks = {
    "FUENTE INCORRECTA": "FUENTE INCORRECTA" in expert,
    "no RACI definitiva": "RACI definitiva" in expert or "matriz RACI definitiva" in expert,
    "N-14 mentioned": "Circuito N-14" in expert,
    "intake": "Briefing de Intake" in expert or "briefing de intake" in expert.lower(),
    "html warn": "Verifica que seleccionaste el correo" in INDEX.read_text(encoding="utf-8"),
    "checklist": "s2f1-src1" in INDEX.read_text(encoding="utf-8"),
    "example": "Ejemplo: Copilot detecta una fuente incorrecta" in INDEX.read_text(encoding="utf-8"),
    "buttons": "s2f1ShowWrongSource" in INDEX.read_text(encoding="utf-8"),
    "S1 intact": "Circuito N-14" in INDEX.read_text(encoding="utf-8")[INDEX.read_text(encoding="utf-8").find('id="sesion1"'): INDEX.read_text(encoding="utf-8").find('id="desafio"')],
}
for k, v in checks.items():
    print(("OK" if v else "FAIL"), k)
if not all(checks.values()):
    raise SystemExit(1)
print("OK reembed")
