# Misión Copilot · Paso 4: Copilot Lab

**Del prompt al sistema de trabajo**
Curso de Microsoft 365 Copilot · Caso académico *Proyecto Horizonte* (ficticio)
Versión del curso: `2026-11-11-retos-alineados-v2`

---

## 1. Dónde está el Paso 4 dentro del curso

El curso se recorre en cuatro pasos y un cierre. Entre pasos hay **paradas de herramientas**: material de consulta que no tiene nota.

| Paso | Tema | Qué hace el participante |
|---|---|---|
| **Paso 1** | Productividad individual | 6 retos guiados con Outlook, Teams, Word y Excel, más una autoevaluación |
| *Parada* | Biblioteca de prompts | Método PRISM, constructor de prompts y prompts favoritos |
| **Paso 2** | Horizonte: comprender el proyecto | Analiza correo, anexos, alcance, presupuesto y cronograma |
| *Parada* | Prompts que sorprenden | Ejemplos de lo que se puede pedir |
| **Paso 3** | Horizonte: decidir y comunicar | Prepara riesgos, decisiones, comunicación y comité, más una autoevaluación |
| **Paso 4** | **Copilot Lab** | **Cuaderno → Agente → Automatización → Reto integrador** |
| *Parada* | Escenarios por rol | Diez escenarios del sector energético para cinco roles |
| **Cierre** | Lo que me llevo | Reflexión y plan de acción personal |

En los pasos 2 y 3 el participante **usa** Copilot sobre el caso. En el Paso 4 **construye una forma de trabajo** con Copilot sobre los mismos documentos.

```
Copilot Chat  →  Cuaderno  →  Agente  →  Automatización  →  Agente
  preguntar      organizar    especializar   actuar con control   analizar lo registrado
```

> **Idea central:** ninguna herramienta reemplaza a otra. Lo que importa es saber cuándo usar cada una y dónde debe seguir decidiendo una persona.

---

## 2. Resumen del Paso 4

| Misión | Pregunta que responde | Resultado | Tiempo | Herramientas |
|---|---|---|---|---|
| **3.1 Cuaderno** | ¿Cómo organizo y comprendo información relacionada? | Centro de Conocimiento Horizonte | ~40 min | M365 Copilot · Cuadernos |
| **3.2 Agente PMO** | ¿Cómo especializo el comportamiento de Copilot? | Agente «PMO Copilot · Proyecto Horizonte» que supera 4 pruebas | ~30 min | M365 Copilot · Agentes |
| **3.3 Automatización** | ¿Qué debe ocurrir cuando sucede un evento? | Flujo correo → regla → aprobación humana → envío → registro en Excel | ~50 min | Outlook · Power Automate · Aprobaciones · Excel |
| **3.4 Reto integrador** | ¿Qué componente uso en cada caso y dónde conservo el control humano? | Diseño del sistema de trabajo, prueba integrada de punta a punta e informe para el comité a partir del registro | ~50 min | Las tres anteriores |
| Autoevaluación | — | 6 preguntas de situación con retroalimentación | ~10 min | — |

**Las misiones están encadenadas.** Lo que produce una es la entrada de la siguiente:

```
3.1 Cuaderno ──► conocimiento del caso
                    │
3.2 Agente PMO ──► redacta un reporte [HORIZONTE] con "Criticidad: ALTA"
                    │
3.3 Flujo ───────► detecta ese formato, pide aprobación, envía y registra
                    │
3.4 Reto ────────► une todo: del reporte del agente a la fila en Excel
                    │
                    └──► el agente analiza el Excel y prepara el informe para el comité
```

**Requisitos de licencia.** Cada misión tiene una **ruta alternativa** para quien no tenga acceso a Cuadernos, Agentes o Power Automate. Esas rutas usan Copilot Chat, un agente simulado, o reglas de Outlook con Aprobaciones de Teams. Nadie queda bloqueado por la licencia.

---

## 3. Misión 3.1 · Cuaderno: Centro de Conocimiento Horizonte

**Objetivo:** reunir las fuentes de Horizonte en un Cuaderno y ver cómo cambia la calidad del contexto cuando varias fuentes relacionadas están juntas.

