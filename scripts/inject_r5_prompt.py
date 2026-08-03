# -*- coding: utf-8 -*-
"""Inject Reto 5 Excel plantilla mode + real file downloads into index.html only for r5."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"

UI_OLD = '''            <div class="m365-box">
              <h4><span class="app-badge">Word</span> + <span class="app-badge">Excel</span> Paso a paso con Copilot</h4>
              <ol>
                <li>Descarga la <strong>planilla oficial</strong> de comparación.</li>
                <li>En Word, pega PRO-OPS-12 v3.1 y v4.0 (textos de esta página).</li>
                <li>Ajusta el prompt configurable y cópialo.</li>
                <li>Pide la tabla Tema | Anterior | Actual | Impacto | Validación requerida.</li>
                <li>No inventes cláusulas. Validación humana y control de calidad los completa la persona.</li>
                <li>Guarda como <code>MCP365_P05_Comparacion_docs_completada.xlsx</code>.</li>
                <li>Después: compara dos versiones reales de un documento propio anonimizado.</li>
              </ol>
            </div>
            <div class="btn-group" style="margin-bottom:1rem">
              <button type="button" class="btn btn--sm btn--energy" data-planilla="comparacion-docs"><i data-lucide="download" width="14" height="14"></i> Descargar planilla oficial (Excel)</button>
            </div>
            <div class="grid grid-2">
              <div class="doc-box">
                <strong>PRO-OPS-12 · Versión 3.1 (vigente hasta 28/02/2026)</strong>
                <p>1. Notificar a usuarios con 48 horas de anticipación.<br>2. El supervisor de turno autoriza el inicio de la intervención.<br>3. Registrar hallazgos en planilla física FO-OPS-12.<br>4. Cierre operativo antes de las 17:00.</p>
              </div>
              <div class="doc-box">
                <strong>PRO-OPS-12 · Versión 4.0 (vigente desde 01/03/2026)</strong>
                <p>1. Notificar a usuarios con 72 horas de anticipación.<br>2. El líder de seguridad y el supervisor de turno autorizan el inicio.<br>3. Registrar hallazgos en el sistema digital compartido (SharePoint Ops).<br>4. Cierre operativo antes de las 16:00, salvo excepción documentada por gerencia de zona.</p>
              </div>
            </div>'''

UI_NEW = '''            <div class="m365-box">
              <h4><span class="app-badge">Excel</span> + <span class="app-badge">Copilot</span> Paso a paso</h4>
              <ol>
                <li>Descarga la <strong>plantilla Excel</strong> y las <strong>fuentes PDF</strong> (botones abajo).</li>
                <li>Opcional: descarga las versiones Word como respaldo.</li>
                <li>Usa la <strong>misma forma de acceso a la plantilla</strong> que te funcionó en los retos anteriores.</li>
                <li>Proporciona a Copilot: <code>PRO-OPS-12_Version_3_1.pdf</code> + <code>PRO-OPS-12_Version_4_0.pdf</code> + <code>MCP365_P05_Comparacion_documental.xlsx</code> + este prompt.</li>
                <li>Copilot completa solo la hoja <strong>Comparación</strong> (secciones autorizadas). No toca <strong>Validación y calidad</strong>.</li>
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
              <p><strong>Fuentes oficiales:</strong> <code>PRO-OPS-12_Version_3_1.pdf</code> (histórica · vigencia hasta 28/02/2026) y <code>PRO-OPS-12_Version_4_0.pdf</code> (vigente desde 01/03/2026).</p>
              <p><strong>Plantilla:</strong> <code>MCP365_P05_Comparacion_documental.xlsx</code> · Entregable: <code>MCP365_P05_Comparacion_documental_completada.xlsx</code>.</p>
              <p class="text-muted" style="font-size:0.88rem;margin:0">Compara ambas versiones: cambios textuales y de significado, impactos, elementos nuevos/eliminados, contradicciones y recomendación de transición. Solo hoja «Comparación».</p>
            </div>'''

SUBTITLE_OLD = '                <span class="text-muted" style="display:block;font-size:0.85rem;color:var(--text-muted)">Word · Cambios de texto y de significado</span>'
SUBTITLE_NEW = '                <span class="text-muted" style="display:block;font-size:0.85rem;color:var(--text-muted)">Excel · PRO-OPS-12 v3.1 vs v4.0 · Modo edición de plantilla</span>'

R5_NEW = r'''  "r5": {
    "id": "r5",
    "title": "Comparación de documentos",
    "apps": ["Excel", "Copilot"],
    "email": false,
    "planilla": {"key": "comparacion-docs", "label": "Plantilla Excel (.xlsx)"},
    "output": "MCP365_P05_Comparacion_documental_completada.xlsx",
    "steps": [
      "Descarga plantilla Excel + fuentes PDF v3.1 y v4.0.",
      "Opcional: respaldos Word.",
      "Usa el mismo acceso a plantilla que en retos anteriores.",
      "Copilot completa solo hoja Comparación; no toca Validación y calidad.",
      "Entrega: <code>MCP365_P05_Comparacion_documental_completada.xlsx</code>."
    ],
    "fields": [
      ["rol", "Rol de Copilot", "Analista documental especializado en comparación normativa, detección de cambios textuales y de significado, evaluación de impactos y recomendaciones de transición."],
      ["app", "Aplicaciones de origen", "Excel + Copilot (fuentes PDF oficiales; Word opcional como respaldo)."],
      ["fuente", "Fuentes que se deben analizar", "PRO-OPS-12_Version_3_1.pdf (histórica) y PRO-OPS-12_Version_4_0.pdf (vigente). Si se usan los .docx de respaldo, deben ser las mismas versiones; no mezclar ni inventar cláusulas."],
      ["caso", "Caso o identificador", "PRO-OPS-12 · Versión 3.1 vs Versión 4.0."],
      ["objetivo", "Objetivo del análisis", "Comparar ambas versiones; identificar cambios textuales y de significado; evaluar impactos; detectar elementos nuevos, eliminados y contradicciones; formular una recomendación de transición verificable."],
      ["archivo", "Archivo Excel que se debe completar", "MCP365_P05_Comparacion_documental.xlsx."],
      ["hoja_autorizada", "Hoja que Copilot puede editar", "Comparación."],
      ["secciones", "Secciones autorizadas en la hoja Comparación", "4. Matriz de cambios (filas 1–12 ya numeradas).\n5. Elementos nuevos, eliminados y contradicciones.\n6. Recomendación de transición."],
      ["sec4", "Sección 4 · Campos autorizados (matriz)", "En las 12 filas existentes, completar:\n* Versión 3.1\n* Evidencia V3.1\n* Versión 4.0\n* Evidencia V4.0\n* Tipo de cambio (Textual / Significado / Ambos)\n* Naturaleza (Modificado / Nuevo / Eliminado / Sin cambio)\n* Impacto posible\n* Acción de transición\n* Aprobador sugerido\n* Prioridad (Alta / Media / Baja)\n\nNo modificar la columna «Estado de validación» (dejar Pendiente).\nNo cambiar el número ni el tema/sección prellenados."],
      ["sec5", "Sección 5 · Campos autorizados", "Filas disponibles:\n* Tipo (Elemento nuevo / Elemento eliminado / Contradicción detectada)\n* Descripción\n* Evidencia precisa\n* Riesgo si se ignora\n* Acción recomendada"],
      ["sec6", "Sección 6 · Campos autorizados", "* Regla efectiva\n* Excepciones\n* Acciones obligatorias\n* Responsable principal\n* Fecha límite\n* Evidencia de cierre"],
      ["restringidos", "Hojas o campos que deben quedar sin completar / sin modificar", "* Hoja «Validación y calidad» completa (validación humana y control de calidad).\n* Hoja «Instrucciones».\n* Hoja «Catálogos».\n* Sección 1 · Datos del participante (Nombre, Correo, Fecha, Área/rol, Estado).\n* Sección 2 · Identificación de documentos (ya prellenada).\n* Sección 3 · Resumen automático (fórmulas).\n* Columna «Estado de validación» de la matriz.\n* Títulos, encabezados, estructura, listas desplegables y formato."],
      ["vacio", "Respuesta cuando no exista información", "No especificado."],
      ["detalle", "Nivel de detalle", "Breve y verificable. Cada diferencia con evidencia precisa (versión, sección y fragmento breve). No inventes impactos ni responsables."],
      ["evidencia", "Formato de evidencia", "Versión · sección o título · cita breve del fragmento."],
      ["salida", "Nombre del archivo de salida", "MCP365_P05_Comparacion_documental_completada.xlsx."]
    ],
    "checklist": [
      ["r5-c1", "Plantilla .xlsx + PDFs v3.1 y v4.0 descargados"],
      ["r5-c2", "Usé el mismo acceso a plantilla que en retos anteriores"],
      ["r5-c3", "Hoja Comparación: matriz, hallazgos y recomendación con evidencia"],
      ["r5-c4", "Hoja Validación y calidad intacta / vacía para la persona"],
      ["r5-c5", "Guardé MCP365_P05_Comparacion_documental_completada.xlsx"]
    ],
    "practice_title": "Al terminar · Compara dos versiones propias",
    "practice": "Usa dos versiones de un procedimiento propio (anonimizado) + la plantilla Excel. Adapta los campos del prompt. Guarda como MCP365_P05_Comparacion_[tu-doc]_completada.xlsx.",
    "deliverable": "Entregable: MCP365_P05_Comparacion_documental_completada.xlsx. Solo hoja Comparación llenada por Copilot; Validación y calidad vacía."
  },'''

FN = r'''
  function getPromptR5Fields() {
    const box = document.getElementById("promptConfig-r5");
    const c = RETO_CASES.r5;
    const out = {};
    if (c && c.fields) c.fields.forEach(([k, , def]) => { out[k] = def; });
    if (box) {
      box.querySelectorAll("[data-reto-field]").forEach(el => {
        out[el.getAttribute("data-reto-field")] = (el.value || "").trim();
      });
    }
    return out;
  }

  /** Prompt Reto 5: modo edición de plantilla Excel (.xlsx real). */
  function buildPromptR5Text(f) {
    const bracket = (v) => "[[" + (v || "") + "]]";
    return [
      "PROMPT CONFIGURABLE PARA COPILOT",
      "MODO EDICIÓN DE PLANTILLA EXCEL",
      "CASO: COMPARACIÓN DOCUMENTAL · PRO-OPS-12 V3.1 vs V4.0 · RETO 5",
      "",
      "INSTRUCCIONES PARA EL PARTICIPANTE",
      "",
      "Revisa los campos de configuración. Utiliza este prompt siguiendo el mismo procedimiento que funcionó en los retos anteriores.",
      "",
      "Archivos requeridos:",
      "",
      "FUENTES OFICIALES (PDF):",
      "",
      "PRO-OPS-12_Version_3_1.pdf",
      "PRO-OPS-12_Version_4_0.pdf",
      "",
      "RESPALDO OPCIONAL (Word):",
      "",
      "PRO-OPS-12_Version_3_1.docx",
      "PRO-OPS-12_Version_4_0.docx",
      "",
      "PLANTILLA:",
      "",
      "MCP365_P05_Comparacion_documental.xlsx",
      "",
      "ENTREGABLE:",
      "",
      "MCP365_P05_Comparacion_documental_completada.xlsx",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "1. CONFIGURACIÓN DEL ANÁLISIS",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "ROL DE COPILOT",
      "",
      bracket(f.rol),
      "",
      "APLICACIONES DE ORIGEN",
      "",
      bracket(f.app),
      "",
      "FUENTES QUE SE DEBEN ANALIZAR",
      "",
      bracket(f.fuente),
      "",
      "CASO O IDENTIFICADOR",
      "",
      bracket(f.caso),
      "",
      "OBJETIVO DEL ANÁLISIS",
      "",
      bracket(f.objetivo),
      "",
      "ARCHIVO EXCEL QUE SE DEBE COMPLETAR",
      "",
      bracket(f.archivo),
      "",
      "HOJA QUE COPILOT PUEDE EDITAR",
      "",
      bracket(f.hoja_autorizada),
      "",
      "SECCIONES AUTORIZADAS EN LA HOJA COMPARACIÓN",
      "",
      bracket("\n" + (f.secciones || "") + "\n"),
      "",
      "SECCIÓN 4 · CAMPOS AUTORIZADOS",
      "",
      bracket("\n" + (f.sec4 || "") + "\n"),
      "",
      "SECCIÓN 5 · CAMPOS AUTORIZADOS",
      "",
      bracket("\n" + (f.sec5 || "") + "\n"),
      "",
      "SECCIÓN 6 · CAMPOS AUTORIZADOS",
      "",
      bracket("\n" + (f.sec6 || "") + "\n"),
      "",
      "HOJAS O CAMPOS QUE DEBEN QUEDAR SIN COMPLETAR / SIN MODIFICAR",
      "",
      bracket("\n" + (f.restringidos || "") + "\n"),
      "",
      "RESPUESTA CUANDO NO EXISTA INFORMACIÓN",
      "",
      bracket(f.vacio),
      "",
      "NIVEL DE DETALLE",
      "",
      bracket(f.detalle),
      "",
      "FORMATO DE EVIDENCIA",
      "",
      bracket(f.evidencia),
      "",
      "NOMBRE DEL ARCHIVO DE SALIDA",
      "",
      bracket(f.salida),
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "2. INSTRUCCIÓN PARA COPILOT",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "ACTÚA EN MODO EDICIÓN DE PLANTILLA EXCEL (.xlsx REAL).",
      "",
      "Analiza exclusivamente las dos versiones de PRO-OPS-12 indicadas y completa una copia editable de la plantilla oficial.",
      "",
      "No reconstruyas el libro desde una representación textual.",
      "",
      "No crees un documento Word ni un Excel con otro diseño.",
      "",
      "No conviertas hojas o tablas en párrafos.",
      "",
      "PRECONDICIÓN DEL ARCHIVO",
      "",
      "1. Comprueba que puedes acceder a ambas fuentes (PDF oficiales; Word solo como respaldo equivalente).",
      "2. Comprueba que puedes acceder a la plantilla Excel editable.",
      "3. Comprueba que puedes crear una copia conservando hojas, fórmulas, listas desplegables y formato.",
      "4. Si puedes editar la copia, continúa.",
      "5. Si solo puedes leer o previsualizar la plantilla, detente.",
      "",
      "Si no puedes conservar la plantilla, responde:",
      "",
      "“No puedo completar la plantilla conservando su formato. No generaré un documento alternativo.”",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "3. TAREA",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "1. Crea una copia de MCP365_P05_Comparacion_documental.xlsx.",
      "2. Lee ambas normas completas (v3.1 y v4.0).",
      "3. Trabaja únicamente en la hoja «Comparación».",
      "4. Completa la sección 4 (matriz de cambios) con evidencia de ambas versiones.",
      "5. Completa la sección 5 (elementos nuevos, eliminados y contradicciones).",
      "6. Completa la sección 6 (recomendación de transición).",
      "7. No modifiques la hoja «Validación y calidad».",
      "8. No modifiques Instrucciones ni Catálogos.",
      "9. Guarda la copia con el nombre definido en la configuración.",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "4. REGLAS DE CONTENIDO",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "* Usa únicamente las dos normas suministradas.",
      "* Distingue cambio textual, cambio de significado o ambos.",
      "* Una obligación nueva no equivale a una simple reescritura.",
      "* Si una regla del cuerpo contradice un anexo, regístrala como contradicción.",
      "* No inventes impactos, responsables, plazos ni cláusulas.",
      "* Cita versión, sección y fragmento breve en cada evidencia.",
      "* Para datos ausentes escribe “No especificado”.",
      "* Deja la columna «Estado de validación» en Pendiente.",
      "* Respeta la vigencia: v4.0 desde 01/03/2026.",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "5. CONSERVACIÓN DE LA PLANTILLA",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "Mantén sin modificaciones: nombres de hojas, títulos, encabezados, estructura, fórmulas, listas desplegables, colores, anchos y formato.",
      "",
      "Las filas pueden aumentar su altura si hace falta.",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "6. PROHIBICIONES",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "* No crees un archivo desde cero.",
      "* No reemplaces la plantilla por un documento nuevo.",
      "* No edites la hoja «Validación y calidad».",
      "* No completes datos del participante.",
      "* No alteres la identificación documental prellenada ni las fórmulas.",
      "* No marques validaciones humanas como cumplidas.",
      "* No inventes información externa.",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "7. VERIFICACIÓN OBLIGATORIA",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "Antes de guardar, confirma:",
      "",
      "1. Se compararon ambas versiones oficiales.",
      "2. La matriz incluye cambios textuales y de significado con evidencia.",
      "3. Hay elementos nuevos, eliminados y/o contradicciones cuando apliquen.",
      "4. Existe recomendación de transición.",
      "5. La hoja «Validación y calidad» permanece sin completar.",
      "6. El archivo final es un `.xlsx` real con el nombre de salida.",
      "",
      "Si alguna comprobación falla, corrige la copia antes de guardarla.",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "8. ENTREGA",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "Guarda y entrega:",
      "",
      "MCP365_P05_Comparacion_documental_completada.xlsx",
      "",
      "No entregues únicamente un resumen en el panel de Copilot."
    ].join("\n");
  }

'''

MARKER = "  /* ========== RETO ENGINE (patrón S1·R1 reutilizable; R1 no se remonta) ========== */"
WIRE_OLD = '    if (caseId === "r4") return buildPromptR4Text(getPromptR4Fields());'
WIRE_NEW = (
    '    if (caseId === "r4") return buildPromptR4Text(getPromptR4Fields());\n'
    '    if (caseId === "r5") return buildPromptR5Text(getPromptR5Fields());'
)

DOWNLOAD_OLD_START = '    "comparacion-docs": () => downloadWord("MCP365_P05_Comparacion_documental.doc"'

DOWNLOAD_NEW = '''    "comparacion-docs": () => downloadStaticFile(
      "planillas/MCP365_P05_Comparacion_documental.xlsx",
      "MCP365_P05_Comparacion_documental.xlsx"
    ),

    "pro-ops-12-v31-pdf": () => downloadStaticFile(
      "planillas/PRO-OPS-12_Version_3_1.pdf",
      "PRO-OPS-12_Version_3_1.pdf"
    ),

    "pro-ops-12-v40-pdf": () => downloadStaticFile(
      "planillas/PRO-OPS-12_Version_4_0.pdf",
      "PRO-OPS-12_Version_4_0.pdf"
    ),

    "pro-ops-12-v31-docx": () => downloadStaticFile(
      "planillas/PRO-OPS-12_Version_3_1.docx",
      "PRO-OPS-12_Version_3_1.docx"
    ),

    "pro-ops-12-v40-docx": () => downloadStaticFile(
      "planillas/PRO-OPS-12_Version_4_0.docx",
      "PRO-OPS-12_Version_4_0.docx"
    ),'''

TEMPLATES_OLD = '    { name: "Comparación documental", desc: "Word · Cambios, impactos y validaciones", key: "comparacion-docs", type: "Word" },'
TEMPLATES_NEW = '''    { name: "Comparación documental", desc: "Excel .xlsx · Matriz PRO-OPS-12 v3.1 vs v4.0", key: "comparacion-docs", type: "Excel" },
    { name: "PRO-OPS-12 v3.1 (PDF)", desc: "Fuente oficial histórica", key: "pro-ops-12-v31-pdf", type: "PDF" },
    { name: "PRO-OPS-12 v4.0 (PDF)", desc: "Fuente oficial vigente", key: "pro-ops-12-v40-pdf", type: "PDF" },
    { name: "PRO-OPS-12 v3.1 (Word)", desc: "Respaldo opcional", key: "pro-ops-12-v31-docx", type: "Word" },
    { name: "PRO-OPS-12 v4.0 (Word)", desc: "Respaldo opcional", key: "pro-ops-12-v40-docx", type: "Word" },'''


def replace_r5_case(text: str) -> str:
    start = text.find('  "r5": {')
    if start < 0:
        raise SystemExit("r5 case not found")
    end = text.find('  "r6": {', start)
    if end < 0:
        raise SystemExit("r6 after r5 not found")
    return text[:start] + R5_NEW + "\n" + text[end:]


def replace_download_block(text: str) -> str:
    start = text.find(DOWNLOAD_OLD_START)
    if start < 0:
        if "pro-ops-12-v31-pdf" in text and "MCP365_P05_Comparacion_documental.xlsx" in text:
            return text
        raise SystemExit("comparacion-docs downloadWord not found")
    marker = '      <div class="box"></div>`),'
    window = text[start:start + 4000]
    idx = window.find(marker)
    if idx < 0:
        raise SystemExit("end of comparacion-docs download not found")
    end = start + idx + len(marker)
    return text[:start] + DOWNLOAD_NEW + text[end:]


def main():
    text = INDEX.read_text(encoding="utf-8")

    if UI_OLD not in text:
        if "pro-ops-12-v31-pdf" in text:
            print("UI already updated")
        else:
            raise SystemExit("UI_OLD not found")
    else:
        text = text.replace(UI_OLD, UI_NEW, 1)
        print("Updated Reto 5 UI")

    if SUBTITLE_OLD in text:
        text = text.replace(SUBTITLE_OLD, SUBTITLE_NEW, 1)
        print("Updated subtitle")

    if "MCP365_P05_Comparacion_documental_completada.xlsx" in text and "hoja_autorizada" in text:
        print("r5 case already updated")
    else:
        text = replace_r5_case(text)
        print("Replaced RETO_CASES.r5")

    if "function buildPromptR5Text" in text:
        print("buildPromptR5Text already present")
    else:
        if MARKER not in text:
            raise SystemExit("MARKER not found")
        # Insert before RETO ENGINE, after R4 prompt if present
        text = text.replace(MARKER, FN + "\n" + MARKER, 1)
        print("Injected buildPromptR5Text")

    if 'if (caseId === "r5") return buildPromptR5Text' in text:
        print("Wire already present")
    elif WIRE_OLD not in text:
        raise SystemExit("WIRE_OLD not found")
    else:
        text = text.replace(WIRE_OLD, WIRE_NEW, 1)
        print("Wired r5 in buildPromptFromCase")

    text = replace_download_block(text)
    print("Updated comparacion downloads to static files")

    if 'key: "pro-ops-12-v31-pdf"' in text:
        print("Templates already updated")
    elif TEMPLATES_OLD not in text:
        raise SystemExit("TEMPLATES_OLD not found")
    else:
        text = text.replace(TEMPLATES_OLD, TEMPLATES_NEW, 1)
        print("Updated TEMPLATES catalog")

    INDEX.write_text(text, encoding="utf-8")
    print(f"OK -> {INDEX}")


if __name__ == "__main__":
    main()
