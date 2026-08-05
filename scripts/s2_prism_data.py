# -*- coding: utf-8 -*-
"""Datos PRISM de la Sesión 2 (Proyecto Horizonte) para embeber en index.html."""

from __future__ import annotations

COMMON_FORMAT_BLOCK = """\
PRESENTA LA RESPUESTA COMO UN INFORME EJECUTIVO

Incluye, cuando sea pertinente:

1. PORTADA
   - Título del informe
   - Objetivo
   - Fecha (solo si aparece en las fuentes; si no, escribe PENDIENTE DE VALIDACIÓN)
   - Archivos analizados (nombres exactos)

2. RESUMEN EJECUTIVO
   - Máximo 250 palabras
   - Lenguaje para gerencia / comité

3. TABLERO EJECUTIVO
   - KPIs o indicadores clave
   - Semáforos de criticidad (🔴 Alto / 🟡 Medio / 🟢 Bajo)
   - Estado general del análisis

4. MATRICES Y TABLAS (Markdown)
   - Matrices de hallazgos, riesgos, dependencias, comparación o información pendiente según aplique
   - Preferir tablas Markdown; evitar párrafos largos sin estructura

5. CLASIFICACIONES
   Cada afirmación relevante debe etiquetarse como una de:
   - Hecho confirmado
   - Inferencia
   - Información pendiente
   - Recomendación

6. RIESGOS (si aplica)
   - Semáforo 🔴 / 🟡 / 🟢
   - Evidencia y fuente

7. RECOMENDACIONES
   Tabla con: Acción | Responsable sugerido (solo si aparece en fuentes; si no, rol sugerido + PENDIENTE DE VALIDACIÓN) | Prioridad | Justificación

8. CONCLUSIONES
   - Máximo 5

9. PRÓXIMOS PASOS
   - Ordenados y accionables

10. PREGUNTAS PARA EL CLIENTE
    - Preguntas abiertas de aclaración

11. VALIDACIÓN HUMANA
    - Qué debe verificar una persona antes de usar este resultado en un comité"""

COMMON_VALIDATION_BLOCK = """\
Antes de responder:
1. Verifica que toda afirmación tenga evidencia en las fuentes autorizadas.
2. Indica explícitamente cuando una conclusión sea una Inferencia.
3. No inventes cifras.
4. No inventes fechas.
5. No inventes responsables.
6. No inventes decisiones ni apruebes el proyecto.
7. Marca toda información faltante como «PENDIENTE DE VALIDACIÓN».
8. No uses Power Automate, listas de SharePoint ni botones de Copilot dentro de Word/Excel/PowerPoint.
9. Trabaja solo con Microsoft 365 Copilot Chat (y Copilot en Outlook cuando el ejercicio sea de correo)."""

_MEJORA_HINTS = [
    "¿Qué información faltó en el prompt o en la respuesta?",
    "¿Qué información sobró o generó ruido?",
    "¿Qué podría especificarse mejor (rol, fuentes, entregables)?",
    "¿Cómo reducirías la ambigüedad del prompt?",
    "¿Qué formato faltó (tablas, matrices, semáforos, portada)?",
    "¿Cómo controlarías las alucinaciones (evidencia, clasificaciones, restricciones)?",
    "¿Qué restricciones adicionales agregarías?",
]


def _prism_prompt(
    *,
    persona: str,
    realidad: str,
    informacion: str,
    solicitud: str,
    metodo: str,
    expert_extra: str = "",
) -> str:
    """Construye un prompt PRISM completo (nivel 3 o 4)."""
    parts = [
        "P → PERSONA",
        persona.strip(),
        "",
        "R → REALIDAD",
        realidad.strip(),
        "",
        "I → INFORMACIÓN",
        informacion.strip(),
        "",
        "S → SOLICITUD",
        solicitud.strip(),
        "",
        "M → MÉTODO",
        metodo.strip(),
    ]
    if expert_extra.strip():
        parts.extend(["", expert_extra.strip()])
    parts.extend(
        [
            "",
            COMMON_VALIDATION_BLOCK,
            "",
            COMMON_FORMAT_BLOCK,
        ]
    )
    return "\n".join(parts)