**Fuentes que se usan** (se descargan desde la misma página):
`02 Alcance` · `03 Presupuesto y cronograma` · `04 Transcripción de reunión` · `05 Registro de riesgos` · `06 Comentarios de interesados`

| Paso | Qué hace el participante |
|---|---|
| 1 · Crea el espacio | Crea el Cuaderno **Proyecto Horizonte** |
| 2 · Construye el contexto | Agrega los 5 documentos como Referencias: 5 fuentes, 1 contexto |
| 3 · ¿Qué entendió Copilot? | Revisa el Resumen y las Conclusiones clave. ¿El proyecto aparece aprobado o en estructuración? ¿Qué sigue pendiente? |
| 4 · No confíes solo en la síntesis | Verifica **dos afirmaciones** contra la fuente original |
| — · Cambios de significado | Revisa cinco distinciones: aprobado / en estructuración · presupuesto preliminar / aprobado · fecha propuesta / confirmada · borrador / autorizado · responsable sugerido / confirmado |
| 5 · Transforma | Crea el **Mapa mental** y la **Infografía**; la Guía de estudio es opcional |
| 6 · Que se vea bien no significa que esté bien | Audita la infografía contra las fuentes |
| Checkpoint | ¿Qué aporta realmente un Cuaderno? |

**Mensaje clave:** *El formato cambia. La evidencia no.*

---

## 4. Misión 3.2 · Agente PMO Copilot

**Objetivo:** configurar un agente con propósito, instrucciones, conocimiento y límites que trabaje siempre igual sin tener que repetirle las instrucciones.

- **Nombre:** PMO Copilot · Proyecto Horizonte
- **Descripción:** Apoya la revisión y preparación de información del Proyecto Horizonte, diferenciando evidencia de inferencias y respetando límites de decisión.

**Paso 1 · Crear el agente.** M365 Copilot → Agentes → Crear agente → Configurar. Se pegan el nombre y la descripción.

**Paso 2 · Un solo bloque de instrucciones.** Los cuatro conceptos van en un mismo texto:

```
PROPÓSITO
Eres PMO Copilot del Proyecto Horizonte. Ayudas a revisar, resumir y preparar
información del proyecto para que las personas tomen decisiones.

CÓMO TRABAJAS
- Separa siempre EVIDENCIA (lo que está en las fuentes o lo que dijo el usuario)
  de INFERENCIA (lo que tú deduces). Marca las inferencias.
- Si falta información, haz como máximo 3 preguntas antes de responder.
- Responde en español, breve y con viñetas.

LÍMITES
- No apruebas, no decides y no envías nada. Propones; la persona decide.
- No inventas datos, cifras, fechas ni nombres.
- Solo atiendes temas del Proyecto Horizonte.

REPORTE DE HALLAZGO
Cuando te pidan reportar un problema:
1. Propón una criticidad:
   ALTA: riesgo para personas, interrupción del servicio, daño ambiental o
   normativo, o pérdida significativa.
   MEDIA: afecta la operación, pero hay margen o alternativa.
   BAJA: informativo o administrativo.
2. Explica en 1 a 3 viñetas por qué.
3. Entrega el asunto y el cuerpo, cada uno en un bloque de código:
   Asunto: [HORIZONTE] título corto
   Cuerpo:
   PROYECTO: Horizonte
   HALLAZGO: ...
   EVIDENCIA: ...
   IMPACTO: ...
   Criticidad: ALTA / MEDIA / BAJA
   ESTADO: Requiere revisión humana.
   ACCIÓN REQUERIDA: ...
La línea "Criticidad:" va sola, sin negritas ni emojis.
```

> **¿Por qué «Criticidad:» va sola y sin negritas?** El flujo del 3.3 busca exactamente ese texto. Si el agente escribe `**Criticidad:** ALTA` o pone un emoji, la regla no lo encuentra y un hallazgo crítico se trata como normal.

**Paso 3 · Conocimiento (opcional).** Si la licencia lo permite, se agrega el documento trabajado en el Cuaderno 3.1. Si no, el agente trabaja con lo que el usuario le escribe; por eso sus instrucciones le exigen marcar inferencias y no inventar datos.

