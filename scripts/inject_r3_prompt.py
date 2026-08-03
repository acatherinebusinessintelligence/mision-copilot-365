# -*- coding: utf-8 -*-
"""Inject buildPromptR3Text + wire buildPromptFromCase into index.html."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"

FN = r'''
  function getPromptR3Fields() {
    const box = document.getElementById("promptConfig-r3");
    const c = RETO_CASES.r3;
    const out = {};
    if (c && c.fields) c.fields.forEach(([k, , def]) => { out[k] = def; });
    if (box) {
      box.querySelectorAll("[data-reto-field]").forEach(el => {
        out[el.getAttribute("data-reto-field")] = (el.value || "").trim();
      });
    }
    return out;
  }

  /** Prompt Reto 3: modo edición de plantilla Word (mismo patrón que Reto 1 y 2). */
  function buildPromptR3Text(f) {
    const bracket = (v) => "[[" + (v || "") + "]]";
    return [
      "PROMPT CONFIGURABLE PARA COPILOT",
      "MODO EDICIÓN DE PLANTILLA WORD",
      "CASO: TRANSCRIPCIÓN DE TEAMS · PROYECTO HORIZONTE · RETO 3",
      "",
      "INSTRUCCIONES PARA EL PARTICIPANTE",
      "",
      "Revisa los campos de configuración. Utiliza este prompt siguiendo el mismo procedimiento que funcionó en los retos anteriores.",
      "",
      "Archivos requeridos:",
      "",
      "FUENTE:",
      "",
      "MCP365_P03_Fuente_transcripcion_Teams_Proyecto_Horizonte.docx",
      "",
      "PLANTILLA:",
      "",
      "MCP365_P03_Matriz_compromisos_reunion.docx",
      "",
      "ENTREGABLE:",
      "",
      "MCP365_P03_Matriz_compromisos_completada.docx",
      "",
      "La lista de propuestas no aprobadas debe quedar incluida dentro de la sección 2 de la matriz. No debe generarse como un documento separado.",
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
      "REUNIÓN O CASO",
      "",
      bracket(f.reunion),
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
      "CAMPOS AUTORIZADOS EN “1. DATOS DE LA REUNIÓN”",
      "",
      bracket("\n" + (f.sec1 || "") + "\n"),
      "",
      "FILAS AUTORIZADAS EN “2. CLASIFICACIÓN DE LA CONVERSACIÓN”",
      "",
      bracket("\n" + (f.sec2 || "") + "\n"),
      "",
      "CAMPOS AUTORIZADOS EN “3. MATRIZ DE COMPROMISOS”",
      "",
      bracket("\n" + (f.sec3 || "") + "\n"),
      "",
      "CAMPOS AUTORIZADOS EN “4. PRÓXIMA AGENDA”",
      "",
      bracket("\n" + (f.sec4 || "") + "\n"),
      "",
      "CAMPO AUTORIZADO EN “5. RESUMEN PARA DIFUSIÓN”",
      "",
      bracket(f.sec5),
      "",
      "CAMPOS O SECCIONES QUE DEBEN QUEDAR SIN COMPLETAR",
      "",
      bracket("\n" + (f.restringidos || "") + "\n"),
      "",
      "RESPUESTA CUANDO FALTE UN DATO DE UN COMPROMISO REAL",
      "",
      bracket(f.vacio),
      "",
      "TRATAMIENTO DE FILAS NO UTILIZADAS",
      "",
      bracket(f.filas_vacias),
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
      "ACTÚA EN MODO EDICIÓN DE PLANTILLA WORD (.docx REAL).",
      "",
      "Analiza exclusivamente la transcripción indicada y completa una copia editable de la plantilla oficial.",
      "",
      "No reconstruyas la matriz desde una representación textual.",
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
      "“No puedo completar la matriz conservando su formato. No generaré un documento alternativo.”",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "3. TAREA",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "1. Crea una copia de la plantilla oficial.",
      "2. Analiza la transcripción completa, desde el inicio hasta el cierre.",
      "3. Identifica a los participantes y conserva sus nombres tal como aparecen.",
      "4. Completa los datos de la reunión.",
      "5. Clasifica la conversación.",
      "6. Elabora dentro de la sección 2 una lista de propuestas no aprobadas.",
      "7. Completa la matriz únicamente con compromisos verificables.",
      "8. Propón la próxima agenda utilizando asuntos pendientes de la reunión.",
      "9. Redacta el resumen para difusión.",
      "10. Guarda la copia con el nombre definido en la configuración.",
      "",
      "Trabaja sección por sección dentro del mismo documento.",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "4. REGLAS PARA CLASIFICAR LA CONVERSACIÓN",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "DECISIONES CONFIRMADAS",
      "",
      "Registra una decisión únicamente cuando la transcripción contenga una confirmación explícita, por ejemplo:",
      "",
      "* “Queda decidido”.",
      "* “Aprobamos”.",
      "* “Se autoriza”.",
      "* “Se confirma”.",
      "* Una aceptación expresa equivalente.",
      "",
      "No conviertas una propuesta, recomendación o posibilidad en una decisión.",
      "",
      "Para cada decisión incluye:",
      "",
      "* Decisión breve.",
      "* Persona que la confirmó.",
      "* Marca de tiempo.",
      "* Evidencia breve.",
      "",
      "Marca la opción “Cerrada” solamente cuando la decisión esté confirmada.",
      "",
      "PROPUESTAS NO APROBADAS",
      "",
      "Incluye todas las propuestas que:",
      "",
      "* Fueron sugeridas, pero no aprobadas.",
      "* Quedaron condicionadas a permisos, accesos o confirmaciones.",
      "* Se conservaron como fecha o alternativa tentativa.",
      "* Requieren una aprobación posterior.",
      "* Fueron discutidas, pero no autorizadas definitivamente.",
      "",
      "Utiliza una lista numerada dentro de la celda.",
      "",
      "Para cada propuesta registra:",
      "",
      "1. Propuesta.",
      "2. Persona que la presentó.",
      "3. Motivo por el que no está aprobada.",
      "4. Estado o condición pendiente.",
      "5. Evidencia con marca de tiempo.",
      "",
      "No incluyas como “no aprobada” una actividad que sí recibió aprobación expresa.",
      "",
      "Si se aprobó preparar un borrador, pero no distribuirlo, diferencia claramente:",
      "",
      "* La preparación aprobada.",
      "* La distribución todavía no aprobada.",
      "",
      "Marca la opción “Abierta” cuando existan propuestas pendientes de aprobación.",
      "",
      "OPINIONES O PREOCUPACIONES",
      "",
      "Registra como opinión o preocupación:",
      "",
      "* Recomendaciones personales o técnicas.",
      "* Expresiones como “me preocupa”, “preferiría” o “me parece”.",
      "* Riesgos mencionados sin que constituyan una decisión.",
      "* Condiciones técnicas señaladas durante la conversación.",
      "",
      "No conviertas una recomendación técnica en compromiso.",
      "",
      "Marca la opción “Registrada”.",
      "",
      "PREGUNTAS SIN RESOLVER",
      "",
      "Incluye preguntas o asuntos para los cuales la transcripción indique:",
      "",
      "* No se conoce la respuesta.",
      "* No está definido.",
      "* Está pendiente de confirmación.",
      "* No se ha identificado al responsable.",
      "* No existe fecha de respuesta.",
      "* Depende de una autorización posterior.",
      "",
      "Marca la opción “Pendiente”.",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "5. REGLAS PARA LA MATRIZ DE COMPROMISOS",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "Registra únicamente compromisos que tengan una acción asignada o aceptada expresamente.",
      "",
      "Una propuesta, recomendación, preocupación o pregunta no constituye por sí sola un compromiso.",
      "",
      "ACTIVIDAD",
      "",
      "* Redacta una acción concreta.",
      "* Comienza con un verbo en infinitivo.",
      "* No combines varias actividades diferentes en una misma fila.",
      "",
      "RESPONSABLE",
      "",
      "* Registra solamente a la persona o área asignada explícitamente.",
      "* No deduzcas responsables por su cargo o participación.",
      "* Si existe el compromiso, pero el responsable no fue definido, escribe “No especificado”.",
      "",
      "FECHA LÍMITE",
      "",
      "* Copia la fecha exacta mencionada.",
      "* Diferencia una fecha límite de una fecha tentativa.",
      "* Si no hay fecha asignada, escribe “No especificado”.",
      "* No calcules fechas por cuenta propia.",
      "",
      "DEPENDENCIA",
      "",
      "Registra las condiciones que deben cumplirse antes de ejecutar el compromiso, por ejemplo:",
      "",
      "* Permiso.",
      "* Autorización.",
      "* Acceso.",
      "* Confirmación de inventario.",
      "* Información de otra área.",
      "* Aprobación de una comunicación.",
      "",
      "Incluye únicamente dependencias mencionadas en la transcripción.",
      "",
      "Si no existe una dependencia explícita, escribe “No especificado”.",
      "",
      "ESTADO",
      "",
      "Marca una sola opción:",
      "",
      "* Pendiente.",
      "* En curso.",
      "* Hecho.",
      "",
      "Utiliza “Hecho” solamente cuando la transcripción confirme que la actividad fue completada.",
      "",
      "Utiliza “En curso” solamente cuando la fuente indique que la actividad ya comenzó.",
      "",
      "Cuando se asigne o acepte un compromiso, pero no se confirme su cumplimiento, marca “Pendiente”.",
      "",
      "EVIDENCIA O ENTREGABLE",
      "",
      "Incluye:",
      "",
      "* Entregable esperado.",
      "* Persona que asumió o asignó el compromiso.",
      "* Marca de tiempo.",
      "* Cita breve o referencia precisa.",
      "",
      "Ejemplo de estructura:",
      "",
      "Entregable: [resultado esperado] · Evidencia: [participante] · [marca de tiempo] · “[cita breve]”",
      "",
      "VALIDADO POR",
      "",
      "Deja completamente vacías las ocho celdas de la columna “Validado por”.",
      "",
      "No escribas nombres, “Copilot”, “Pendiente” ni “No especificado”.",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "6. REGLAS PARA LA PRÓXIMA AGENDA",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "Utiliza únicamente:",
      "",
      "* Temas expresamente previstos para la siguiente reunión.",
      "* Preguntas sin resolver.",
      "* Dependencias pendientes.",
      "* Compromisos que deban revisarse posteriormente.",
      "",
      "Si el tema de agenda se deriva de un pendiente y no fue definido expresamente, comienza con:",
      "",
      "“Propuesta de agenda:”",
      "",
      "Registra como dueño únicamente a una persona asignada expresamente.",
      "",
      "Si no existe dueño identificado, escribe “No especificado”.",
      "",
      "No presentes una agenda propuesta como decisión confirmada.",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "7. RESUMEN PARA DIFUSIÓN",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "Redacta un resumen de máximo cinco líneas.",
      "",
      "Incluye:",
      "",
      "* Propósito de la reunión.",
      "* Principales decisiones confirmadas.",
      "* Compromisos más relevantes.",
      "* Dependencias o asuntos pendientes.",
      "* Fecha de la siguiente reunión, si está confirmada.",
      "",
      "No presentes propuestas abiertas como decisiones.",
      "",
      "No incluyas información técnica innecesaria.",
      "",
      "No incluyas datos inventados.",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "8. CONSERVACIÓN DE LA PLANTILLA",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "Mantén sin modificaciones:",
      "",
      "* Banner.",
      "* Título.",
      "* Subtítulo.",
      "* Chips o etiquetas.",
      "* Colores.",
      "* Tablas.",
      "* Bordes.",
      "* Tipografías.",
      "* Recuadros.",
      "* Numeración.",
      "* Encabezados de columnas.",
      "* Número de filas.",
      "* Número de columnas.",
      "* Texto institucional.",
      "* Control de calidad.",
      "* Firmas.",
      "",
      "Las filas pueden aumentar su altura si hace falta.",
      "",
      "No cambies el ancho de las columnas ni la composición.",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "9. PROHIBICIONES",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "* No crees un documento desde cero.",
      "* No reemplaces la plantilla por un documento nuevo.",
      "* No conviertas tablas en párrafos.",
      "* No utilices barras verticales para simular tablas.",
      "* No agregues compromisos implícitos.",
      "* No conviertas propuestas en decisiones.",
      "* No asignes responsables por inferencia.",
      "* No calcules fechas.",
      "* No escribas en “Validado por”.",
      "* No completes el control de calidad.",
      "* No marques sus casillas.",
      "* No completes las firmas.",
      "* No escribas el nombre del archivo como título.",
      "* No agregues conclusiones después del texto institucional.",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "10. VERIFICACIÓN OBLIGATORIA",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "Antes de guardar, confirma:",
      "",
      "1. Los datos de la reunión provienen de la transcripción.",
      "2. Las decisiones tienen confirmación explícita.",
      "3. Las propuestas no aprobadas aparecen en una lista separada dentro de la sección 2.",
      "4. Las propuestas no fueron presentadas como decisiones.",
      "5. Las opiniones no fueron convertidas en compromisos.",
      "6. Las preguntas abiertas siguen identificadas como pendientes.",
      "7. Cada compromiso tiene actividad, responsable, fecha, dependencia, estado y evidencia.",
      "8. Los datos faltantes de compromisos reales aparecen como “No especificado”.",
      "9. Las filas no utilizadas están vacías.",
      "10. Solo se marcó un estado por compromiso.",
      "11. La columna “Validado por” está completamente vacía.",
      "12. El control de calidad está completamente vacío.",
      "13. Sus casillas Sí y No permanecen sin marcar.",
      "14. Las firmas permanecen vacías.",
      "15. El documento conserva el formato original.",
      "16. El archivo final es un `.docx` real.",
      "",
      "Si alguna comprobación falla, corrige la copia antes de guardarla.",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "11. ENTREGA",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "Guarda y entrega la copia completa con el nombre:",
      "",
      "MCP365_P03_Matriz_compromisos_completada.docx",
      "",
      "El documento debe conservar el formato oficial e incluir:",
      "",
      "* Datos de la reunión.",
      "* Clasificación de la conversación.",
      "* Lista de propuestas no aprobadas.",
      "* Matriz de compromisos.",
      "* Próxima agenda.",
      "* Resumen para difusión.",
      "",
      "La validación humana, la columna “Validado por”, el control de calidad y las firmas deben permanecer vacíos.",
      "",
      "No entregues la lista de propuestas como un archivo independiente.",
      "",
      "No entregues únicamente un resumen o una tabla en el panel de Copilot."
    ].join("\n");
  }

'''

MARKER = "  /* ========== RETO ENGINE (patrón S1·R1 reutilizable; R1 no se remonta) ========== */"
WIRE_OLD = '    if (caseId === "r2") return buildPromptR2Text(getPromptR2Fields());'
WIRE_NEW = (
    '    if (caseId === "r2") return buildPromptR2Text(getPromptR2Fields());\n'
    '    if (caseId === "r3") return buildPromptR3Text(getPromptR3Fields());'
)

DOWNLOAD_OLD = '''    "matriz-compromisos": () => downloadWord("MCP365_P03_Matriz_compromisos_reunion.doc", "Matriz de compromisos post-reunión", "MCP-365-P03", "Teams + Word + Copilot", `
      <h2>1. Datos de la reunión</h2>
      <table class="data">
        <tr><th>Campo</th><th>Información</th></tr>
        <tr><td>Nombre / código de reunión</td><td></td></tr>
        <tr><td>Fecha y hora</td><td></td></tr>
        <tr><td>Facilitador</td><td></td></tr>
        <tr><td>Participantes</td><td></td></tr>
        <tr><td>Objetivo declarado</td><td></td></tr>
      </table>
      <h2>2. Clasificación de la conversación</h2>
      <table class="data">
        <tr><th>Tipo</th><th>Contenido (pega o resume con evidencia)</th><th>Estado</th></tr>
        <tr><td>Decisiones confirmadas</td><td></td><td>☐ Cerrada</td></tr>
        <tr><td>Propuestas no aprobadas</td><td></td><td>☐ Abierta</td></tr>
        <tr><td>Opiniones / preocupaciones</td><td></td><td>☐ Registrada</td></tr>
        <tr><td>Preguntas sin resolver</td><td></td><td>☐ Pendiente</td></tr>
      </table>
      <h2>3. Matriz de compromisos</h2>
      <table class="data">
        <tr><th>#</th><th>Actividad</th><th>Responsable</th><th>Fecha límite</th><th>Dependencia</th><th>Estado</th><th>Evidencia / entregable</th><th>Validado por</th></tr>
        <tr><td>1</td><td></td><td></td><td></td><td></td><td>☐ Pendiente ☐ En curso ☐ Hecho</td><td></td><td></td></tr>
        <tr><td>2</td><td></td><td></td><td></td><td></td><td>☐ Pendiente ☐ En curso ☐ Hecho</td><td></td><td></td></tr>
        <tr><td>3</td><td></td><td></td><td></td><td></td><td>☐ Pendiente ☐ En curso ☐ Hecho</td><td></td><td></td></tr>
        <tr><td>4</td><td></td><td></td><td></td><td></td><td>☐ Pendiente ☐ En curso ☐ Hecho</td><td></td><td></td></tr>
        <tr><td>5</td><td></td><td></td><td></td><td></td><td>☐ Pendiente ☐ En curso ☐ Hecho</td><td></td><td></td></tr>
        <tr><td>6</td><td></td><td></td><td></td><td></td><td>☐ Pendiente ☐ En curso ☐ Hecho</td><td></td><td></td></tr>
        <tr><td>7</td><td></td><td></td><td></td><td></td><td>☐ Pendiente ☐ En curso ☐ Hecho</td><td></td><td></td></tr>
        <tr><td>8</td><td></td><td></td><td></td><td></td><td>☐ Pendiente ☐ En curso ☐ Hecho</td><td></td><td></td></tr>
      </table>
      <h2>4. Próxima agenda</h2>
      <table class="data">
        <tr><th>Tema</th><th>Objetivo</th><th>Preparación requerida</th><th>Dueño</th></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
        <tr><td></td><td></td><td></td><td></td></tr>
      </table>
      <h2>5. Resumen para difusión (5 líneas)</h2>
      <div class="box"></div>`),'''

DOWNLOAD_NEW = '''    "matriz-fuente": () => downloadStaticFile(
      "planillas/MCP365_P03_Fuente_transcripcion_Teams_Proyecto_Horizonte.docx",
      "MCP365_P03_Fuente_transcripcion_Teams_Proyecto_Horizonte.docx"
    ),

    "matriz-compromisos": () => downloadStaticFile(
      "planillas/MCP365_P03_Matriz_compromisos_reunion.docx",
      "MCP365_P03_Matriz_compromisos_reunion.docx"
    ),'''

TEMPLATES_OLD = '    { name: "Matriz de compromisos", desc: "Teams/Word · Decisiones, tareas y próxima agenda", key: "matriz-compromisos", type: "Word" },'
TEMPLATES_NEW = '''    { name: "Fuente transcripción Horizonte", desc: "Word .docx · Transcripción Teams Proyecto Horizonte (solo lectura)", key: "matriz-fuente", type: "Word" },
    { name: "Matriz de compromisos", desc: "Word .docx · Datos, clasificación, matriz, agenda y difusión", key: "matriz-compromisos", type: "Word" },'''


def main():
    text = INDEX.read_text(encoding="utf-8")
    if "function buildPromptR3Text" in text:
        print("buildPromptR3Text already present — skip inject")
    else:
        if MARKER not in text:
            raise SystemExit("MARKER not found")
        text = text.replace(MARKER, FN + "\n" + MARKER, 1)
        print("Injected buildPromptR3Text")

    if WIRE_NEW.split("\n")[1] in text:
        print("Wire already present")
    elif WIRE_OLD not in text:
        raise SystemExit("WIRE_OLD not found")
    else:
        text = text.replace(WIRE_OLD, WIRE_NEW, 1)
        print("Wired r3 in buildPromptFromCase")

    if '"matriz-fuente"' in text and "downloadStaticFile(\n      \"planillas/MCP365_P03_Matriz" in text:
        print("Downloads already updated")
    elif DOWNLOAD_OLD not in text:
        # try softer match
        if "MCP365_P03_Matriz_compromisos_reunion.doc\"" in text and "downloadWord" in text:
            raise SystemExit("DOWNLOAD_OLD mismatch — check index.html matriz block")
        print("Downloads already static or missing old block")
    else:
        text = text.replace(DOWNLOAD_OLD, DOWNLOAD_NEW, 1)
        print("Updated matriz downloads to static .docx")

    if 'key: "matriz-fuente"' in text:
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
