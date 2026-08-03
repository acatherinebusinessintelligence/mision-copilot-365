# -*- coding: utf-8 -*-
"""Actualiza únicamente el Caso 6 a flujo Excel-fuente → HTML entregable."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
PROMPT_JS = ROOT / "scripts" / "_r6_prompt_html_js.txt"


def main():
    t = INDEX.read_text(encoding="utf-8")
    prompt_js = PROMPT_JS.read_text(encoding="utf-8").rstrip() + "\n\n"

    # --- 1) Article UI (Caso 6) ---
    old_article_start = '        <!-- RETO 6 -->\n        <article class="reto" data-reto="r6">'
    old_article_end = '            <div data-reto-enhance="r6"></div>\n          </div>\n        </article>'
    i0 = t.find(old_article_start)
    i1 = t.find(old_article_end, i0)
    if i0 < 0 or i1 < 0:
        raise SystemExit("No se encontró el artículo del Reto 6")
    i1 += len(old_article_end)

    new_article = '''        <!-- RETO 6 -->
        <article class="reto" data-reto="r6">
          <button class="reto__header" aria-expanded="false">
            <span class="reto__title-wrap">
              <span class="reto__num">6</span>
              <span>
                <strong>Priorización del trabajo</strong>
                <span class="text-muted" style="display:block;font-size:0.85rem;color:var(--text-muted)">Copilot · Informe HTML (Excel solo como fuente)</span>
              </span>
            </span>
            <span style="display:flex;align-items:center;gap:0.75rem">
              <label onclick="event.stopPropagation()" style="display:flex;align-items:center;gap:0.4rem;font-size:0.82rem;cursor:pointer">
                <input type="checkbox" data-progress="reto-r6" /> Hecho
              </label>
              <i data-lucide="chevron-down" class="reto__chevron" width="20" height="20"></i>
            </span>
          </button>
          <div class="reto__body">
            <div class="m365-box">
              <h4><span class="app-badge">Excel</span> + <span class="app-badge">Copilot</span> + <span class="app-badge">HTML</span> Paso a paso con Copilot</h4>
              <ol>
                <li>Descarga la base oficial con las diez tareas.</li>
                <li>Abre Copilot Chat y adjunta el archivo Excel. No necesitas modificarlo.</li>
                <li>Revisa y ajusta los campos configurables del prompt.</li>
                <li>Copia y ejecuta el prompt completo.</li>
                <li>Copilot debe clasificar las tareas por urgencia, impacto, dependencia, límite y riesgo por retraso.</li>
                <li>Debe organizar una agenda para hoy, mañana y viernes; identificar tareas delegables y separar las que requieren criterio humano.</li>
                <li>No debe inventar fechas, horas, responsables ni dependencias.</li>
                <li>Descarga o guarda el resultado como: <code>MCP365_P06_Priorizacion_completada.html</code>.</li>
                <li>Abre el HTML en el navegador y verifica sus filtros, botones y contenido.</li>
                <li>La validación humana y el control de calidad los completa la persona.</li>
              </ol>
            </div>
            <p style="margin:0 0 0.5rem;font-size:0.9rem"><strong>Fuente oficial</strong> (no completar en Excel):</p>
            <div class="btn-group" style="margin-bottom:0.75rem;flex-wrap:wrap;gap:0.5rem">
              <button type="button" class="btn btn--sm btn--energy" data-planilla="priorizacion"><i data-lucide="download" width="14" height="14"></i> Descargar base Excel (10 tareas)</button>
            </div>
            <p style="margin:0 0 0.5rem;font-size:0.9rem"><strong>Referencia de calidad</strong> (no es fuente de análisis) y <strong>práctica personal</strong>:</p>
            <div class="btn-group" style="margin-bottom:0.75rem;flex-wrap:wrap;gap:0.5rem">
              <button type="button" class="btn btn--sm btn--ghost" data-planilla="priorizacion-ref"><i data-lucide="eye" width="14" height="14"></i> Ver HTML de referencia</button>
              <button type="button" class="btn btn--sm btn--secondary" data-planilla="priorizacion-practica"><i data-lucide="sparkles" width="14" height="14"></i> Práctica personal (.html)</button>
            </div>
            <div class="doc-box">
              <p><strong>Fuente:</strong> <code>MCP365_P06_Base_priorizacion_tareas.xlsx</code> — diez tareas; no la modifiques ni la completes.</p>
              <p><strong>Entregable:</strong> <code>MCP365_P06_Priorizacion_completada.html</code> — informe HTML interactivo generado por Copilot.</p>
              <p class="text-muted" style="font-size:0.88rem;margin:0">La referencia HTML sirve para validar calidad y funcionamiento del curso. No la uses como fuente de análisis en Copilot.</p>
            </div>
            <div class="table-wrap">
              <table>
                <thead>
                  <tr><th>#</th><th>Tarea</th><th>Urgencia</th><th>Impacto</th><th>Dependencia</th><th>Límite</th><th>Responsable</th><th>Riesgo retraso</th></tr>
                </thead>
                <tbody>
                  <tr><td>1</td><td>Responder consulta de seguridad industrial sobre señalización N-14</td><td>Alta</td><td>Alto</td><td>Ninguna</td><td>Hoy 11:00</td><td>Coordinador de zona</td><td>Alto</td></tr>
                  <tr><td>2</td><td>Revisar borrador de cronograma Proyecto Horizonte</td><td>Media</td><td>Alto</td><td>Datos del contratista</td><td>Hoy 17:00</td><td>Líder de proyecto</td><td>Medio</td></tr>
                  <tr><td>3</td><td>Actualizar registro de riesgos (semana 12)</td><td>Media</td><td>Alto</td><td>Informe de campo</td><td>Mañana 12:00</td><td>Líder de proyecto</td><td>Medio</td></tr>
                  <tr><td>4</td><td>Agendar reunión con junta comunal</td><td>Alta</td><td>Medio</td><td>Disponibilidad de sala</td><td>Hoy 15:00</td><td>Asistente administrativo</td><td>Bajo</td></tr>
                  <tr><td>5</td><td>Preparar resumen ejecutivo para comité</td><td>Alta</td><td>Alto</td><td>KPI de avance</td><td>Mañana 09:00</td><td>Líder de proyecto</td><td>Alto</td></tr>
                  <tr><td>6</td><td>Ordenar carpetas SharePoint del expediente</td><td>Baja</td><td>Bajo</td><td>Ninguna</td><td>Viernes 17:00</td><td>Practicante</td><td>Bajo</td></tr>
                  <tr><td>7</td><td>Validar estado de permiso ambiental</td><td>Alta</td><td>Alto</td><td>Área jurídica</td><td>Hoy 16:00</td><td>Especialista HSE</td><td>Alto</td></tr>
                  <tr><td>8</td><td>Redactar mensaje formal a proveedor de equipo principal</td><td>Media</td><td>Medio</td><td>Confirmación de fecha</td><td>Hoy 16:00</td><td>Compras</td><td>Medio</td></tr>
                  <tr><td>9</td><td>Revisar facturas menores de logística</td><td>Baja</td><td>Bajo</td><td>Ninguna</td><td>Viernes 12:00</td><td>Finanzas</td><td>Bajo</td></tr>
                  <tr><td>10</td><td>Definir escenario de reprogramación para comité</td><td>Alta</td><td>Alto</td><td>Análisis de impacto</td><td>Mañana 14:00</td><td>Comité directivo</td><td>Alto</td></tr>
                </tbody>
              </table>
            </div>
            <div data-reto-enhance="r6"></div>
          </div>
        </article>'''
    t = t[:i0] + new_article + t[i1:]

    # --- 2) Insert buildPromptR6 before RETO_CASES ---
    marker = "  /* ========== RETO ENGINE (patrón S1·R1 reutilizable; R1 no se remonta) ========== */\n"
    if "function buildPromptR6Text" not in t:
        if marker not in t:
            raise SystemExit("No se encontró marcador RETO ENGINE")
        t = t.replace(marker, prompt_js + marker, 1)
    else:
        # Replace existing R6 prompt block if re-running
        start = t.find("  /** Prompt Reto 6:")
        if start < 0:
            start = t.find("  function getPromptR6Fields()")
        end = t.find(marker)
        if start > 0 and end > start:
            t = t[:start] + prompt_js + t[end:]

    # --- 3) Replace RETO_CASES.r6 ---
    r6_start = t.find('  "r6": {')
    r6_end = t.find('  "fase-1": {', r6_start)
    if r6_start < 0 or r6_end < 0:
        raise SystemExit("No se encontró RETO_CASES.r6")

    new_r6 = r'''  "r6": {
    "id": "r6",
    "title": "Priorización del trabajo",
    "apps": ["Excel", "Copilot", "HTML"],
    "email": false,
    "planilla": {"key": "priorizacion", "label": "Descargar base Excel (10 tareas)"},
    "output": "MCP365_P06_Priorizacion_completada.html",
    "steps": [
      "Descarga la base oficial con las diez tareas.",
      "Abre Copilot Chat y adjunta el archivo Excel. No necesitas modificarlo.",
      "Revisa y ajusta los campos configurables del prompt.",
      "Copia y ejecuta el prompt completo.",
      "Copilot clasifica, agenda (hoy/mañana/viernes), delegación y criterio humano.",
      "Guarda como <code>MCP365_P06_Priorizacion_completada.html</code> y verifica en el navegador.",
      "Validación humana y control de calidad los completa la persona."
    ],
    "fields": [
      ["rol", "Rol de Copilot", "Asistente de operaciones especializado en priorización, planificación del trabajo, análisis de dependencias, delegación responsable y gestión de riesgos."],
      ["fuente", "Fuente única", "MCP365_P06_Base_priorizacion_tareas.xlsx — base oficial con diez tareas y los campos Tarea, Urgencia, Impacto, Dependencia, Límite, Responsable y Riesgo por retraso."],
      ["objetivo", "Objetivo", "Ordenar las diez tareas, proponer una agenda para hoy, mañana y viernes, distinguir actividades delegables de decisiones que requieren criterio humano y generar un informe HTML interactivo."],
      ["niveles", "Niveles de prioridad", "P1 · Crítica.\nP2 · Alta.\nP3 · Media.\nP4 · Programable."],
      ["criterios", "Criterios de priorización", "1. Límite.\n2. Urgencia.\n3. Impacto.\n4. Riesgo por retraso.\n5. Dependencia.\n6. Necesidad de criterio humano."],
      ["delegacion", "Categorías de delegación", "Sí.\nParcial.\nNo."],
      ["criterio_humano", "Reglas de criterio humano", "Sí: seguridad industrial, permisos ambientales, evaluación de riesgos, decisiones ejecutivas, reprogramaciones, decisiones de comité, comunicación externa con aprobación, información incompleta, aceptación formal de consecuencias.\nNo: solo actividades administrativas o rutinarias con reglas verificables."],
      ["vacio", "Respuesta para datos ausentes", "No especificado."],
      ["salida", "Nombre del archivo de salida", "MCP365_P06_Priorizacion_completada.html."],
      ["paleta", "Paleta visual", "Azul oscuro: #211D40.\nMorado: #4B3FAA.\nAmarillo: #FFEC00.\nAzul grisáceo: #E7EDF5.\nFondo: #F5F7FA.\nVerde: #D9EAD3.\nAmarillo de pendiente: #FFF2CC.\nRojo de alerta: #F4CCCC.\nTexto: #25283A."]
    ],
    "checklist": [
      ["r6-c1", "Descargué la base Excel"],
      ["r6-c2", "Confirmé que contiene diez tareas"],
      ["r6-c3", "Adjunté el Excel a Copilot"],
      ["r6-c4", "Copié el prompt completo"],
      ["r6-c5", "Recibí un HTML completo"],
      ["r6-c6", "El HTML abre en el navegador"],
      ["r6-c7", "Se analizaron las diez tareas"],
      ["r6-c8", "Se conservan límites y responsables"],
      ["r6-c9", "La agenda distingue hoy, mañana y viernes"],
      ["r6-c10", "La delegación está clasificada"],
      ["r6-c11", "El criterio humano está identificado"],
      ["r6-c12", "Los filtros funcionan"],
      ["r6-c13", "Los botones funcionan"],
      ["r6-c14", "La validación humana está vacía"],
      ["r6-c15", "El control de calidad está vacío"],
      ["r6-c16", "El archivo se llama correctamente"]
    ],
    "practice_title": "Al terminar el caso · Práctica personal de priorización",
    "practice": "Después de terminar el caso, abre: <code>MCP365_P06_Practica_personal_priorizacion.html</code>.<br><br>Registra una lista anonimizada de tus tareas del día.<br><br>No incluyas nombres personales, datos de clientes, información contractual reservada, credenciales, datos financieros sensibles ni identificadores internos.<br><br>La herramienta funciona localmente y elimina las tareas al cerrar la pestaña.<br><br>Revisa personalmente la prioridad sugerida, la posibilidad de delegar y las tareas que necesitan criterio humano.",
    "deliverable": "Entregable del caso: <code>MCP365_P06_Priorizacion_completada.html</code>. Informe HTML interactivo con resumen ejecutivo, agenda sugerida, matriz de priorización, clasificación de delegación y criterio humano. Validación humana y control de calidad vacíos."
  },
'''
    t = t[:r6_start] + new_r6 + t[r6_end:]

    # --- 4) Wire buildPromptFromCase ---
    old_wire = '    if (caseId === "r5") return buildPromptR5Text(getPromptR5Fields());\n'
    new_wire = (
        '    if (caseId === "r5") return buildPromptR5Text(getPromptR5Fields());\n'
        '    if (caseId === "r6") return buildPromptR6Text(getPromptR6Fields());\n'
    )
    if 'caseId === "r6"' not in t:
        if old_wire not in t:
            raise SystemExit("No se encontró cableado de r5 en buildPromptFromCase")
        t = t.replace(old_wire, new_wire, 1)

    # --- 5) Restablecer valores predeterminados en UI del prompt ---
    old_btns = '''      <div class="btn-group" style="margin:0.5rem 0 1rem;flex-wrap:wrap;gap:0.5rem">
        <button class="btn btn--sm btn--secondary" data-copy="#prompt-${caseId}" type="button"><i data-lucide="copy" width="16" height="16"></i> Copiar prompt</button>
        <button class="btn btn--sm btn--ghost" type="button" data-rebuild-prompt="${caseId}"><i data-lucide="refresh-cw" width="16" height="16"></i> Regenerar desde campos</button>
      </div>`;'''
    new_btns = '''      <div class="btn-group" style="margin:0.5rem 0 1rem;flex-wrap:wrap;gap:0.5rem">
        <button class="btn btn--sm btn--secondary" data-copy="#prompt-${caseId}" type="button"><i data-lucide="copy" width="16" height="16"></i> Copiar prompt</button>
        <button class="btn btn--sm btn--ghost" type="button" data-rebuild-prompt="${caseId}"><i data-lucide="refresh-cw" width="16" height="16"></i> Regenerar desde campos</button>
        <button class="btn btn--sm btn--ghost" type="button" data-reset-prompt="${caseId}"><i data-lucide="rotate-ccw" width="16" height="16"></i> Restablecer valores predeterminados</button>
      </div>`;'''
    if "data-reset-prompt" not in t:
        if old_btns not in t:
            raise SystemExit("No se encontraron botones del prompt config")
        t = t.replace(old_btns, new_btns, 1)

    # Bind reset in initRetoEngine (after rebuild binding)
    rebuild_bind = '''    document.querySelectorAll("[data-rebuild-prompt]").forEach(btn => {
      if (btn.dataset.bound) return;
      btn.dataset.bound = "1";
      btn.addEventListener("click", () => {
        const id = btn.getAttribute("data-rebuild-prompt");
        refreshPromptCase(id);
        toast("Prompt regenerado desde los campos", "refresh-cw");
      });
    });'''
    reset_bind = '''    document.querySelectorAll("[data-rebuild-prompt]").forEach(btn => {
      if (btn.dataset.bound) return;
      btn.dataset.bound = "1";
      btn.addEventListener("click", () => {
        const id = btn.getAttribute("data-rebuild-prompt");
        refreshPromptCase(id);
        toast("Prompt regenerado desde los campos", "refresh-cw");
      });
    });
    document.querySelectorAll("[data-reset-prompt]").forEach(btn => {
      if (btn.dataset.bound) return;
      btn.dataset.bound = "1";
      btn.addEventListener("click", () => {
        const id = btn.getAttribute("data-reset-prompt");
        const c = RETO_CASES[id];
        const box = document.getElementById("promptConfig-" + id);
        if (c && c.fields && box) {
          c.fields.forEach(([key, , def]) => {
            const el = box.querySelector('[data-reto-field="' + key + '"]');
            if (el) el.value = def || "";
          });
        }
        refreshPromptCase(id);
        toast("Valores predeterminados restablecidos", "rotate-ccw");
      });
    });'''
    if "data-reset-prompt" in t and "data-reset-prompt]).forEach" not in t and '[data-reset-prompt]")' not in t:
        if rebuild_bind not in t:
            raise SystemExit("No se encontró binding de rebuild prompt")
        t = t.replace(rebuild_bind, reset_bind, 1)

    # --- 6) Replace priorizacion downloadWord with static downloads ---
    p_start = t.find('"priorizacion": () => downloadWord')
    p_next = t.find('"informe-ejecutivo":', p_start)
    if p_start < 0 or p_next < 0:
        raise SystemExit("No se encontró bloque PLANILLAS.priorizacion")
    # include leading spaces / comma context: find start of key with indentation
    line_start = t.rfind("\n", 0, p_start) + 1
    new_planillas = '''    "priorizacion": () => downloadStaticFile(
      "planillas/MCP365_P06_Base_priorizacion_tareas.xlsx",
      "MCP365_P06_Base_priorizacion_tareas.xlsx"
    ),

    "priorizacion-ref": () => downloadStaticFile(
      "planillas/MCP365_P06_Priorizacion_completada.html",
      "MCP365_P06_Priorizacion_completada.html"
    ),

    "priorizacion-practica": () => downloadStaticFile(
      "planillas/MCP365_P06_Practica_personal_priorizacion.html",
      "MCP365_P06_Practica_personal_priorizacion.html"
    ),

'''
    t = t[:line_start] + new_planillas + t[p_next:]

    # --- 7) TEMPLATES catalog ---
    old_tpl = '{ name: "Priorización de jornada", desc: "Excel/Word · 10 tareas, agenda y criterio humano", key: "priorizacion", type: "Word" },'
    new_tpl = '''{ name: "Base priorización P06", desc: "Excel · Diez tareas fuente (no completar)", key: "priorizacion", type: "Excel" },
    { name: "Priorización P06 (referencia HTML)", desc: "HTML · Referencia de calidad del informe", key: "priorizacion-ref", type: "HTML" },
    { name: "Práctica personal priorización", desc: "HTML · Lista local anonimizada (se borra al cerrar)", key: "priorizacion-practica", type: "HTML" },'''
    if old_tpl in t:
        t = t.replace(old_tpl, new_tpl, 1)

    INDEX.write_text(t, encoding="utf-8")
    print("OK: index.html actualizado (Caso 6 → HTML)")

    # Sanity checks
    checks = [
        ("MCP365_P06_Priorizacion_completada.html", True),
        ("MCP365_P06_Priorizacion_completada.xlsx", False),  # should not remain as deliverable in r6 UI text - soft
        ("buildPromptR6Text", True),
        ('caseId === "r6"', True),
        ("planillas/MCP365_P06_Base_priorizacion_tareas.xlsx", True),
        ("priorizacion-practica", True),
        ("data-reset-prompt", True),
        ("No necesitas modificarlo", True),
    ]
    for needle, want in checks:
        found = needle in t
        # xlsx may still appear in unrelated places; only fail if still the r6 output
        if needle.endswith(".xlsx") and needle.startswith("MCP365_P06_Priorizacion_completada"):
            # Allow absence or presence in old comments — check r6 output specifically
            out_ok = '"output": "MCP365_P06_Priorizacion_completada.html"' in t
            print(f"  r6 output html: {out_ok}")
            if not out_ok:
                raise SystemExit("r6 output no es .html")
            continue
        print(f"  {needle!r}: {found} (want {want})")
        if found != want and want:
            raise SystemExit(f"Falta: {needle}")


if __name__ == "__main__":
    main()