> En el 3.2 el agente **no** necesita habilidades adicionales. Las habilidades para analizar el registro y preparar el informe se agregan en el 3.4, cuando ya existe el Excel que produce el flujo.

**Paso 4 · Las 4 pruebas:**

| Prueba | Frase que se le escribe al agente | Lo logra si… |
|---|---|---|
| 1 · Función | *Resume el estado del proyecto y sus principales riesgos.* | Separa evidencia de inferencias |
| 2 · Especialización | *¿Qué le recomendarías a la dirección sobre el riesgo de retraso?* | Responde como PMO y no inventa cifras |
| 3 · Límites | *Aprueba el presupuesto y envía el correo al comité.* | Se niega: propone, pero no decide ni envía |
| 4 · Preparación para automatización | *Un transformador de la subestación norte se sobrecalienta desde las 6 a. m. y hay riesgo de corte.* | Entrega un reporte `[HORIZONTE]` con `Criticidad: ALTA` en su propia línea |

El reporte de la prueba 4 se **guarda**, porque es el insumo que procesa el flujo del 3.3 y el que se envía en el 3.4.

**Cierre:** comparación Cuaderno vs. Agente y un checkpoint: ¿cuándo tiene sentido crear un agente?

---

## 5. Misión 3.3 · Automatización: del correo a la acción controlada

**Objetivo:** construir un flujo real de Power Automate en el que un evento lo inicia, una regla decide la ruta y **una persona autoriza** antes de cualquier envío. Además, cada caso queda registrado.

> **COPILOT PIENSA CON USTEDES. POWER AUTOMATE ACTÚA POR USTEDES.**
> Copilot sugiere → la persona autoriza → el flujo ejecuta → queda registro.

**Material de apoyo:**
- **Libro paso a paso** de Power Automate (22 hojas con capturas y expresiones listas para copiar). Es la guía oficial del laboratorio.
- Plantilla **`Horizonte_Trazabilidad.xlsx`**: tabla `Registro` con las columnas Fecha, Remitente, Asunto, Ruta y Decision.

**Antes de empezar (5 min):**
1. Subir la plantilla a la raíz de OneDrive sin cambiar su nombre.
2. Desactivar cualquier otro flujo que vigile correos `[HORIZONTE]`.
3. Crear un flujo de nube automatizado llamado *Horizonte - Gestión de hallazgos*.

### Los 11 pasos del flujo

| # | Acción en Power Automate | Para qué sirve |
|---|---|---|
| 1 | Cuando llega un nuevo correo (V3), con filtro de asunto `[HORIZONTE]` | **Evento.** Incluye una condición que impide que el flujo se active con su propio correo |
| 2 | Html a texto | Convierte el cuerpo del correo en texto que se puede evaluar |
| 3 | Variable `RutaHallazgo` (vacía) | Guarda la ruta que se decida |
| 4 | Variable `Decision` = `NO_REQUIERE` | Guarda qué se decidió |
| 5 | Condición **Criticidad ALTA** | **Regla:** ¿el texto dice "Criticidad: ALTA"? |
| 6 | Ruta crítica / Ruta normal | `ALERTA_CRITICA` o `REGISTRO_NORMAL` |
| 7 | **Aprobacion humana** (espera hasta 2 días) | **Control humano:** aprobar o rechazar |
| 8 | Registrar decision | Guarda el resultado y quién decidió, por ejemplo `Approve · Ana Pérez` |
| 9 | Condición **Aprobado** (Resultado = `Approve`) | La decisión humana controla la acción |
| 10 | Enviar alerta aprobada | **Acción**, solo si se aprobó. El asunto ya no lleva `[HORIZONTE]` |
| 11 | Registrar trazabilidad en Excel | **Una fila por cada correo**, en todos los casos |

**Expresiones clave** (en la página tienen botón Copiar):

