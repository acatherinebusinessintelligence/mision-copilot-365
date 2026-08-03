# -*- coding: utf-8 -*-
"""Reto 5: replace plantilla Excel flow with generate-xlsx-from-scratch."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
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
                <span class="text-muted" style="display:block;font-size:0.85rem;color:var(--text-muted)">Copilot + Excel · Generación de libro desde cero (sin plantilla)</span>
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
              <h4><span class="app-badge">Copilot</span> + <span class="app-badge">Excel</span> Paso a paso</h4>
              <ol>
                <li>Descarga las dos normas oficiales en <strong>PDF</strong>.</li>
                <li>Abre <strong>Copilot</strong> y adjunta ambos PDF.</li>
                <li>Copia el prompt prellenado y pégalo en Copilot.</li>
                <li>Descarga el Excel generado: <code>MCP365_P05_Comparacion_documental_completada.xlsx</code>.</li>
                <li>Abre el archivo y verifica hojas, contenido y formato.</li>
                <li>Realiza la validación humana y el control de calidad (hoja preparada, vacía).</li>
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
              <p><strong>Entregable:</strong> <code>MCP365_P05_Comparacion_documental_completada.xlsx</code> (libro generado por Copilot desde cero · 4 hojas).</p>
              <p class="text-muted" style="font-size:0.88rem;margin:0">No hay plantilla Excel. Copilot debe generar el libro profesional completo a partir de los PDF y este prompt.</p>
            </div>
            <div data-reto-enhance="r5"></div>
          </div>
        </article>

'''

R5_CASE = r'''  "r5": {
    "id": "r5",
    "title": "Comparación documental · Cambios e impactos",
    "apps": ["Copilot", "Excel"],
    "email": false,
    "planilla": null,
    "output": "MCP365_P05_Comparacion_documental_completada.xlsx",
    "steps": [
      "Descarga las dos normas oficiales en PDF.",
      "Abre Copilot y adjunta ambos PDF.",
      "Copia el prompt prellenado y pégalo en Copilot.",
      "Descarga el Excel generado y verifica hojas, contenido y formato.",
      "Realiza la validación humana y el control de calidad."
    ],
    "fields": [
      ["rol", "Rol de Copilot", "Analista documental especializado en comparación normativa, control de cambios, análisis de impactos y transición operativa."],
      ["doc_anterior", "Documento anterior", "PRO-OPS-12_Version_3_1.pdf · Versión histórica vigente hasta el 28/02/2026."],
      ["doc_vigente", "Documento vigente", "PRO-OPS-12_Version_4_0.pdf · Versión vigente desde el 01/03/2026."],
      ["objetivo", "Objetivo", "Comparar ambas versiones e identificar cambios textuales y de significado, elementos nuevos, obligaciones eliminadas, impactos, contradicciones, aprobaciones y acciones de transición."],
      ["temas", "Temas de comparación", "1. Anticipación a usuarios.\n2. Autorización de inicio.\n3. Registro de hallazgos.\n4. Horario y cierre.\n5. Clasificación de impacto.\n6. Confirmación de recursos.\n7. Criterios de detención.\n8. Evidencia y trazabilidad.\n9. Conservación de registros.\n10. Responsabilidad del contratista.\n11. Indicadores.\n12. Régimen de transición."],
      ["vacio", "Respuesta cuando falte información", "No especificado."],
      ["detalle", "Nivel de detalle", "Operativo y verificable. Máximo tres oraciones por celda."],
      ["salida", "Nombre del archivo", "MCP365_P05_Comparacion_documental_completada.xlsx"]
    ],
    "checklist": [
      ["r5-c1", "Descargué las dos versiones de PRO-OPS-12"],
      ["r5-c2", "Adjunté ambos PDF a Copilot"],
      ["r5-c3", "Copié el prompt completo"],
      ["r5-c4", "Copilot generó un archivo .xlsx"],
      ["r5-c5", "El archivo tiene el nombre correcto"],
      ["r5-c6", "El libro contiene cuatro hojas"],
      ["r5-c7", "La matriz contiene doce temas"],
      ["r5-c8", "Las evidencias citan versión y sección"],
      ["r5-c9", "Se identificaron elementos nuevos o eliminados"],
      ["r5-c10", "Se revisaron posibles contradicciones"],
      ["r5-c11", "El plan de transición contiene responsables y fechas verificables"],
      ["r5-c12", "Los indicadores funcionan"],
      ["r5-c13", "Las listas desplegables funcionan"],
      ["r5-c14", "El formato es profesional y legible"],
      ["r5-c15", "La validación humana permanece vacía"],
      ["r5-c16", "El control de calidad permanece vacío"],
      ["r5-c17", "No se inventó información"],
      ["r5-c18", "El archivo abre correctamente"]
    ],
    "practice_title": "Al terminar · Practica con dos versiones propias",
    "practice": "Adapta este prompt para comparar dos versiones anonimizadas de una norma, procedimiento, política o manual de tu organización. Utiliza únicamente documentos autorizados y elimina nombres, datos personales, información confidencial y detalles operativos restringidos.",
    "deliverable": "Entregable: MCP365_P05_Comparacion_documental_completada.xlsx (libro Excel profesional generado desde cero). Validación humana y control de calidad vacíos."
  },'''

# Prompt file will be written separately due to size - build as join list in apply


def build_prompt_fn() -> str:
    # Keep getPromptR5Fields; replace only buildPromptR5Text
    lines = Path(__file__).with_name("_r5_prompt_generate_js.txt")
    return lines.read_text(encoding="utf-8")


def replace_ui(text: str) -> str:
    start = text.find(UI_OLD_START)
    end = text.find(UI_OLD_END)
    if start < 0 or end < 0:
        raise SystemExit("RETO 5/6 markers not found")
    return text[:start] + UI_NEW + text[end:]


def replace_r5_case(text: str) -> str:
    start = text.find('  "r5": {')
    end = text.find('  "r6": {', start)
    if start < 0 or end < 0:
        raise SystemExit("r5/r6 not found")
    return text[:start] + R5_CASE + "\n" + text[end:]


def replace_prompt_fn(text: str) -> str:
    start = text.find("  /** Prompt Reto 5:")
    if start < 0:
        start = text.find("  function buildPromptR5Text")
        # include getPromptR5Fields? Keep getPromptR5Fields, only replace buildPromptR5Text
        start = text.find("  /** Prompt Reto 5:")
    if start < 0:
        # find function buildPromptR5Text
        start = text.find("  function buildPromptR5Text(f)")
        # go back to comment if present
        prev = text.rfind("  /** Prompt Reto 5", 0, start)
        if prev >= 0:
            start = prev
    end = text.find("\n\n  /* ========== RETO ENGINE", start)
    if start < 0 or end < 0:
        raise SystemExit("buildPromptR5Text block not found")
    new_fn = build_prompt_fn()
    return text[:start] + new_fn.rstrip() + text[end:]


def remove_comparacion_docs_download(text: str) -> str:
    old = '''    "comparacion-docs": () => downloadStaticFile(
      "planillas/MCP365_P05_Comparacion_documental.xlsx",
      "MCP365_P05_Comparacion_documental.xlsx"
    ),

'''
    if old not in text:
        if '"comparacion-docs"' not in text:
            return text
        raise SystemExit("comparacion-docs download block not found as expected")
    return text.replace(old, "", 1)


def update_templates(text: str) -> str:
    old = '    { name: "Comparación documental", desc: "Excel .xlsx · Matriz PRO-OPS-12 v3.1 vs v4.0", key: "comparacion-docs", type: "Excel" },\n'
    if old in text:
        text = text.replace(old, "", 1)
    return text


def verify(text: str):
    bad = []
    # residual plantilla refs in r5 UI zone / prompt
    if "data-planilla=\"comparacion-docs\"" in text:
        bad.append("button comparacion-docs still present")
    if '"comparacion-docs"' in text:
        bad.append("comparacion-docs key still referenced")
    if "MCP365_P05_Comparacion_documental.xlsx" in text and "completada" not in text.split("MCP365_P05_Comparacion_documental.xlsx")[0][-20:]:
        # allow only if somehow leftover without completada - check exact plantilla name
        import re
        for m in re.finditer(r"MCP365_P05_Comparacion_documental\.xlsx", text):
            # check surrounding isn't "completada.xlsx" already matched wrong
            pass
        # Find non-completada references
        for m in re.finditer(r"MCP365_P05_Comparacion_documental\.xlsx(?!\w)", text):
            ctx = text[max(0, m.start()-30):m.end()+20]
            if "completada" not in ctx:
                bad.append(f"residual plantilla xlsx: ...{ctx}...")
                break
    if "Generación de libro Excel profesional desde cero" not in text and "GENERACIÓN DE LIBRO EXCEL PROFESIONAL" not in text:
        bad.append("new prompt title missing")
    if bad:
        raise SystemExit("VERIFY FAILED:\n" + "\n".join(bad))
    print("VERIFY OK")


def main():
    text = INDEX.read_text(encoding="utf-8")
    text = replace_ui(text)
    print("UI replaced")
    text = replace_prompt_fn(text)
    print("Prompt function replaced")
    text = replace_r5_case(text)
    print("RETO_CASES.r5 replaced")
    text = remove_comparacion_docs_download(text)
    print("comparacion-docs download removed")
    text = update_templates(text)
    print("TEMPLATES updated")
    verify(text)
    INDEX.write_text(text, encoding="utf-8")
    if XLSX.exists():
        XLSX.unlink()
        print(f"Deleted {XLSX.name}")
    else:
        print("xlsx already absent")
    print(f"OK -> {INDEX}")


if __name__ == "__main__":
    main()
