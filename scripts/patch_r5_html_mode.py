# -*- coding: utf-8 -*-
"""Convert Reto 5 from Excel plantilla to self-contained HTML deliverable."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
PROMPT_JS = Path(__file__).with_name("_r5_prompt_html_js.txt")
XLSX = ROOT / "planillas" / "MCP365_P05_Comparacion_documental.xlsx"

UI_OLD_START = "        <!-- RETO 5 -->"
UI_OLD_END = "        <!-- RETO 6 -->"

UI_NEW = r'''        <!-- RETO 5 -->
        <article class="reto" data-reto="r5">
          <button class="reto__header" aria-expanded="false">
            <span class="reto__title-wrap">
              <span class="reto__num">5</span>
              <span>
                <strong>Comparación documental · Cambios e impactos</strong>
                <span class="text-muted" style="display:block;font-size:0.85rem;color:var(--text-muted)">Copilot · Informe HTML autocontenido (sin Excel)</span>
              </span>
            </span>
            <span style="display:flex;align-items:center;gap:0.75rem">
              <label onclick="event.stopPropagation()" style="display:flex;align-items:center;gap:0.4rem;font-size:0.82rem;cursor:pointer">
                <input type="checkbox" data-progress="reto-r5" /> Hecho
              </label>
              <i data-lucide="chevron-down" class="reto__chevron" width="20" height="20"></i>
            </span>
          </button>
          <div class="reto__body">
            <div class="m365-box">
              <h4><span class="app-badge">Copilot</span> + <span class="app-badge">HTML</span> Paso a paso</h4>
              <ol>
                <li>Descarga las dos normas oficiales en <strong>PDF</strong>.</li>
                <li>Adjunta ambos PDF a <strong>Copilot</strong>.</li>
                <li>Copia el prompt configurable y pégalo en Copilot.</li>
                <li>Copilot analiza las dos normas y genera un único archivo HTML autocontenido.</li>
                <li>Descarga o guarda: <code>MCP365_P05_Comparacion_documental_completada.html</code>.</li>
                <li>Ábrelo en el navegador; verifica contenido, filtros, diseño e interactividad.</li>
                <li>Completa manualmente la validación humana y el control de calidad.</li>
              </ol>
            </div>
            <p style="margin:0 0 0.5rem;font-size:0.9rem"><strong>Descargas obligatorias</strong> (fuentes PDF):</p>
            <div class="btn-group" style="margin-bottom:0.75rem;flex-wrap:wrap;gap:0.5rem">
              <button type="button" class="btn btn--sm btn--energy" data-planilla="pro-ops-12-v31-pdf"><i data-lucide="file-text" width="14" height="14"></i> Fuente PDF v3.1</button>
              <button type="button" class="btn btn--sm btn--energy" data-planilla="pro-ops-12-v40-pdf"><i data-lucide="file-text" width="14" height="14"></i> Fuente PDF v4.0</button>
            </div>
            <p style="margin:0 0 0.5rem;font-size:0.9rem"><strong>Respaldo opcional (Word)</strong>:</p>
            <div class="btn-group" style="margin-bottom:0.75rem;flex-wrap:wrap;gap:0.5rem">
              <button type="button" class="btn btn--sm btn--ghost" data-planilla="pro-ops-12-v31-docx"><i data-lucide="file" width="14" height="14"></i> Word v3.1</button>
              <button type="button" class="btn btn--sm btn--ghost" data-planilla="pro-ops-12-v40-docx"><i data-lucide="file" width="14" height="14"></i> Word v4.0</button>
            </div>
            <div class="doc-box">
              <p><strong>Fuentes oficiales:</strong> <code>PRO-OPS-12_Version_3_1.pdf</code> y <code>PRO-OPS-12_Version_4_0.pdf</code>.</p>
              <p><strong>Entregable:</strong> <code>MCP365_P05_Comparacion_documental_completada.html</code> (informe HTML autocontenido, interactivo y sin Internet).</p>
              <p class="text-muted" style="font-size:0.88rem;margin:0">No hay plantilla Excel. Copilot genera el HTML desde cero con CSS y JavaScript internos. Validación humana y control de calidad se completan en el navegador.</p>
            </div>
            <div data-reto-enhance="r5"></div>
          </div>
        </article>

'''

R5_CASE = r'''  "r5": {
    "id": "r5",
    "title": "Comparación documental · Cambios e impactos",
    "apps": ["Copilot", "HTML"],
    "email": false,
    "planilla": null,
    "output": "MCP365_P05_Comparacion_documental_completada.html",
    "steps": [
      "Descarga los dos PDF oficiales.",
      "Adjunta ambos documentos a Copilot.",
      "Copia el prompt configurable y pégalo en Copilot.",
      "Descarga o guarda el HTML generado y ábrelo en el navegador.",
      "Verifica filtros, diseño e interactividad; completa la validación humana."
    ],
    "fields": [
      ["rol", "Rol de Copilot", "Analista senior de procesos, control documental y transición operativa, especializado en comparar procedimientos, identificar cambios de significado, detectar contradicciones y formular acciones de transición verificables."],
      ["fuentes", "Fuentes únicas", "PRO-OPS-12 · Versión 3.1, vigente hasta el 28/02/2026.\n\nPRO-OPS-12 · Versión 4.0, vigente desde el 01/03/2026."],
      ["objetivo", "Objetivo", "Comparar integralmente ambas versiones, identificar diferencias, impactos, elementos nuevos o eliminados, contradicciones, acciones de transición y propuestas que no tengan aprobación confirmada."],
      ["formato", "Formato de salida", "Un único archivo HTML autocontenido, visual, interactivo, responsive, imprimible y funcional sin conexión a Internet."],
      ["salida", "Nombre de salida", "MCP365_P05_Comparacion_documental_completada.html."],
      ["vacio", "Respuesta cuando falte información", "No especificado."]
    ],
    "checklist": [
      ["r5-c1", "Descargué las dos versiones PDF de PRO-OPS-12"],
      ["r5-c2", "Adjunté ambos PDF a Copilot"],
      ["r5-c3", "Copié el prompt completo"],
      ["r5-c4", "Copilot generó un archivo .html"],
      ["r5-c5", "El archivo tiene el nombre correcto"],
      ["r5-c6", "El HTML abre localmente sin Internet"],
      ["r5-c7", "Los doce temas están en la matriz"],
      ["r5-c8", "Los filtros y la búsqueda funcionan"],
      ["r5-c9", "Los indicadores se calculan automáticamente"],
      ["r5-c10", "Hay sección de propuestas no aprobadas"],
      ["r5-c11", "Validación humana y control de calidad vacíos"],
      ["r5-c12", "Diseño legible en escritorio y móvil"],
      ["r5-c13", "No se inventó información"],
      ["r5-c14", "Botón Descargar HTML / impresión verificados"]
    ],
    "practice_title": "Al terminar · Practica con dos versiones propias",
    "practice": "Adapta el prompt a dos versiones anonimizadas de un procedimiento real de tu trabajo. Antes: elimina nombres personales, datos sensibles, credenciales e información contractual reservada; sustituye identificadores internos. El resultado debe ser un nuevo informe HTML comparativo para revisión humana.",
    "deliverable": "Entregable: MCP365_P05_Comparacion_documental_completada.html (informe HTML autocontenido). Validación humana y control de calidad vacíos para Copilot."
  },'''


def replace_ui(text: str) -> str:
    start = text.find(UI_OLD_START)
    end = text.find(UI_OLD_END)
    if start < 0 or end < 0:
        raise SystemExit("RETO 5/6 markers not found")
    return text[:start] + UI_NEW + text[end:]


def replace_prompt(text: str) -> str:
    start = text.find("  /** Prompt Reto 5:")
    if start < 0:
        start = text.find("  function buildPromptR5Text(f)")
    end = text.find("\n\n  /* ========== RETO ENGINE", start)
    if start < 0 or end < 0:
        raise SystemExit("prompt block not found")
    return text[:start] + PROMPT_JS.read_text(encoding="utf-8").rstrip() + text[end:]


def replace_r5(text: str) -> str:
    start = text.find('  "r5": {')
    end = text.find('  "r6": {', start)
    if start < 0 or end < 0:
        raise SystemExit("r5/r6 not found")
    return text[:start] + R5_CASE + "\n" + text[end:]


def remove_xlsx_download(text: str) -> str:
    old = '''    "comparacion-docs": () => downloadStaticFile(
      "planillas/MCP365_P05_Comparacion_documental.xlsx",
      "MCP365_P05_Comparacion_documental.xlsx"
    ),

'''
    if old in text:
        text = text.replace(old, "", 1)
    elif '"comparacion-docs"' in text:
        raise SystemExit("comparacion-docs still present with unexpected format")
    return text


def remove_template_entry(text: str) -> str:
    old = '    { name: "Comparación documental", desc: "Excel .xlsx · Plantilla PRO-OPS-12 v3.1 vs v4.0", key: "comparacion-docs", type: "Excel" },\n'
    old2 = '    { name: "Comparación documental", desc: "Excel .xlsx · Matriz PRO-OPS-12 v3.1 vs v4.0", key: "comparacion-docs", type: "Excel" },\n'
    if old in text:
        text = text.replace(old, "", 1)
    elif old2 in text:
        text = text.replace(old2, "", 1)
    elif 'key: "comparacion-docs"' in text:
        raise SystemExit("comparacion-docs template still present")
    return text


def verify(text: str):
    r5 = text[text.find("<!-- RETO 5 -->"):text.find("<!-- RETO 6 -->")]
    bad = []
    if ".xlsx" in r5:
        bad.append("xlsx still in RETO 5 UI")
    if "comparacion-docs" in r5:
        bad.append("comparacion-docs button in UI")
    if "MCP365_P05_Comparacion_documental_completada.html" not in r5:
        bad.append("html deliverable missing in UI")
    if "GENERACIÓN DE INFORME HTML" not in text:
        bad.append("HTML prompt missing")
    if '"comparacion-docs"' in text:
        bad.append("comparacion-docs still in PLANILLAS/templates")
    # allow xlsx only outside r5 (other retos)
    import re
    for m in re.finditer(r"MCP365_P05[^\n]*\.xlsx", text):
        bad.append(f"residual P05 xlsx: {m.group(0)}")
    if bad:
        raise SystemExit("VERIFY FAIL:\n" + "\n".join(bad))
    print("VERIFY OK")


def main():
    if not PROMPT_JS.exists():
        raise SystemExit(f"Missing {PROMPT_JS}")
    text = INDEX.read_text(encoding="utf-8")
    text = replace_ui(text)
    print("UI OK")
    text = replace_prompt(text)
    print("Prompt OK")
    text = replace_r5(text)
    print("CASE OK")
    text = remove_xlsx_download(text)
    print("Download removed")
    text = remove_template_entry(text)
    print("Template removed")
    verify(text)
    INDEX.write_text(text, encoding="utf-8")
    if XLSX.exists():
        XLSX.unlink()
        print(f"Deleted {XLSX.name}")
    print(f"OK -> {INDEX}")


if __name__ == "__main__":
    main()
