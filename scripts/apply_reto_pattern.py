# -*- coding: utf-8 -*-
"""
Aplica el patrón Sesión 1 · Reto 1 al resto de retos S1/S2.
- Corrige fechas N-14 (sábados 21 y 28 / martes 17 de marzo 2026)
- Extiende backend de correos
- Inserta motor JS reutilizable
- Reemplaza cuerpos r2-r6 y enriquece F1-F8
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
APP = ROOT / "app.py"

# Fechas coherentes: 17=mar martes, 21=sáb, 28=sáb
OLD_DATES = [
    ("sábado 22/03/2026", "sábado 21/03/2026"),
    ("sábado 29/03/2026", "sábado 28/03/2026"),
    ("martes 18/03/2026", "martes 17/03/2026"),
    ("22/03/2026 de 07:00", "21/03/2026 de 07:00"),
    ("29/03/2026 en el mismo", "28/03/2026 en el mismo"),
]


def fix_n14_dates(text: str) -> str:
    for a, b in OLD_DATES:
        text = text.replace(a, b)
    # prompt default asunto field if still old
    text = text.replace(
        "URGENTE · Reprogramación intervención preventiva Circuito N-14.",
        "URGENTE · Reprogramación intervención preventivo Circuito N-14.",
    )
    return text


def esc_js(s: str) -> str:
    return (
        s.replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("${", "\\${")
    )


# ---------------------------------------------------------------------------
# Case definitions (content for r2-r6 and f1-f8 enhancements)
# ---------------------------------------------------------------------------

CASES = {
    "r2": {
        "id": "r2",
        "title": "Cadena de correos",
        "apps": ["Outlook", "Word"],
        "email": True,
        "planilla": {"key": "cadena-correos", "label": "Descargar planilla oficial (Word)"},
        "output": "MCP365_P02_Cadena_correos_completado.docx",
        "steps": [
            "Pulsa <strong>Enviar correo del reto a mi bandeja</strong>. Llegará un resumen de la cadena ST-Urb-03 desde <code>analizamostunegocio@gmail.com</code>.",
            "Abre <strong>Outlook</strong> y localiza el asunto de la cadena (también puedes usar las pestañas de esta página como respaldo).",
            "Descarga la <strong>planilla oficial</strong> y ábrela en <strong>Word</strong>.",
            "Ajusta el prompt configurable (remitente, objetivo, entregable) si lo necesitas y cópialo.",
            "En Word → Copilot, analiza la cadena: cronología, cambios, compromisos y tres borradores (técnico, ejecutivo, usuarios).",
            "No inventes datos. Marca supuestos. Deja validación humana y control de calidad para la persona.",
            "Guarda como <code>MCP365_P02_Cadena_correos_completado.docx</code>.",
            "Después: elige una cadena real de tu bandeja, adapta el prompt y reutiliza la planilla con tu caso.",
        ],
        "fields": [
            ("rol", "Rol de Copilot", "Asistente de operaciones que reconstruye cronologías y redacta respuestas por audiencia."),
            ("app", "Aplicación de origen", "Outlook."),
            ("fuente", "Fuente que se debe analizar", "Cadena de cuatro correos sobre el transformador auxiliar ST-Urb-03 (01, 04, 06 y 07/03/2026)."),
            ("objetivo", "Objetivo del análisis", "Construir cronología, cambios vs plan inicial, compromisos vigentes y tres borradores de respuesta (técnica, ejecutiva y usuarios)."),
            ("archivo", "Archivo que se debe completar", "MCP365_P02_Cadena_correos_audiencias.doc (planilla oficial del reto)."),
            ("seccion", "Secciones autorizadas", "Cronología, cambios, compromisos y borradores por audiencia."),
            ("restringidos", "Campos que deben quedar sin completar", "Validación humana.\nControl de calidad.\nFirmas."),
            ("vacio", "Respuesta cuando no exista información", "No especificado."),
            ("detalle", "Nivel de detalle", "Cronología fecha a fecha; borrador ejecutivo máx. 8 líneas; mensaje a usuarios máx. 6 líneas."),
            ("salida", "Nombre del archivo de salida", "MCP365_P02_Cadena_correos_completado.docx."),
        ],
        "checklist": [
            ("r2-c1", "Correo/cadena del reto disponible (bandeja o pestañas)"),
            ("r2-c2", "Planilla oficial usada sin reconstruir el diseño"),
            ("r2-c3", "Cronología, cambios y tres borradores sin inventar datos"),
            ("r2-c4", "Validación humana y control de calidad sin completar por Copilot"),
            ("r2-c5", "Práctica propia con una cadena real de mi bandeja"),
        ],
        "practice_title": "Al terminar el caso · Practica con una cadena real de tu bandeja",
        "practice": "Aplica el mismo método a una cadena de correos propia (sin datos confidenciales). Cambia remitente, asunto, objetivo y nombre de salida. Conserva la estructura de cronología + tres audiencias. Guarda como MCP365_P02_Cadena_[tu-tema]_completado.docx.",
        "deliverable": "Entregable del caso: MCP365_P02_Cadena_correos_completado.docx con cronología, cambios, compromisos y tres borradores. Validación humana y control de calidad vacíos.",
    },
    "r3": {
        "id": "r3",
        "title": "Reunión a plan de acción",
        "apps": ["Teams", "Word"],
        "email": False,
        "planilla": {"key": "matriz-compromisos", "label": "Descargar planilla oficial (Word/Excel)"},
        "output": "MCP365_P03_Matriz_compromisos_completada.docx",
        "steps": [
            "Descarga la <strong>planilla oficial</strong> de matriz de compromisos.",
            "Copia la transcripción del comité (en esta página) o ábrela en <strong>Teams/Word</strong>.",
            "Ajusta el prompt configurable según tu reunión y cópialo.",
            "En Word o Teams → Copilot, separa decisiones, propuestas, opiniones y tareas.",
            "Completa la matriz: Actividad | Responsable | Fecha | Estado | Evidencia. Usa “No especificado” si falta un dato.",
            "No inventes responsables ni fechas. Deja validación humana y control de calidad a la persona.",
            "Guarda como <code>MCP365_P03_Matriz_compromisos_completada.docx</code>.",
            "Después: usa una transcripción propia (sin datos sensibles), adapta el prompt y reutiliza la planilla.",
        ],
        "fields": [
            ("rol", "Rol de Copilot", "Facilitador de reuniones que convierte transcripciones en matrices de compromisos."),
            ("app", "Aplicación de origen", "Teams / Word."),
            ("fuente", "Fuente que se debe analizar", "Acta verbal · Comité operativo Proyecto Horizonte · 20/03/2026 09:00."),
            ("objetivo", "Objetivo del análisis", "Diferenciar decisiones, propuestas, opiniones y tareas; construir matriz Actividad | Responsable | Fecha | Estado | Evidencia."),
            ("archivo", "Archivo que se debe completar", "MCP365_P03 matriz de compromisos (planilla oficial)."),
            ("restringidos", "Campos que deben quedar sin completar", "Validación humana.\nControl de calidad.\nFirmas."),
            ("vacio", "Respuesta cuando no exista información", "No especificado."),
            ("detalle", "Nivel de detalle", "Una fila por compromiso; evidencia breve citada de la transcripción."),
            ("salida", "Nombre del archivo de salida", "MCP365_P03_Matriz_compromisos_completada.docx."),
        ],
        "checklist": [
            ("r3-c1", "Transcripción del caso utilizada como única fuente"),
            ("r3-c2", "Planilla de matriz completada sin inventar datos"),
            ("r3-c3", "Decisiones separadas de propuestas y opiniones"),
            ("r3-c4", "Validación humana y control de calidad sin completar por Copilot"),
            ("r3-c5", "Práctica propia con una reunión real (sin datos sensibles)"),
        ],
        "practice_title": "Al terminar el caso · Practica con tu propia reunión",
        "practice": "Toma una transcripción o notas de una reunión propia (anonimiza nombres si hace falta). Cambia fuente, objetivo y nombre de salida. Conserva la matriz de 5 columnas. Guarda como MCP365_P03_Matriz_[tu-reunion]_completada.docx.",
        "deliverable": "Entregable del caso: MCP365_P03_Matriz_compromisos_completada.docx + lista de propuestas no aprobadas. Validación humana y control de calidad vacíos.",
    },
    "r4": {
        "id": "r4",
        "title": "Informe para tres audiencias",
        "apps": ["Word"],
        "email": False,
        "planilla": {"key": "tres-audiencias", "label": "Descargar planilla oficial (Word)"},
        "output": "MCP365_P04_Tres_audiencias_completado.docx",
        "steps": [
            "Descarga la <strong>planilla oficial</strong> de comunicación por audiencia.",
            "Abre <strong>Word → Copilot</strong> y usa el informe técnico ST-14 de esta página como fuente.",
            "Ajusta el prompt (audiencias, extensión, omisiones permitidas) y cópialo.",
            "Genera tres versiones sin alterar hechos: técnica, gerencia y comunidad.",
            "Indica qué se omitió en cada versión y por qué.",
            "Pega solo lo validado en la planilla. Validación humana y control de calidad quedan para la persona.",
            "Guarda como <code>MCP365_P04_Tres_audiencias_completado.docx</code>.",
            "Después: adapta el prompt a un informe propio no confidencial.",
        ],
        "fields": [
            ("rol", "Rol de Copilot", "Comunicador técnico que adapta un mismo hecho a tres audiencias."),
            ("app", "Aplicación de origen", "Word."),
            ("fuente", "Fuente que se debe analizar", "Informe técnico · Hallazgo ST-14 · Subestación Urbana 7 · 18/03/2026."),
            ("objetivo", "Objetivo del análisis", "Generar tres versiones (técnica, gerencia, comunidad) con los mismos hechos y distinto nivel de detalle."),
            ("archivo", "Archivo que se debe completar", "MCP365_P04 planilla de tres audiencias."),
            ("restringidos", "Campos que deben quedar sin completar", "Validación humana.\nControl de calidad.\nFirmas."),
            ("vacio", "Respuesta cuando no exista información", "No especificado."),
            ("detalle", "Nivel de detalle", "Mantener hechos idénticos; variar solo lenguaje y prioridad."),
            ("salida", "Nombre del archivo de salida", "MCP365_P04_Tres_audiencias_completado.docx."),
        ],
        "checklist": [
            ("r4-c1", "Informe técnico ST-14 usado como única fuente de hechos"),
            ("r4-c2", "Tres versiones generadas sin alterar hechos"),
            ("r4-c3", "Omisiones por audiencia explicadas"),
            ("r4-c4", "Validación humana y control de calidad sin completar por Copilot"),
            ("r4-c5", "Práctica propia con un informe no confidencial"),
        ],
        "practice_title": "Al terminar el caso · Practica con tu propio informe",
        "practice": "Elige un informe operativo propio (sin datos sensibles). Cambia fuente, objetivo y nombre de salida. Conserva el esquema de tres audiencias. Guarda como MCP365_P04_Tres_audiencias_[tu-tema]_completado.docx.",
        "deliverable": "Entregable del caso: MCP365_P04_Tres_audiencias_completado.docx con versiones técnica, gerencia y comunidad. Validación humana y control de calidad vacíos.",
    },
    "r5": {
        "id": "r5",
        "title": "Comparación de documentos",
        "apps": ["Word", "Excel"],
        "email": False,
        "planilla": {"key": "comparacion-docs", "label": "Descargar planilla oficial (Excel/Word)"},
        "output": "MCP365_P05_Comparacion_docs_completada.xlsx",
        "steps": [
            "Descarga la <strong>planilla oficial</strong> de comparación documental.",
            "En <strong>Word</strong>, pega PRO-OPS-12 v3.1 y v4.0 (textos de esta página).",
            "Ajusta el prompt y cópialo.",
            "Pide a Copilot la tabla: Tema | Versión anterior | Versión actual | Impacto posible | Validación requerida.",
            "No inventes cláusulas. Marca qué cambios requieren aprobación formal.",
            "Transfiere a la planilla. Validación humana y control de calidad para la persona.",
            "Guarda como <code>MCP365_P05_Comparacion_docs_completada.xlsx</code> (o .docx si usas Word).",
            "Después: compara dos versiones reales de un procedimiento propio (anonimizado).",
        ],
        "fields": [
            ("rol", "Rol de Copilot", "Analista documental que detecta cambios de texto y de significado."),
            ("app", "Aplicación de origen", "Word / Excel."),
            ("fuente", "Fuente que se debe analizar", "PRO-OPS-12 versión 3.1 vs versión 4.0."),
            ("objetivo", "Objetivo del análisis", "Identificar cambios textuales y de significado; impacto posible y validación requerida."),
            ("archivo", "Archivo que se debe completar", "MCP365_P05 planilla de comparación."),
            ("tabla", "Tabla que se debe completar", "Tema | Versión anterior | Versión actual | Impacto posible | Validación requerida."),
            ("restringidos", "Campos que deben quedar sin completar", "Validación humana.\nControl de calidad.\nFirmas."),
            ("vacio", "Respuesta cuando no exista información", "No especificado."),
            ("salida", "Nombre del archivo de salida", "MCP365_P05_Comparacion_docs_completada.xlsx."),
        ],
        "checklist": [
            ("r5-c1", "Ambas versiones PRO-OPS-12 usadas sin agregar cláusulas"),
            ("r5-c2", "Tabla de comparación completa"),
            ("r5-c3", "Impactos y validaciones marcados"),
            ("r5-c4", "Validación humana y control de calidad sin completar por Copilot"),
            ("r5-c5", "Práctica propia con dos versiones de un documento real"),
        ],
        "practice_title": "Al terminar el caso · Compara dos versiones propias",
        "practice": "Toma dos versiones de un procedimiento o instructivo propio (sin datos sensibles). Cambia fuente, objetivo y salida. Conserva la tabla de 5 columnas. Guarda como MCP365_P05_Comparacion_[tu-doc]_completada.xlsx.",
        "deliverable": "Entregable del caso: MCP365_P05_Comparacion_docs_completada.xlsx con impactos y validaciones. Validación humana y control de calidad vacíos.",
    },
    "r6": {
        "id": "r6",
        "title": "Priorización del trabajo",
        "apps": ["Excel"],
        "email": False,
        "planilla": {"key": "priorizacion", "label": "Descargar base del ejercicio (Excel)"},
        "output": "MCP365_P06_Priorizacion_completada.xlsx",
        "steps": [
            "Descarga la <strong>base del ejercicio</strong> (10 tareas).",
            "Ábrela en <strong>Excel → Copilot</strong>.",
            "Ajusta el prompt (horizonte de agenda, criterios de delegación) y cópialo.",
            "Clasifica por urgencia/impacto, propone agenda de hoy y mañana, marca delegables vs criterio humano.",
            "No inventes fechas ni responsables nuevos.",
            "Guarda como <code>MCP365_P06_Priorizacion_completada.xlsx</code>.",
            "Después: prioriza tu propia lista de tareas del día (sin datos sensibles).",
        ],
        "fields": [
            ("rol", "Rol de Copilot", "Asistente de priorización operativa que propone agendas realistas."),
            ("app", "Aplicación de origen", "Excel."),
            ("fuente", "Fuente que se debe analizar", "Lista de 10 tareas del Reto 6 (tabla de la plataforma / planilla)."),
            ("objetivo", "Objetivo del análisis", "Clasificar por urgencia e impacto; proponer agenda hoy/mañana; marcar delegables y tareas de criterio humano."),
            ("archivo", "Archivo que se debe completar", "MCP365_P06 planilla de priorización."),
            ("restringidos", "Campos que deben quedar sin completar", "Validación humana.\nControl de calidad.\nDecisiones finales de priorización (las confirma la persona)."),
            ("vacio", "Respuesta cuando no exista información", "No especificado."),
            ("detalle", "Nivel de detalle", "Agenda por bloques de tiempo; explicar supuestos brevemente."),
            ("salida", "Nombre del archivo de salida", "MCP365_P06_Priorizacion_completada.xlsx."),
        ],
        "checklist": [
            ("r6-c1", "Planilla con las 10 tareas descargada"),
            ("r6-c2", "Agenda hoy/mañana propuesta sin inventar responsables"),
            ("r6-c3", "Delegables vs criterio humano marcados"),
            ("r6-c4", "Validación humana y control de calidad sin completar por Copilot"),
            ("r6-c5", "Práctica propia con mi lista real de tareas"),
        ],
        "practice_title": "Al terminar el caso · Prioriza tu propia jornada",
        "practice": "Exporta o escribe 8–12 tareas reales de tu día (sin información confidencial). Cambia fuente, objetivo y salida. Conserva urgencia/impacto y la distinción delegable vs humano. Guarda como MCP365_P06_Priorizacion_[tu-fecha]_completada.xlsx.",
        "deliverable": "Entregable del caso: MCP365_P06_Priorizacion_completada.xlsx con agenda y delegación. Validación humana y control de calidad vacíos.",
    },
}

# Session 2 enhancements (append blocks; keep existing widgets)
S2 = {
    "fase-1": {
        "id": "fase-1",
        "apps": ["Word"],
        "email": False,
        "planilla": None,
        "output": "MCP365_S2_F1_Brief_Horizonte_completado.docx",
        "fields": [
            ("rol", "Rol de Copilot", "Analista de proyectos energéticos."),
            ("app", "Aplicación de origen", "Word."),
            ("fuente", "Fuente que se debe analizar", "Documentos del caso Proyecto Horizonte (pestañas 1 a 10)."),
            ("objetivo", "Objetivo del análisis", "Construir brief: objetivo, justificación, alcance, exclusiones, entregables, supuestos, restricciones, interesados y vacíos."),
            ("archivo", "Archivo que se debe completar", "Planilla de informe ejecutivo / brief (MCP365_P07)."),
            ("restringidos", "Campos que deben quedar sin completar", "Validación humana.\nControl de calidad.\nFirmas."),
            ("vacio", "Respuesta cuando no exista información", "No especificado."),
            ("salida", "Nombre del archivo de salida", "MCP365_S2_F1_Brief_Horizonte_completado.docx."),
        ],
        "checklist": [
            ("f1-c1", "Documentos del caso usados sin inventar"),
            ("f1-c2", "Brief en planilla con hechos vs no especificado"),
            ("f1-c3", "Validación humana y control de calidad vacíos para la persona"),
            ("f1-c4", "Práctica propia: brief de un proyecto real anonimizado"),
        ],
        "practice_title": "Al terminar · Practica con un proyecto propio",
        "practice": "Arma un brief de un proyecto real de tu área (anonimiza). Cambia fuente y salida. Conserva secciones del brief. Guarda como MCP365_S2_F1_Brief_[tu-proyecto]_completado.docx.",
        "deliverable": "Entregable del caso: MCP365_S2_F1_Brief_Horizonte_completado.docx.",
    },
    "fase-2": {
        "id": "fase-2",
        "apps": ["Excel", "Word"],
        "fields": [
            ("rol", "Rol de Copilot", "Planificador de proyectos que propone EDT y RACI."),
            ("app", "Aplicación de origen", "Excel / Word."),
            ("fuente", "Fuente que se debe analizar", "Brief del Proyecto Horizonte y documentos del caso."),
            ("objetivo", "Objetivo del análisis", "Proponer EDT, hitos, dependencias, criterios de aceptación y matriz RACI."),
            ("archivo", "Archivo que se debe completar", "Matriz RACI MCP365_P09."),
            ("restringidos", "Campos que deben quedar sin completar", "Fechas definitivas.\nValidación humana.\nControl de calidad."),
            ("vacio", "Respuesta cuando no exista información", "No especificado."),
            ("salida", "Nombre del archivo de salida", "MCP365_S2_F2_RACI_Horizonte_completado.xlsx."),
        ],
        "checklist": [
            ("f2-c1", "RACI/EDT propuestos a partir del brief"),
            ("f2-c2", "Fechas y responsables marcados como pendientes de validación humana"),
            ("f2-c3", "Planilla RACI diligenciada sin inventar datos críticos"),
            ("f2-c4", "Práctica propia: RACI de un proyecto real anonimizado"),
        ],
        "practice_title": "Al terminar · Arma un RACI propio",
        "practice": "Usa un proyecto real (anonimizado). Cambia fuente y salida. Conserva EDT + RACI. Las fechas finales las valida tu equipo.",
        "deliverable": "Entregable del caso: MCP365_S2_F2_RACI_Horizonte_completado.xlsx.",
    },
    "fase-3": {
        "id": "fase-3",
        "apps": ["Excel"],
        "fields": [
            ("rol", "Rol de Copilot", "Analista de riesgos de proyecto."),
            ("app", "Aplicación de origen", "Excel."),
            ("fuente", "Fuente que se debe analizar", "Documentos del caso + registro inicial de riesgos del Proyecto Horizonte."),
            ("objetivo", "Objetivo del análisis", "Completar causa, consecuencia, probabilidad, impacto, respuesta, responsable y alerta."),
            ("archivo", "Archivo que se debe completar", "Registro de riesgos MCP365_P08."),
            ("restringidos", "Campos que deben quedar sin completar", "Aprobación final de severidad.\nValidación humana.\nControl de calidad."),
            ("vacio", "Respuesta cuando no exista información", "No especificado."),
            ("salida", "Nombre del archivo de salida", "MCP365_S2_F3_Riesgos_Horizonte_completado.xlsx."),
        ],
        "checklist": [
            ("f3-c1", "Registro de riesgos basado solo en el caso"),
            ("f3-c2", "Niveles y respuestas sin inventar severidad no sustentada"),
            ("f3-c3", "Validación humana pendiente en severidades críticas"),
            ("f3-c4", "Práctica propia: registro de riesgos de un proyecto real anonimizado"),
        ],
        "practice_title": "Al terminar · Registra riesgos de tu proyecto",
        "practice": "Completa 5–8 riesgos reales anonimizados. Conserva la estructura del registro. Guarda como MCP365_S2_F3_Riesgos_[tu-proyecto]_completado.xlsx.",
        "deliverable": "Entregable del caso: MCP365_S2_F3_Riesgos_Horizonte_completado.xlsx.",
    },
    "fase-4": {
        "id": "fase-4",
        "apps": ["Excel"],
        "fields": [
            ("rol", "Rol de Copilot", "Analista de interesados y comunicaciones."),
            ("app", "Aplicación de origen", "Excel."),
            ("fuente", "Fuente que se debe analizar", "Documentos del caso Horizonte (comunidad, acta, ficha)."),
            ("objetivo", "Objetivo del análisis", "Completar mapa de interesados: interés, influencia, mensaje, canal, frecuencia y responsable."),
            ("archivo", "Archivo que se debe completar", "Mapa de interesados MCP365_P10."),
            ("restringidos", "Campos que deben quedar sin completar", "Validación humana.\nControl de calidad."),
            ("vacio", "Respuesta cuando no exista información", "No especificado."),
            ("salida", "Nombre del archivo de salida", "MCP365_S2_F4_Interesados_Horizonte_completado.xlsx."),
        ],
        "checklist": [
            ("f4-c1", "Mapa de interesados alineado al caso"),
            ("f4-c2", "Mensajes y canales sin inventar compromisos no aprobados"),
            ("f4-c3", "Validación humana pendiente"),
            ("f4-c4", "Práctica propia: mapa de interesados de un proyecto real anonimizado"),
        ],
        "practice_title": "Al terminar · Mapea interesados de tu proyecto",
        "practice": "Elabora un mapa para un proyecto propio (anonimizado). Conserva columnas del formato. Guarda como MCP365_S2_F4_Interesados_[tu-proyecto]_completado.xlsx.",
        "deliverable": "Entregable del caso: MCP365_S2_F4_Interesados_Horizonte_completado.xlsx.",
    },
    "fase-5": {
        "id": "fase-5",
        "apps": ["Excel", "Word"],
        "fields": [
            ("rol", "Rol de Copilot", "Analista de control de avance de proyecto."),
            ("app", "Aplicación de origen", "Excel / Word."),
            ("fuente", "Fuente que se debe analizar", "KPI del Proyecto Horizonte: avance esperado 58%, real 46%, presupuesto 52%, 3 críticas retrasadas, 4 riesgos altos."),
            ("objetivo", "Objetivo del análisis", "Responder: qué ocurre, qué se desvía, causas posibles, impacto, información faltante y decisiones para el comité."),
            ("restringidos", "Campos que deben quedar sin completar", "Decisiones del comité.\nValidación humana.\nControl de calidad."),
            ("vacio", "Respuesta cuando no exista información", "No especificado."),
            ("salida", "Nombre del archivo de salida", "MCP365_S2_F5_Analisis_avance_Horizonte.docx."),
        ],
        "checklist": [
            ("f5-c1", "Análisis basado solo en KPI del caso"),
            ("f5-c2", "Hechos separados de inferencias"),
            ("f5-c3", "Campos de avance en la plataforma completados"),
            ("f5-c4", "Práctica propia: lectura de avance de un proyecto real anonimizado"),
        ],
        "practice_title": "Al terminar · Analiza el avance de tu proyecto",
        "practice": "Usa indicadores reales anonimizados. Cambia fuente y salida. Separa hechos e inferencias. Guarda como MCP365_S2_F5_Analisis_avance_[tu-proyecto].docx.",
        "deliverable": "Entregable del caso: MCP365_S2_F5_Analisis_avance_Horizonte.docx + respuestas en la plataforma.",
    },
    "fase-6": {
        "id": "fase-6",
        "apps": ["Word"],
        "fields": [
            ("rol", "Rol de Copilot", "Asesor de decisión ante eventos críticos de proyecto."),
            ("app", "Aplicación de origen", "Word."),
            ("fuente", "Fuente que se debe analizar", "Evento crítico: retraso de 3 semanas del equipo principal + solicitud de cambio de horario de la comunidad. Escenarios A/B/C de la plataforma."),
            ("objetivo", "Objetivo del análisis", "Impacto, escenarios, pros/contras, mitigación, mensajes a proveedor/comunidad y resumen a dirección."),
            ("restringidos", "Campos que deben quedar sin completar", "Decisión final del comité.\nValidación humana.\nControl de calidad."),
            ("vacio", "Respuesta cuando no exista información", "No especificado."),
            ("salida", "Nombre del archivo de salida", "MCP365_S2_F6_Evento_critico_Horizonte.docx."),
        ],
        "checklist": [
            ("f6-c1", "Escenarios A/B/C analizados sin inventar costos no dados"),
            ("f6-c2", "Mensajes a proveedor y comunidad redactados con hechos"),
            ("f6-c3", "Validación humana pendiente sobre la recomendación"),
            ("f6-c4", "Práctica propia: análisis de un evento crítico real anonimizado"),
        ],
        "practice_title": "Al terminar · Analiza un evento crítico propio",
        "practice": "Describe un imprevisto real anonimizado y arma 3 escenarios. Conserva la lógica de impacto y recomendación. Guarda como MCP365_S2_F6_Evento_critico_[tu-caso].docx.",
        "deliverable": "Entregable del caso: MCP365_S2_F6_Evento_critico_Horizonte.docx.",
    },
    "fase-7": {
        "id": "fase-7",
        "apps": ["PowerPoint", "Word"],
        "fields": [
            ("rol", "Rol de Copilot", "Asesor ejecutivo que prepara comité directivo."),
            ("app", "Aplicación de origen", "PowerPoint / Word."),
            ("fuente", "Fuente que se debe analizar", "Expediente Horizonte: avance, riesgos, evento crítico y escenarios."),
            ("objetivo", "Objetivo del análisis", "Construir informe de 10 bloques y borrador de 8 diapositivas con lenguaje ejecutivo."),
            ("archivo", "Archivo que se debe completar", "Informe ejecutivo MCP365_P07 + deck de 8 slides."),
            ("restringidos", "Campos que deben quedar sin completar", "Aprobación del comité.\nValidación humana de cifras.\nControl de calidad."),
            ("vacio", "Respuesta cuando no exista información", "No especificado."),
            ("detalle", "Nivel de detalle", "Máximo 4 viñetas por diapositiva; tono ejecutivo."),
            ("salida", "Nombre del archivo de salida", "MCP365_S2_F7_Comite_Horizonte.pptx."),
        ],
        "checklist": [
            ("f7-c1", "Informe ejecutivo con los 10 bloques"),
            ("f7-c2", "Deck de 8 diapositivas sin inventar cifras"),
            ("f7-c3", "Validación humana de recomendación pendiente"),
            ("f7-c4", "Práctica propia: deck ejecutivo de un proyecto real anonimizado"),
        ],
        "practice_title": "Al terminar · Prepara tu propio comité",
        "practice": "Arma 8 slides de un proyecto propio anonimizado. Conserva la estructura de la plantilla visual. Guarda como MCP365_S2_F7_Comite_[tu-proyecto].pptx.",
        "deliverable": "Entregable del caso: MCP365_S2_F7_Comite_Horizonte.pptx (+ informe Word si aplica).",
    },
    "fase-8": {
        "id": "fase-8",
        "apps": ["Excel", "Word"],
        "fields": [
            ("rol", "Rol de Copilot", "Auditor de proyectos que cruza lecciones aprendidas con ofertas."),
            ("app", "Aplicación de origen", "Excel / Word."),
            ("fuente", "Fuente que se debe analizar", "Histórico de 20 lecciones + oferta OF-HZ-SUR-2026-04."),
            ("objetivo", "Objetivo del análisis", "Detectar reincidencias, nivel de alarma y generar memorando de solicitud de revisión."),
            ("archivo", "Archivo que se debe completar", "Plantilla de alarma MCP365_P14."),
            ("restringidos", "Campos que deben quedar sin completar", "Aprobación de la oferta.\nValidación humana.\nControl de calidad.\nFirmas."),
            ("vacio", "Respuesta cuando no exista información", "No especificado."),
            ("salida", "Nombre del archivo de salida", "MCP365_S2_F8_Alarma_reincidencia_Horizonte.docx."),
        ],
        "checklist": [
            ("f8-c1", "Cruce lecciones vs oferta sin inventar cláusulas"),
            ("f8-c2", "Alarma con puntos de revisión y plazo"),
            ("f8-c3", "Validación humana y control de calidad vacíos para la persona"),
            ("f8-c4", "Práctica propia: cruce de lecciones con una oferta real anonimizada"),
        ],
        "practice_title": "Al terminar · Cruza lecciones con una oferta propia",
        "practice": "Usa un histórico interno anonimizado y una oferta de ejemplo. Conserva la lógica de alarma. Guarda como MCP365_S2_F8_Alarma_[tu-caso].docx.",
        "deliverable": "Entregable del caso: MCP365_S2_F8_Alarma_reincidencia_Horizonte.docx.",
    },
}


def build_engine_js() -> str:
    # Merge r2-r6 + s2 into one object for the engine (r1 stays native)
    data = {**CASES, **S2}
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    return f"""
  /* ========== RETO ENGINE (patrón S1·R1 reutilizable; R1 no se remonta) ========== */
  const RETO_CASES = {payload};

  function buildPromptFromCase(caseId) {{
    const c = RETO_CASES[caseId];
    if (!c) return "";
    const box = document.getElementById("promptConfig-" + caseId);
    const vals = {{}};
    if (box) {{
      box.querySelectorAll("[data-reto-field]").forEach(el => {{
        vals[el.getAttribute("data-reto-field")] = (el.value || "").trim();
      }});
    }} else if (c.fields) {{
      c.fields.forEach(([k, , def]) => {{ vals[k] = def; }});
    }}
    const lines = [
      "PROMPT CONFIGURABLE PARA COPILOT",
      "Caso: " + (c.title || caseId),
      "",
      "INSTRUCCIONES PARA EL PARTICIPANTE",
      "Edita los campos de configuración. Luego copia este prompt y úsalo en Microsoft 365 Copilot con el archivo del reto.",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "1. CONFIGURACIÓN DEL ANÁLISIS",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      ""
    ];
    (c.fields || []).forEach(([key, label]) => {{
      lines.push(label.toUpperCase());
      lines.push("[[" + (vals[key] || "") + "]]");
      lines.push("");
    }});
    lines.push(
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "2. INSTRUCCIÓN PARA COPILOT",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "ACTÚA SEGÚN LA CONFIGURACIÓN.",
      "Analiza exclusivamente la fuente indicada.",
      "Completa solo los campos/secciones autorizados del archivo indicado.",
      "No inventes datos. Si falta información, usa la respuesta definida en la configuración.",
      "No completes validación humana, control de calidad ni firmas salvo que estén autorizados.",
      "Conserva el diseño del archivo oficial; no reconstruyas el documento desde cero.",
      "",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "3. VERIFICACIÓN Y ENTREGA",
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
      "",
      "Antes de entregar: confirma que solo se editó lo autorizado y que el archivo final usa el nombre de salida definido.",
      "Si no puedes editar el archivo conservando el diseño, informa la limitación. No entregues una versión parcial reconstruida."
    );
    return lines.join("\\n");
  }}

  function renderPromptConfigHtml(caseId) {{
    const c = RETO_CASES[caseId];
    if (!c || !c.fields) return "";
    const fields = c.fields.map(([key, label, def]) => `
      <div class="prompt-field">
        <label for="pf-${{caseId}}-${{key}}">${{label}}</label>
        <textarea id="pf-${{caseId}}-${{key}}" data-reto-field="${{key}}" rows="${{Math.min(8, Math.max(1, (def || "").split("\\n").length))}}">${{def.replace(/</g, "&lt;")}}</textarea>
      </div>`).join("");
    return `
      <p><strong>Prompt configurable para Copilot</strong></p>
      <p class="text-muted" style="font-size:0.88rem;margin-top:-0.35rem">Edita cada campo. El prompt completo se actualiza abajo. Luego pulsa <em>Copiar prompt</em>.</p>
      <div class="prompt-config" id="promptConfig-${{caseId}}">${{fields}}</div>
      <p style="margin:1rem 0 0.35rem;font-size:0.9rem"><strong>Prompt completo</strong> <span class="text-muted">(editable; se regenera al cambiar los campos)</span></p>
      <textarea class="prompt-box prompt-edit" id="prompt-${{caseId}}" rows="18" spellcheck="false" aria-label="Prompt completo editable"></textarea>
      <div class="btn-group" style="margin:0.5rem 0 1rem;flex-wrap:wrap;gap:0.5rem">
        <button class="btn btn--sm btn--secondary" data-copy="#prompt-${{caseId}}" type="button"><i data-lucide="copy" width="16" height="16"></i> Copiar prompt</button>
        <button class="btn btn--sm btn--ghost" type="button" data-rebuild-prompt="${{caseId}}"><i data-lucide="refresh-cw" width="16" height="16"></i> Regenerar desde campos</button>
      </div>`;
  }}

  function renderChecklistHtml(caseId) {{
    const c = RETO_CASES[caseId];
    if (!c || !c.checklist) return "";
    const items = c.checklist.map(([key, label]) =>
      `<li><input type="checkbox" data-progress="${{key}}" /> ${{label}}</li>`
    ).join("");
    return `<ul class="check-list">${{items}}</ul>`;
  }}

  function renderPracticeHtml(caseId) {{
    const c = RETO_CASES[caseId];
    if (!c || !c.practice) return "";
    return `<div class="practice-invite">
      <h4><i data-lucide="sparkles" width="18" height="18"></i> ${{c.practice_title || "Al terminar el caso · Practica con tu propio trabajo"}}</h4>
      <p>${{c.practice}}</p>
      <p class="practice-invite__note"><strong>Recuerda:</strong> no copies el ejemplo sin adaptarlo. No uses información confidencial. Validación humana y control de calidad quedan para la persona.</p>
    </div>`;
  }}

  function renderDeliverableHtml(caseId) {{
    const c = RETO_CASES[caseId];
    if (!c || !c.deliverable) return "";
    return `<div class="entregable"><strong>Entregable del caso</strong><br>${{c.deliverable}}<br><strong>Práctica propia recomendada al terminar:</strong> adapta prompt y formato a un caso real anonimizado de tu trabajo.</div>`;
  }}

  function refreshPromptCase(caseId) {{
    const ta = document.getElementById("prompt-" + caseId);
    if (ta) ta.value = buildPromptFromCase(caseId);
  }}

  function initRetoEngine() {{
    document.querySelectorAll("[data-reto-enhance]").forEach(host => {{
      const caseId = host.getAttribute("data-reto-enhance");
      if (!RETO_CASES[caseId] || host.dataset.mounted) return;
      host.dataset.mounted = "1";
      host.innerHTML =
        renderDeliverableHtml(caseId) +
        renderPromptConfigHtml(caseId) +
        renderChecklistHtml(caseId) +
        renderPracticeHtml(caseId);
      const box = document.getElementById("promptConfig-" + caseId);
      if (box) {{
        box.querySelectorAll("[data-reto-field]").forEach(el => {{
          el.addEventListener("input", () => refreshPromptCase(caseId));
        }});
      }}
      refreshPromptCase(caseId);
    }});
    document.querySelectorAll("[data-rebuild-prompt]").forEach(btn => {{
      if (btn.dataset.bound) return;
      btn.dataset.bound = "1";
      btn.addEventListener("click", () => {{
        const id = btn.getAttribute("data-rebuild-prompt");
        refreshPromptCase(id);
        toast("Prompt regenerado desde los campos", "refresh-cw");
      }});
    }});
    document.querySelectorAll("[data-reto-email]").forEach(btn => {{
      if (btn.dataset.bound) return;
      btn.dataset.bound = "1";
      btn.addEventListener("click", async () => {{
        const retoId = btn.getAttribute("data-reto-email");
        const status = document.getElementById("retoEmailStatus-" + retoId);
        if (!serverMode) {{
          toast("Inicia sesión para enviar el correo a tu bandeja", "alert-triangle");
          if (status) status.textContent = "Disponible solo con sesión iniciada.";
          return;
        }}
        btn.disabled = true;
        const prev = btn.innerHTML;
        btn.innerHTML = "Enviando…";
        try {{
          const res = await fetch("/api/reto/send-email", {{
            method: "POST",
            credentials: "same-origin",
            headers: {{ "Content-Type": "application/json" }},
            body: JSON.stringify({{ reto_id: retoId }}),
          }});
          const raw = await res.text();
          let data = {{}};
          try {{ data = JSON.parse(raw); }} catch (_) {{}}
          if (!res.ok || !data.ok) {{
            const msg = data.error || ("Error HTTP " + res.status);
            toast(msg, "alert-triangle");
            if (status) status.textContent = msg;
            return;
          }}
          toast("Correo enviado a " + data.to, "mail");
          if (status) status.innerHTML = "Enviado a <strong>" + esc(data.to) + "</strong>. Asunto: <em>" + esc(data.subject || "") + "</em>. Revisa también spam.";
        }} catch (e) {{
          toast("Error de red al enviar el correo", "alert-triangle");
        }} finally {{
          btn.disabled = false;
          btn.innerHTML = prev;
          if (window.lucide) lucide.createIcons({{ nodes: [btn] }});
        }}
      }});
    }});
    // Actualizar textos de destino de correo
    if (currentStudent && currentStudent.email) {{
      document.querySelectorAll("[data-reto-email-hint]").forEach(el => {{
        el.innerHTML = "El correo se enviará a <strong>" + esc(currentStudent.email) + "</strong> desde <code>analizamostunegocio@gmail.com</code>.";
      }});
    }}
    initCopyButtons();
    bindProgressInputs();
    if (window.lucide) lucide.createIcons();
  }}
