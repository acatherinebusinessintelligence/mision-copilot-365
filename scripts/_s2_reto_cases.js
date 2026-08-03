  "fase-1": {
    "id": "fase-1",
    "title": "Recepción automatizada del proyecto",
    "apps": ["Outlook", "Power Automate", "SharePoint"],
    "email": false,
    "planilla": {"key": "s2-correo", "label": "Correo de inicio"},
    "output": "MCP365_S2_F01_Recepcion_Proyecto_Horizonte",
    "fields": [
      ["rol", "Rol de Copilot / diseño del flujo", "Asistente de automatización que describe un flujo de Power Automate para recepción de proyectos sin inventar credenciales ni endpoints."],
      ["fuente", "Fuente de disparo", "Correo Outlook cuyo asunto contiene exactamente: NUEVO PROYECTO · HORIZONTE. Adjunto esperado: MCP365_S2_Ficha_Proyecto_Horizonte.docx."],
      ["objetivo", "Objetivo del flujo", "Detectar el correo; capturar remitente, asunto y fecha; verificar la ficha Word; crear carpeta MCP365_S2_F01_Recepcion_Proyecto_Horizonte; guardar el adjunto; registrar la recepción; enviar confirmación."],
      ["destino", "Destino documental", "SharePoint o OneDrive del participante (carpeta de práctica). No uses rutas de producción reales."],
      ["prohibiciones", "Prohibiciones", "No inventar credenciales.\nNo inventar URLs de API.\nNo inventar cuentas de correo reales ajenas al ejercicio.\nNo marcar la recepción como validada sin revisión humana."],
      ["vacio", "Respuesta cuando falte información", "No especificado."],
      ["salida", "Nombre / identificador de salida", "MCP365_S2_F01_Recepcion_Proyecto_Horizonte"]
    ],
    "checklist": [
      ["s2f1-c1", "Descargué correo de inicio y ficha Word"],
      ["s2f1-c2", "El flujo se dispara con el asunto NUEVO PROYECTO · HORIZONTE"],
      ["s2f1-c3", "Se crea la carpeta y se guarda el adjunto"],
      ["s2f1-c4", "Se registra la recepción y se envía confirmación"],
      ["s2f1-c5", "No inventé credenciales ni endpoints"]
    ],
    "practice_title": "Al terminar · Practica con tu propia solicitud",
    "practice": "Adapta el disparador a un asunto anonimizado de tu trabajo. Elimina datos personales y credenciales antes de practicar.",
    "deliverable": "Entregable: flujo de recepción + carpeta <code>MCP365_S2_F01_Recepcion_Proyecto_Horizonte</code> con la ficha Word guardada y registro de recepción."
  },
  "fase-2": {
    "id": "fase-2",
    "title": "Extracción de información del Word",
    "apps": ["Copilot", "Word", "Power Automate"],
    "email": false,
    "planilla": {"key": "s2-ficha", "label": "Ficha Word"},
    "output": "MCP365_S2_Datos_Proyecto_Horizonte.json",
    "fields": [
      ["rol", "Rol de Copilot", "Analista de proyectos que extrae datos estructurados desde una ficha Word sin inventar información."],
      ["fuente", "Fuente única", "MCP365_S2_Ficha_Proyecto_Horizonte.docx (guardada en la carpeta del Reto 1)."],
      ["objetivo", "Objetivo", "Extraer código, nombre, objetivo, alcance, patrocinador, líder, fechas, presupuesto preliminar, entregables, dependencias, restricciones, riesgos y criterios de éxito en un objeto JSON."],
      ["formato", "Formato de salida", "Único archivo JSON válido UTF-8 con claves en español o snake_case consistente."],
      ["vacio", "Respuesta cuando falte información", "No especificado."],
      ["prohibiciones", "Prohibiciones", "No inventar fechas.\nNo inventar cifras.\nNo inventar responsables.\nNo inventar decisiones.\nNo omitir campos: si faltan, usar No especificado."],
      ["salida", "Nombre del archivo de salida", "MCP365_S2_Datos_Proyecto_Horizonte.json"]
    ],
    "checklist": [
      ["s2f2-c1", "Analicé la ficha Word del Reto 1"],
      ["s2f2-c2", "Obtuve un JSON con todos los campos pedidos"],
      ["s2f2-c3", "Usé No especificado donde faltaba dato"],
      ["s2f2-c4", "Comparé JSON vs Word (validación humana)"],
      ["s2f2-c5", "Archivo nombrado MCP365_S2_Datos_Proyecto_Horizonte.json"]
    ],
    "practice_title": "Al terminar · Extrae datos de una ficha propia",
    "practice": "Usa una ficha o solicitud anonimizada. Conserva No especificado. No inventes cifras ni fechas.",
    "deliverable": "Entregable: <code>MCP365_S2_Datos_Proyecto_Horizonte.json</code> validado por la persona frente al Word."
  },
  "fase-3": {
    "id": "fase-3",
    "title": "Presupuesto del proyecto",
    "apps": ["Power Automate", "Excel", "Copilot"],
    "email": false,
    "planilla": {"key": "s2-control", "label": "Control Excel"},
    "output": "MCP365_S2_Control_Proyecto_Horizonte.xlsx",
    "fields": [
      ["rol", "Rol de Copilot", "Analista de costos que clasifica partidas y distingue cifras confirmadas, estimadas y no especificadas."],
      ["fuente", "Fuentes", "MCP365_S2_Datos_Proyecto_Horizonte.json + hoja Presupuesto de MCP365_S2_Control_Proyecto_Horizonte.xlsx."],
      ["objetivo", "Objetivo", "Registrar partidas con código, categoría, descripción, cantidad, costo unitario, costo total, responsable, fuente, tipo de cifra, estado de validación y observación; calcular subtotales, total, diferencia vs preliminar y % desviación."],
      ["tipos", "Tipos de cifra", "Valor confirmado.\nValor estimado.\nValor no especificado."],
      ["regla_pa", "Regla Power Automate", "Agregar o actualizar filas. No modificar una cifra confirmada sin aprobación humana."],
      ["vacio", "Respuesta cuando falte información", "No especificado."],
      ["salida", "Archivo de control", "MCP365_S2_Control_Proyecto_Horizonte.xlsx"]
    ],
    "checklist": [
      ["s2f3-c1", "Usé el JSON del Reto 2 como entrada"],
      ["s2f3-c2", "Hoja Presupuesto con columnas completas"],
      ["s2f3-c3", "Tipos de cifra diferenciados"],
      ["s2f3-c4", "Fórmulas de total y desviación visibles"],
      ["s2f3-c5", "No alteré cifras confirmadas sin aprobación"]
    ],
    "practice_title": "Al terminar · Presupuesto de un caso propio",
    "practice": "Adapta categorías a un proyecto anonimizado. Marca claramente estimado vs confirmado.",
    "deliverable": "Entregable: hoja <strong>Presupuesto</strong> en <code>MCP365_S2_Control_Proyecto_Horizonte.xlsx</code> con totales y desviación."
  },
  "fase-4": {
    "id": "fase-4",
    "title": "Matriz de riesgos",
    "apps": ["Copilot", "Excel", "Power Automate"],
    "email": false,
    "planilla": {"key": "s2-control", "label": "Control Excel"},
    "output": "MCP365_S2_Control_Proyecto_Horizonte.xlsx",
    "fields": [
      ["rol", "Rol de Copilot", "Analista de riesgos que distingue riesgos explícitos, inferidos, supuestos e información ausente."],
      ["fuente", "Fuentes", "Ficha / JSON del Proyecto Horizonte + hoja Riesgos de MCP365_S2_Control_Proyecto_Horizonte.xlsx."],
      ["objetivo", "Objetivo", "Completar la matriz con identificador, riesgo, causa, consecuencia, probabilidad, impacto, nivel, control, tratamiento, responsable, fecha de revisión, estado y fuente."],
      ["etiquetas", "Etiquetas obligatorias", "Riesgo explícito.\nRiesgo inferido → etiqueta Interpretación para validación.\nSupuesto.\nInformación ausente."],
      ["prohibiciones", "Prohibiciones", "No marcar automáticamente como validado.\nNo inventar controles inexistentes.\nNo inventar fechas de revisión sin fuente."],
      ["vacio", "Respuesta cuando falte información", "No especificado."],
      ["salida", "Archivo de control", "MCP365_S2_Control_Proyecto_Horizonte.xlsx"]
    ],
    "checklist": [
      ["s2f4-c1", "Completé la hoja Riesgos del control Excel"],
      ["s2f4-c2", "Distinguí explícito / inferido / supuesto / ausente"],
      ["s2f4-c3", "Inferidos llevan Interpretación para validación"],
      ["s2f4-c4", "Ningún riesgo quedó auto-validado"],
      ["s2f4-c5", "Usé datos del Reto 2/3 sin inventar"]
    ],
    "practice_title": "Al terminar · Riesgos de un proyecto propio",
    "practice": "Registra riesgos anonimizados. Todo lo inferido lleva Interpretación para validación.",
    "deliverable": "Entregable: hoja <strong>Riesgos</strong> en <code>MCP365_S2_Control_Proyecto_Horizonte.xlsx</code> lista para validación humana."
  },
  "fase-5": {
    "id": "fase-5",
    "title": "Informe y aprobación",
    "apps": ["Power Automate", "Word", "Approvals", "Outlook"],
    "email": false,
    "planilla": {"key": "s2-informe-plantilla", "label": "Plantilla informe"},
    "output": "MCP365_S2_Informe_Proyecto_Horizonte.docx",
    "fields": [
      ["rol", "Rol de Copilot", "Redactor de informes de proyecto que completa solo secciones autorizadas de una plantilla Word y deja validación humana y CQ vacías."],
      ["fuente", "Fuentes", "JSON del Reto 2 + hojas y riesgos del Excel de control + plantilla MCP365_S2_Plantilla_Informe_Proyecto.docx."],
      ["objetivo", "Objetivo", "Generar MCP365_S2_Informe_Proyecto_Horizonte.docx y orquestar aprobación humana con Power Automate Approvals."],
      ["secciones", "Secciones autorizadas", "Identificación.\nResumen ejecutivo.\nObjetivo.\nAlcance.\nEntregables.\nCronograma general.\nPresupuesto.\nDesviaciones.\nRiesgos prioritarios.\nDependencias.\nDecisiones pendientes.\nRecomendaciones.\nFuentes."],
      ["restringidos", "Secciones que deben quedar vacías", "Validación humana.\nControl de calidad.\nFirmas.\nDecisión de aprobación (solo Approvals humano)."],
      ["flujo_pa", "Pasos Power Automate", "1. Rellenar plantilla.\n2. Guardar informe.\n3. Enviar a aprobación.\n4. Esperar respuesta.\n5. Registrar decisión.\n6. Notificar resultado.\nSi rechazo: registrar observaciones, notificar y detener presentación."],
      ["vacio", "Respuesta cuando falte información", "No especificado."],
      ["salida", "Nombre del archivo de salida", "MCP365_S2_Informe_Proyecto_Horizonte.docx"]
    ],
    "checklist": [
      ["s2f5-c1", "Generé el informe desde la plantilla"],
      ["s2f5-c2", "Incluí presupuesto y riesgos de retos previos"],
      ["s2f5-c3", "Envié a aprobación humana (Approvals)"],
      ["s2f5-c4", "Registré la decisión y notifiqué"],
      ["s2f5-c5", "Validación humana y CQ vacíos para la persona"],
      ["s2f5-c6", "Copilot no aprobó el informe"]
    ],
    "practice_title": "Al terminar · Informe de un caso propio",
    "practice": "Usa plantilla + datos anonimizados. La aprobación debe ser humana. Si hay rechazo, no avances a presentación.",
    "deliverable": "Entregable: <code>MCP365_S2_Informe_Proyecto_Horizonte.docx</code> + registro de aprobación (Approvals / Outlook)."
  },
  "fase-6": {
    "id": "fase-6",
    "title": "Presentación ejecutiva",
    "apps": ["Word", "PowerPoint", "Copilot"],
    "email": false,
    "planilla": {"key": "s2-resultado", "label": "Resultado esperado"},
    "output": "MCP365_S2_Presentacion_Proyecto_Horizonte.pptx",
    "fields": [
      ["rol", "Rol de Copilot", "Diseñador de presentaciones ejecutivas que resume únicamente un informe aprobado, sin agregar hechos nuevos."],
      ["fuente", "Fuente única", "MCP365_S2_Informe_Proyecto_Horizonte.docx aprobado (precondición obligatoria)."],
      ["objetivo", "Objetivo", "Crear presentación de 8 a 10 diapositivas: portada, necesidad/oportunidad, objetivo y alcance, entregables, cronograma, presupuesto, riesgos prioritarios, decisiones pendientes, próximos pasos, cierre."],
      ["prohibiciones", "Prohibiciones", "No generar la presentación si el informe fue rechazado.\nNo agregar beneficios no citados.\nNo agregar cifras, fechas ni responsables ausentes en el informe.\nNo inventar próximos pasos no documentados."],
      ["vacio", "Respuesta cuando falte información", "No especificado."],
      ["salida", "Nombre del archivo de salida", "MCP365_S2_Presentacion_Proyecto_Horizonte.pptx"]
    ],
    "checklist": [
      ["s2f6-c1", "Confirmé que el informe está aprobado"],
      ["s2f6-c2", "Presentación basada solo en el informe"],
      ["s2f6-c3", "Entre 8 y 10 diapositivas con la estructura pedida"],
      ["s2f6-c4", "Sin cifras ni responsables inventados"],
      ["s2f6-c5", "Archivo MCP365_S2_Presentacion_Proyecto_Horizonte.pptx"]
    ],
    "practice_title": "Al terminar · Presentación de un informe propio",
    "practice": "Parte solo de un informe anonimizado ya revisado por una persona. No inventes contenido.",
    "deliverable": "Entregable: <code>MCP365_S2_Presentacion_Proyecto_Horizonte.pptx</code> + correo final de notificación del ciclo."
  }
