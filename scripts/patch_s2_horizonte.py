# -*- coding: utf-8 -*-
"""Aplica rediseño Sesión 2 a index.html + bump version en app.py."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
APP = ROOT / "app.py"
SECTION = Path(__file__).with_name("_s2_section.html")
CASES = Path(__file__).with_name("_s2_reto_cases.js")


def main():
    t = INDEX.read_text(encoding="utf-8")
    section = SECTION.read_text(encoding="utf-8").rstrip() + "\n\n"
    cases = CASES.read_text(encoding="utf-8").rstrip() + "\n"

    # 1) Replace Sesión 2 HTML block
    a = t.find("    <!-- ========== 6. SESIÓN 2 ========== -->")
    b = t.find("    <!-- ========== 7. PROMPTS ==========")
    if a < 0 or b < 0:
        raise SystemExit("No se encontró bloque Sesión 2 / PROMPTS")
    t = t[:a] + section + t[b:]

    # 2) Replace fase-1 .. fase-8 in RETO_CASES
    c0 = t.find('  "fase-1": {')
    c1 = t.find("};\n\n  function buildPromptFromCase", c0)
    if c0 < 0 or c1 < 0:
        raise SystemExit("No se encontró RETO_CASES fase-*")
    t = t[:c0] + cases + t[c1:]

    # 3) Insert S2 static downloads after priorizacion-practica (or before informe-ejecutivo)
    insert_marker = '    "informe-ejecutivo": () => downloadWord'
    s2_downloads = '''    "s2-correo": () => downloadStaticFile(
      "planillas/MCP365_S2_Correo_Inicio_Proyecto_Horizonte.html",
      "MCP365_S2_Correo_Inicio_Proyecto_Horizonte.html"
    ),

    "s2-ficha": () => downloadStaticFile(
      "planillas/MCP365_S2_Ficha_Proyecto_Horizonte.docx",
      "MCP365_S2_Ficha_Proyecto_Horizonte.docx"
    ),

    "s2-control": () => downloadStaticFile(
      "planillas/MCP365_S2_Control_Proyecto_Horizonte.xlsx",
      "MCP365_S2_Control_Proyecto_Horizonte.xlsx"
    ),

    "s2-informe-plantilla": () => downloadStaticFile(
      "planillas/MCP365_S2_Plantilla_Informe_Proyecto.docx",
      "MCP365_S2_Plantilla_Informe_Proyecto.docx"
    ),

    "s2-guia-pa": () => downloadStaticFile(
      "planillas/MCP365_S2_Guia_Power_Automate.pdf",
      "MCP365_S2_Guia_Power_Automate.pdf"
    ),

    "s2-resultado": () => downloadStaticFile(
      "planillas/MCP365_S2_Resultado_Esperado.html",
      "MCP365_S2_Resultado_Esperado.html"
    ),

'''
    if '"s2-correo"' not in t:
        if insert_marker not in t:
            raise SystemExit("No se encontró informe-ejecutivo en PLANILLAS")
        t = t.replace(insert_marker, s2_downloads + insert_marker, 1)

    # 4) Update TEMPLATES: replace old S2-heavy entries after priorizacion-practica
    old_tpl_tail = '''    { name: "Informe ejecutivo", desc: "Word/PowerPoint · 10 bloques para comité", key: "informe-ejecutivo", type: "Word" },
    { name: "Registro de riesgos", desc: "Excel/Word · Matriz con IDs y escalamiento", key: "registro-riesgos", type: "Word" },
    { name: "Matriz RACI", desc: "Excel/Word · Roles, aceptación y chequeos", key: "raci", type: "Word" },
    { name: "Mapa de interesados", desc: "Excel/Word · Cuadrantes y plan de mensajes", key: "interesados", type: "Word" },
    { name: "Bitácora de validación", desc: "Todas las apps · Control humano de Copilot", key: "bitacora-validacion", type: "Word" },
    { name: "Lecciones aprendidas (20)", desc: "Excel/Word · Histórico para cruzar con ofertas", key: "lecciones-aprendidas", type: "Word" },
    { name: "Oferta en evaluación", desc: "Word · Proyecto Horizonte Extensión Sur", key: "oferta-proyecto", type: "Word" },
    { name: "Alarma de reincidencia", desc: "Word · Solicitud formal de revisión", key: "alarma-revision", type: "Word" }
  ];'''
    new_tpl_tail = '''    { name: "S2 Correo inicio Horizonte", desc: "HTML · Asunto NUEVO PROYECTO · HORIZONTE", key: "s2-correo", type: "HTML" },
    { name: "S2 Ficha Proyecto Horizonte", desc: "Word · Fuente principal de datos del proyecto", key: "s2-ficha", type: "Word" },
    { name: "S2 Control Proyecto Horizonte", desc: "Excel · Registro, Presupuesto y Riesgos", key: "s2-control", type: "Excel" },
    { name: "S2 Plantilla informe", desc: "Word · Informe + validación humana vacía", key: "s2-informe-plantilla", type: "Word" },
    { name: "S2 Guía Power Automate", desc: "PDF · Cadena de 6 retos", key: "s2-guia-pa", type: "PDF" },
    { name: "S2 Resultado esperado", desc: "HTML · Referencia de calidad del flujo", key: "s2-resultado", type: "HTML" },
    { name: "Bitácora de validación", desc: "Todas las apps · Control humano de Copilot", key: "bitacora-validacion", type: "Word" }
  ];'''
    if old_tpl_tail in t:
        t = t.replace(old_tpl_tail, new_tpl_tail, 1)
    elif '"s2-correo"' not in t[t.find("const TEMPLATES"):t.find("function renderTemplates")]:
        raise SystemExit("No se pudo actualizar TEMPLATES")

    INDEX.write_text(t, encoding="utf-8")
    print("OK index.html Sesion 2")

    # 5) Version bump
    app = APP.read_text(encoding="utf-8")
    import re
    app2, n = re.subn(
        r'APP_CODE_VERSION = "[^"]+"',
        'APP_CODE_VERSION = "2026-08-03-s2-horizonte-pa-v1"',
        app,
        count=1,
    )
    if n != 1:
        raise SystemExit("No se actualizo APP_CODE_VERSION")
    APP.write_text(app2, encoding="utf-8")
    print("OK app.py version")

    # Sanity
    checks = [
        "Copilot y Power Automate para la gestión inteligente de proyectos",
        "NUEVO PROYECTO · HORIZONTE",
        "MCP365_S2_Datos_Proyecto_Horizonte.json",
        "MCP365_S2_Presentacion_Proyecto_Horizonte.pptx",
        "Interpretación para validación",
        'data-reto-enhance="fase-6"',
        "s2-guia-pa",
        "data-reto-enhance=\"fase-8\"",
    ]
    for needle in checks[:-1]:
        if needle not in t:
            raise SystemExit(f"Falta: {needle}")
        print("OK", needle[:60])
    if 'data-reto-enhance="fase-8"' in t:
        raise SystemExit("Aun existe fase-8 en UI")
    print("OK sin fase-8 en enhance")
    # Sesion 1 marker intact
    if 'data-reto="r1"' not in t and 'data-progress="reto-r1"' not in t:
        raise SystemExit("Sesion 1 alterada?")
    print("OK Sesion 1 intacta")


if __name__ == "__main__":
    main()