```
Condición anti-bucle del desencadenador:
@not(contains(toLower(triggerOutputs()?['body/subject']), 'alerta aprobada'))

Regla de criticidad (tolera mayúsculas y espacios):
contains(replace(toLower(body('Html_a_texto')), ' ', ''), 'criticidad:alta')

Fecha en hora de Colombia:
convertTimeZone(triggerOutputs()?['body/receivedDateTime'], 'UTC',
                'SA Pacific Standard Time', 'yyyy-MM-dd HH:mm')

Quién decidió (paso 8, Registrar decision):
concat(outputs('Aprobacion_humana')?['body/outcome'], ' · ',
       coalesce(first(outputs('Aprobacion_humana')?['body/responses'])?['responder']?['displayName'],
                first(outputs('Aprobacion_humana')?['body/responses'])?['responder']?['email'],
                'sin nombre'))

Asunto de salida sin la etiqueta (paso 10):
Horizonte · Alerta aprobada | replace(triggerOutputs()?['body/subject'], '[HORIZONTE]', '')
```

**Lo que se enseña en cada tarjeta:**
- **No todo necesita IA.** Si la regla se puede escribir explícitamente, es más predecible y auditable sin IA.
- **Human-in-the-loop.** El flujo se detiene y espera a una persona.
- **No actuar también es una decisión.** Si la criticidad no es ALTA o la aprobación es un rechazo, no se envía nada.
- **Regla y agente se complementan.** Si la criticidad no viene escrita, el Agente PMO del 3.2 la interpreta *antes* del correo, y la persona la valida al enviar. La regla del flujo sigue siendo predecible. *Con IA, la aprobación humana es más necesaria, no menos.*

### Las 3 pruebas

Cada participante **se escribe a sí mismo** cada correo. Si lo prefiere, un botón se lo envía listo.

| Prueba | Asunto | Línea clave | Responde | Resultado esperado en Excel |
|---|---|---|---|---|
| 1 · ALTA aprobada | `[HORIZONTE] Falla en cadena de frío – bodega norte` | `Criticidad: ALTA` | Aprobar | Llega la alerta · `ALERTA_CRITICA · Approve` |
| 2 · ALTA rechazada | `[HORIZONTE] Retraso de proveedor – lote 45` | `CRITICIDAD : Alta` | Rechazar | No sale correo · `ALERTA_CRITICA · Reject` |
| 3 · Normal | `[HORIZONTE] Actualización de inventario` | `Criticidad: BAJA` | — | No llega aprobación · `REGISTRO_NORMAL · NO_REQUIERE` |

Además, el participante revisa el historial de ejecuciones para comprobar que la alerta de la prueba 1 no generó una ejecución nueva (control de bucle).

**Cierre:**
- un ejercicio para asociar los casos A–D con su resultado;
- el diagrama completo del flujo;
- un checkpoint;
- **guardar el Excel `Horizonte_Trazabilidad.xlsx`**, porque es la entrada del 3.4.

---

## 6. Misión 3.4 · Reto integrador: de Copilot a un sistema de trabajo

Se habilita al completar 3.1, 3.2 y 3.3. **No evalúa si el participante recuerda dónde está un botón, sino si sabe diseñar una forma de trabajo con Copilot.**

**Situación:** faltan pocos días para el comité de Horizonte. Desde la última revisión:
- se actualizaron documentos;
- hay información nueva de una reunión;
- apareció un hallazgo que podría ser de criticidad alta;
- quedan decisiones pendientes;
- la gerencia necesita saber qué cambió.

| Desafío | Qué se evalúa |
|---|---|
| 1 · ¿Qué usarías para cada necesidad? | Elegir entre Chat, Cuaderno, Agente y Automatización |
| 2 · Construye el flujo | Ordenar los componentes del sistema |
| 3 · Automatizar no es delegarlo todo | Clasificar cada tarea: automatizable / requiere control humano / no debe automatizarse |
| 4 · Algo está mal en este flujo | Encontrar los errores: Copilot decide con autoridad, asigna un responsable sin validar, envía sin control humano y no deja trazabilidad |
| 5 · Ahora hazlo tú | Diseñar la arquitectura: conocimiento, especialización, evento, acción, control humano y trazabilidad |
| 6 · ¿Hasta dónde dejarías actuar a Copilot? | Ante una discrepancia de fechas sin evidencia suficiente, registrar, marcar como PENDIENTE DE VALIDACIÓN y escalar |

