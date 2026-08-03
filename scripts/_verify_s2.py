# -*- coding: utf-8 -*-
from pathlib import Path

root = Path(r"c:\Users\USER\OneDrive\Documentos\Sergio arboleda\Clases_Enel")
t = (root / "index.html").read_text(encoding="utf-8")
app = (root / "app.py").read_text(encoding="utf-8")

s2a = t.find('id="sesion2"')
s2b = t.find('id="prompts"')
s2 = t[s2a:s2b]

checks = {
    "title PA": "Copilot y Power Automate para la gestión inteligente de proyectos" in s2,
    "old title gone": "Copilot para la gestión inteligente de proyectos" not in s2,
    "6 enhances": s2.count('data-reto-enhance="fase-') == 6,
    "no fase-7 enhance": 'data-reto-enhance="fase-7"' not in t,
    "no fase-8 enhance": 'data-reto-enhance="fase-8"' not in t,
    "progress keys keep 7-8": '"fase-7","fase-8"' in t or ('"fase-7"' in t and '"fase-8"' in t),
    "s1 r1": 'data-progress="reto-r1"' in t,
    "s2 downloads": all(k in t for k in ["s2-correo", "s2-ficha", "s2-control", "s2-informe-plantilla", "s2-guia-pa", "s2-resultado"]),
    "planillas static": 'planillas/MCP365_S2_Ficha_Proyecto_Horizonte.docx' in t,
    "fase-1 case": '"title": "Recepción automatizada del proyecto"' in t,
    "fase-6 case": '"title": "Presentación ejecutiva"' in t,
    "no fase-7 case": '"fase-7":' not in t[t.find("const RETO_CASES"): t.find("function buildPromptFromCase")],
    "version": '2026-08-03-s2-horizonte-pa-v1' in app,
    "auth intact": "require_student" in app and "student_id" in app,
}
for k, v in checks.items():
    print(("OK" if v else "FAIL"), k)

files = [
    "MCP365_S2_Correo_Inicio_Proyecto_Horizonte.html",
    "MCP365_S2_Ficha_Proyecto_Horizonte.docx",
    "MCP365_S2_Control_Proyecto_Horizonte.xlsx",
    "MCP365_S2_Plantilla_Informe_Proyecto.docx",
    "MCP365_S2_Guia_Power_Automate.pdf",
    "MCP365_S2_Resultado_Esperado.html",
]
for n in files:
    p = root / "planillas" / n
    print(("OK" if p.exists() and p.stat().st_size > 0 else "FAIL"), n, p.stat().st_size if p.exists() else 0)

# brace balance around RETO_CASES end
chunk = t[t.find("const RETO_CASES"): t.find("function buildPromptFromCase")]
print("RETO_CASES ends with", repr(chunk[-40:]))