"""


def enhance_r2_body(html: str) -> str:
    """Replace r2 body internals while keeping tabs + emails, upgrading steps and adding enhance mount."""
    # Update steps + buttons + add email send + enhance mount before closing body
    old = """            <div class="m365-box">
              <h4><span class="app-badge">Outlook</span> Paso a paso con Copilot</h4>
              <ol>
                <li>Descarga la planilla de cronología y respuestas.</li>
                <li>En Outlook, abre Copilot y pega la cadena completa (los 4 correos).</li>
                <li>Pide primero la cronología de cambios y compromisos.</li>
                <li>Luego solicita tres borradores: respuesta técnica, ejecutiva y para usuarios.</li>
                <li>Compara tono y extensión; copia solo lo validado a la planilla.</li>
              </ol>
            </div>
            <div class="btn-group" style="margin-bottom:1rem">
              <button type="button" class="btn btn--sm btn--energy" data-planilla="cadena-correos"><i data-lucide="download" width="14" height="14"></i> Descargar planilla (Word)</button>
            </div>"""

    new = """            <div class="m365-box">
              <h4><span class="app-badge">Outlook</span> + <span class="app-badge">Word</span> Paso a paso con Copilot</h4>
              <ol>
                <li>Pulsa <strong>Enviar correo del reto a mi bandeja</strong> (cadena ST-Urb-03). Llega desde <code>analizamostunegocio@gmail.com</code>.</li>
                <li>Abre <strong>Outlook</strong> y localiza el mensaje (o usa las pestañas de la cadena en esta página).</li>
                <li>Descarga la <strong>planilla oficial</strong> y ábrela en <strong>Word</strong>.</li>
                <li>Ajusta el prompt configurable y cópialo.</li>
                <li>Con Copilot: cronología, cambios, compromisos y tres borradores (técnico, ejecutivo, usuarios).</li>
                <li>No inventes datos. Validación humana y control de calidad los completa la persona.</li>
                <li>Guarda como <code>MCP365_P02_Cadena_correos_completado.docx</code>.</li>
                <li>Después: practica con una cadena real de tu bandeja adaptando el prompt.</li>
              </ol>
            </div>
            <div class="btn-group" style="margin-bottom:0.5rem;flex-wrap:wrap;gap:0.5rem">
              <button type="button" class="btn btn--sm btn--primary" data-reto-email="r2"><i data-lucide="mail" width="14" height="14"></i> Enviar correo del reto a mi bandeja</button>
              <button type="button" class="btn btn--sm btn--energy" data-planilla="cadena-correos"><i data-lucide="download" width="14" height="14"></i> Descargar planilla oficial (Word)</button>
            </div>
            <p id="retoEmailStatus-r2" data-reto-email-hint style="margin:0 0 1rem;font-size:0.88rem;color:var(--text-muted)">El correo se enviará a tu correo de acceso desde <code>analizamostunegocio@gmail.com</code>.</p>"""

    if old not in html:
        raise SystemExit("r2 steps block not found")
    html = html.replace(old, new, 1)

    # Remove old entregable/prompt/copy; add enhance mount
    old_tail = """            <div class="entregable"><strong>Entregable:</strong> planilla con cronología, cambios, compromisos y tres borradores de respuesta (técnica, ejecutiva, usuarios), listos para revisión humana.</div>
            <div class="prompt-box" id="prompt-r2">Con la cadena de correos, elabora: 1) cronología fecha a fecha, 2) cambios respecto al plan inicial, 3) compromisos vigentes, 4) borrador de respuesta técnica, 5) borrador ejecutivo (máx. 8 líneas), 6) mensaje a usuarios (máx. 6 líneas). No inventes. Marca supuestos.</div>
            <button class="btn btn--sm btn--secondary" data-copy="#prompt-r2"><i data-lucide="copy" width="16" height="16"></i> Copiar prompt</button>
          </div>
        </article>

        <!-- RETO 3 -->"""
    new_tail = """            <div data-reto-enhance="r2"></div>
          </div>
        </article>

        <!-- RETO 3 -->"""
    if old_tail not in html:
        raise SystemExit("r2 tail not found")
    return html.replace(old_tail, new_tail, 1)


def replace_simple_reto(html: str, reto: str, old_m365: str, new_m365: str, old_tail: str, new_tail: str) -> str:
    if old_m365 not in html:
        raise SystemExit(f"{reto} m365 not found")
    html = html.replace(old_m365, new_m365, 1)
    if old_tail not in html:
        raise SystemExit(f"{reto} tail not found")
    return html.replace(old_tail, new_tail, 1)


def patch_s1_r3_to_r6(html: str) -> str:
    # R3
    html = replace_simple_reto(
        html,
        "r3",
        """            <div class="m365-box">
              <h4><span class="app-badge">Teams</span> + <span class="app-badge">Word</span> Paso a paso</h4>
              <ol>
                <li>Descarga la planilla de matriz de compromisos.</li>
                <li>Abre <strong>Microsoft Teams</strong> → Copilot (o pega la transcripción en Word con Copilot).</li>
                <li>Pega la transcripción y el prompt.</li>
                <li>Exige que separe: decisiones, propuestas, opiniones y tareas.</li>
                <li>Abre la planilla en Excel o Word y completa la matriz. Donde falte dato: “no especificado”.</li>
              </ol>
            </div>
            <div class="btn-group" style="margin-bottom:1rem">
              <button type="button" class="btn btn--sm btn--energy" data-planilla="matriz-compromisos"><i data-lucide="download" width="14" height="14"></i> Descargar planilla (Excel)</button>
            </div>""",
        """            <div class="m365-box">
              <h4><span class="app-badge">Teams</span> + <span class="app-badge">Word</span> Paso a paso con Copilot</h4>
              <ol>
                <li>Descarga la <strong>planilla oficial</strong> de matriz de compromisos.</li>
                <li>Usa la transcripción del comité de esta página (o Teams).</li>
                <li>Ajusta el prompt configurable y cópialo.</li>
                <li>En Word/Teams → Copilot, separa decisiones, propuestas, opiniones y tareas.</li>
                <li>Completa la matriz Actividad | Responsable | Fecha | Estado | Evidencia. Usa “No especificado” si falta un dato.</li>
                <li>Validación humana y control de calidad los completa la persona.</li>
                <li>Guarda como <code>MCP365_P03_Matriz_compromisos_completada.docx</code>.</li>
                <li>Después: practica con una reunión propia anonimizada.</li>
              </ol>
            </div>
            <div class="btn-group" style="margin-bottom:1rem">
              <button type="button" class="btn btn--sm btn--energy" data-planilla="matriz-compromisos"><i data-lucide="download" width="14" height="14"></i> Descargar planilla oficial (Word/Excel)</button>
            </div>""",
        """            <div class="entregable"><strong>Entregable:</strong> resumen + matriz de compromisos descargada y diligenciada + lista de propuestas no aprobadas.</div>
            <div class="prompt-box" id="prompt-r3">Analiza esta transcripción. Diferencia con claridad: decisiones confirmadas, propuestas, opiniones, preguntas y tareas asignadas. Construye una matriz con columnas: Actividad | Responsable | Fecha | Estado | Evidencia. Si un dato no aparece, escribe “no especificado”. No inventes.</div>
            <button class="btn btn--sm btn--secondary" data-copy="#prompt-r3"><i data-lucide="copy" width="16" height="16"></i> Copiar prompt</button>
          </div>
        </article>

        <!-- RETO 4 -->""",
        """            <div data-reto-enhance="r3"></div>
          </div>
        </article>

        <!-- RETO 4 -->""",
    )

    # R4
    html = replace_simple_reto(
        html,
        "r4",
        """            <div class="m365-box">
              <h4><span class="app-badge">Word</span> Paso a paso con Copilot</h4>
              <ol>
                <li>Descarga la planilla de comunicación por audiencia.</li>
                <li>Abre <strong>Word</strong> → Copilot.</li>
                <li>Pega el informe técnico y pide las tres versiones en un solo documento.</li>
                <li>Revisa que los hechos se mantengan iguales en las tres versiones.</li>
                <li>Copia cada versión a la planilla y valida extensión/tono.</li>
              </ol>
            </div>
            <div class="btn-group" style="margin-bottom:1rem">
              <button type="button" class="btn btn--sm btn--energy" data-planilla="tres-audiencias"><i data-lucide="download" width="14" height="14"></i> Descargar planilla (Word)</button>
            </div>""",
        """            <div class="m365-box">
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
            </div>""",
        """            <div class="entregable"><strong>Entregable:</strong> tres versiones en la planilla (técnica, gerencia, comunidad) con los mismos hechos y distinto nivel de detalle.</div>
            <div class="prompt-box" id="prompt-r4">A partir del informe técnico, genera tres versiones sin alterar los hechos: 1) resumen técnico, 2) resumen para gerencia (impacto, riesgo, decisión), 3) comunicación breve para comunidad. Indica al final qué información se omitió en cada versión y por qué.</div>
            <button class="btn btn--sm btn--secondary" data-copy="#prompt-r4"><i data-lucide="copy" width="16" height="16"></i> Copiar prompt</button>
          </div>
        </article>

        <!-- RETO 5 -->""",
        """            <div data-reto-enhance="r4"></div>
          </div>
        </article>

        <!-- RETO 5 -->""",
    )

    # R5
    html = replace_simple_reto(
        html,
        "r5",
        """            <div class="m365-box">
              <h4><span class="app-badge">Word</span> Paso a paso con Copilot</h4>
              <ol>
                <li>Descarga la planilla de comparación documental.</li>
                <li>En Word, pega Versión A y Versión B en el mismo documento.</li>
                <li>Usa Copilot con el prompt de comparación.</li>
                <li>Exige tabla: tema | anterior | actual | impacto | validación requerida.</li>
                <li>Marca en la planilla qué cambios requieren aprobación formal.</li>
              </ol>
            </div>
            <div class="btn-group" style="margin-bottom:1rem">
              <button type="button" class="btn btn--sm btn--energy" data-planilla="comparacion-docs"><i data-lucide="download" width="14" height="14"></i> Descargar planilla (Excel)</button>
            </div>""",
        """            <div class="m365-box">
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
            </div>""",
        """            <div class="entregable"><strong>Entregable:</strong> planilla de comparación completa, con impactos y validaciones requeridas.</div>
            <div class="prompt-box" id="prompt-r5">Compara PRO-OPS-12 v3.1 y v4.0. Identifica cambios textuales y de significado. Tabla: Tema | Versión anterior | Versión actual | Impacto posible | Validación requerida. No inventes cláusulas que no estén en el texto.</div>
            <button class="btn btn--sm btn--secondary" data-copy="#prompt-r5"><i data-lucide="copy" width="16" height="16"></i> Copiar prompt</button>
          </div>
        </article>

        <!-- RETO 6 -->""",
        """            <div data-reto-enhance="r5"></div>
          </div>
        </article>

        <!-- RETO 6 -->""",
    )

    # R6
    html = replace_simple_reto(
        html,
        "r6",
        """            <div class="m365-box">
              <h4><span class="app-badge">Excel</span> Paso a paso con Copilot</h4>
              <ol>
                <li>Descarga la planilla de priorización (ya trae las 10 tareas).</li>
                <li>Ábrela en <strong>Excel</strong> → Copilot.</li>
                <li>Pide clasificar por urgencia/impacto, proponer agenda del día y marcar delegables.</li>
                <li>Identifica qué tareas exigen criterio humano (no automatizar la decisión).</li>
                <li>Guarda tu versión priorizada en OneDrive/SharePoint.</li>
              </ol>
            </div>
            <div class="btn-group" style="margin-bottom:1rem">
              <button type="button" class="btn btn--sm btn--energy" data-planilla="priorizacion"><i data-lucide="download" width="14" height="14"></i> Descargar planilla (Excel)</button>
            </div>""",
        """            <div class="m365-box">
              <h4><span class="app-badge">Excel</span> Paso a paso con Copilot</h4>
              <ol>
                <li>Descarga la <strong>base del ejercicio</strong> (10 tareas).</li>
                <li>Ábrela en <strong>Excel → Copilot</strong>.</li>
                <li>Ajusta el prompt configurable y cópialo.</li>
                <li>Clasifica por urgencia/impacto; agenda hoy/mañana; marca delegables vs criterio humano.</li>
                <li>No inventes fechas ni responsables. Validación humana y control de calidad los completa la persona.</li>
                <li>Guarda como <code>MCP365_P06_Priorizacion_completada.xlsx</code>.</li>
                <li>Después: prioriza tu propia lista de tareas del día (sin datos sensibles).</li>
              </ol>
            </div>
            <div class="btn-group" style="margin-bottom:1rem">
              <button type="button" class="btn btn--sm btn--energy" data-planilla="priorizacion"><i data-lucide="download" width="14" height="14"></i> Descargar base del ejercicio (Excel)</button>
            </div>""",
        """            <div class="entregable"><strong>Entregable:</strong> planilla Excel priorizada + agenda propuesta + lista de tareas delegables vs. criterio humano.</div>
            <div class="prompt-box" id="prompt-r6">Con esta lista de tareas, clasifica por urgencia e impacto, propone una agenda realista para hoy y mañana, marca qué se puede delegar y qué requiere criterio humano. Explica supuestos. No inventes fechas ni responsables nuevos.</div>
            <button class="btn btn--sm btn--secondary" data-copy="#prompt-r6"><i data-lucide="copy" width="16" height="16"></i> Copiar prompt</button>
          </div>
        </article>

        <!-- AUTOEVALUACIÓN S1 -->""",
        """            <div data-reto-enhance="r6"></div>
          </div>
        </article>

        <!-- AUTOEVALUACIÓN S1 -->""",
    )
    return html


def patch_s2(html: str) -> str:
    """Append enhance mounts and improve steps for F1-F8 without removing widgets."""
    replacements = [
        (
            """              <p>Elabora: objetivo, justificación, alcance, exclusiones, entregables, supuestos, restricciones, interesados, información faltante y preguntas de validación.</p>
              <div class="prompt-box" id="prompt-f1">Rol: actúa como analista de proyectos energéticos. Contexto: expediente del Proyecto Horizonte (capacitación operativa). Tarea: construir un brief de comprensión del proyecto usando solo los documentos suministrados. Criterios: no inventar; separar hechos de supuestos; listar vacíos. Formato: secciones numeradas. Verificación: marca cada ítem como ‘evidenciado’ o ‘no especificado’.</div>
              <button class="btn btn--sm btn--secondary" data-copy="#prompt-f1"><i data-lucide="copy" width="16" height="16"></i> Copiar prompt avanzado</button>
            </div>
          </article>""",
            """              <p>Elabora: objetivo, justificación, alcance, exclusiones, entregables, supuestos, restricciones, interesados, información faltante y preguntas de validación.</p>
              <div data-reto-enhance="fase-1"></div>
            </div>
          </article>""",
        ),
        (
            """              <div class="disclaimer disclaimer--danger">
                <i data-lucide="shield-alert" width="18" height="18"></i>
                <span>Copilot puede proponer una estructura, pero las fechas, dependencias y responsabilidades deben validarse con el equipo del proyecto.</span>
              </div>
            </div>
          </article>

          <article class="reto">
            <button class="reto__header" aria-expanded="false">
              <span class="reto__title-wrap"><span class="reto__num">F3</span><span><strong>Analizar riesgos</strong></span></span>""",
            """              <div class="disclaimer disclaimer--danger">
                <i data-lucide="shield-alert" width="18" height="18"></i>
                <span>Copilot puede proponer una estructura, pero las fechas, dependencias y responsabilidades deben validarse con el equipo del proyecto.</span>
              </div>
              <div data-reto-enhance="fase-2"></div>
            </div>
          </article>

          <article class="reto">
            <button class="reto__header" aria-expanded="false">
              <span class="reto__title-wrap"><span class="reto__num">F3</span><span><strong>Analizar riesgos</strong></span></span>""",
        ),
        (
            """                  <tbody id="riskBody"></tbody>
                </table>
              </div>
            </div>
          </article>

          <article class="reto">
            <button class="reto__header" aria-expanded="false">
              <span class="reto__title-wrap"><span class="reto__num">F4</span><span><strong>Gestionar interesados</strong></span></span>""",
            """                  <tbody id="riskBody"></tbody>
                </table>
              </div>
              <div data-reto-enhance="fase-3"></div>
            </div>
          </article>

          <article class="reto">
            <button class="reto__header" aria-expanded="false">
              <span class="reto__title-wrap"><span class="reto__num">F4</span><span><strong>Gestionar interesados</strong></span></span>""",
        ),
        (
            """              <div class="stakeholder-map" id="stakeMap" aria-label="Mapa de poder e interés">
                <span class="stakeholder-map__label stakeholder-map__label--top">Alta influencia</span>
                <span class="stakeholder-map__label stakeholder-map__label--bottom">Baja influencia</span>
                <span class="stakeholder-map__label stakeholder-map__label--left">Bajo interés</span>
                <span class="stakeholder-map__label stakeholder-map__label--right">Alto interés</span>
              </div>
            </div>
          </article>

          <article class="reto">
            <button class="reto__header" aria-expanded="false">
              <span class="reto__title-wrap"><span class="reto__num">F5</span><span><strong>Analizar el avance</strong></span></span>""",
            """              <div class="stakeholder-map" id="stakeMap" aria-label="Mapa de poder e interés">
                <span class="stakeholder-map__label stakeholder-map__label--top">Alta influencia</span>
                <span class="stakeholder-map__label stakeholder-map__label--bottom">Baja influencia</span>
                <span class="stakeholder-map__label stakeholder-map__label--left">Bajo interés</span>
                <span class="stakeholder-map__label stakeholder-map__label--right">Alto interés</span>
              </div>
              <div data-reto-enhance="fase-4"></div>
            </div>
          </article>

          <article class="reto">
            <button class="reto__header" aria-expanded="false">
              <span class="reto__title-wrap"><span class="reto__num">F5</span><span><strong>Analizar el avance</strong></span></span>""",
        ),
        (
            """                <div class="field"><label for="av6">¿Qué decisiones requiere el comité?</label><textarea id="av6" data-store="avance.q6"></textarea></div>
              </div>
            </div>
          </article>

          <article class="reto">
            <button class="reto__header" aria-expanded="false">
              <span class="reto__title-wrap"><span class="reto__num">F6</span><span><strong>Evento crítico</strong></span></span>""",
            """                <div class="field"><label for="av6">¿Qué decisiones requiere el comité?</label><textarea id="av6" data-store="avance.q6"></textarea></div>
              </div>
              <div data-reto-enhance="fase-5"></div>
            </div>
          </article>

          <article class="reto">
            <button class="reto__header" aria-expanded="false">
              <span class="reto__title-wrap"><span class="reto__num">F6</span><span><strong>Evento crítico</strong></span></span>""",
        ),
        (
            """                    <tr><td>Decisión clave</td><td>Forzar recuperación</td><td>Rebaseline parcial</td><td>Aprobar bridge + plan B</td></tr>
                  </tbody>
                </table>
              </div>
            </div>
          </article>

          <article class="reto">
            <button class="reto__header" aria-expanded="false">
              <span class="reto__title-wrap"><span class="reto__num">F7</span><span><strong>Comité directivo</strong></span></span>""",
            """                    <tr><td>Decisión clave</td><td>Forzar recuperación</td><td>Rebaseline parcial</td><td>Aprobar bridge + plan B</td></tr>
                  </tbody>
                </table>
              </div>
              <div data-reto-enhance="fase-6"></div>
            </div>
          </article>

          <article class="reto">
            <button class="reto__header" aria-expanded="false">
              <span class="reto__title-wrap"><span class="reto__num">F7</span><span><strong>Comité directivo</strong></span></span>""",
        ),
        (
            """                <div class="slide"><span class="slide__num">08</span><h4>Próximos 14 días</h4><p>Dueños, fechas, validaciones</p></div>
              </div>
            </div>
          </article>

          <article class="reto">
            <button class="reto__header" aria-expanded="false">
              <span class="reto__title-wrap"><span class="reto__num">F8</span><span><strong>Lecciones aprendidas vs oferta de proyecto</strong></span></span>""",
            """                <div class="slide"><span class="slide__num">08</span><h4>Próximos 14 días</h4><p>Dueños, fechas, validaciones</p></div>
              </div>
              <div data-reto-enhance="fase-7"></div>
            </div>
          </article>

          <article class="reto">
            <button class="reto__header" aria-expanded="false">
              <span class="reto__title-wrap"><span class="reto__num">F8</span><span><strong>Lecciones aprendidas vs oferta de proyecto</strong></span></span>""",
        ),
    ]
    for old, new in replacements:
        if old not in html:
            raise SystemExit(f"S2 block not found: {old[:80]}...")
        html = html.replace(old, new, 1)

    # F8: replace dual prompts with enhance mount
    start = html.find('<div class="prompt-box" id="prompt-f8a">')
    end_btn = html.find('id="prompt-f8b"')
    if start < 0 or end_btn < 0:
        raise SystemExit("F8 prompts not found")
    end = html.find("</button>", end_btn)
    if end < 0:
        raise SystemExit("F8b button end not found")
    end = end + len("</button>")
    pre = html.rfind('<div class="entregable">', 0, start)
    wrap = html.rfind("leccionesTableWrap", 0, start)
    if pre > 0 and pre > wrap:
        # include entregable + prompt labels
        label = html.rfind("<p><strong>Prompt 1", 0, start)
        start = pre if label < 0 else min(pre, label)
    html = html[:start] + '<div data-reto-enhance="fase-8"></div>\n            ' + html[end:]
    return html


def patch_index():
    html = INDEX.read_text(encoding="utf-8")
    html = fix_n14_dates(html)
    # Fix r1 status text if wrong
    html = html.replace(
        "desde <code>analizamostunegocio@gmail.com</code> desde",
        "desde",
    )
    html = enhance_r2_body(html)
    html = patch_s1_r3_to_r6(html)
    html = patch_s2(html)

    engine = build_engine_js()
    # Fix join newline in engine - use real \n in JS
    engine = engine.replace('.join("\\n")', '.join("\\n")')  # already correct from f-string... 
    # In build_engine_js I used lines.join("\\n") inside an f-string - that becomes .join("\n") in output? 
    # f""" ... join("\\n") ...""" -> join("\n") in file. Good.

    anchor = "  function initPromptR1Editor() {"
    if anchor not in html:
        raise SystemExit("initPromptR1Editor not found")
    html = html.replace(anchor, engine + "\n" + anchor, 1)

    boot = "    initPromptR1Editor();\n"
    if boot not in html:
        raise SystemExit("boot initPromptR1Editor not found")
    html = html.replace(boot, boot + "    initRetoEngine();\n", 1)

    # Fix r1 email hint wording in JS
    html = html.replace(
        'r1Status.innerHTML = `El correo se enviará a: <strong>${esc(currentStudent.email)}</strong> desde <code>analizamostunegocio@gmail.com</code>.`;',
        'r1Status.innerHTML = `El correo se enviará a <strong>${esc(currentStudent.email)}</strong> (tu correo de acceso) desde <code>analizamostunegocio@gmail.com</code>.`;',
    )

    # Update default r1 date fields in prompt config
    html = html.replace("sábado 22/03/2026", "sábado 21/03/2026")
    html = html.replace("sábado 29/03/2026", "sábado 28/03/2026")
    html = html.replace("martes 18/03/2026", "martes 17/03/2026")

    INDEX.write_text(html, encoding="utf-8")
    print("index.html patched")


def patch_app():
    text = APP.read_text(encoding="utf-8")
    text = fix_n14_dates(text)

    # Add multi-reto email bodies and generic endpoint if not present
    if "def get_reto_email_content" not in text:
        helper = '''
def get_reto_email_content(reto_id: str, to_email: str, name: str, smtp_email: str) -> tuple[str, str]:
    """Contenido centralizado de correos simulados por reto."""
    reto_id = (reto_id or "r1").strip().lower()
    if reto_id in ("r1", "reto1", "reto-1"):
        return _reto1_email_content(to_email, name, smtp_email)

    if reto_id in ("r2", "reto2", "reto-2"):
        subject = "Cadena ST-Urb-03 · Programación y cambios de ventana (Reto 2)"
        body = f"""Hola {name},