S2_PRISM = {
    "f0": {
        "title": "Prepara tu espacio de trabajo",
        "file": "Kit Proyecto Horizonte (archivos 01–07) · Microsoft 365 Copilot Chat",
        "persona": "Analista de PMO / facilitador de análisis documental",
        "levels": {
            "1": {
                "label": "Básico",
                "text": "Dime qué archivos tengo cargados.",
            },
            "2": {
                "label": "Mejorado",
                "text": (
                    "Confirma los archivos del Proyecto Horizonte que puedes ver en esta conversación "
                    "y resume en una línea el propósito aparente de cada uno."
                ),
            },
            "3": {
                "label": "Profesional (PRISM)",
                "text": _prism_prompt(
                    persona=(
                        "Actúa como analista senior de una oficina de gestión de proyectos (PMO) "
                        "especializado en preparación de espacios de trabajo para análisis multiarchivo "
                        "con Microsoft 365 Copilot Chat."
                    ),
                    realidad=(
                        "Estamos iniciando la revisión académica del Proyecto Horizonte "
                        "(modernización de infraestructura energética urbana, datos ficticios). "
                        "Antes de analizar contenido, necesitamos verificar que Copilot reconozca "
                        "correctamente los archivos autorizados y sus limitaciones. "
                        "El proyecto NO está aprobado; solo se prepara el entorno de análisis."
                    ),
                    informacion=(
                        "Fuentes autorizadas (usar nombres exactos si están cargados):\n"
                        "- 01_Correo_Solicitud_Proyecto_Horizonte (Outlook / PDF de referencia)\n"
                        "- 02_Alcance_Proyecto_Horizonte.docx\n"
                        "- 03_Presupuesto_y_Cronograma_Horizonte.xlsx\n"
                        "- 04_Transcripcion_Reunion_Horizonte.docx\n"
                        "- 05_Registro_Inicial_Riesgos_Horizonte.xlsx\n"
                        "- 06_Comentarios_Interesados_Horizonte.docx\n"
                        "- 07_Plantilla_Comite_Horizonte.pptx\n\n"
                        "No uses documentos externos ni conocimiento general del sector para completar vacíos. "
                        "Si un archivo no está visible, indícalo como PENDIENTE DE VALIDACIÓN / no disponible en la sesión."
                    ),
                    solicitud=(
                        "Realiza un reconocimiento previo (sin recomendaciones de negocio):\n"
                        "1) Lista los archivos que efectivamente reconoces en esta conversación.\n"
                        "2) Para cada uno: nombre exacto, tipo, propósito aparente, secciones o hojas visibles.\n"
                        "3) Señala limitaciones (ilegibilidad, tablas ambiguas, multiarchivo incompleto).\n"
                        "4) Propón el orden óptimo de análisis (correo → alcance → presupuesto → transcripción → riesgos → comentarios → presentación).\n"
                        "5) Indica qué NO debes hacer todavía (no inventar cifras, no aprobar el proyecto, no generar el comité)."
                    ),
                    metodo=(
                        "Organiza la salida como informe breve de preparación.\n"
                        "Incluye una tabla Markdown: Archivo | Visible (Sí/No) | Propósito aparente | Limitación | Listo para análisis.\n"
                        "Clasifica cada observación como Hecho confirmado / Inferencia / Información pendiente.\n"
                        "Cierra con checklist de validación humana antes de pasar a la Fase 1."
                    ),
                ),
            },
            "4": {
                "label": "Experto",
                "text": _prism_prompt(
                    persona=(
                        "Actúa como consultor senior de PMO de una firma internacional, "
                        "responsable de asegurar la trazabilidad documental antes de un comité directivo."
                    ),
                    realidad=(
                        "El equipo debe dejar evidencia de que el entorno de Copilot Chat está listo "
                        "para el caso Proyecto Horizonte. La gerencia exige un «acta de reconocimiento "
                        "de fuentes» que demuestre control de alucinaciones desde el minuto cero."
                    ),
                    informacion=(
                        "Solo las fuentes del kit Horizonte con nombres exactos "
                        "(02_Alcance_Proyecto_Horizonte.docx, 03_Presupuesto_y_Cronograma_Horizonte.xlsx, "
                        "04_Transcripcion_Reunion_Horizonte.docx, 05_Registro_Inicial_Riesgos_Horizonte.xlsx, "
                        "06_Comentarios_Interesados_Horizonte.docx, 07_Plantilla_Comite_Horizonte.pptx "
                        "y el correo 01). Sin Power Automate ni SharePoint."
                    ),
                    solicitud=(
                        "Entrega un Acta Ejecutiva de Reconocimiento de Fuentes lista para archivo en el expediente del caso, "
                        "incluyendo: inventario de archivos, estado de carga, riesgos de interpretación multiarchivo, "
                        "plan de análisis por fases, y criterios de rechazo de respuestas de Copilot (alucinación, "
                        "mezcla de fuentes, cifras no trazables)."
                    ),
                    metodo=(
                        "Formato de acta ejecutiva con portada, tablero (listo / parcial / bloqueado), "
                        "matriz de fuentes, matriz de riesgos de proceso (no del proyecto aún), "
                        "próximos pasos y preguntas al instructor si faltan archivos."
                    ),
                    expert_extra=(
                        "ENTREGABLE PARA GERENCIA: el documento debe poder firmarse conceptualmente "
                        "como «entorno validado para iniciar análisis» sin afirmar que el Proyecto Horizonte está aprobado."
                    ),
                ),
            },
        },
        "explain": {
            "persona": "Define a Copilot como analista/consultor de PMO, no como asistente genérico.",
            "realidad": "Aclara que es preparación del entorno del caso Horizonte, sin aprobación del proyecto.",
            "informacion": "Fija el inventario exacto de archivos autorizados y qué hacer si faltan.",
            "solicitud": "Pide reconocimiento y orden de trabajo, no análisis de negocio todavía.",
            "metodo": "Exige tablas, clasificaciones y checklist antes de la Fase 1.",
            "restricciones": "Prohíbe inventar, usar fuentes externas y automatizaciones fuera de alcance.",
            "formato": "Informe ejecutivo / acta de reconocimiento con tablero y matrices.",
            "validacion": "La persona confirma que cada archivo visible coincide con el kit oficial.",
        },
        "compare": (
            "El nivel 1 solo pregunta «qué archivos hay» y deja ambigüedad; el nivel 3 (PRISM) fija persona, "
            "inventario exacto, límites y formato, lo que reduce alucinaciones y mezclas de fuentes."
        ),
        "improveHints": list(_MEJORA_HINTS),
    },
    "f1": {
        "title": "Comprender el correo",
        "file": "Correo Outlook / 01_Correo_Solicitud_Proyecto_Horizonte",
        "persona": "Analista senior de proyectos / consultor de PMO",
        "levels": {
            "1": {
                "label": "Básico",
                "text": "Resume este correo.",
            },
            "2": {
                "label": "Mejorado",
                "text": (
                    "Resume este correo del Proyecto Horizonte e identifica los archivos recibidos, "
                    "los entregables solicitados por el comité y las restricciones explícitas "
                    "(por ejemplo, no asumir que el proyecto está aprobado)."
                ),
            },
            "3": {
                "label": "Profesional (PRISM)",
                "text": _prism_prompt(
                    persona=(
                        "Actúa como analista senior de proyectos y consultor de PMO con experiencia "
                        "en intake de solicitudes ejecutivas y preparación de paquetes para comité."
                    ),
                    realidad=(
                        "Has recibido un correo de Laura Méndez (Dirección de Infraestructura) con asunto "
                        "«SOLICITUD DE ANÁLISIS | Proyecto Horizonte». Se trata de una revisión inicial "
                        "de modernización de infraestructura energética urbana. El comité aún no ha aprobado "
                        "la iniciativa. Debes comprender la solicitud sin ampliar el alcance ni inventar contexto."
                    ),
                    informacion=(
                        "Fuente única autorizada: el correo seleccionado "
                        "(01_Correo_Solicitud_Proyecto_Horizonte / mensaje en Outlook).\n"
                        "Los adjuntos se mencionan en el correo; no analices todavía el contenido de:\n"
                        "02_Alcance_Proyecto_Horizonte.docx, "
                        "03_Presupuesto_y_Cronograma_Horizonte.xlsx, "
                        "04_Transcripcion_Reunion_Horizonte.docx, "
                        "05_Registro_Inicial_Riesgos_Horizonte.xlsx, "
                        "06_Comentarios_Interesados_Horizonte.docx, "
                        "07_Plantilla_Comite_Horizonte.pptx "
                        "salvo lo que el propio correo diga explícitamente sobre ellos.\n"
                        "No uses información externa."
                    ),
                    solicitud=(
                        "Identifica y entrega:\n"
                        "- Objetivo de la solicitud\n"
                        "- Proyecto mencionado\n"
                        "- Área / remitente solicitante\n"
                        "- Documentos adjuntos o referidos\n"
                        "- Entregables requeridos por el comité\n"
                        "- Restricciones expresas\n"
                        "- Acciones solicitadas\n"
                        "- Información faltante en el correo\n"
                        "- Decisiones que NO deben asumirse\n"
                        "- Riesgos de interpretación del mensaje\n"
                        "- Lista de tareas para el equipo de análisis\n"
                        "- Cinco preguntas de aclaración para la solicitante"
                    ),
                    metodo=(
                        "Diferencia rigurosamente: Información explícita | Inferencia | No especificado.\n"
                        "Incluye: (1) tabla de análisis del correo, (2) lista de tareas priorizada, "
                        "(3) cinco preguntas de aclaración, (4) resumen ejecutivo ≤120 palabras dentro del bloque de 250 del informe, "
                        "(5) tablero con semáforo de claridad de la solicitud."
                    ),
                ),
            },
            "4": {
                "label": "Experto",
                "text": _prism_prompt(
                    persona=(
                        "Actúa como socio consultor de PMO que prepara el briefing de arranque "
                        "para la gerencia de proyectos antes de abrir los adjuntos."
                    ),
                    realidad=(
                        "La Dirección de Infraestructura solicitó la revisión inicial del Proyecto Horizonte. "
                        "Gerencia necesita un briefing de intake listo para comité: qué se pidió, qué se entregará, "
                        "qué queda fuera y qué riesgos de malinterpretación existen si se empieza a analizar sin orden."
                    ),
                    informacion=(
                        "Solo el correo 01_Correo_Solicitud_Proyecto_Horizonte. "
                        "Referencia los nombres de adjuntos exactamente como aparecen o se listan en el mensaje; "
                        "no extraigas cifras de otros archivos en esta fase."
                    ),
                    solicitud=(
                        "Produce un Briefing de Intake Ejecutivo (1–2 páginas equivalentes) que incluya: "
                        "mapa de entregables vs. adjuntos, matriz RACI preliminar solo con roles explícitos en el correo "
                        "(si no hay responsables, PENDIENTE DE VALIDACIÓN), riesgos de interpretación, "
                        "plan de lectura de archivos en orden, y decisiones que el equipo NO puede tomar aún."
                    ),
                    metodo=(
                        "Informe ejecutivo completo con portada «Briefing de Intake – Proyecto Horizonte», "
                        "tablero de claridad de la solicitud, matriz entregable–fuente, "
                        "recomendaciones de gobernanza del análisis y preguntas para Laura Méndez."
                    ),
                    expert_extra=(
                        "ENTREGABLE PARA GERENCIA/COMITÉ: tono formal, sin jerga técnica innecesaria, "
                        "sin afirmar aprobación del proyecto, listo para reenviarse como pre-read."
                    ),
                ),
            },
        },
        "explain": {
            "persona": "Analista senior / consultor PMO orientado a intake ejecutivo.",
            "realidad": "Solicitud de Laura Méndez; revisión inicial; proyecto no aprobado.",
            "informacion": "Solo el correo; adjuntos se listan pero no se profundizan aún.",
            "solicitud": "Objetivo, adjuntos, entregables, restricciones, tareas y preguntas.",
            "metodo": "Tablas, clasificación explícito/inferencia/no especificado, resumen acotado.",
            "restricciones": "No inventar ni usar fuentes externas; no asumir aprobación.",
            "formato": "Informe ejecutivo con tablero y matrices Markdown.",
            "validacion": "Contrastar cada hallazgo línea por línea con el correo original.",
        },
        "compare": (
            "El nivel 1 («Resume este correo») produce texto vago; el profesional PRISM obliga a separar "
            "hechos, inferencias y faltantes, y fija entregables, lo que reduce ambigüedad y alucinaciones."
        ),
        "improveHints": list(_MEJORA_HINTS),
    },
    "f2": {
        "title": "Analizar alcance",
        "file": "02_Alcance_Proyecto_Horizonte.docx",
        "persona": "Consultor senior en estructuración de proyectos",
        "levels": {
            "1": {
                "label": "Básico",
                "text": "Resume el documento de alcance.",
            },
            "2": {
                "label": "Mejorado",
                "text": (
                    "Analiza el archivo 02_Alcance_Proyecto_Horizonte.docx y resume objetivo, "
                    "alcance incluido, exclusiones, entregables e información que falte."
                ),
            },
            "3": {
                "label": "Profesional (PRISM)",
                "text": _prism_prompt(
                    persona=(
                        "Actúa como consultor senior en estructuración de proyectos de infraestructura energética, "
                        "experto en WBS conceptual, exclusiones y criterios de aceptación."
                    ),
                    realidad=(
                        "El Proyecto Horizonte se encuentra en fase de revisión preliminar. "
                        "El documento de alcance es un borrador académico ficticio. "
                        "Debes estructurar el alcance para el comité sin completar vacíos con supuestos no escritos "
                        "y sin tratar el documento como aprobación formal."
                    ),
                    informacion=(
                        "Fuente exclusiva: 02_Alcance_Proyecto_Horizonte.docx.\n"
                        "No uses 03_Presupuesto_y_Cronograma_Horizonte.xlsx, "
                        "04_Transcripcion_Reunion_Horizonte.docx ni otros archivos en esta fase, "
                        "salvo para marcar como PENDIENTE DE VALIDACIÓN cualquier cruce que requieras más adelante.\n"
                        "No completes vacíos con información inventada."
                    ),
                    solicitud=(
                        "Identifica con evidencia:\n"
                        "necesidad que origina el proyecto; objetivo general; objetivos específicos; "
                        "alcance incluido; exclusiones; entregables; hitos; restricciones; supuestos; "
                        "dependencias; interesados; requisitos técnicos; requisitos de seguridad; "
                        "consideraciones ambientales; necesidades de comunicación; criterios de aceptación; "
                        "información faltante.\n"
                        "Para cada hallazgo: Elemento | Evidencia | Sección/fragmento | "
                        "Clasificación (explícito / inferido / no especificado) | Validación requerida.\n"
                        "Después entrega: 10 preguntas de validación; 5 riesgos iniciales; "
                        "3 posibles contradicciones internas; resumen ejecutivo ≤200 palabras."
                    ),
                    metodo=(
                        "Primero un prompt mental de reconocimiento (propósito y secciones), luego el análisis.\n"
                        "Usa matrices Markdown de alcance, exclusiones y faltantes.\n"
                        "Semáforos de madurez del alcance (🔴/🟡/🟢).\n"
                        "No conviertas supuestos en hechos."
                    ),
                ),
            },
            "4": {
                "label": "Experto",
                "text": _prism_prompt(
                    persona=(
                        "Actúa como socio de consultoría en definición de alcance (scope baseline) "
                        "que presenta a gerencia un dictamen de madurez documental."
                    ),
                    realidad=(
                        "Gerencia necesita saber si el alcance de Horizonte está listo para discusión de comité "
                        "o si hay huecos críticos (exclusiones ambiguas, criterios de aceptación débiles, "
                        "interesados incompletos) que impiden decidir."
                    ),
                    informacion=(
                        "Únicamente 02_Alcance_Proyecto_Horizonte.docx. "
                        "Cita secciones o fragmentos. Sin cifras de presupuesto ni fechas de Excel."
                    ),
                    solicitud=(
                        "Entrega un Dictamen Ejecutivo de Madurez de Alcance: scorecard de madurez por dimensión, "
                        "mapa incluido/excluido, lista de «no negociables» explícitos vs. ambigüedades, "
                        "riesgos de scope creep, y recomendaciones priorizadas para cerrar vacíos antes del comité."
                    ),
                    metodo=(
                        "Informe ejecutivo con portada, tablero de madurez, matrices, "
                        "clasificaciones Hecho/Inferencia/Pendiente/Recomendación, "
                        "máximo 5 conclusiones y preguntas para el cliente."
                    ),
                    expert_extra=(
                        "ENTREGABLE PARA GERENCIA: debe poder usarse como anexo del paquete de comité "
                        "sin reescribir; marca todo lo no evidenciado como PENDIENTE DE VALIDACIÓN."
                    ),
                ),
            },
        },
        "explain": {
            "persona": "Consultor senior de estructuración / scope.",
            "realidad": "Borrador preliminar; no hay aprobación; evitar scope creep por inventiva.",
            "informacion": "Solo 02_Alcance_Proyecto_Horizonte.docx.",
            "solicitud": "Desglose completo de alcance + preguntas, riesgos y contradicciones.",
            "metodo": "Matriz por hallazgo con evidencia y clasificación.",
            "restricciones": "No inventar; no cruzar aún con Excel/transcripción.",
            "formato": "Informe ejecutivo con scorecard y tablas Markdown.",
            "validacion": "Cada ítem debe poder señalarse en el Word original.",
        },
        "compare": (
            "El básico pide un resumen narrativo; el PRISM obliga evidencia por sección y clasificación "
            "explícito/inferido/faltante, reduciendo alucinaciones de alcance."
        ),
        "improveHints": list(_MEJORA_HINTS),
    },
    "f3": {
        "title": "Presupuesto y cronograma",
        "file": "03_Presupuesto_y_Cronograma_Horizonte.xlsx",
        "persona": "Analista financiero y de planificación de proyectos",
        "levels": {
            "1": {
                "label": "Básico",
                "text": "Analiza este Excel de presupuesto.",
            },
            "2": {
                "label": "Mejorado",
                "text": (
                    "Analiza 03_Presupuesto_y_Cronograma_Horizonte.xlsx: calcula el total, "
                    "señala las partidas más altas, revisa fechas del cronograma y marca "
                    "celdas vacías o datos dudosos. Advierte que debo validar en Excel."
                ),
            },
            "3": {
                "label": "Profesional (PRISM)",
                "text": _prism_prompt(
                    persona=(
                        "Actúa como analista financiero y de planificación de proyectos (cost & schedule) "
                        "con experiencia en auditorías preliminares de libros Excel de proyectos energéticos."
                    ),
                    realidad=(
                        "El comité requiere hallazgos presupuestales y de cronograma del Proyecto Horizonte. "
                        "Copilot puede interpretar mal las tablas: todo cálculo es preliminar hasta validación humana en Excel. "
                        "No modifiques el archivo."
                    ),
                    informacion=(
                        "Fuente exclusiva: 03_Presupuesto_y_Cronograma_Horizonte.xlsx.\n"
                        "No inventes hojas, columnas ni valores. Si no puedes leer una celda, marca PENDIENTE DE VALIDACIÓN.\n"
                        "No uses 02_Alcance_Proyecto_Horizonte.docx ni otras fuentes para «completar» cifras."
                    ),
                    solicitud=(
                        "Antes de conclusiones: identifica hojas; describe columnas; indica qué datos son analizables; "
                        "señala limitaciones del archivo.\n"
                        "Luego: presupuesto total; participación % por categoría; tres partidas más altas; "
                        "valores vacíos/duplicados/atípicos; comparación actividades–fechas–costos; "
                        "actividades críticas; posibles desviaciones; dependencias; riesgos presupuestales; "
                        "riesgos de cronograma; datos que requieren validación.\n"
                        "Diferencia: Datos originales | Cálculos | Interpretaciones | Recomendaciones."
                    ),
                    metodo=(
                        "Entrega: resumen ejecutivo; tabla de análisis presupuestal; tabla de cronograma; "
                        "lista de inconsistencias; 5 preguntas de validación; 5 recomendaciones preliminares.\n"
                        "Incluye tablero con semáforos de calidad de datos y criticidad de partidas.\n"
                        "Indica explícitamente: «Validar cada cifra abriendo el Excel»."
                    ),
                ),
            },
            "4": {
                "label": "Experto",
                "text": _prism_prompt(
                    persona=(
                        "Actúa como controller de proyectos / socio de assurance financiera "
                        "que presenta un memorando de hallazgos de costo y tiempo a gerencia."
                    ),
                    realidad=(
                        "Gerencia quiere un paquete listo para comité: totales, concentraciones de gasto, "
                        "presión de cronograma y puntos ciegos del Excel, sin tratar los números de Copilot "
                        "como auditados."
                    ),
                    informacion=(
                        "Solo 03_Presupuesto_y_Cronograma_Horizonte.xlsx. "
                        "Toda cifra debe etiquetarse como leída / calculada / no verificable en esta sesión."
                    ),
                    solicitud=(
                        "Produce un Memorando Ejecutivo de Costos y Cronograma: "
                        "tablero de KPIs (total, top 3 partidas, ventana temporal, % datos incompletos), "
                        "matriz de hallazgos con impacto 🔴🟡🟢, inconsistencias, "
                        "preguntas al dueño del presupuesto y plan de validación en Excel "
                        "(checklist: total, mayor partida, fecha inicial, fecha final, Nº actividades, vacíos, duplicados)."
                    ),
                    metodo=(
                        "Informe ejecutivo formal; tablas Markdown; no modificar el archivo; "
                        "cerrar con «limitación de assurance»: Copilot ≠ validación contable."
                    ),
                    expert_extra=(
                        "ENTREGABLE PARA GERENCIA: tono de memorando de auditoría preliminar; "
                        "ninguna recomendación debe inventar responsables nominados si no aparecen en el Excel."
                    ),
                ),
            },
        },
        "explain": {
            "persona": "Analista financiero y de planificación (cost & schedule).",
            "realidad": "Hallazgos para comité; cálculos preliminares; validación obligatoria en Excel.",
            "informacion": "Solo 03_Presupuesto_y_Cronograma_Horizonte.xlsx.",
            "solicitud": "Totales, concentraciones, calidad de datos, riesgos de costo/tiempo.",
            "metodo": "Separar datos, cálculos, interpretaciones y recomendaciones.",
            "restricciones": "No modificar el archivo; no inventar celdas; no cruzar aún con otras fuentes.",
            "formato": "Informe ejecutivo con tablas presupuestales y de cronograma.",
            "validacion": "Abrir Excel y verificar total, partidas, fechas y anomalías.",
        },
        "compare": (
            "El básico pide «analiza el Excel» sin método; el PRISM fuerza inventario de hojas, "
            "separación dato/cálculo/inferencia y validación humana, cortando alucinaciones numéricas."
        ),
        "improveHints": list(_MEJORA_HINTS),
    },
    "f4": {
        "title": "Transcripción de la reunión",
        "file": "04_Transcripcion_Reunion_Horizonte.docx",
        "persona": "Secretario técnico de un comité de proyectos",
        "levels": {
            "1": {
                "label": "Básico",
                "text": "Resume la reunión.",
            },
            "2": {
                "label": "Mejorado",
                "text": (
                    "A partir de 04_Transcripcion_Reunion_Horizonte.docx, resume la reunión, "
                    "lista compromisos, decisiones y temas pendientes. No conviertas propuestas en decisiones."
                ),
            },
            "3": {
                "label": "Profesional (PRISM)",
                "text": _prism_prompt(
                    persona=(
                        "Actúa como secretario técnico de un comité de proyectos, "
                        "especializado en actas con trazabilidad legal-operativa (sin inventar acuerdos)."
                    ),
                    realidad=(
                        "Existe una transcripción de la reunión inicial del Proyecto Horizonte. "
                        "El riesgo principal es convertir opiniones o propuestas en decisiones confirmadas. "
                        "El proyecto sigue sin aprobación formal."
                    ),
                    informacion=(
                        "Fuente exclusiva: 04_Transcripcion_Reunion_Horizonte.docx.\n"
                        "No asignes responsables ni fechas que no aparezcan expresamente.\n"
                        "Si falta un dato, escribe «No especificado» o PENDIENTE DE VALIDACIÓN.\n"
                        "No uses el Excel ni el alcance para «corregir» lo dicho en la reunión en esta fase."
                    ),
                    solicitud=(
                        "Diferencia rigurosamente: decisiones confirmadas; propuestas; opiniones; preguntas; "
                        "preocupaciones; tareas asignadas; fechas confirmadas; fechas tentativas; "
                        "responsables confirmados; responsables sugeridos.\n"
                        "Entrega: (1) resumen de la reunión, (2) matriz de compromisos, (3) registro de decisiones, "
                        "(4) propuestas no aprobadas, (5) temas pendientes, (6) riesgos mencionados, "
                        "(7) agenda recomendada para la siguiente reunión."
                    ),
                    metodo=(
                        "Usa tablas Markdown con columnas: Ítem | Tipo | Evidencia (cita breve) | Responsable | Fecha | Clasificación.\n"
                        "Semáforo de certeza del compromiso (🔴 ambiguo / 🟡 parcial / 🟢 explícito).\n"
                        "Nunca conviertas una propuesta en decisión."
                    ),
                ),
            },
            "4": {
                "label": "Experto",
                "text": _prism_prompt(
                    persona=(
                        "Actúa como secretario general de comité / governance officer "
                        "que emite un extracto ejecutivo de la reunión para gerencia."
                    ),
                    realidad=(
                        "Gerencia no leerá la transcripción completa. Necesita un extracto confiable "
                        "que separe lo decidido de lo solo discutido, con riesgos citados y pendientes claros."
                    ),
                    informacion=(
                        "Solo 04_Transcripcion_Reunion_Horizonte.docx. Citas breves como evidencia. "
                        "Sin completar con 02/03/05/06."
                    ),
                    solicitud=(
                        "Emite un Extracto Ejecutivo de Comité (pre-read): "
                        "decisiones vs. no-decisiones, matriz de compromisos con gaps, "
                        "riesgos mencionados con semáforo, lista de información que la reunión dejó abierta, "
                        "y recomendaciones de gobernanza para la próxima sesión."
                    ),
                    metodo=(
                        "Informe ejecutivo con portada «Extracto – Reunión Horizonte», "
                        "tablero de certeza, matrices y máximo 5 conclusiones. "
                        "Incluye sección «Lo que NO se aprobó»."
                    ),
                    expert_extra=(
                        "ENTREGABLE PARA GERENCIA: listo para adjuntar al paquete de comité; "
                        "lenguaje neutro; cero nombres inventados."
                    ),
                ),
            },
        },
        "explain": {
            "persona": "Secretario técnico / governance de comité.",
            "realidad": "Reunión inicial; alto riesgo de malclasificar propuestas como decisiones.",
            "informacion": "Solo 04_Transcripcion_Reunion_Horizonte.docx.",
            "solicitud": "Resumen, compromisos, decisiones, pendientes, riesgos, agenda.",
            "metodo": "Matrices con tipo, evidencia y semáforo de certeza.",
            "restricciones": "No inventar responsables/fechas; no convertir propuesta en decisión.",
            "formato": "Informe / extracto ejecutivo con tablas Markdown.",
            "validacion": "Contrastar cada compromiso con la cita en la transcripción.",
        },
        "compare": (
            "El básico resume sin tipificar; el PRISM obliga a etiquetar decisión vs. propuesta y exigir evidencia, "
            "lo que reduce alucinaciones de acuerdos inexistentes."
        ),
        "improveHints": list(_MEJORA_HINTS),
    },
    "f5": {
        "title": "Comparar fuentes",
        "file": "02_Alcance · 03_Presupuesto · 04_Transcripción",
        "persona": "Auditor de consistencia documental de proyectos",
        "levels": {
            "1": {
                "label": "Básico",
                "text": "Compara estos tres archivos y dime las diferencias.",
            },
            "2": {
                "label": "Mejorado",
                "text": (
                    "Compara 02_Alcance_Proyecto_Horizonte.docx, "
                    "03_Presupuesto_y_Cronograma_Horizonte.xlsx y "
                    "04_Transcripcion_Reunion_Horizonte.docx. "
                    "Lista coincidencias, contradicciones y datos faltantes sin decidir cuál documento «tiene la razón»."
                ),
            },
            "3": {
                "label": "Profesional (PRISM)",
                "text": _prism_prompt(
                    persona=(
                        "Actúa como auditor de consistencia documental de proyectos "
                        "con enfoque en trazabilidad entre alcance, costo/tiempo y actas."
                    ),
                    realidad=(
                        "Las tres fuentes del Proyecto Horizonte pueden estar desalineadas por ser borradores "
                        "o por propuestas no aprobadas. Copilot no reemplaza el control de versiones. "
                        "Tu rol es detectar inconsistencias, no arbitrar la verdad sin evidencia."
                    ),
                    informacion=(
                        "Fuentes exclusivas:\n"
                        "- 02_Alcance_Proyecto_Horizonte.docx\n"
                        "- 03_Presupuesto_y_Cronograma_Horizonte.xlsx\n"
                        "- 04_Transcripcion_Reunion_Horizonte.docx\n"
                        "No uses 05_Registro_Inicial_Riesgos_Horizonte.xlsx ni "
                        "06_Comentarios_Interesados_Horizonte.docx en esta fase.\n"
                        "No inventes valores de conciliación."
                    ),
                    solicitud=(
                        "Identifica: datos coincidentes; contradictorios; fechas diferentes; montos diferentes; "
                        "responsables inconsistentes; entregables sin presupuesto; actividades sin responsable; "
                        "compromisos de la reunión que no aparecen en el alcance; riesgos mencionados en una sola fuente; "
                        "información faltante para decidir.\n"
                        "Por cada hallazgo: Tema | Archivo(s) | Evidencia | Tipo de inconsistencia | "
                        "Impacto potencial | Pregunta de validación | Prioridad."
                    ),
                    metodo=(
                        "Matriz comparativa Markdown y matriz de conflictos.\n"
                        "Semáforo de severidad 🔴🟡🟢.\n"
                        "Si dos fuentes chocan, registra la inconsistencia y formula pregunta; "
                        "no elijas «la verdad» sin evidencia suficiente.\n"
                        "Documenta qué versión usarías para comité solo como recomendación etiquetada."
                    ),
                ),
            },
            "4": {
                "label": "Experto",
                "text": _prism_prompt(
                    persona=(
                        "Actúa como socio de auditoría interna / quality assurance de proyectos "
                        "que emite un informe de alineación documental para el comité."
                    ),
                    realidad=(
                        "El comité necesita ver, en una sola vista, dónde chocan alcance, presupuesto/cronograma "
                        "y transcripción, y qué preguntas deben resolverse antes de cualquier decisión."
                    ),
                    informacion=(
                        "Solo los tres archivos: 02_Alcance_Proyecto_Horizonte.docx, "
                        "03_Presupuesto_y_Cronograma_Horizonte.xlsx, "
                        "04_Transcripcion_Reunion_Horizonte.docx."
                    ),
                    solicitud=(
                        "Emite un Informe de Alineación Documental Horizonte: "
                        "tablero de consistencia global, top 10 hallazgos priorizados, "
                        "mapa de impactos (alcance/costo/tiempo/gobernanza), "
                        "matriz de información pendiente y paquete de preguntas para el cliente."
                    ),
                    metodo=(
                        "Informe ejecutivo completo; sin adjudicar verdad sin evidencia; "
                        "recomendaciones orientadas a cerrar gaps, no a aprobar el proyecto."
                    ),
                    expert_extra=(
                        "ENTREGABLE PARA GERENCIA: anexo listo para comité con semáforos y preguntas abiertas."
                    ),
                ),
            },
        },
        "explain": {
            "persona": "Auditor de consistencia documental.",
            "realidad": "Borradores posiblemente desalineados; no arbitrar sin evidencia.",
            "informacion": "Solo 02, 03 y 04 con nombres exactos.",
            "solicitud": "Coincidencias, contradicciones, gaps y preguntas de validación.",
            "metodo": "Matrices comparativas y de conflictos con prioridad.",
            "restricciones": "No decidir cuál documento manda sin evidencia; no inventar conciliaciones.",
            "formato": "Informe ejecutivo de alineación con tablero y tablas.",
            "validacion": "Reabrir cada fuente y confirmar citas antes del comité.",
        },
        "compare": (
            "El básico pide «diferencias» sin método; el PRISM estructura evidencia por archivo e impacto, "
            "evitando que Copilot invente una versión «correcta»."
        ),
        "improveHints": list(_MEJORA_HINTS),
    },
    "f6": {
        "title": "Matriz de riesgos",
        "file": "02–06 (alcance, presupuesto, transcripción, riesgos, comentarios)",
        "persona": "Especialista en gestión de riesgos de proyectos del sector energético",
        "levels": {
            "1": {
                "label": "Básico",
                "text": "Hazme una lista de riesgos del proyecto.",
            },
            "2": {
                "label": "Mejorado",
                "text": (
                    "Con los archivos del Proyecto Horizonte (alcance, presupuesto, transcripción, "
                    "05_Registro_Inicial_Riesgos_Horizonte.xlsx y 06_Comentarios_Interesados_Horizonte.docx), "
                    "arma una matriz preliminar de riesgos con fuente y sin inventar controles."
                ),
            },
            "3": {
                "label": "Profesional (PRISM)",
                "text": _prism_prompt(
                    persona=(
                        "Actúa como especialista en gestión de riesgos de proyectos del sector energético, "
                        "con experiencia en consolidados multi-fuente para comités."
                    ),
                    realidad=(
                        "Debes construir una matriz preliminar de riesgos del Proyecto Horizonte "
                        "a partir de cinco fuentes. La valoración NO es definitiva. "
                        "Existen riesgos explícitos, derivados e hipótesis que requieren validación."
                    ),
                    informacion=(
                        "Fuentes exclusivas:\n"
                        "- 02_Alcance_Proyecto_Horizonte.docx\n"
                        "- 03_Presupuesto_y_Cronograma_Horizonte.xlsx\n"
                        "- 04_Transcripcion_Reunion_Horizonte.docx\n"
                        "- 05_Registro_Inicial_Riesgos_Horizonte.xlsx\n"
                        "- 06_Comentarios_Interesados_Horizonte.docx\n"
                        "No inventes controles existentes. No uses 07_Plantilla_Comite_Horizonte.pptx como fuente de riesgos."
                    ),
                    solicitud=(
                        "Consolida una matriz preliminar con columnas: "
                        "ID | Riesgo | Categoría | Fuente | Causa | Evento | Consecuencia | "
                        "Probabilidad preliminar | Impacto preliminar | Nivel preliminar | "
                        "Control existente | Acción sugerida | Señal de alerta | "
                        "Responsable sugerido por rol | Información requerida para validar.\n"
                        "Categorías permitidas: Técnico, Operativo, Seguridad, Ambiental, Social, "
                        "Contractual, Financiero, Regulatorio, Reputacional, Cronograma.\n"
                        "Marca cada riesgo: Explícito en las fuentes / Derivado / Hipótesis que requiere validación.\n"
                        "Finaliza con: 5 riesgos prioritarios; posibles duplicados; riesgos sin evidencia suficiente; "
                        "preguntas para especialistas."
                    ),
                    metodo=(
                        "Usa semáforos 🔴 Alto / 🟡 Medio / 🟢 Bajo en el nivel preliminar.\n"
                        "Separa claramente valoración preliminar de valoración aprobada.\n"
                        "Tablas Markdown; tablero de top riesgos; no presentes la matriz como definitiva."
                    ),
                ),
            },
            "4": {
                "label": "Experto",
                "text": _prism_prompt(
                    persona=(
                        "Actúa como director de riesgos de proyecto (Risk Lead) de una firma de consultoría "
                        "que prepara el anexo de riesgos para el comité directivo."
                    ),
                    realidad=(
                        "El comité necesita un paquete de riesgos priorizados, trazables a fuentes, "
                        "con huecos de control y preguntas a especialistas, sin fingir un risk assessment cerrado."
                    ),
                    informacion=(
                        "Las cinco fuentes 02–06 con nombres exactos. "
                        "Toda probabilidad/impacto es preliminar y debe etiquetarse como Inferencia o dato del registro 05."
                    ),
                    solicitud=(
                        "Entrega el Anexo Ejecutivo de Riesgos Horizonte: "
                        "tablero top 5, matriz consolidada, mapa de calor textual, "
                        "duplicidades, riesgos sin dueño, plan de validación con especialistas, "
                        "y recomendaciones Acción|Responsable(rol)|Prioridad|Justificación."
                    ),
                    metodo=(
                        "Informe ejecutivo completo; semáforos; clasificaciones Hecho/Inferencia/Pendiente/Recomendación; "
                        "máximo 5 conclusiones; preguntas abiertas al cliente."
                    ),
                    expert_extra=(
                        "ENTREGABLE PARA GERENCIA/COMITÉ: apto como anexo del paquete; "
                        "disclaimer visible: «valoración preliminar – requiere validación humana»."
                    ),
                ),
            },
        },
        "explain": {
            "persona": "Especialista / Risk Lead de proyectos energéticos.",
            "realidad": "Matriz preliminar multi-fuente; no definitiva.",
            "informacion": "02–06 con nombres exactos; sin inventar controles.",
            "solicitud": "Matriz completa + top 5 + duplicados + preguntas a especialistas.",
            "metodo": "Semáforos, etiquetas explícito/derivado/hipótesis, tablas Markdown.",
            "restricciones": "No inventar controles ni responsables nominados sin evidencia.",
            "formato": "Informe/anexo ejecutivo de riesgos.",
            "validacion": "Contrastar cada riesgo con su archivo fuente antes del comité.",
        },
        "compare": (
            "El básico pide una lista libre; el PRISM exige fuente, categoría, control existente real "
            "y etiqueta de certeza, lo que reduce riesgos inventados."
        ),
        "improveHints": list(_MEJORA_HINTS),
    },
    "f7": {
        "title": "Presentación ejecutiva (comité)",
        "file": "07_Plantilla_Comite_Horizonte.pptx (+ análisis validados)",
        "persona": "Responsable de una oficina de gestión de proyectos (PMO)",
        "levels": {
            "1": {
                "label": "Básico",
                "text": "Hazme una presentación del proyecto.",
            },
            "2": {
                "label": "Mejorado",
                "text": (
                    "Prepara el contenido de una presentación ejecutiva de máximo 8 diapositivas "
                    "para el comité del Proyecto Horizonte, usando solo información validada de los archivos del caso "
                    "y la estructura de 07_Plantilla_Comite_Horizonte.pptx. Marca pendientes de validación."
                ),
            },
            "3": {
                "label": "Profesional (PRISM)",
                "text": _prism_prompt(
                    persona=(
                        "Actúa como responsable de una oficina de gestión de proyectos (PMO) "
                        "que diseña narrativas ejecutivas para comités directivos."
                    ),
                    realidad=(
                        "Debes preparar el contenido de una presentación ejecutiva de exactamente ocho diapositivas "
                        "sobre la revisión inicial del Proyecto Horizonte. "
                        "No se garantiza que Copilot genere el archivo PowerPoint automáticamente: "
                        "si no puede crear el .pptx, entrega la estructura completa para pegarla en "
                        "07_Plantilla_Comite_Horizonte.pptx. "
                        "No presentes propuestas como decisiones aprobadas."
                    ),
                    informacion=(
                        "Usa exclusivamente los archivos y análisis validados del caso, referenciando cuando cites:\n"
                        "02_Alcance_Proyecto_Horizonte.docx, "
                        "03_Presupuesto_y_Cronograma_Horizonte.xlsx, "
                        "04_Transcripcion_Reunion_Horizonte.docx, "
                        "05_Registro_Inicial_Riesgos_Horizonte.xlsx, "
                        "06_Comentarios_Interesados_Horizonte.docx, "
                        "y la plantilla 07_Plantilla_Comite_Horizonte.pptx.\n"
                        "No inventes datos. Cuando falte información, escribe «Pendiente de validación».\n"
                        "No indiques botones de Copilot dentro de PowerPoint."
                    ),
                    solicitud=(
                        "Estructura exactamente 8 diapositivas:\n"
                        "1. Contexto y necesidad\n"
                        "2. Objetivo y alcance\n"
                        "3. Entregables e hitos\n"
                        "4. Presupuesto\n"
                        "5. Cronograma\n"
                        "6. Riesgos prioritarios\n"
                        "7. Decisiones requeridas\n"
                        "8. Próximos pasos\n"
                        "Para cada diapositiva: Título | Mensaje principal | Máximo 4 puntos | "
                        "Dato o evidencia de soporte | Recomendación visual | Información pendiente | Notas del presentador."
                    ),
                    metodo=(
                        "Lenguaje ejecutivo, preciso y orientado a decisiones.\n"
                        "Incluye tablero de semáforos en la diapositiva de riesgos.\n"
                        "Entrega además un resumen de storyline (arco narrativo) de ≤150 palabras.\n"
                        "Si generas archivo, indícalo; si no, entrega guion listo para la plantilla 07."
                    ),
                ),
            },
            "4": {
                "label": "Experto",
                "text": _prism_prompt(
                    persona=(
                        "Actúa como socio de comunicación ejecutiva + PMO que entrega el paquete "
                        "«listo para comité» (contenido + notas + checklist de calidad)."
                    ),
                    realidad=(
                        "Gerencia presentará Horizonte en un slot corto. Necesitan guion impecable, "
                        "cifras trazables, decisiones explícitas y pendientes visibles, "
                        "alineado a 07_Plantilla_Comite_Horizonte.pptx."
                    ),
                    informacion=(
                        "Fuentes del caso con nombres exactos (02–07). "
                        "Solo datos previamente contrastables; todo lo demás PENDIENTE DE VALIDACIÓN."
                    ),
                    solicitud=(
                        "Entrega el Paquete de Comité Horizonte: "
                        "guion de 8 diapositivas, storyline, tablero KPI sugerido, "
                        "anexo de fuentes por diapositiva, checklist de calidad "
                        "(cifras, fechas, riesgos con fuente, decisiones diferenciadas, faltantes marcados, "
                        "plantilla respetada, revisión humana) y versión «speaking notes» para el presentador."
                    ),
                    metodo=(
                        "Informe ejecutivo que contiene el guion slide-by-slide; "
                        "sin afirmar aprobación del proyecto; recomendaciones solo como decisiones requeridas."
                    ),
                    expert_extra=(
                        "ENTREGABLE PARA GERENCIA/COMITÉ: listo para transferir a "
                        "07_Plantilla_Comite_Horizonte.pptx sin reescritura conceptual."
                    ),
                ),
            },
        },
        "explain": {
            "persona": "PMO / comunicación ejecutiva para comité.",
            "realidad": "Ocho diapositivas; posible ruta estructura→plantilla 07.",
            "informacion": "Archivos 02–07; solo datos validados; sin botones Copilot-in-PPT.",
            "solicitud": "Guion completo por diapositiva + evidencias + pendientes.",
            "metodo": "Storyline, semáforos, notas del presentador, checklist de calidad.",
            "restricciones": "No inventar; no vender el proyecto como aprobado.",
            "formato": "Informe ejecutivo + guion de presentación.",
            "validacion": "Verificar cifras/fechas/riesgos contra fuentes antes de proyectar.",
        },
        "compare": (
            "El básico pide «una presentación» sin estructura; el PRISM fija 8 slides, evidencia por slide "
            "y plantilla 07, reduciendo contenido genérico o inventado."
        ),
        "improveHints": list(_MEJORA_HINTS),
    },
    "f8": {
        "title": "Correo ejecutivo final",
        "file": "Outlook / Microsoft 365 Copilot Chat",
        "persona": "Coordinador del Proyecto Horizonte",
        "levels": {
            "1": {
                "label": "Básico",
                "text": "Redacta un correo para el comité.",
            },
            "2": {
                "label": "Mejorado",
                "text": (
                    "Redacta un correo al comité directivo del Proyecto Horizonte informando la revisión inicial, "
                    "hallazgos principales, inconsistencias, riesgos prioritarios, decisiones requeridas "
                    "e información pendiente. No digas que el proyecto fue aprobado."
                ),
            },
            "3": {
                "label": "Profesional (PRISM)",
                "text": _prism_prompt(
                    persona=(
                        "Actúa como coordinador del Proyecto Horizonte con experiencia en "
                        "comunicaciones ejecutivas a comités directivos."
                    ),
                    realidad=(
                        "Se completó la revisión inicial académica del Proyecto Horizonte a partir de los archivos del caso. "
                        "Debes informar al comité sin afirmar aprobación, sin inventar compromisos "
                        "y dejando claros los pendientes de validación."
                    ),
                    informacion=(
                        "Basa el correo solo en hallazgos trazables a:\n"
                        "01_Correo_Solicitud_Proyecto_Horizonte, "
                        "02_Alcance_Proyecto_Horizonte.docx, "
                        "03_Presupuesto_y_Cronograma_Horizonte.xlsx, "
                        "04_Transcripcion_Reunion_Horizonte.docx, "
                        "05_Registro_Inicial_Riesgos_Horizonte.xlsx, "
                        "06_Comentarios_Interesados_Horizonte.docx, "
                        "y la presentación basada en 07_Plantilla_Comite_Horizonte.pptx.\n"
                        "Si un dato no fue validado, márcalo como PENDIENTE DE VALIDACIÓN.\n"
                        "Trabaja en Outlook Copilot o Microsoft 365 Copilot Chat; sin Power Automate."
                    ),
                    solicitud=(
                        "El correo debe: informar que se realizó la revisión inicial; resumir hallazgos principales; "
                        "indicar inconsistencias; presentar riesgos prioritarios; enumerar decisiones requeridas; "
                        "identificar información pendiente; mencionar archivos adjuntos sugeridos; "
                        "no afirmar que el proyecto fue aprobado; no inventar compromisos.\n"
                        "Incluye: asunto sugerido; cuerpo del correo; lista de anexos; próxima acción recomendada."
                    ),
                    metodo=(
                        "Además del correo listo para enviar, incluye dentro del informe: "
                        "tablero breve de criticidad, tabla de decisiones requeridas, "
                        "y checklist de validación humana antes del envío.\n"
                        "Tono formal, conciso, orientado a acción."
                    ),
                ),
            },
            "4": {
                "label": "Experto",
                "text": _prism_prompt(
                    persona=(
                        "Actúa como jefe de gabinete / liaison de PMO que redacta la comunicación "
                        "oficial de pre-comité para la alta dirección."
                    ),
                    realidad=(
                        "La alta dirección recibirá el correo como puerta de entrada al paquete de comité. "
                        "Debe caber en una lectura de 2–3 minutos, con anexos claros y decisiones pedidas "
                        "sin ambigüedad ni sobrepromesa."
                    ),
                    informacion=(
                        "Solo hechos trazables a los archivos 01–07 del caso Horizonte. "
                        "Cero cifras nuevas. Cero responsables inventados."
                    ),
                    solicitud=(
                        "Entrega el Paquete de Comunicación Ejecutiva: "
                        "(A) asunto + correo listo para enviar, "
                        "(B) versión ultracorta (≤120 palabras) para reenvío interno, "
                        "(C) lista de anexos con propósito de cada uno, "
                        "(D) matriz de decisiones solicitadas al comité, "
                        "(E) riesgos de comunicación (malentendidos posibles) con mitigación."
                    ),
                    metodo=(
                        "Informe ejecutivo que contiene el correo como pieza central; "
                        "semáforos solo si aportan; preguntas para el cliente si faltan datos para el envío."
                    ),
                    expert_extra=(
                        "ENTREGABLE PARA GERENCIA: el correo debe poder copiarse a Outlook sin edición conceptual; "
                        "disclaimer implícito: revisión inicial, no aprobación."
                    ),
                ),
            },
        },
        "explain": {
            "persona": "Coordinador Horizonte / liaison ejecutivo.",
            "realidad": "Cierre de revisión inicial; comunicación a comité sin sobreprometer.",
            "informacion": "Hallazgos trazables a archivos 01–07.",
            "solicitud": "Correo completo + anexos + decisiones + pendientes.",
            "metodo": "Asunto, cuerpo, anexos, próxima acción + tablero y checklist.",
            "restricciones": "No afirmar aprobación; no inventar compromisos; sin Power Automate.",
            "formato": "Informe ejecutivo que incluye el correo listo para enviar.",
            "validacion": "Releer anexos y cifras antes de pulsar enviar.",
        },
        "compare": (
            "El básico pide «un correo» genérico; el PRISM ancla el mensaje a fuentes, decisiones y pendientes, "
            "evitando alucinaciones de aprobación o compromisos."
        ),
        "improveHints": list(_MEJORA_HINTS),
    },
}


if __name__ == "__main__":
    import json
    from pathlib import Path

    Path(__file__).with_name("s2_prism_data.json").write_text(
        json.dumps(S2_PRISM, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("ok", len(S2_PRISM))
