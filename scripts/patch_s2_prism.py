# -*- coding: utf-8 -*-
"""Inyecta metodología PRISM + Prompt Lab 4 niveles en Sesión 2."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
JSON_PATH = Path(__file__).with_name("s2_prism_data.json")

CSS = r"""
    /* ========== S2 PRISM PROMPT LAB ========== */
    .prism-method {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 0.55rem;
      margin: 0.75rem 0 1rem;
    }
    .prism-method__item {
      background: var(--bg-elevated);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 0.7rem 0.75rem;
      border-top: 3px solid var(--brand-primary);
    }
    .prism-method__item strong {
      display: block;
      font-size: 0.78rem;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: var(--brand-primary);
      margin-bottom: 0.25rem;
    }
    .prism-method__item span { font-size: 0.84rem; color: var(--text-muted); }
    .prism-host { margin: 1.25rem 0 1.5rem; }
    .prism-host__title {
      margin: 0 0 0.75rem;
      font-size: 1.05rem;
    }
    .prism-levels {
      display: grid;
      grid-template-columns: 1fr;
      gap: 0.85rem;
    }
    .prism-card {
      background: var(--bg-elevated);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 0.85rem 1rem;
    }
    .prism-card--l1 { border-left: 4px solid #c0392b; }
    .prism-card--l2 { border-left: 4px solid #d68910; }
    .prism-card--l3 { border-left: 4px solid var(--brand-primary); }
    .prism-card--l4 { border-left: 4px solid #2f9e6a; }
    .prism-card h5 { margin: 0 0 0.5rem; font-size: 0.95rem; }
    .prism-card .prompt-box {
      max-height: 220px;
      overflow: auto;
      white-space: pre-wrap;
      font-size: 0.84rem;
      margin: 0.4rem 0 0.65rem;
    }
    .prism-panel {
      display: none;
      margin-top: 0.65rem;
      padding: 0.75rem;
      border-radius: var(--radius-sm);
      background: color-mix(in srgb, var(--brand-primary) 8%, var(--bg));
      border: 1px solid var(--border);
      font-size: 0.88rem;
    }
    .prism-panel.is-open { display: block; }
    .prism-panel h6 { margin: 0 0 0.4rem; font-size: 0.86rem; }
    .prism-panel ul { margin: 0.35rem 0 0; padding-left: 1.1rem; }
    .prism-improve textarea {
      width: 100%;
      min-height: 110px;
      font: inherit;
      padding: 0.55rem 0.65rem;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: var(--bg);
      color: var(--text);
    }
    .visual-ask-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 0.5rem;
      margin: 0.75rem 0;
    }
    .visual-ask-grid span {
      display: block;
      padding: 0.55rem 0.65rem;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      background: var(--bg-elevated);
      font-size: 0.84rem;
    }
    @media (max-width: 900px) {
      .prism-method { grid-template-columns: 1fr 1fr; }
    }
    @media (max-width: 560px) {
      .prism-method { grid-template-columns: 1fr; }
    }
    @media print {
      .prism-card .prompt-box { max-height: none; }
      .prism-panel { display: block !important; }
    }

"""

JS_ENGINE = r'''
  /* ========== S2 PRISM ENGINE ========== */
  const S2_PRISM = __S2_PRISM_JSON__;

  function escHtml(s) {
    return String(s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function renderPrismLab(key, data) {
    const levels = data.levels || {};
    const cards = ["1", "2", "3", "4"].map(n => {
      const L = levels[n] || { label: "Nivel " + n, text: "" };
      const id = "prism-" + key + "-l" + n;
      const cls = "prism-card prism-card--l" + n;
      return (
        '<div class="' + cls + '">' +
        '<h5><span class="dyn-chip">Nivel ' + n + '</span> ' + escHtml(L.label) + '</h5>' +
        '<div class="prompt-box" id="' + id + '">' + escHtml(L.text) + '</div>' +
        '<div class="btn-group" style="flex-wrap:wrap;gap:0.4rem">' +
        '<button type="button" class="btn btn--sm btn--secondary" data-copy="#' + id + '"><i data-lucide="copy" width="14" height="14"></i> Copiar</button>' +
        '<button type="button" class="btn btn--sm btn--ghost" data-prism-action="explain" data-prism-key="' + key + '" data-prism-level="' + n + '"><i data-lucide="help-circle" width="14" height="14"></i> Explicar</button>' +
        '<button type="button" class="btn btn--sm btn--ghost" data-prism-action="compare" data-prism-key="' + key + '" data-prism-level="' + n + '"><i data-lucide="git-compare" width="14" height="14"></i> Comparar</button>' +
        '<button type="button" class="btn btn--sm btn--energy" data-prism-action="improve" data-prism-key="' + key + '" data-prism-level="' + n + '"><i data-lucide="sparkles" width="14" height="14"></i> Mejorar</button>' +
        '</div>' +
        '<div class="prism-panel" id="panel-' + id + '" hidden></div>' +
        '</div>'
      );
    }).join("");

    const hints = (data.improveHints || []).map(h => "<li>" + escHtml(h) + "</li>").join("");
    const improveId = "prism-improve-" + key;
    return (
      '<div class="prism-host" data-prism-ready="' + key + '">' +
      '<h4 class="prism-host__title"><i data-lucide="layers" width="18" height="18"></i> Prompt Lab · ' + escHtml(data.title) + '</h4>' +
      '<p class="text-muted" style="font-size:0.88rem;margin:0 0 0.75rem">Fuente: <strong>' + escHtml(data.file) + '</strong> · Persona sugerida: ' + escHtml(data.persona) + '. Usa la metodología <strong>PRISM</strong> (Persona · Realidad · Información · Solicitud · Método).</p>' +
      '<div class="prism-levels">' + cards + '</div>' +
      '<div class="card prism-improve" style="margin:1rem 0 0;padding:1rem">' +
      '<h4 style="margin:0 0 0.5rem">Mejora tu prompt</h4>' +
      '<p class="text-muted" style="font-size:0.88rem">Responde las preguntas y construye una segunda versión. Se guarda en LocalStorage.</p>' +
      '<ul style="font-size:0.9rem">' + hints + '</ul>' +
      '<label for="' + improveId + '" style="display:block;margin:0.65rem 0 0.35rem;font-weight:600">Tu segunda versión (PRISM)</label>' +
      '<textarea id="' + improveId + '" data-s2-note="' + improveId + '" placeholder="Reescribe el prompt profesional con más precisión…"></textarea>' +
      '</div></div>'
    );
  }

  function fillPrismPanel(panel, key, action, level) {
    const data = S2_PRISM[key];
    if (!data || !panel) return;
    if (action === "explain") {
      const e = data.explain || {};
      panel.innerHTML =
        "<h6>¿Por qué este prompt funciona?</h6>" +
        "<ul>" +
        "<li><strong>P · Persona:</strong> " + escHtml(e.persona) + "</li>" +
        "<li><strong>R · Realidad:</strong> " + escHtml(e.realidad) + "</li>" +
        "<li><strong>I · Información:</strong> " + escHtml(e.informacion) + "</li>" +
        "<li><strong>S · Solicitud:</strong> " + escHtml(e.solicitud) + "</li>" +
        "<li><strong>M · Método:</strong> " + escHtml(e.metodo) + "</li>" +
        "<li><strong>Restricciones:</strong> " + escHtml(e.restricciones) + "</li>" +
        "<li><strong>Formato:</strong> " + escHtml(e.formato) + "</li>" +
        "<li><strong>Validación:</strong> " + escHtml(e.validacion) + "</li>" +
        "</ul>" +
        "<p style='margin:0.5rem 0 0;font-size:0.84rem' class='text-muted'>Nivel actual: " + escHtml(level) + ". Los niveles 3 y 4 aplican PRISM completo + informe ejecutivo.</p>";
    } else if (action === "compare") {
      const l1 = (data.levels && data.levels["1"] && data.levels["1"].text) || "";
      const l3 = (data.levels && data.levels["3"] && data.levels["3"].text) || "";
      panel.innerHTML =
        "<h6>Comparar · Básico vs Profesional</h6>" +
        "<p>" + escHtml(data.compare || "") + "</p>" +
        "<p><strong>Básico (" + l1.length + " caracteres):</strong> corto, ambiguo, sin fuentes ni formato.</p>" +
        "<p><strong>Profesional (" + l3.length + " caracteres):</strong> fija rol, contexto, archivos, entregables, clasificaciones y validación humana.</p>" +
        "<p class='text-muted' style='font-size:0.84rem;margin:0'>Un buen resultado depende más de la calidad del prompt que de «probar suerte» con Copilot.</p>";
    } else if (action === "improve") {
      const ta = document.getElementById("prism-improve-" + key);
      if (ta) {
        ta.focus();
        ta.scrollIntoView({ behavior: "smooth", block: "center" });
      }
      panel.innerHTML =
        "<h6>Mejorar</h6>" +
        "<p>Usa el bloque <strong>Mejora tu prompt</strong> debajo. Partiendo del nivel " + escHtml(level) + ", agrega restricciones, formato y evidencia. Luego copia tu segunda versión a Copilot.</p>";
    }
    panel.hidden = false;
    panel.classList.add("is-open");
  }

  function initS2PrismEngine() {
    if (!window.S2_PRISM && typeof S2_PRISM === "undefined") return;
    document.querySelectorAll('article.reto[data-reto^="s2-f"]').forEach(art => {
      const reto = art.getAttribute("data-reto") || "";
      const key = reto.replace(/^s2-/, "");
      if (!S2_PRISM[key] || art.dataset.prismMounted) return;
      art.dataset.prismMounted = "1";
      const body = art.querySelector(".reto__body");
      if (!body) return;

      // Quitar labs/prompt cards antiguos (se reemplazan por PRISM)
      body.querySelectorAll(".prompt-lab").forEach(el => el.remove());
      body.querySelectorAll(".improve-card").forEach(el => {
        if (el.querySelector(".prompt-box")) el.remove();
      });
      // Quitar prompt-box sueltos de fases anteriores (ids s2f*-p*)
      body.querySelectorAll('[id^="s2f"][id*="-p"]').forEach(el => {
        const wrap = el.closest(".m365-box") || el.parentElement;
        if (wrap && wrap !== body) {
          // keep m365-box if it has non-prompt content
          const onlyPrompt = wrap.querySelectorAll(".prompt-box").length && !wrap.querySelector("ol, ul.check-list, table");
        }
      });

      const host = document.createElement("div");
      host.innerHTML = renderPrismLab(key, S2_PRISM[key]);
      const node = host.firstElementChild;

      // Insertar antes de la primera checklist de validación o al final
      const anchor =
        body.querySelector("ul.check-list") ||
        body.querySelector(".table-wrap") ||
        null;
      if (anchor && anchor.parentElement === body) {
        body.insertBefore(node, anchor);
      } else if (anchor) {
        anchor.parentElement.insertBefore(node, anchor);
      } else {
        body.appendChild(node);
      }
    });

    document.querySelectorAll("[data-prism-action]").forEach(btn => {
      if (btn.dataset.boundPrism) return;
      btn.dataset.boundPrism = "1";
      btn.addEventListener("click", () => {
        const key = btn.getAttribute("data-prism-key");
        const level = btn.getAttribute("data-prism-level");
        const action = btn.getAttribute("data-prism-action");
        const panel = document.getElementById("panel-prism-" + key + "-l" + level);
        if (!panel) return;
        if (panel.classList.contains("is-open") && panel.dataset.lastAction === action) {
          panel.classList.remove("is-open");
          panel.hidden = true;
          return;
        }
        panel.dataset.lastAction = action;
        fillPrismPanel(panel, key, action, level);
        if (window.lucide) lucide.createIcons({ nodes: [panel] });
      });
    });

    initCopyButtons();
    // re-bind notes for new textareas
    document.querySelectorAll("[data-s2-note]").forEach(el => {
      if (el.dataset.boundNote) return;
      el.dataset.boundNote = "1";
      const key = el.getAttribute("data-s2-note");
      state.s2Notes = state.s2Notes || {};
      if (state.s2Notes[key] != null) el.value = state.s2Notes[key];
      const persist = () => {
        state.s2Notes = state.s2Notes || {};
        state.s2Notes[key] = el.value;
        saveState();
      };
      el.addEventListener("input", persist);
      el.addEventListener("change", persist);
    });
    if (window.lucide) {
      const s2 = document.getElementById("sesion2");
      if (s2) lucide.createIcons({ nodes: [s2] });
    }
  }

'''

METHOD_HTML = r'''
        <div class="card" style="margin:1.5rem 0">
          <h3>Prompt Engineering Empresarial · Metodología PRISM</h3>
          <p>Esta sesión enseña a <strong>diseñar, justificar, mejorar y validar</strong> prompts reutilizables. Copilot es la herramienta; la calidad del resultado depende del prompt.</p>
          <div class="prism-method" aria-label="Metodología PRISM">
            <div class="prism-method__item"><strong>P · Persona</strong><span>¿Quién debe ser Copilot? (PMO, auditor, analista financiero, especialista en riesgos…)</span></div>
            <div class="prism-method__item"><strong>R · Realidad</strong><span>Contexto de negocio, tipo de proyecto, objetivo y limitaciones.</span></div>
            <div class="prism-method__item"><strong>I · Información</strong><span>Archivos autorizados, fuentes prohibidas y tratamiento de faltantes.</span></div>
            <div class="prism-method__item"><strong>S · Solicitud</strong><span>Análisis, entregables y preguntas que debe responder.</span></div>
            <div class="prism-method__item"><strong>M · Método</strong><span>Tablas, matrices, semáforos, conclusiones y validación humana.</span></div>
          </div>
          <p class="text-muted" style="font-size:0.88rem;margin:0">Cada actividad incluye Prompt Lab en <strong>4 niveles</strong>: Básico → Mejorado → Profesional (PRISM) → Experto (entregable para gerencia).</p>
        </div>

        <div class="card" style="margin:1.5rem 0">
          <h3>Cómo pedir resultados profesionales</h3>
          <p>Enseña a Copilot a responder con estructura visual. Solicita explícitamente:</p>
          <div class="visual-ask-grid">
            <span>Tablas Markdown</span>
            <span>Matrices</span>
            <span>Listas jerarquizadas</span>
            <span>Cuadros comparativos</span>
            <span>Indicadores / KPIs</span>
            <span>Resúmenes ejecutivos</span>
            <span>Diagramas en texto</span>
            <span>Árboles de decisión</span>
            <span>Tablas de priorización</span>
            <span>Cuadros de riesgos 🔴🟡🟢</span>
          </div>
          <p style="margin:0.5rem 0 0;font-size:0.9rem"><strong>Ejemplo de instrucción final:</strong> «PRESENTA LA RESPUESTA COMO UN INFORME EJECUTIVO» con portada, tablero, matrices, clasificaciones (Hecho / Inferencia / Pendiente / Recomendación) y validación humana.</p>
        </div>

'''


def main() -> None:
    prism = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    t = INDEX.read_text(encoding="utf-8")

    # CSS
    if "S2 PRISM PROMPT LAB" not in t:
        anchor = "    /* ========== S2 HORIZONTE (Copilot Chat) ========== */"
        if anchor in t:
            t = t.replace(anchor, CSS + anchor, 1)
        else:
            t = t.replace("    .entregable", CSS + "    .entregable", 1)

    # Subtitle / lead
    t = t.replace(
        '<p class="lead">Analiza, integra y transforma archivos empresariales mediante Microsoft 365 Copilot.</p>',
        '<p class="lead">Prompt Engineering Empresarial con Microsoft 365 Copilot: analiza, integra y transforma archivos del Proyecto Horizonte diseñando prompts profesionales reutilizables.</p>',
        1,
    )
    t = t.replace(
        '<span><strong>Principio pedagógico.</strong> “Copilot organiza, relaciona y propone. La persona verifica las fuentes, corrige el resultado y toma las decisiones.”</span>',
        '<span><strong>Principio pedagógico.</strong> “Copilot organiza, relaciona y propone. La persona verifica las fuentes, corrige el resultado y toma las decisiones.” Un buen resultado no depende solo de Copilot: depende de la calidad del prompt.</span>',
        1,
    )

    # Insert PRISM method cards after pedagogy / before s2-done or herramientas
    if "Metodología PRISM" not in t:
        marker = '        <label class="principle" style="margin:1rem 0;cursor:pointer">\n          <input type="checkbox" data-progress="s2-done"'
        # find within sesion2
        s2a = t.find('id="sesion2"')
        idx = t.find(marker, s2a)
        if idx < 0:
            raise SystemExit("No marker for method cards")
        t = t[:idx] + METHOD_HTML + t[idx:]

    # Learning outcomes add prompt engineering
    if "Construir prompts con metodología PRISM" not in t:
        t = t.replace(
            "<li>Referenciar archivos correctamente.</li>",
            "<li>Construir prompts con metodología PRISM.</li>\n            <li>Comparar prompts básicos vs profesionales.</li>\n            <li>Referenciar archivos correctamente.</li>",
            1,
        )

    # File buttons: add banco + guia + eml
    if 'data-planilla="s2v2-banco"' not in t:
        t = t.replace(
            '<button type="button" class="btn btn--sm btn--primary" data-planilla="s2v2-kit"><i data-lucide="package" width="14" height="14"></i> Kit completo (.zip)</button>\n          </div>',
            '<button type="button" class="btn btn--sm btn--primary" data-planilla="s2v2-kit"><i data-lucide="package" width="14" height="14"></i> Kit completo (.zip)</button>\n'
            '            <button type="button" class="btn btn--sm btn--secondary" data-planilla="s2v2-banco"><i data-lucide="library" width="14" height="14"></i> 09 Banco de prompts</button>\n'
            '            <button type="button" class="btn btn--sm btn--ghost" data-planilla="s2v2-guia-instructor"><i data-lucide="graduation-cap" width="14" height="14"></i> Guía instructor</button>\n'
            '            <button type="button" class="btn btn--sm btn--ghost" data-planilla="s2v2-eml"><i data-lucide="mail" width="14" height="14"></i> 01 Correo (.eml)</button>\n'
            '          </div>',
            1,
        )

    # PLANILLAS entries
    if '"s2v2-banco"' not in t:
        t = t.replace(
            '    "s2v2-kit": () => downloadStaticFile(\n'
            '      "planillas/MCP365_S2_Kit_Proyecto_Horizonte.zip",\n'
            '      "MCP365_S2_Kit_Proyecto_Horizonte.zip"\n'
            '    ),\n',
            '    "s2v2-kit": () => downloadStaticFile(\n'
            '      "planillas/MCP365_S2_Kit_Proyecto_Horizonte.zip",\n'
            '      "MCP365_S2_Kit_Proyecto_Horizonte.zip"\n'
            '    ),\n'
            '    "s2v2-banco": () => downloadStaticFile(\n'
            '      "planillas/09_Banco_Prompts_Sesion2_Copilot.docx",\n'
            '      "09_Banco_Prompts_Sesion2_Copilot.docx"\n'
            '    ),\n'
            '    "s2v2-guia-instructor": () => downloadStaticFile(\n'
            '      "planillas/00_Guia_Instructor_Sesion2.docx",\n'
            '      "00_Guia_Instructor_Sesion2.docx"\n'
            '    ),\n'
            '    "s2v2-eml": () => downloadStaticFile(\n'
            '      "planillas/01_Correo_Solicitud_Proyecto_Horizonte.eml",\n'
            '      "01_Correo_Solicitud_Proyecto_Horizonte.eml"\n'
            '    ),\n',
            1,
        )

    # TEMPLATES
    if 'key: "s2v2-banco"' not in t:
        t = t.replace(
            '{ name: "S2 Kit Horizonte (zip)", desc: "Los 8 archivos del caso", key: "s2v2-kit", type: "ZIP" },\n',
            '{ name: "S2 Kit Horizonte (zip)", desc: "Archivos del caso + banco de prompts", key: "s2v2-kit", type: "ZIP" },\n'
            '    { name: "S2 Banco de prompts", desc: "Word · Banco profesional Sesión 2", key: "s2v2-banco", type: "Word" },\n'
            '    { name: "S2 Guía instructor", desc: "Word · Secuencia sugerida", key: "s2v2-guia-instructor", type: "Word" },\n'
            '    { name: "S2 Correo (.eml)", desc: "Mensaje de práctica importable", key: "s2v2-eml", type: "Email" },\n',
            1,
        )

    # Update global Prompt Lab header to PRISM 4 levels note
    t = t.replace(
          '<h3><i data-lucide="flask-conical" width="20" height="20"></i> Prompt Lab</h3>\n'
          '          <p>Cada actividad sólida combina estos bloques:</p>',
          '<h3><i data-lucide="flask-conical" width="20" height="20"></i> Prompt Lab · Constructor PRISM</h3>\n'
          '          <p>Además del Prompt Lab de cada fase (4 niveles), construye aquí tu propio prompt. Bloques:</p>',
          1,
    )

    # Update builder labels to PRISM
    replacements = [
        ('<label for="s2pb-rol">Rol</label>', '<label for="s2pb-rol">P · Persona (rol)</label>'),
        ('<label for="s2pb-contexto">Contexto</label>', '<label for="s2pb-contexto">R · Realidad (contexto)</label>'),
        ('<label for="s2pb-archivos">Archivo o archivos</label>', '<label for="s2pb-archivos">I · Información (archivos autorizados)</label>'),
        ('<label for="s2pb-objetivo">Objetivo</label>', '<label for="s2pb-objetivo">S · Objetivo de negocio</label>'),
        ('<label for="s2pb-tarea">Tarea</label>', '<label for="s2pb-tarea">S · Solicitud / entregable</label>'),
        ('<label for="s2pb-formato">Formato de salida</label>', '<label for="s2pb-formato">M · Método / formato (informe ejecutivo)</label>'),
    ]
    for a, b in replacements:
        t = t.replace(a, b, 1)

    # Upgrade buildS2PromptFromFields to PRISM structure
    old_build = None
    # Replace function body via marker
    if "P → PERSONA" not in t[t.find("function buildS2PromptFromFields"): t.find("function buildS2PromptFromFields") + 1200]:
        t = re.sub(
            r"function buildS2PromptFromFields\(\) \{[\s\S]*?\n  \}\n\n  function renderS2SavedPrompts",
            '''function buildS2PromptFromFields() {
    const g = (id) => {
      const el = document.getElementById(id);
      return el ? String(el.value || "").trim() : "";
    };
    const rol = g("s2pb-rol") || "Consultor senior";
    const ctx = g("s2pb-contexto") || "No especificado";
    const archivos = g("s2pb-archivos") || "No especificado";
    const objetivo = g("s2pb-objetivo") || "No especificado";
    const tarea = g("s2pb-tarea") || "No especificado";
    const elementos = g("s2pb-elementos") || "No especificado";
    const restricciones = g("s2pb-restricciones") || "No inventar datos. Usar solo las fuentes indicadas.";
    const formato = g("s2pb-formato") || "Informe ejecutivo con tablas Markdown y clasificaciones.";
    const verificacion = g("s2pb-verificacion") || "Indica evidencia y sección de origen.";
    const faltantes = g("s2pb-faltantes") || "Marca faltantes como PENDIENTE DE VALIDACIÓN.";
    return (
      "P → PERSONA\\nActúa como " + rol + ".\\n\\n" +
      "R → REALIDAD\\n" + ctx + "\\n\\n" +
      "I → INFORMACIÓN\\nFuentes autorizadas: " + archivos + "\\nNo uses fuentes externas.\\nTratamiento de faltantes: " + faltantes + "\\n\\n" +
      "S → SOLICITUD\\nObjetivo: " + objetivo + "\\nTarea: " + tarea + "\\nElementos a identificar:\\n" + elementos + "\\n\\n" +
      "M → MÉTODO\\n" + formato + "\\nVerificación: " + verificacion + "\\nRestricciones:\\n" + restricciones + "\\n\\n" +
      "Antes de responder:\\n1. Verifica que toda afirmación tenga evidencia.\\n2. Indica cuando una conclusión sea una inferencia.\\n3. No inventes cifras.\\n4. No inventes fechas.\\n5. No inventes responsables.\\n6. No inventes decisiones.\\n7. Marca toda información faltante como \\"PENDIENTE DE VALIDACIÓN\\".\\n\\n" +
      "PRESENTA LA RESPUESTA COMO UN INFORME EJECUTIVO\\nIncluye portada, resumen ejecutivo (máx. 250 palabras), tablero con semáforos, matrices en Markdown, clasificaciones (Hecho confirmado / Inferencia / Información pendiente / Recomendación), riesgos 🔴🟡🟢, recomendaciones, conclusiones (máx. 5), próximos pasos, preguntas para el cliente y validación humana."
    );
  }

  function renderS2SavedPrompts''',
            t,
            count=1,
        )

    # Embed prism engine: replace or insert before S2 PROMPT LAB
    prism_json = json.dumps(prism, ensure_ascii=False)
    engine = JS_ENGINE.replace("__S2_PRISM_JSON__", prism_json)

    if "S2 PRISM ENGINE" in t:
        a = t.find("  /* ========== S2 PRISM ENGINE ========== */")
        b = t.find("  /* ========== S2 PROMPT LAB + NOTES ========== */", a)
        if a >= 0 and b > a:
            t = t[:a] + engine + "\n" + t[b:]
        else:
            # replace until BOOT
            b = t.find("  /* ========== BOOT ========== */", a)
            t = t[:a] + engine + "\n" + t[b:]
    else:
        marker = "  /* ========== S2 PROMPT LAB + NOTES ========== */"
        if marker not in t:
            marker = "  /* ========== BOOT ========== */"
        t = t.replace(marker, engine + "\n" + marker, 1)

    # Boot call
    if "initS2PrismEngine();" not in t:
        t = t.replace(
            "    initS2PromptLab();\n",
            "    initS2PromptLab();\n    initS2PrismEngine();\n",
            1,
        )

    # Version
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    app = re.sub(
        r'APP_CODE_VERSION = "[^"]+"',
        'APP_CODE_VERSION = "2026-08-04-s2-prism-prompt-lab-v1"',
        app,
        count=1,
    )
    (ROOT / "app.py").write_text(app, encoding="utf-8")

    INDEX.write_text(t, encoding="utf-8")

    # Verify
    tt = INDEX.read_text(encoding="utf-8")
    s2a = tt.find('id="sesion2"')
    s2b = tt.find('id="prompts"')
    s2 = tt[s2a:s2b]
    checks = {
        "PRISM method": "Metodología PRISM" in s2,
        "visual ask": "Cómo pedir resultados profesionales" in s2,
        "engine": "initS2PrismEngine" in tt,
        "json f8": '"f8"' in tt[tt.find("S2_PRISM"): tt.find("S2_PRISM") + 500] or '"f8"' in tt,
        "banco planilla": "s2v2-banco" in tt,
        "no PA except unavailable": all(
            "Power Automate" not in ln or ln.strip() == "<li>Power Automate.</li>"
            for ln in s2.splitlines()
        ),
        "S1 ok": "Circuito N-14" in tt,
    }
    for k, v in checks.items():
        print(("OK" if v else "FAIL"), k)
    if not all(checks.values()):
        raise SystemExit(1)
    print("OK prism patch")


if __name__ == "__main__":
    main()