Este mensaje simula la cadena de correos del Reto 2 · Misión Copilot 365.

--- Correo 1 · 01/03/2026 · Planeación de Mantenimiento ---
Asunto: Programación transformador auxiliar ST-Urb-03
Se confirma mantenimiento del transformador auxiliar para el 12/03/2026, 08:00–14:00.
Compromiso: notificar a usuarios con mínimo 72 horas de anticipación.
Responsable de aviso: Comunicaciones Zona.

--- Correo 2 · 04/03/2026 · Logística de Materiales ---
Asunto: RE: adelanto de repuestos
El proveedor confirma entrega anticipada. Se propone adelantar la ventana al 10/03/2026.
Pendiente: validar disponibilidad de personal de seguridad industrial para esa fecha.

--- Correo 3 · 06/03/2026 · Seguridad Industrial ---
Asunto: RE: personal 10/03
Se confirma personal para el 10/03. Se solicita ampliar el cierre de área hasta las 16:00.
Riesgo: señalización insuficiente si no se refuerza perímetro antes de las 07:30.

--- Correo 4 · 07/03/2026 · Gerencia de Zona Norte ---
Asunto: Aprobación ventana 10/03
Se aprueba intervención el 10/03 con cierre hasta 16:00.
Solicita: 1) mensaje claro a la comunidad, 2) reporte ejecutivo al cierre de la jornada.

