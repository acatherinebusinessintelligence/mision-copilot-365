# -*- coding: utf-8 -*-
"""Datos PRISM de la Sesión 2 (Proyecto Horizonte) para embeber en index.html."""

from __future__ import annotations

COMMON_FORMAT_BLOCK = """\
======================================================================
ENTREGABLE FINAL
======================================================================

Tu respuesta NO debe ser un resumen conversacional.

Debes elaborar un documento ejecutivo completo, listo para copiar directamente a Microsoft Word y posteriormente exportar a PDF sin necesidad de reorganizar el contenido.

Imagina que este documento será entregado al Comité Directivo como insumo para la toma de decisiones.

Debe tener calidad equivalente a un informe elaborado por una firma internacional de consultoría.

======================================================================
ESTRUCTURA OBLIGATORIA DEL DOCUMENTO
======================================================================

# Portada

Incluye:

• Título del documento.
• Nombre del proyecto.
• Objetivo del informe.
• Fecha del análisis (si no aparece en las fuentes escribe "PENDIENTE DE VALIDACIÓN").
• Documentos analizados.
• Estado del documento.

======================================================================

# Tabla de Contenido

Genera automáticamente el índice de las secciones principales.

======================================================================

# Resumen Ejecutivo

Entre 200 y 300 palabras.

Debe permitir que un directivo comprenda el resultado sin leer el resto del documento.

======================================================================

# Objetivo del análisis

Explica qué se evaluó.

Qué documentos fueron utilizados.

Qué limitaciones existen.

======================================================================

# Alcance del análisis

Indica claramente:

Qué se analizó.

Qué NO se analizó.

Qué información quedó fuera del alcance.

======================================================================

# Desarrollo del análisis

Organiza toda la información mediante:

• Tablas profesionales.
• Matrices.
• Cuadros comparativos.
• Listas jerarquizadas.
• Semáforos de criticidad.
• Cuadros de observaciones.

Evita bloques largos de texto.

Cada afirmación relevante debe etiquetarse como: Hecho confirmado | Inferencia | Información pendiente | Recomendación.

======================================================================

# Hallazgos principales

Presenta únicamente los hallazgos relevantes.

Para cada uno indica:

• Hallazgo.
• Evidencia.
• Impacto.
• Nivel de criticidad.
• Acción recomendada.

======================================================================

# Riesgos

Construye una tabla con:

• Riesgo.
• Evidencia.
• Probabilidad.
• Impacto.
• Criticidad.
• Recomendación.

Usa semáforos 🔴 Alto / 🟡 Medio / 🟢 Bajo cuando aplique.

======================================================================

# Información pendiente de validación

Genera una tabla específica indicando:

• Información faltante.
• Impacto.
• Fuente esperada.
• Prioridad.

======================================================================

# Recomendaciones

Presenta una tabla con:

• Acción.
• Responsable sugerido (solo si aparece en las fuentes; de lo contrario indicar el rol y marcar "PENDIENTE DE VALIDACIÓN").
• Prioridad.
• Justificación.

======================================================================

# Próximos pasos

Lista ordenada de actividades sugeridas.

======================================================================

# Conclusiones

Máximo cinco conclusiones.

Deben ser claras, ejecutivas y sustentadas.

======================================================================

# Validación Humana

Finaliza con una lista de verificación indicando qué aspectos deben revisarse antes de presentar el documento al Comité Directivo.

======================================================================
FORMATO DEL DOCUMENTO
======================================================================

El documento debe poder copiarse directamente a Microsoft Word conservando una estructura profesional.

Utiliza:

• Encabezados jerárquicos (# ## ###).
• Tablas Markdown.
• Listas numeradas.
• Listas con viñetas.
• Separadores entre secciones.
• Iconos discretos únicamente cuando aporten claridad.

No utilices lenguaje conversacional.
No escribas párrafos excesivamente largos.
No abras con frases del tipo «Claro», «Por supuesto», «Aquí tienes un resumen» o similares.

======================================================================
CRITERIOS DE CALIDAD
======================================================================

Antes de finalizar verifica que:

✓ Toda afirmación tenga evidencia.
✓ No existan datos inventados.
✓ Hechos, inferencias y recomendaciones estén claramente diferenciados.
✓ Toda información faltante esté marcada como "PENDIENTE DE VALIDACIÓN".
✓ El documento pueda convertirse directamente en un informe PDF para presentación ejecutiva."""


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
    include_format: bool = True,
    include_validation: bool = True,
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
    if include_validation:
        parts.extend(["", COMMON_VALIDATION_BLOCK])
    if include_format:
        parts.extend(["", COMMON_FORMAT_BLOCK])
    return "\n".join(parts)