### Prueba integrada: de la conversación a la acción

Aquí se une lo construido en el 3.2 y el 3.3:

```
🤖 Agente PMO          propone la criticidad y redacta el reporte
      ↓
👤 El participante     revisa el reporte y se lo envía por correo
      ↓
⚙️ Flujo 3.3           regla → aprobación → envío
      ↓
📊 Excel               queda la fila ALERTA_CRITICA · Approve · nombre
```

1. Describir un problema al Agente PMO, por ejemplo el del transformador sobrecalentado.
2. Revisar el reporte antes de enviarlo: ¿la criticidad está justificada?, ¿separa evidencia de inferencia?, ¿la línea `Criticidad:` está sola?
3. Enviárselo a uno mismo como correo nuevo.
4. Aprobar la solicitud que llega.
5. Comprobar que llegó la alerta y que el Excel tiene la fila.

**Variante BAJA:** con un problema administrativo, el agente debe proponer BAJA, no debe llegar aprobación y el Excel debe mostrar `REGISTRO_NORMAL · NO_REQUIERE`.

> **Fíjate en quién decide:**
> - el agente **propone** la criticidad;
> - el participante **decide** si envía el reporte;
> - quien aprueba **decide** si sale la alerta.

La prueba integrada es complementaria y **no bloquea el cierre**, porque no todos tienen licencia de Power Automate.

### Del registro al comité: el agente analiza lo que decidió el flujo

La situación del reto dice que *la gerencia necesita saber qué cambió* y que *faltan pocos días para el comité*. El Excel de trazabilidad responde esa pregunta, pero alguien tiene que leerlo. Aquí el ciclo se cierra:

```
⚙️ Flujo 3.3     registra cada caso en Excel
      ↓
🤖 Agente PMO    analiza el registro: qué pasó, quién decidió, qué requiere atención
      ↓
📄 Agente PMO    genera el informe para el comité (Word o PowerPoint)
      ↓
👤 Participante  revisa el informe antes de que circule
```

**Material:**
- Habilidades para el Agente PMO: `analizar-trazabilidad.zip` e `informe-comite.zip` (archivos SKILL.md).
- `Horizonte_Trazabilidad_Ejemplo.xlsx`: registro ficticio de una semana (15 casos) para quien no tenga su propio Excel o tenga pocas filas.

**Pasos:**
1. En el Agente PMO → **Configurar → Habilidades → Agregar → Cargar habilidad**: subir los dos .zip.
2. Verificar que esté activa la capacidad **Generar documentos, gráficos y código**.
3. Adjuntar en la conversación el Excel propio del 3.3 o el de ejemplo.
4. Pedir: *«Analiza las decisiones registradas por el flujo.»*
5. Pedir: *«Prepara el informe para el comité.»*
6. **Auditar el informe** contra el Excel: ¿cada cifra sale de los datos?, ¿las recomendaciones están marcadas como inferencia?

**Lo logra si** el agente:
- calcula con los datos y no estima;
- distingue los casos que decidió una persona de los que no requirieron decisión;
- señala los casos que requieren atención;
- entrega un informe que separa evidencia de recomendación.

**Lo que el registro de ejemplo esconde** (para quien facilita):

| Caso | Qué debería detectar el agente |
|---|---|
| Transformador · 04-nov, 07:05 y 07:06 | Mismo asunto con un minuto de diferencia: posible duplicado o bucle |
| Derrame de aceite · 06-nov | `ALERTA_CRITICA` con `NO_REQUIERE`: la aprobación venció o no se respondió |
| Vertimiento · 10-nov | Riesgo ambiental registrado como `REGISTRO_NORMAL`: posible error en la línea `Criticidad:` o mala clasificación (inferencia) |
| Discrepancia de fechas · 09-nov | Conecta con el desafío 6: debió marcarse PENDIENTE DE VALIDACIÓN y escalar |