---
Simulación formativa · Reto 2
Remitente técnico: {smtp_email}
Destinatario: {name} <{to_email}>
La planilla se descarga en la plataforma (no va adjunta).
"""
        return subject, body

    return "", ""


def send_reto_email(reto_id: str, to_email: str, name: str) -> tuple[bool, str]:
    smtp_email, smtp_password, _, _ = _smtp_config()
    subject, body = get_reto_email_content(reto_id, to_email, name, smtp_email)
    if not subject or not body:
        return False, f"No hay correo simulado configurado para el reto '{reto_id}'."

    from_display = f"Misión Copilot 365 · Simulación <{smtp_email}>"
    if (reto_id or "").lower() in ("r1", "reto1", "reto-1"):
        from_display = f"Laura Méndez · Coordinación de Campo <{smtp_email}>"

    errors: list[str] = []
    if (os.getenv("EMAIL_WEBHOOK_URL") or "").strip():
        ok, detail = _send_email_webhook(to_email, name, subject, body)
        if ok:
            return True, detail
        errors.append(detail)
    if (os.getenv("RESEND_API_KEY") or "").strip():
        ok, detail = _send_email_resend(to_email, subject, body)
        if ok:
            return True, detail
        errors.append(detail)
    if smtp_password:
        ok, detail = _send_email_smtp(to_email, subject, body, from_display)
        if ok:
            return True, detail
        errors.append(detail)
    else:
        errors.append("Falta SMTP_APP_PASSWORD en .env")
    return False, " · ".join(errors) if errors else "No hay método de envío configurado"

'''
        # Insert before send_reto1_email and make send_reto1_email call send_reto_email
        text = text.replace(
            "def send_reto1_email(to_email: str, name: str) -> tuple[bool, str]:\n"
            '    """Envía el correo operativo del Reto 1. Prioriza HTTPS (webhook/Resend) y luego SMTP."""\n',
            helper
            + "def send_reto1_email(to_email: str, name: str) -> tuple[bool, str]:\n"
            '    """Envía el correo operativo del Reto 1. Prioriza HTTPS (webhook/Resend) y luego SMTP."""\n'
            "    return send_reto_email('r1', to_email, name)\n\n"
            "def send_reto1_email_legacy_unused(to_email: str, name: str) -> tuple[bool, str]:\n"
            '    """Legacy body kept for reference — not used."""\n',
            1,
        )

    if "/api/reto/send-email" not in text:
        endpoint = '''
@app.post("/api/reto/send-email")
@require_student
def api_send_reto_email():
    """Envía el correo simulado del reto indicado al estudiante autenticado."""
    payload = request.get_json(silent=True) or {}
    reto_id = (payload.get("reto_id") or request.args.get("reto_id") or "r1").strip().lower()
    to_email = (session.get("student_email") or "").strip()
    name = (session.get("student_name") or "Participante").strip()
    if not to_email:
        return jsonify({"ok": False, "error": "No hay correo en la sesión. Vuelve a iniciar sesión."}), 400

    now = datetime.now(timezone.utc).timestamp()
    key = f"reto_email_at_{reto_id}"
    last = float(session.get(key) or 0)
    wait = 90 - int(now - last)
    if wait > 0:
        return jsonify({"ok": False, "error": f"Espera {wait} s antes de reenviar este reto."}), 429

    ok, detail = send_reto_email(reto_id, to_email, name)
    if not ok:
        return jsonify({"ok": False, "error": detail}), 502

    session[key] = now
    subject, _ = get_reto_email_content(reto_id, to_email, name, os.getenv("SMTP_EMAIL", "analizamostunegocio@gmail.com"))
    return jsonify({
        "ok": True,
        "message": detail,
        "to": to_email,
        "from": os.getenv("SMTP_EMAIL", "analizamostunegocio@gmail.com"),
        "subject": subject,
        "reto_id": reto_id,
    })


'''
        text = text.replace(
            "@app.post(\"/api/reto1/send-email\")",
            endpoint + "@app.post(\"/api/reto1/send-email\")",
            1,
        )

    # Fix fase-8 in calc_percent
    text = text.replace(
        '"fase-1", "fase-2", "fase-3", "fase-4", "fase-5", "fase-6", "fase-7",',
        '"fase-1", "fase-2", "fase-3", "fase-4", "fase-5", "fase-6", "fase-7", "fase-8",',
    )

    APP.write_text(text, encoding="utf-8")
    print("app.py patched")


def main():
    patch_index()
    patch_app()
    # Verify
    html = INDEX.read_text(encoding="utf-8")
    for key in ["data-reto-enhance=\"r2\"", "data-reto-enhance=\"r6\"", "data-reto-enhance=\"fase-1\"",
                "data-reto-enhance=\"fase-8\"", "initRetoEngine", "sábado 21/03/2026"]:
        if key not in html:
            print("MISSING in index:", key)
        else:
            print("OK", key)
    app = APP.read_text(encoding="utf-8")
    for key in ["get_reto_email_content", "/api/reto/send-email", "21/03/2026"]:
        print("APP", key, key in app)


if __name__ == "__main__":
    main()
