# -*- coding: utf-8 -*-
"""Restore Reto 5 to Excel plantilla edit mode with official prompt."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
PROMPT_JS = Path(__file__).with_name("_r5_prompt_plantilla_js.txt")

UI_OLD_START = "        <!-- RETO 5 -->"
UI_OLD_END = "        <!-- RETO 6 -->"

UI_NEW = r'''        <!-- RETO 5 -->
        <article class="reto" data-reto="r5">
          <button class="reto__header" aria-expanded="false">
            <span class="reto__title-wrap">
              <span class="reto__num">5</span>
              <span>
                <strong>Comparación documental · Cambios e impactos</strong>
                <span class="text-muted" style="display:block;font-size:0.85rem;color:var(--text-muted)">Excel + Copilot · Modo edición de plantilla (.xlsx real)</span>
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
              <h4><span class="app-badge">Excel</span> + <span class="app-badge">Copilot</span> Paso a paso</h4>
              <ol>
                <li>Descarga la <strong>plantilla Excel</strong> y las <strong>fuentes PDF</strong>.</li>
                <li>Opcional: descarga los respaldos Word.</li>
                <li>Usa la <strong>misma forma de acceso a la plantilla</strong> que te funcionó en los retos anteriores.</li>
                <li>Proporciona a Copilot: plantilla <code>MCP365_P05_Comparacion_documental.xlsx</code> + PDF v3.1 + PDF v4.0 + este prompt.</li>
                <li>Copilot edita una copia de la plantilla (hoja Comparación + hoja Propuestas no aprobadas). No completa Validación y calidad.</li>
                <li>Guarda como <code>MCP365_P05_Comparacion_documental_completada.xlsx</code>.</li>
              </ol>
            </div>
            <p style="margin:0 0 0.5rem;font-size:0.9rem"><strong>Descargas obligatorias</strong>:</p>
            <div class="btn-group" style="margin-bottom:0.75rem;flex-wrap:wrap;gap:0.5rem">
              <button type="button" class="btn btn--sm btn--energy" data-planilla="comparacion-docs"><i data-lucide="download" width="14" height="14"></i> Plantilla Excel (.xlsx)</button>
              <button type="button" class="btn btn--sm btn--secondary" data-planilla="pro-ops-12-v31-pdf"><i data-lucide="file-text" width="14" height="14"></i> Fuente PDF v3.1</button>
              <button type="button" class="btn btn--sm btn--secondary" data-planilla="pro-ops-12-v40-pdf"><i data-lucide="file-text" width="14" height="14"></i> Fuente PDF v4.0</button>
            </div>
            <p style="margin:0 0 0.5rem;font-size:0.9rem"><strong>Respaldo opcional (Word)</strong>:</p>
            <div class="btn-group" style="margin-bottom:0.75rem;flex-wrap:wrap;gap:0.5rem">
              <button type="button" class="btn btn--sm btn--ghost" data-planilla="pro-ops-12-v31-docx"><i data-lucide="file" width="14" height="14"></i> Word v3.1</button>
              <button type="button" class="btn btn--sm btn--ghost" data-planilla="pro-ops-12-v40-docx"><i data-lucide="file" width="14" height="14"></i> Word v4.0</button>
            </div>
            <div class="doc-box">
              <p><strong>Plantilla:</strong> <code>MCP365_P05_Comparacion_documental.xlsx</code></p>
              <p><strong>Fuentes:</strong> <code>PRO-OPS-12_Version_3_1.pdf</code> y <code>PRO-OPS-12_Version_4_0.pdf</code></p>
              <p><strong>Entregable:</strong> <code>MCP365_P05_Comparacion_documental_completada.xlsx</code></p>
              <p class="text-muted" style="font-size:0.88rem;margin:0">Modo edición de plantilla. Conserva hojas Instrucciones, Comparación, Validación y calidad, Catálogos. Se autoriza crear la hoja «Propuestas no aprobadas».</p>
            </div>
            <div data-reto-enhance="r5"></div>
          </div>
        </article>

'''

R5_CASE = r'''  "r5": {
    "id": "r5",
    "title": "Comparación documental · Cambios e impactos",
    "apps": ["Excel", "Copilot"],
    "email": false,
    "planilla": {"key": "comparacion-docs", "label": "Plantilla Excel (.xlsx)"},
    "output": "MCP365_P05_Comparacion_documental_completada.xlsx",
    "steps": [
      "Descarga plantilla Excel + fuentes PDF v3.1 y v4.0.",
      "Usa el mismo acceso a plantilla que en retos anteriores.",
      "Proporciona a Copilot: plantilla + PDFs + este prompt.",
      "Copilot completa Comparación y crea «Propuestas no aprobadas»; no toca Validación y calidad.",
      "Entrega: <code>MCP365_P05_Comparacion_documental_completada.xlsx</code>."
    ],
    "fields": [
      ["rol", "Rol de Copilot", "Analista senior de procesos, control documental y transición operativa, especializado en comparar procedimientos, detectar cambios de significado, identificar contradicciones y formular acciones verificables."],
      ["app", "Aplicación", "Excel + Copilot."],
      ["documentos", "Documentos fuente", "PRO-OPS-12 · Versión 3.1, vigente hasta el 28/02/2026.\n\nPRO-OPS-12 · Versión 4.0, vigente desde el 01/03/2026."],
      ["archivo", "Archivo Excel que se debe completar", "MCP365_P05_Comparacion_documental.xlsx."],
      ["hojas", "Hojas existentes que deben conservarse", "1. Instrucciones.\n2. Comparación.\n3. Validación y calidad.\n4. Catálogos."],
      ["hoja_nueva", "Nueva hoja autorizada", "Propuestas no aprobadas."],
      ["salida", "Nombre del archivo de salida", "MCP365_P05_Comparacion_documental_completada.xlsx."],
      ["vacio", "Respuesta cuando falte información", "No especificado."]
    ],
    "checklist": [
      ["r5-c1", "Plantilla .xlsx + PDFs v3.1 y v4.0 descargados"],
      ["r5-c2", "Usé el mismo acceso a plantilla que en retos anteriores"],
      ["r5-c3", "Copié el prompt completo"],
      ["r5-c4", "Matriz de 12 temas completa con evidencias"],
      ["r5-c5", "Indicadores recalculados con fórmulas"],
      ["r5-c6", "Hoja Propuestas no aprobadas creada"],
      ["r5-c7", "Validación humana y control de calidad vacíos"],
      ["r5-c8", "Guardé MCP365_P05_Comparacion_documental_completada.xlsx"]
    ],
    "practice_title": "Al terminar · Practica con dos versiones propias",
    "practice": "Adapta este prompt para comparar dos versiones anonimizadas de una norma, procedimiento, política o manual de tu organización. Utiliza únicamente documentos autorizados y elimina nombres, datos personales, información confidencial y detalles operativos restringidos.",
    "deliverable": "Entregable: MCP365_P05_Comparacion_documental_completada.xlsx (copia de la plantilla + hoja Propuestas no aprobadas). Validación humana y control de calidad vacíos."
  },'''

DOWNLOAD_BLOCK = '''    "comparacion-docs": () => downloadStaticFile(
      "planillas/MCP365_P05_Comparacion_documental.xlsx",
      "MCP365_P05_Comparacion_documental.xlsx"
    ),

'''

TEMPLATE_ENTRY = '    { name: "Comparación documental", desc: "Excel .xlsx · Plantilla PRO-OPS-12 v3.1 vs v4.0", key: "comparacion-docs", type: "Excel" },\n'


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


def ensure_download(text: str) -> str:
    if '"comparacion-docs"' in text and "MCP365_P05_Comparacion_documental.xlsx" in text.split('"comparacion-docs"')[1][:200]:
        return text
    anchor = '    "pro-ops-12-v31-pdf": () => downloadStaticFile('
    if anchor not in text:
        raise SystemExit("pro-ops download anchor not found")
    return text.replace(anchor, DOWNLOAD_BLOCK + anchor, 1)


def ensure_template(text: str) -> str:
    if 'key: "comparacion-docs"' in text:
        return text
    anchor = '    { name: "PRO-OPS-12 v3.1 (PDF)"'
    if anchor not in text:
        raise SystemExit("template anchor not found")
    return text.replace(anchor, TEMPLATE_ENTRY + anchor, 1)


def main():
    text = INDEX.read_text(encoding="utf-8")
    text = replace_ui(text)
    print("UI OK")
    text = replace_prompt(text)
    print("Prompt OK")
    text = replace_r5(text)
    print("CASE OK")
    text = ensure_download(text)
    print("Download OK")
    text = ensure_template(text)
    print("Template OK")
    assert "MODO EDICIÓN DE PLANTILLA EXCEL" in text
    assert "Propuestas no aprobadas" in text
    assert 'data-planilla="comparacion-docs"' in text
    assert "desde cero" not in text[text.find("<!-- RETO 5 -->"):text.find("<!-- RETO 6 -->")]
    INDEX.write_text(text, encoding="utf-8")
    print(f"OK -> {INDEX}")


if __name__ == "__main__":
    main()