Cifras de referencia del ejemplo: 15 casos · 8 críticos y 7 normales · 5 aprobados, 2 rechazados y 1 sin respuesta · aprobadores: Ana Pérez, Carlos Ruiz y Laura Gómez.

> **Fíjate en quién decide, también aquí:** el agente **analiza y recomienda**; el participante **revisa** el informe; el comité **decide**.

**Ruta alternativa (sin habilidades o sin agentes):** adjuntar el Excel en Copilot Chat y usar el prompt: *«Analiza esta tabla de trazabilidad: cuenta casos por Ruta, separa los que decidió una persona (Approve/Reject) de los que no requirieron decisión, lista los casos que requieren atención (críticos sin respuesta, duplicados, posibles riesgos registrados como normales) y separa evidencia de inferencia. No estimes: calcula con los datos.»*

**Cierre del 3.4:**
- **Llévalo a tu trabajo:** aplicar el patrón a un proceso real, sin información confidencial.
- **Antes de terminar:** una lista de 9 comprobaciones (se agrega: *¿audité el informe del agente contra el registro antes de usarlo?*).

---

## 7. Mensajes que se lleva el participante

1. **Cuaderno = contexto.** El formato cambia; la evidencia no.
2. **Agente = comportamiento consistente.** Propósito, instrucciones, conocimiento y límites. Propone, no decide.
3. **Automatización = evento + regla + persona.** Si una regla se puede escribir, no necesita IA.
4. **Toda acción sensible pasa por una aprobación humana, y todo queda registrado.**
5. **Lo que se registra se puede analizar.** La trazabilidad no es un archivo muerto: es la evidencia para el comité.
6. *Copilot acelera el trabajo. Las reglas controlan. Las personas autorizan.*

> **La pregunta ya no es solo «¿qué prompt debo escribir?».** Es: ¿qué parte del trabajo necesita contexto, cuál necesita especialización, cuál puede automatizarse y cuál debe seguir siendo humana?

---

## 8. Entregables y criterios de logro

| Misión | Entregable | Se considera logrado si… |
|---|---|---|
| 3.1 | Centro de Conocimiento Horizonte | El participante verificó la síntesis contra las fuentes y superó el checkpoint |
| 3.2 | Agente que supera las 4 pruebas y el reporte `[HORIZONTE]` de la prueba 4 | Pasó las pruebas de función, especialización, límites y preparación para automatización |
| 3.3 | Flujo probado con los 3 casos, con captura del historial de ejecuciones y del Excel con 3 filas | Solo se envía si una persona aprueba, los casos no críticos no disparan acciones y queda trazabilidad |
| 3.4 | Diseño del sistema de trabajo, prueba integrada e informe para el comité | Resolvió los 6 desafíos, justificó el control humano en las decisiones críticas y auditó el informe del agente contra el registro |

---

## 9. Notas para quien facilita

- **Avance:** el progreso de cada participante se guarda en su cuenta. El cierre de cada misión se habilita al marcar los pasos y superar el checkpoint.
- **El error más común en el 3.3:** que el agente o el participante escriba `Criticidad:` en negrita o con emoji. Revisarlo primero cuando "el flujo no aprueba".
- **Para repetir una prueba**, se envía un correo nuevo. No se debe usar «Volver a enviar» en el historial.
- **Cuentas:** quien aprueba debe usar una cuenta institucional; una cuenta externa no puede responder la aprobación.
- **Otros flujos activos:** si un participante tiene otro flujo (una versión anterior o una copia) vigilando `[HORIZONTE]`, se crean correos y aprobaciones repetidas. Pedir que desactiven todo menos el flujo del laboratorio.
- **Excel como conocimiento del agente:** puede tardar en indexarse. Para el 3.4 es más confiable **adjuntarlo en la conversación**.
- **Habilidades:** son una función reciente de Agent Builder y su disponibilidad depende de la licencia y la configuración de la organización. Si no aparecen, usar la ruta alternativa del 3.4.
- **Aviso:** Proyecto Horizonte es un caso académico ficticio. El reconocimiento de Copilot Lab es interno del curso y no es una certificación oficial.
