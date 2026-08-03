# -*- coding: utf-8 -*-
"""Inject Reto 4 plantilla-mode prompt and static downloads into index.html."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"

UI_OLD = '''            <div class="m365-box">
              <h4><span class="app-badge">Word</span> Paso a paso con Copilot</h4>
              <ol>
                <li>Descarga la <strong>planilla oficial</strong> de tres audiencias.</li>
                <li>Abre <strong>Word → Copilot</strong> con el informe técnico ST-14 de esta página.</li>
                <li>Ajusta el prompt configurable y cópialo.</li>
                <li>Genera versiones técnica, gerencia y comunidad sin alterar hechos.</li>
                <li>Indica omisiones por audiencia. Validación humana y control de calidad los completa la persona.</li>
                <li>Guarda como <code>MCP365_P04_Tres_audiencias_completado.docx</code>.</li>
                <li>Después: adapta el prompt a un informe propio no confidencial.</li>
              </ol>
            </div>
            <div class="btn-group" style="margin-bottom:1rem">
              <button type="button" class="btn btn--sm btn--energy" data-planilla="tres-audiencias"><i data-lucide="download" width="14" height="14"></i> Descargar planilla oficial (Word)</button>
            </div>
            <div class="doc-box">
              <p><strong>Informe técnico · Hallazgo ST-14 · Subestación Urbana 7 · 18/03/2026</strong></p>
              <p>Durante inspección rutinaria (turno 06:00–14:00) se detectó lectura intermitente en el sensor de temperatura <strong>ST-14</strong>, tablero de control secundario. Se activó el protocolo de verificación PV-OPS-07. No se registró interrupción de servicio ni afectación a usuarios. Inventario: 1 sensor de reemplazo en almacén central (código INV-ST14-A). Reemplazo programado en ventana del <strong>05/04/2026 09:00–11:00</strong>. Impacto estimado: bajo. Si el cierre de área se extiende más de 30 minutos, Comunicaciones debe emitir aviso preventivo a la comunidad aledaña.</p>
            </div>'''

UI_NEW = '''            <div class="m365-box">
              <h4><span class="app-badge">WhatsApp</span> + <span class="app-badge">Word</span> + <span class="app-badge">Copilot</span> Paso a paso</h4>
              <ol>
                <li>Descarga <strong>fuente</strong> (chat WhatsApp) y <strong>plantilla</strong> (dos botones).</li>
                <li>Usa la <strong>misma forma de acceso a la plantilla</strong> que te funcionó en los retos anteriores.</li>
                <li>Proporciona a Copilot: <code>MCP365_P04_Fuente_chat_WhatsApp_ST14_SU7.docx</code> + <code>MCP365_P04_Comunicacion_tres_audiencias.docx</code> + este prompt.</li>
                <li>Copilot debe entregar <code>MCP365_P04_Tres_audiencias_completado.docx</code> (tres versiones sin alterar hechos del chat).</li>
                <li>Control de calidad y firmas los completa la persona.</li>
              </ol>
            </div>
            <p style="margin:0 0 0.5rem;font-size:0.9rem"><strong>Descargas obligatorias</strong> (dos archivos):</p>
            <div class="btn-group" style="margin-bottom:0.75rem;flex-wrap:wrap;gap:0.5rem">
              <button type="button" class="btn btn--sm btn--secondary" data-planilla="tres-audiencias-fuente"><i data-lucide="message-circle" width="14" height="14"></i> Descargar fuente chat WhatsApp ST-14 (.docx)</button>
              <button type="button" class="btn btn--sm btn--energy" data-planilla="tres-audiencias"><i data-lucide="download" width="14" height="14"></i> Descargar plantilla de llenado (.docx)</button>
            </div>
            <p style="margin:0 0 0.35rem;font-size:0.88rem;color:var(--text-muted)">Vista previa (la fuente completa está en el .docx):</p>
            <div class="doc-box">
              <p><strong>CHAT DE WHATSAPP · Caso ficticio · Grupo Operación y Mantenimiento · SU7 · 18/03/2026 · Hallazgo ST-14</strong></p>
              <p><strong>7:12 · Andrés Molina:</strong> Lectura intermitente en sensor ST-14 (tablero secundario).</p>
              <p><strong>7:16 · Laura Méndez:</strong> Activar PV-OPS-07; no concluir calentamiento real aún.</p>
              <p><strong>8:08 · Laura Méndez:</strong> Intervención 05/04/2026 09:00–11:00 · OT-MNT-2026-0417.</p>
              <p><strong>8:24 · Paula Rincón:</strong> Repuesto INV-ST14-A reservado en almacén.</p>
              <p><strong>8:44 · Jorge Salazar:</strong> No autorizar aviso a comunidad por ahora. Impacto bajo; sin afectación a usuarios.</p>
              <p><strong>8:55 · Jorge Salazar:</strong> Si restricción &gt; 30 min, Comunicaciones emite aviso preventivo.</p>
            </div>'''

R4_CASE_OLD_START = '  "r4": {'
# We'll replace by finding unique block via fields fuente line

R4_NEW = r'''  "r4": {
    "id": "r4",
    "title": "Informe para tres audiencias",
    "apps": ["WhatsApp", "Word", "Copilot"],
    "email": false,
    "planilla": {"key": "tres-audiencias", "label": "Descargar plantilla de llenado (.docx)"},
    "output": "MCP365_P04_Tres_audiencias_completado.docx",
    "steps": [
      "Descarga <strong>fuente</strong> (chat WhatsApp) y <strong>plantilla</strong> (dos botones).",
      "Usa la <strong>misma forma de acceso a la plantilla</strong> que funcionó en los retos anteriores.",
      "Proporciona a Copilot: fuente .docx + plantilla + este prompt.",
      "Entrega: <code>MCP365_P04_Tres_audiencias_completado.docx</code>. CQ y firmas solo la persona."
    ],
    "fields": [
      ["rol", "Rol de Copilot", "Comunicador técnico que adapta un mismo conjunto de hechos verificables a tres audiencias sin alterar el significado."],
      ["app", "Aplicaciones de origen", "WhatsApp (fuente) + Word + Copilot."],
      ["fuente", "Fuente que se debe analizar", "MCP365_P04_Fuente_chat_WhatsApp_ST14_SU7.docx — chat de WhatsApp del grupo Operación y Mantenimiento · Subestación Urbana 7 · 18/03/2026 · Hallazgo ST-14 (caso ficticio y anonimizado)."],
      ["caso", "Caso o identificador", "Hallazgo ST-14 · Subestación Urbana 7."],
      ["objetivo", "Objetivo del análisis", "Extraer hechos verificables del chat y generar tres versiones (técnica, gerencia, comunidad) con los mismos hechos, distinto lenguaje y prioridad; completar la matriz de consistencia y las omisiones a propósito."],
      ["archivo", "Archivo Word que se debe completar", "MCP365_P04_Comunicacion_tres_audiencias.docx."],
      ["secciones", "Secciones que Copilot puede completar", "1. Fuente técnica (extracto clave).\n2. Versión A · Resumen técnico.\n3. Versión B · Resumen para gerencia.\n4. Versión C · Comunicación a comunidad / usuarios.\n5. Matriz de consistencia de hechos.\n6. Información omitida a propósito."],
      ["sec1", "Sección 1 · Campo autorizado", "Cuadro de extracto clave con hechos verificables del chat."],
      ["sec2", "Sección 2 · Versión técnica", "Audiencia: especialistas. Prioriza protocolo, mediciones, hipótesis no confirmada, controles y criterios de escalamiento. Lenguaje especializado permitido."],
      ["sec3", "Sección 3 · Versión gerencia", "Audiencia: dirección. Prioriza impacto, riesgo, decisión vigente, plazo y recursos. Máximo 10 líneas."],
      ["sec4", "Sección 4 · Versión comunidad", "Audiencia general. Qué ocurre, cuándo, cómo afecta y a quién contactar. Sin códigos técnicos innecesarios. Sin afirmar “falla térmica” ni causa raíz confirmada. No presentar el aviso como ya publicado si el chat indica que aún no está autorizado."],
      ["sec5", "Sección 5 · Matriz de consistencia", "Cinco filas existentes: Hecho original | ¿En técnica? | ¿En gerencia? | ¿En comunidad? | ¿Se alteró el significado? | Corrección."],
      ["sec6", "Sección 6 · Omisiones", "Tres filas (Técnica, Gerencia, Comunidad): Qué se omitió | Por qué | ¿Riesgo de malentendido?"],
      ["restringidos", "Campos o secciones que deben quedar sin completar", "* Datos del participante.\n* Área o rol.\n* Fecha del participante.\n* Aplicación utilizada.\n* Fuente utilizada.\n* Estado general del documento.\n* Sección 7: Control de calidad.\n* Casillas Sí y No del control de calidad.\n* Observaciones del control de calidad.\n* Sección 8: Firmas.\n* Elaboró.\n* Revisó.\n* Aprobó."],
      ["vacio", "Respuesta cuando no exista información", "No especificado."],
      ["detalle", "Nivel de detalle", "Hechos idénticos entre versiones; variar solo lenguaje y prioridad. No inventar mediciones, fechas, códigos ni autorizaciones."],
      ["prohibiciones_contenido", "Prohibiciones de contenido específicas del caso", "* No afirmar “sensor dañado” ni causa raíz confirmada.\n* No mencionar “falla térmica” o sobretemperatura confirmada.\n* No inventar publicación del aviso comunitario ya emitida.\n* En comunidad: evitar códigos PV-OPS-07, INV-ST14-A y OT-MNT-2026-0417."],
      ["salida", "Nombre del archivo de salida", "MCP365_P04_Tres_audiencias_completado.docx."]
    ],
    "checklist": [
      ["r4-c1", "Fuente chat WhatsApp + plantilla disponibles"],
      ["r4-c2", "Usé el mismo acceso a plantilla que en retos anteriores"],
      ["r4-c3", "Tres versiones sin alterar hechos; causa raíz no afirmada como confirmada"],
      ["r4-c4", "Comunidad sin códigos técnicos innecesarios; CQ y firmas vacíos"],
      ["r4-c5", "Descargué MCP365_P04_Tres_audiencias_completado.docx con diseño intacto"]
    ],
    "practice_title": "Al terminar · Practica con tu propio chat u informe",
    "practice": "Usa un chat o informe operativo propio (anonimizado) + la plantilla. Adapta los campos del prompt. Guarda como MCP365_P04_Tres_audiencias_[tu-tema]_completado.docx.",
    "deliverable": "Entregable: MCP365_P04_Tres_audiencias_completado.docx (copia de la plantilla). CQ y firmas vacíos para Copilot."
  },'''

FN = r'''
  function getPromptR4Fields() {
    const box = document.getElementById("promptConfig-r4");
    const c = RETO_CASES.r4;
    const out = {};
    if (c && c.fields) c.fields.forEach(([k, , def]) => { out[k] = def; });
    if (box) {
      box.querySelectorAll("[data-reto-field]").forEach(el => {
        out[el.getAttribute("data-reto-field")] = (el.value || "").trim();
      });
    }
    return out;
  }

  /** Prompt Reto 4: modo edición de plantilla Word (mismo patrón que Reto 1–3). */
  function buildPromptR4Text(f) {
    const bracket = (v) => "[[" + (v || "") + "]]";
    return [
      "PROMPT CONFIGURABLE PARA COPILOT",
      "MODO EDICIÓN DE PLANTILLA WORD",
      "CASO: CHAT WHATSAPP · HALLAZGO ST-14 · TRES AUDIENCIAS · RETO 4",
      "",
      "INSTRUCCIONES PARA EL PARTICIPANTE",
      "",
      "Revisa los campos de configuración. Utiliza este prompt siguiendo el mismo procedimiento que funcionó en los retos anteriores.",
      "",
      "Archivos requeridos:",
      "",
      "FUENTE:",
      "",
      "MCP365_P04_Fuente_chat_WhatsApp_ST14_SU7.docx",
      "",
      "PLANTILLA:",
      "",
      "MCP365_P04_Comunicacion_tres_audiencias.docx",
      "",
      "ENTREGABLE:",
      "",
      "MCP365_P04_Tres_audiencias_completado.docx",
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
      "FUENTE QUE SE DEBE ANALIZAR",
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
      "ARCHIVO WORD QUE SE DEBE COMPLETAR",
      "",
      bracket(f.archivo),
      "",
      "SECCIONES QUE COPILOT PUEDE COMPLETAR",
      "",
      bracket("\n" + (f.secciones || "") + "\n"),
      "",
      "SECCIÓN 1 · CAMPO AUTORIZADO",
      "",
      bracket(f.sec1),
      "",
      "SECCIÓN 2 · VERSIÓN TÉCNICA",
      "",
      bracket(f.sec2),
      "",
      "SECCIÓN 3 · VERSIÓN GERENCIA",
      "",
      bracket(f.sec3),
      "",
      "SECCIÓN 4 · VERSIÓN COMUNIDAD",
      "",
      bracket(f.sec4),
      "",
      "SECCIÓN 5 · MATRIZ DE CONSISTENCIA",
      "",
      bracket(f.sec5),
      "",
      "SECCIÓN 6 · OMISIONES",
      "",
      bracket(f.sec6),
      "",
      "CAMPOS O SECCIONES QUE DEBEN QUEDAR SIN COMPLETAR",
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
      "PROHIBICIONES DE CONTENIDO ESPECÍFICAS DEL CASO",
      "",
      bracket("\n" + (f.prohibiciones_contenido || "") + "\n"),
      "",
      "NOMBRE DEL ARCHIVO DE SALIDA",
      "",
      bracket(f.salida),
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "2. INSTRUCCIÓN PARA COPILOT",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "ACTÚA EN MODO EDICIÓN DE PLANTILLA WORD (.docx REAL).",
      "",
      "Analiza exclusivamente el chat de WhatsApp indicado y completa una copia editable de la plantilla oficial.",
      "",
      "No reconstruyas el documento desde una representación textual.",
      "",
      "No crees un documento con otro diseño.",
      "",
      "No conviertas las tablas en párrafos o listas.",
      "",
      "PRECONDICIÓN DEL ARCHIVO",
      "",
      "1. Comprueba que puedes acceder al archivo fuente.",
      "2. Comprueba que puedes acceder a la plantilla Word editable.",
      "3. Comprueba que puedes crear una copia conservando su diseño.",
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
      "1. Crea una copia de la plantilla oficial.",
      "2. Analiza el chat completo, desde el inicio hasta el cierre del turno.",
      "3. Extrae solo hechos verificables (confirmados en el chat).",
      "4. Completa el extracto de la sección 1.",
      "5. Redacta las tres versiones (secciones 2, 3 y 4) con los mismos hechos.",
      "6. Completa la matriz de consistencia (sección 5).",
      "7. Completa las omisiones a propósito (sección 6).",
      "8. Conserva sin cambios las secciones 7 y 8.",
      "9. Guarda la copia con el nombre definido en la configuración.",
      "",
      "Trabaja sección por sección dentro del mismo documento.",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "4. REGLAS DE CONTENIDO",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "* Utiliza únicamente información del chat fuente.",
      "* Diferencia hecho confirmado, hipótesis, propuesta y decisión.",
      "* La causa raíz permanece pendiente; no afirmes “sensor dañado”.",
      "* No menciones “falla térmica” ni sobretemperatura confirmada.",
      "* Impacto: bajo, sin afectación a usuarios, servicio normal.",
      "* Intervención: 5 de abril de 2026, 09:00–11:00; sin interrupción de servicio prevista.",
      "* Comunicación externa: no autorizada todavía; borrador preventivo sí; publicar solo si se cumplen criterios (restricción > 30 min u otros definidos).",
      "* En versión comunidad: evita códigos técnicos innecesarios.",
      "* Si falta un dato, escribe “No especificado”.",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "5. CONSERVACIÓN DE LA PLANTILLA",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "Mantén banner, título, chips, colores, tablas, bordes, tipografías, recuadros, numeración, encabezados, número de filas/columnas, control de calidad y firmas.",
      "",
      "Las filas pueden aumentar su altura si hace falta. No cambies anchos ni composición.",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "6. PROHIBICIONES",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "* No crees un documento desde cero.",
      "* No reemplaces la plantilla por un documento nuevo.",
      "* No conviertas tablas en párrafos.",
      "* No utilices barras verticales para simular tablas.",
      "* No inventes hechos, fechas, mediciones ni autorizaciones.",
      "* No completes control de calidad ni firmas.",
      "* No escribas el nombre del archivo como título.",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "7. VERIFICACIÓN OBLIGATORIA",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "Antes de guardar, confirma:",
      "",
      "1. Los hechos provienen solo del chat.",
      "2. Las tres versiones no alteran el significado.",
      "3. No se afirmó causa raíz confirmada ni falla térmica.",
      "4. La versión comunidad no usa códigos técnicos innecesarios.",
      "5. La matriz de consistencia y omisiones están completas.",
      "6. Secciones 7 y 8 siguen vacías.",
      "7. El documento conserva el formato original.",
      "8. El archivo final es un `.docx` real.",
      "",
      "Si alguna comprobación falla, corrige la copia antes de guardarla.",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "8. ENTREGA",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "Guarda y entrega la copia completa con el nombre:",
      "",
      "MCP365_P04_Tres_audiencias_completado.docx",
      "",
      "No entregues únicamente un resumen en el panel de Copilot."
    ].join("\n");
  }

'''

MARKER = "  /* ========== RETO ENGINE (patrón S1·R1 reutilizable; R1 no se remonta) ========== */"
WIRE_OLD = '    if (caseId === "r3") return buildPromptR3Text(getPromptR3Fields());'
WIRE_NEW = (
    '    if (caseId === "r3") return buildPromptR3Text(getPromptR3Fields());\n'
    '    if (caseId === "r4") return buildPromptR4Text(getPromptR4Fields());'
)

DOWNLOAD_OLD_START = '    "tres-audiencias": () => downloadWord("MCP365_P04_Comunicacion_tres_audiencias.doc"'

DOWNLOAD_NEW = '''    "tres-audiencias-fuente": () => downloadStaticFile(
      "planillas/MCP365_P04_Fuente_chat_WhatsApp_ST14_SU7.docx",
      "MCP365_P04_Fuente_chat_WhatsApp_ST14_SU7.docx"
    ),

    "tres-audiencias": () => downloadStaticFile(
      "planillas/MCP365_P04_Comunicacion_tres_audiencias.docx",
      "MCP365_P04_Comunicacion_tres_audiencias.docx"
    ),'''

TEMPLATES_OLD = '    { name: "Tres audiencias", desc: "Word · Técnico, gerencia, comunidad + control de hechos", key: "tres-audiencias", type: "Word" },'
TEMPLATES_NEW = '''    { name: "Fuente chat WhatsApp ST-14", desc: "Word .docx · Chat O&M SU7 · Hallazgo ST-14 (solo lectura)", key: "tres-audiencias-fuente", type: "Word" },
    { name: "Tres audiencias", desc: "Word .docx · Técnico, gerencia, comunidad + consistencia", key: "tres-audiencias", type: "Word" },'''

SUBTITLE_OLD = '                <span class="text-muted" style="display:block;font-size:0.85rem;color:var(--text-muted)">Word · Adaptar lenguaje y prioridad</span>'
SUBTITLE_NEW = '                <span class="text-muted" style="display:block;font-size:0.85rem;color:var(--text-muted)">WhatsApp + Word · Modo edición de plantilla (como Reto 1–3)</span>'


def replace_r4_case(text: str) -> str:
    start = text.find('  "r4": {')
    if start < 0:
        raise SystemExit("r4 case not found")
    end = text.find('  "r5": {', start)
    if end < 0:
        raise SystemExit("r5 after r4 not found")
    return text[:start] + R4_NEW + "\n" + text[end:]


def replace_download_block(text: str) -> str:
    start = text.find(DOWNLOAD_OLD_START)
    if start < 0:
        if '"tres-audiencias-fuente"' in text:
            return text
        raise SystemExit("tres-audiencias download not found")
    # find end of that template literal call: `), after the closing backtick
    # Pattern ends with `),
    marker = '      </table>`),'
    # There may be multiple; search from start within a reasonable window
    window = text[start:start + 2500]
    idx = window.find(marker)
    if idx < 0:
        raise SystemExit("end of tres-audiencias download not found")
    end = start + idx + len(marker)
    return text[:start] + DOWNLOAD_NEW + text[end:]


def main():
    text = INDEX.read_text(encoding="utf-8")

    if UI_OLD not in text:
        if "tres-audiencias-fuente" in text and "Fuente chat WhatsApp" in text:
            print("UI already updated")
        else:
            raise SystemExit("UI_OLD not found")
    else:
        text = text.replace(UI_OLD, UI_NEW, 1)
        print("Updated Reto 4 UI")

    if SUBTITLE_OLD in text:
        text = text.replace(SUBTITLE_OLD, SUBTITLE_NEW, 1)
        print("Updated subtitle")

    if '"MCP365_P04_Fuente_chat_WhatsApp_ST14_SU7.docx' in text and 'prohibiciones_contenido' in text:
        print("r4 case already updated")
    else:
        text = replace_r4_case(text)
        print("Replaced RETO_CASES.r4")

    if "function buildPromptR4Text" in text:
        print("buildPromptR4Text already present")
    else:
        if MARKER not in text:
            raise SystemExit("MARKER not found")
        text = text.replace(MARKER, FN + "\n" + MARKER, 1)
        print("Injected buildPromptR4Text")

    if 'if (caseId === "r4") return buildPromptR4Text' in text:
        print("Wire already present")
    elif WIRE_OLD not in text:
        raise SystemExit("WIRE_OLD not found")
    else:
        text = text.replace(WIRE_OLD, WIRE_NEW, 1)
        print("Wired r4 in buildPromptFromCase")

    text = replace_download_block(text)
    print("Updated tres-audiencias downloads")

    if 'key: "tres-audiencias-fuente"' in text:
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