# Prompt oficial Caso 7 · Comité (PowerPoint con plantilla; sin Word/PDF)
F7_PPTX_PROMPT = """\
P → PERSONA

Actúa como socio senior de comunicación ejecutiva, dirección de proyectos y diseño de presentaciones corporativas para comités directivos.

Combina las capacidades de:

- Director de PMO.
- Consultor estratégico.
- Analista de información.
- Storyteller ejecutivo.
- Diseñador senior de presentaciones corporativas.

Tu responsabilidad es transformar la información validada del Proyecto Horizonte en una presentación ejecutiva clara, visual, elegante y lista para exponer ante la alta dirección.

R → REALIDAD

La Gerencia presentará el Proyecto Horizonte en un espacio corto de comité.

La audiencia necesita comprender rápidamente:

- Por qué existe la iniciativa.
- Qué se propone.
- Cuál es su alcance.
- Cuál es el estado actual.
- Qué muestran el presupuesto y el cronograma.
- Cuáles son los riesgos prioritarios.
- Qué información continúa pendiente.
- Qué decisiones debe tomar el comité.
- Cuáles son los siguientes pasos.

La presentación debe permitir tomar decisiones sin revisar previamente todos los documentos fuente.

No debe presentar la iniciativa como aprobada.

I → INFORMACIÓN Y FUENTES AUTORIZADAS

Utiliza exclusivamente los siguientes archivos seleccionados o cargados en esta conversación:

1. 02_Alcance_Proyecto_Horizonte.docx
2. 03_Presupuesto_y_Cronograma_Horizonte.xlsx
3. 04_Transcripcion_Reunion_Horizonte.docx
4. 05_Registro_Inicial_Riesgos_Horizonte.xlsx
5. 06_Comentarios_Interesados_Horizonte.docx
6. 07_Plantilla_Comite_Horizonte.pptx

REGLA CRÍTICA DE FUENTES

Antes de crear la presentación:

1. Confirma que puedes acceder al contenido de los archivos 02 al 06.
2. Confirma que puedes abrir y utilizar visualmente la plantilla:
   07_Plantilla_Comite_Horizonte.pptx.
3. No consideres analizado un archivo únicamente porque reconoces su nombre.
4. No utilices información externa.
5. No mezcles información de otros casos o sesiones.
6. No utilices el correo del Circuito N-14.
7. Si un archivo no está disponible, indícalo como:
   “NO DISPONIBLE PARA ANÁLISIS”.
8. Si falta un dato, utiliza:
   “PENDIENTE DE VALIDACIÓN”.

USO OBLIGATORIO DE LA PLANTILLA

Debes crear la presentación utilizando como base visual el archivo:

07_Plantilla_Comite_Horizonte.pptx

No diseñes una presentación genérica desde cero.

Conserva de la plantilla:

- Logotipos.
- Colores corporativos.
- Tipografías.
- Fondos.
- Formas.
- Encabezados.
- Pies de página.
- Márgenes.
- Jerarquía visual.
- Estilo de títulos.
- Numeración.
- Distribución general.

No alteres, deformes, recortes ni recolorees los logotipos.

No elimines elementos institucionales de la plantilla.

Puedes reorganizar cajas de texto, gráficos y elementos internos cuando sea necesario para mejorar la comunicación, pero debes conservar la identidad visual original.

S → SOLICITUD

Genera directamente un archivo de Microsoft PowerPoint editable denominado:

Presentacion_Comite_Proyecto_Horizonte.pptx

No entregues únicamente:

- Un guion.
- Una lista de diapositivas.
- Un documento Word.
- Un PDF.
- Un resumen conversacional.
- Instrucciones para que el usuario arme la presentación.

Debes crear el archivo `.pptx` completo y listo para descarga.

La presentación debe contener exactamente ocho diapositivas principales y, únicamente si es necesario, un máximo de tres diapositivas adicionales de anexo.

OBJETIVO DE COMUNICACIÓN

La presentación debe responder de forma visual y ejecutiva:

1. ¿Qué problema o necesidad origina el proyecto?
2. ¿Qué se propone realizar?
3. ¿Qué está incluido y qué está excluido?
4. ¿Cuál es el estado del presupuesto y del cronograma?
5. ¿Cuáles son los riesgos prioritarios?
6. ¿Qué inconsistencias o vacíos existen?
7. ¿Qué decisiones necesita tomar el comité?
8. ¿Qué debe ocurrir después?

M → MÉTODO

FASE 1 · VALIDACIÓN PREVIA

Antes de generar el archivo:

- Verifica las fuentes.
- Identifica cifras, fechas, hitos y riesgos respaldados.
- Separa hechos, cálculos, inferencias y recomendaciones.
- Comprueba que la plantilla esté disponible.
- No generes la presentación hasta confirmar estas condiciones.

FASE 2 · STORYLINE EJECUTIVO

Construye una narrativa progresiva:

Necesidad
→ Propuesta
→ Alcance
→ Situación actual
→ Presupuesto y cronograma
→ Riesgos
→ Decisiones
→ Próximos pasos

Cada diapositiva debe desarrollar una sola idea principal.

No conviertas las diapositivas en páginas de informe.

ESTRUCTURA OBLIGATORIA DE LAS 8 DIAPOSITIVAS

DIAPOSITIVA 1 · PORTADA

Título:

Proyecto Horizonte

Subtítulo:

Revisión inicial para Comité Directivo

Incluye:

- Propósito de la presentación.
- Fecha del análisis, solo si aparece en las fuentes.
- Estado:
  “Iniciativa en evaluación”.
- Nota discreta:
  “Caso académico ficticio”.

Utiliza la portada oficial de la plantilla.

DIAPOSITIVA 2 · CONTEXTO Y NECESIDAD

Objetivo:

Explicar por qué surge la iniciativa.

Incluye:

- Necesidad identificada.
- Problema que se busca resolver.
- Impacto esperado.
- Área solicitante.
- Restricciones relevantes.

Diseño recomendado:

- Un mensaje central destacado.
- Máximo tres bloques visuales.
- Íconos discretos.
- No más de 45 palabras visibles.

DIAPOSITIVA 3 · OBJETIVO, ALCANCE Y EXCLUSIONES

Incluye:

- Objetivo general.
- Alcance incluido.
- Exclusiones.
- Entregables principales.
- Supuestos o dependencias críticas.

Diseño recomendado:

- Dos columnas:
  “Incluye” y “No incluye”.
- Una franja inferior para entregables.
- Diferenciar hechos de elementos pendientes.

DIAPOSITIVA 4 · HITOS Y CRONOGRAMA

Incluye:

- Principales fases.
- Hitos.
- Fechas relevantes.
- Dependencias.
- Actividades críticas.
- Desviaciones o vacíos.

Diseño recomendado:

- Línea de tiempo.
- No usar una tabla extensa.
- Marcar fechas pendientes como:
  “PENDIENTE DE VALIDACIÓN”.
- Resaltar hitos críticos.

DIAPOSITIVA 5 · PRESUPUESTO Y DISTRIBUCIÓN

Incluye únicamente cifras verificadas del archivo Excel:

- Presupuesto total.
- Principales categorías.
- Tres partidas de mayor valor.
- Participación porcentual.
- Hallazgos financieros.
- Vacíos o anomalías.

Diseño recomendado:

- Gráfico de barras o dona.
- Tarjeta de cifra principal.
- Máximo tres hallazgos.
- Indicar la fuente debajo del gráfico.

No inventes cálculos.

No generes cifras si no están disponibles.

DIAPOSITIVA 6 · RIESGOS PRIORITARIOS

Selecciona máximo cinco riesgos relevantes.

Para cada uno muestra:

- Riesgo.
- Categoría.
- Probabilidad.
- Impacto.
- Nivel.
- Acción sugerida.
- Fuente.

Usa semáforos:

- 🔴 Alto.
- 🟡 Medio.
- 🟢 Bajo.

Diseño recomendado:

- Matriz de calor o tarjetas.
- No presentar una tabla de texto saturada.
- Aclarar:
  “Valoración preliminar sujeta a validación”.

DIAPOSITIVA 7 · HALLAZGOS Y DECISIONES REQUERIDAS

Divide la diapositiva en dos secciones:

A. Hallazgos relevantes

- Inconsistencias entre fuentes.
- Información faltante.
- Decisiones o compromisos no confirmados.
- Restricciones.

B. Decisiones requeridas del comité

Incluye únicamente decisiones realmente necesarias, por ejemplo:

- Validar el avance a la siguiente fase.
- Solicitar información adicional.
- Confirmar patrocinio.
- Definir responsables.
- Validar criterios de alcance.

No conviertas recomendaciones en decisiones aprobadas.

DIAPOSITIVA 8 · PRÓXIMOS PASOS

Incluye:

- Acciones inmediatas.
- Responsable sugerido por rol.
- Prioridad.
- Resultado esperado.
- Validaciones antes de continuar.

Cierra con un mensaje ejecutivo:

“Copilot organiza y acelera el análisis; la organización valida y decide.”

Diseño recomendado:

- Hoja de ruta de 3 a 5 pasos.
- Cierre visual limpio.
- Una sola llamada a la acción.

ANEXOS OPCIONALES

Utiliza anexos únicamente cuando aporten valor.

Máximo tres:

- Anexo 1: Fuentes utilizadas por diapositiva.
- Anexo 2: Matriz ampliada de riesgos.
- Anexo 3: Información pendiente de validación.

No dupliques el contenido de las diapositivas principales.

REQUISITOS DE DISEÑO

La presentación debe verse como un producto de comunicación ejecutiva de alta calidad.

Debe ser:

- Elegante.
- Moderna.
- Corporativa.
- Limpia.
- Visual.
- Consistente.
- Sobria.
- Fácil de leer en una pantalla grande.

Aplica estas reglas:

- Una idea principal por diapositiva.
- Máximo 35 a 50 palabras visibles por diapositiva, salvo tablas breves.
- Máximo cuatro mensajes secundarios.
- Títulos con conclusión, no títulos genéricos.
- Evitar párrafos extensos.
- Evitar diapositivas saturadas.
- Evitar tablas con demasiadas filas.
- Utilizar espacio en blanco.
- Respetar alineación y márgenes.
- Mantener tamaños de fuente legibles.
- Utilizar gráficos únicamente cuando comuniquen mejor que el texto.
- No usar imágenes decorativas sin propósito.
- No usar fotografías genéricas de bancos de imágenes.
- No utilizar emojis como elemento central.
- No agregar animaciones excesivas.
- No crear estilos diferentes entre diapositivas.

TÍTULOS CON MENSAJE

Evita títulos como:

- Presupuesto.
- Riesgos.
- Cronograma.
- Conclusiones.

Utiliza títulos que expresen un hallazgo, por ejemplo:

- “La inversión se concentra en tres componentes principales”.
- “Cinco riesgos requieren validación antes de avanzar”.
- “El cronograma depende de información aún no confirmada”.
- “El comité debe resolver tres decisiones para habilitar la siguiente fase”.

Solo utiliza estas conclusiones cuando estén respaldadas por las fuentes.

GRÁFICOS Y ELEMENTOS VISUALES

Cuando los datos lo permitan:

- Utiliza barras para comparar partidas.
- Utiliza dona para distribución porcentual.
- Utiliza línea de tiempo para cronograma.
- Utiliza matriz de calor para riesgos.
- Utiliza tarjetas KPI para cifras principales.
- Utiliza diagramas de flujo simples para próximos pasos.

Todos los gráficos deben:

- Ser editables.
- Tener título.
- Tener etiquetas legibles.
- Mostrar unidad.
- Indicar la fuente.
- Coincidir con el Excel.
- Respetar la paleta de la plantilla.

No conviertas tablas o gráficos en imágenes.

NOTAS DEL PRESENTADOR

Incluye notas completas en cada diapositiva.

Las notas deben contener:

- Propósito de la diapositiva.
- Mensaje que debe comunicar el presentador.
- Explicación de cifras.
- Fuente utilizada.
- Advertencias.
- Preguntas probables del comité.
- Tiempo sugerido de exposición.

Extensión por diapositiva:

Entre 80 y 150 palabras.

No copies literalmente el texto visible de la diapositiva.

TRAZABILIDAD

Cada diapositiva debe identificar discretamente su fuente, por ejemplo:

Fuente: 03_Presupuesto_y_Cronograma_Horizonte.xlsx · Hoja Presupuesto

En las notas del presentador incluye la trazabilidad completa:

- Archivo.
- Hoja o sección.
- Dato utilizado.
- Clasificación:
  - Hecho confirmado.
  - Cálculo.
  - Inferencia.
  - Recomendación.
  - Información pendiente.

CHECKLIST DE CALIDAD

Antes de generar el archivo, verifica:

1. Todas las cifras coinciden con el Excel.
2. Todas las fechas tienen fuente.
3. Los riesgos tienen respaldo documental.
4. Las decisiones se diferencian de las propuestas.
5. Los responsables no fueron inventados.
6. Los datos faltantes están marcados.
7. La presentación no afirma aprobación.
8. La plantilla fue utilizada realmente.
9. Los logotipos no fueron alterados.
10. Los colores coinciden con la plantilla.
11. Los gráficos son editables.
12. Las notas están incluidas.
13. La presentación puede entenderse sin leer los documentos fuente.
14. El archivo no contiene textos provisionales.
15. No existen diapositivas vacías.
16. No existen elementos desalineados.
17. No hay texto cortado o fuera de los márgenes.
18. La presentación está lista para exposición.

RESTRICCIONES

- No generar un documento Word.
- No generar un PDF como producto principal.
- No entregar solo el guion.
- No entregar únicamente recomendaciones.
- No explicar cómo construir la presentación.
- No crear una presentación genérica.
- No ignorar la plantilla.
- No sustituir la plantilla por otro diseño.
- No inventar cifras.
- No inventar fechas.
- No inventar responsables.
- No inventar decisiones.
- No analizar información externa.
- No presentar el proyecto como aprobado.
- No reducir todo el contenido a texto.
- No copiar el informe completo dentro de las diapositivas.

ENTREGABLE FINAL

Genera directamente el archivo editable:

Presentacion_Comite_Proyecto_Horizonte.pptx

El archivo debe contener:

- Las ocho diapositivas principales.
- Los anexos que sean estrictamente necesarios.
- Notas del presentador.
- Gráficos editables.
- Fuentes por diapositiva.
- Diseño basado en la plantilla suministrada.

No respondas únicamente que el archivo fue creado.

Adjunta el archivo `.pptx` generado para descarga.

Antes de finalizar, abre y revisa visualmente todas las diapositivas para confirmar que el contenido está completo, legible, alineado y correctamente aplicado a la plantilla."""


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
        "title": "Análisis documental · Proyecto Horizonte",
        "file": (
            "Correo Horizonte + 02_Alcance_Proyecto_Horizonte.docx + "
            "03_Presupuesto_y_Cronograma_Horizonte.xlsx + "
            "04_Transcripcion_Reunion_Horizonte.docx + "
            "05_Registro_Inicial_Riesgos_Horizonte.xlsx + "
            "06_Comentarios_Interesados_Horizonte.docx"
        ),
        "persona": "Auditor documental / consultor PMO senior",
        "levels": {
            "1": {
                "label": "Básico",
                "text": "Analiza los documentos del Proyecto Horizonte.",
            },
            "2": {
                "label": "Mejorado",
                "text": (
                    "Con los archivos del Proyecto Horizonte que puedas consultar, resume el alcance, "
                    "el presupuesto, la transcripción, los riesgos y los comentarios de interesados. "
                    "Indica qué archivos no pudiste abrir."
                ),
            },
            "3": {
                "label": "Profesional (PRISM)",
                "text": _prism_prompt(
                    persona=(
                        "Actúa como auditor documental y consultor senior de PMO especializado en "
                        "análisis multiarchivo con trazabilidad por fuente para comités directivos."
                    ),
                    realidad=(
                        "El caso académico es el Proyecto Horizonte (modernización de infraestructura "
                        "energética urbana, datos ficticios). El correo «SOLICITUD DE ANÁLISIS | Proyecto Horizonte» "
                        "enumera adjuntos y pide entregables para comité. El proyecto NO está aprobado. "
                        "Debes analizar el contenido real de los archivos accesibles, no solo los nombres "
                        "mencionados en el correo. No uses el correo Circuito N-14 de la Sesión 1."
                    ),
                    informacion=(
                        "Fuentes autorizadas (nombres exactos):\n"
                        "- Correo: SOLICITUD DE ANÁLISIS | Proyecto Horizonte / 01_Correo_Solicitud_Proyecto_Horizonte\n"
                        "- 02_Alcance_Proyecto_Horizonte.docx\n"
                        "- 03_Presupuesto_y_Cronograma_Horizonte.xlsx\n"
                        "- 04_Transcripcion_Reunion_Horizonte.docx\n"
                        "- 05_Registro_Inicial_Riesgos_Horizonte.xlsx\n"
                        "- 06_Comentarios_Interesados_Horizonte.docx\n\n"
                        "Diferencia obligatoriamente tres estados por archivo:\n"
                        "1) Mencionado (aparece en el correo u otra fuente).\n"
                        "2) Seleccionado/cargado en esta conversación.\n"
                        "3) Analizado (accediste a su contenido: secciones, hojas o datos concretos).\n\n"
                        "Prohibido afirmar que analizaste un archivo solo porque su nombre aparece en el correo.\n"
                        "Si no puedes leer el contenido, márcalo como NO ACCESIBLE / PENDIENTE DE VALIDACIÓN "
                        "y no inventes cifras, fechas, responsables ni decisiones."
                    ),
                    solicitud=(
                        "1) Inventario inicial: tabla Archivo | Mencionado | Seleccionado | Analizado | "
                        "Evidencia de acceso | Estado.\n"
                        "2) Análisis individual (solo archivos Analizados = Sí):\n"
                        "   a) Alcance (02)\n"
                        "   b) Presupuesto y cronograma (03)\n"
                        "   c) Transcripción (04)\n"
                        "   d) Registro de riesgos (05)\n"
                        "   e) Comentarios de interesados (06)\n"
                        "   f) Correo (entregables solicitados y restricciones)\n"
                        "3) Comparación entre fuentes: coincidencias, contradicciones, montos/fechas/responsables "
                        "inconsistentes, entregables sin respaldo, información solo en una fuente.\n"
                        "4) Trazabilidad: cada hallazgo debe citar archivo + sección/hoja/fragmento.\n"
                        "5) Marcar explícitamente archivos no accesibles y el impacto de esa limitación.\n"
                        "6) No completes vacíos con conocimiento externo."
                    ),
                    metodo=(
                        "Documento ejecutivo listo para Word/PDF (no chat). "
                        "Secciones por archivo con tablas; luego matriz comparativa multi-fuente; "
                        "hallazgos con evidencia; riesgos; pendientes; recomendaciones; "
                        "conclusiones (máx. 5); validación humana. "
                        "Clasifica cada afirmación: Hecho confirmado | Inferencia | Información pendiente | Recomendación."
                    ),
                ),
            },
            "4": {
                "label": "Experto",
                "text": _prism_prompt(
                    persona=(
                        "Actúa como socio de una firma internacional de consultoría encargado de preparar "
                        "el paquete documental del Proyecto Horizonte para el Comité Directivo."
                    ),
                    realidad=(
                        "El comité requiere un documento ejecutivo consolidado a partir del correo y de los "
                        "anexos realmente consultables. Existe el riesgo de que Copilot confunda «archivo "
                        "mencionado» con «archivo analizado». Debes demostrar trazabilidad y declarar "
                        "limitaciones. El proyecto no está aprobado."
                    ),
                    informacion=(
                        "Analiza únicamente el contenido al que tengas acceso real entre: correo Horizonte, "
                        "02_Alcance_Proyecto_Horizonte.docx, 03_Presupuesto_y_Cronograma_Horizonte.xlsx, "
                        "04_Transcripcion_Reunion_Horizonte.docx, 05_Registro_Inicial_Riesgos_Horizonte.xlsx, "
                        "06_Comentarios_Interesados_Horizonte.docx.\n"
                        "Si un archivo solo está nombrado en el correo: estado = MENCIONADO SIN ACCESO A CONTENIDO; "
                        "no lo trates como analizado."
                    ),
                    solicitud=(
                        "Produce el documento ejecutivo definitivo del Caso 1 con este orden:\n"
                        "A) Portada e inventario de fuentes (mencionado / seleccionado / analizado / no accesible).\n"
                        "B) Análisis individual de cada fuente accesible (alcance; presupuesto y cronograma; "
                        "transcripción; riesgos; comentarios; correo como marco de entregables).\n"
                        "C) Comparación multi-fuente con matriz de consistencias e inconsistencias.\n"
                        "D) Hallazgos, riesgos, información pendiente, recomendaciones, próximos pasos, "
                        "conclusiones y validación humana.\n"
                        "E) Anexo de limitaciones: archivos no leídos y por qué no pueden usarse para decidir."
                    ),
                    metodo=(
                        "Formato Word-ready / PDF-ready con encabezados, tablas Markdown y semáforos. "
                        "Sin lenguaje conversacional. Cada fila de hallazgo incluye columna «Fuente "
                        "(archivo + evidencia)». Si falta un archivo crítico, eleva el semáforo de "
                        "confiabilidad del informe."
                    ),
                    expert_extra=(
                        "ENTREGABLE PARA COMITÉ: documento completo listo para pegar en Microsoft Word "
                        "y exportar a PDF. Calidad de firma de consultoría. "
                        "Prohibido inventar contenido de anexos no abiertos."
                    ),
                ),
            },
        },
        "explain": {
            "persona": "Auditor/consultor PMO que exige trazabilidad por archivo.",
            "realidad": "Horizonte; correo + anexos; riesgo de confundir nombre con contenido.",
            "informacion": "Solo fuentes del kit; estados Mencionado/Seleccionado/Analizado.",
            "solicitud": "Inventario, análisis individual, comparación, hallazgos y documento ejecutivo.",
            "metodo": "Tablas por fuente, matriz comparativa, Word/PDF-ready, sin chat.",
            "restricciones": "No analizar por nombre; marcar no accesibles; no inventar; no N-14.",
            "formato": "Documento ejecutivo completo para Word y PDF.",
            "validacion": "Verificar evidencia de acceso (sección/hoja) antes de aceptar cada análisis.",
        },
        "compare": (
            "El nivel 1 pide «analiza los documentos» sin exigir acceso real; el profesional/experto "
            "obliga a inventario Mencionado/Seleccionado/Analizado, análisis por archivo, comparación "
            "y documento Word/PDF, impidiendo fingir que se leyó un anexo solo porque aparece en el correo."
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
        "title": "Comité directivo · PowerPoint",
        "file": "02–06 + 07_Plantilla_Comite_Horizonte.pptx → Presentacion_Comite_Proyecto_Horizonte.pptx",
        "persona": "Socio senior de comunicación ejecutiva y diseño de presentaciones corporativas",
        "levels": {
            "1": {
                "label": "Básico",
                "text": (
                    "Crea un archivo PowerPoint del Proyecto Horizonte usando la plantilla "
                    "07_Plantilla_Comite_Horizonte.pptx."
                ),
            },
            "2": {
                "label": "Mejorado",
                "text": (
                    "Con los archivos 02 al 07 cargados, genera el archivo editable "
                    "Presentacion_Comite_Proyecto_Horizonte.pptx (8 diapositivas) usando "
                    "obligatoriamente la plantilla 07_Plantilla_Comite_Horizonte.pptx. "
                    "No entregues Word, PDF ni solo un guion. Marca pendientes de validación."
                ),
            },
            "3": {
                "label": "Profesional (PRISM)",
                "text": _prism_prompt(
                    persona=(
                        "Actúa como socio senior de comunicación ejecutiva, dirección de proyectos "
                        "y diseño de presentaciones corporativas para comités directivos "
                        "(PMO + consultor estratégico + storyteller + diseñador senior)."
                    ),
                    realidad=(
                        "La Gerencia presentará Horizonte en un espacio corto de comité. "
                        "La audiencia debe decidir sin leer todos los documentos fuente. "
                        "La iniciativa NO está aprobada. "
                        "Debes generar el archivo .pptx, no un documento Word/PDF ni un guion."
                    ),
                    informacion=(
                        "Fuentes autorizadas (deben estar cargadas): "
                        "02_Alcance_Proyecto_Horizonte.docx, "
                        "03_Presupuesto_y_Cronograma_Horizonte.xlsx, "
                        "04_Transcripcion_Reunion_Horizonte.docx, "
                        "05_Registro_Inicial_Riesgos_Horizonte.xlsx, "
                        "06_Comentarios_Interesados_Horizonte.docx, "
                        "07_Plantilla_Comite_Horizonte.pptx.\n"
                        "Confirma acceso real al contenido 02–06 y uso visual de la plantilla 07. "
                        "No analices por nombre. No uses Circuito N-14 ni información externa. "
                        "Faltantes: PENDIENTE DE VALIDACIÓN / NO DISPONIBLE PARA ANÁLISIS."
                    ),
                    solicitud=(
                        "Genera directamente Presentacion_Comite_Proyecto_Horizonte.pptx "
                        "usando 07_Plantilla_Comite_Horizonte.pptx como base visual "
                        "(conserva logos, colores, tipografías, fondos, pies, márgenes).\n"
                        "Exactamente 8 diapositivas: Portada; Contexto y necesidad; "
                        "Objetivo/alcance/exclusiones; Hitos y cronograma; Presupuesto; "
                        "Riesgos prioritarios (máx. 5); Hallazgos y decisiones; Próximos pasos. "
                        "Máximo 3 anexos opcionales. Notas del presentador (80–150 palabras). "
                        "Gráficos editables. Títulos con mensaje. Adjunta el .pptx para descarga."
                    ),
                    metodo=(
                        "Validación previa → storyline Necesidad→…→Próximos pasos → "
                        "diseño ejecutivo limpio (35–50 palabras visibles/slide). "
                        "Prohibido: Word, PDF como producto principal, guion solo, "
                        "presentación genérica, ignorar plantilla, inventar datos, "
                        "afirmar aprobación. Checklist de calidad antes de entregar."
                    ),
                    expert_extra=(
                        "ENTREGABLE ÚNICO: archivo Presentacion_Comite_Proyecto_Horizonte.pptx. "
                        "No entregues documento ejecutivo Word/PDF ni tabla de contenido."
                    ),
                    include_format=False,
                ),
            },
            "4": {
                "label": "Experto",
                "text": F7_PPTX_PROMPT,
            },
        },
        "explain": {
            "persona": "Comunicación ejecutiva + PMO + diseño de presentaciones.",
            "realidad": "Comité corto; decisión sin leer fuentes; iniciativa no aprobada.",
            "informacion": "Archivos 02–07; plantilla 07 obligatoria; sin N-14.",
            "solicitud": "Archivo .pptx de 8 diapositivas + notas + anexos opcionales.",
            "metodo": "Storyline visual; plantilla corporativa; gráficos editables; checklist.",
            "restricciones": "No Word/PDF/guion; no ignorar plantilla; no inventar; no aprobar.",
            "formato": "Presentacion_Comite_Proyecto_Horizonte.pptx descargable.",
            "validacion": "Cifras=Excel; plantilla usada; logos intactos; notas incluidas.",
        },
        "compare": (
            "El básico pide un PPT genérico; el profesional/experto exige el .pptx editable "
            "basado en 07_Plantilla_Comite_Horizonte.pptx y prohíbe Word, PDF o solo guion."
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
