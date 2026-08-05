# -*- coding: utf-8 -*-
"""Reemplaza Sesión 2 (sin Power Automate) por el caso Horizonte Copilot Chat."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
APP = ROOT / "app.py"
SECTION = Path(__file__).with_name("_s2v2_section.html")

NEW_PLANILLAS = '''    "s2v2-correo": () => downloadStaticFile(
      "planillas/01_Correo_Solicitud_Proyecto_Horizonte.pdf",
      "01_Correo_Solicitud_Proyecto_Horizonte.pdf"
    ),
    "s2v2-alcance": () => downloadStaticFile(
      "planillas/02_Alcance_Proyecto_Horizonte.docx",
      "02_Alcance_Proyecto_Horizonte.docx"
    ),
    "s2v2-presupuesto": () => downloadStaticFile(
      "planillas/03_Presupuesto_y_Cronograma_Horizonte.xlsx",
      "03_Presupuesto_y_Cronograma_Horizonte.xlsx"
    ),
    "s2v2-transcripcion": () => downloadStaticFile(
      "planillas/04_Transcripcion_Reunion_Horizonte.docx",
      "04_Transcripcion_Reunion_Horizonte.docx"
    ),
    "s2v2-riesgos": () => downloadStaticFile(
      "planillas/05_Registro_Inicial_Riesgos_Horizonte.xlsx",
      "05_Registro_Inicial_Riesgos_Horizonte.xlsx"
    ),
    "s2v2-comentarios": () => downloadStaticFile(
      "planillas/06_Comentarios_Interesados_Horizonte.docx",
      "06_Comentarios_Interesados_Horizonte.docx"
    ),
    "s2v2-pptx": () => downloadStaticFile(
      "planillas/07_Plantilla_Comite_Horizonte.pptx",
      "07_Plantilla_Comite_Horizonte.pptx"
    ),
    "s2v2-guia": () => downloadStaticFile(
      "planillas/08_Guia_Validacion_Resultados.pdf",
      "08_Guia_Validacion_Resultados.pdf"
    ),
    "s2v2-kit": () => downloadStaticFile(
      "planillas/MCP365_S2_Kit_Proyecto_Horizonte.zip",
      "MCP365_S2_Kit_Proyecto_Horizonte.zip"
    ),

'''

S2_JS = r'''
  /* ========== S2 PROMPT LAB + NOTES ========== */
  function buildS2PromptFromFields() {
    const g = (id) => {
      const el = document.getElementById(id);
      return el ? String(el.value || "").trim() : "";
    };
    const rol = g("s2pb-rol") || "Analista";
    const ctx = g("s2pb-contexto") || "No especificado";
    const archivos = g("s2pb-archivos") || "No especificado";
    const objetivo = g("s2pb-objetivo") || "No especificado";
    const tarea = g("s2pb-tarea") || "No especificado";
    const elementos = g("s2pb-elementos") || "No especificado";
    const restricciones = g("s2pb-restricciones") || "No inventar datos. Usar solo las fuentes indicadas.";
    const formato = g("s2pb-formato") || "Estructura clara con tablas cuando aplique.";
    const verificacion = g("s2pb-verificacion") || "Indica evidencia y sección de origen.";
    const faltantes = g("s2pb-faltantes") || "Escribe «No especificado» cuando falte información.";
    return (
      "Actúa como " + rol + ".\n\n" +
      "Contexto: " + ctx + "\n\n" +
      "Fuentes (únicas): " + archivos + "\n\n" +
      "Objetivo: " + objetivo + "\n\n" +
      "Tarea: " + tarea + "\n\n" +
      "Elementos a identificar:\n" + elementos + "\n\n" +
      "Restricciones:\n" + restricciones + "\n\n" +
      "Formato de salida:\n" + formato + "\n\n" +
      "Verificación:\n" + verificacion + "\n\n" +
      "Tratamiento de información faltante:\n" + faltantes + "\n\n" +
      "Validación humana: toda cifra, fecha, responsable y decisión debe contrastarse con las fuentes originales antes de usarse en un entregable."
    );
  }

  function renderS2SavedPrompts() {
    const list = document.getElementById("s2SavedPrompts");
    if (!list) return;
    const items = (state.s2SavedPrompts || []);
    if (!items.length) {
      list.innerHTML = "<li class=\"text-muted\" style=\"list-style:none\">Aún no hay prompts guardados.</li>";
      return;
    }
    list.innerHTML = items.map((p, i) => {
      const title = (p.title || ("Prompt " + (i + 1))).replace(/</g, "&lt;");
      const preview = String(p.text || "").slice(0, 120).replace(/</g, "&lt;");
      return (
        "<li style=\"list-style:none;margin:0.5rem 0;padding:0.65rem;border:1px solid var(--border);border-radius:var(--radius-sm)\">" +
        "<strong>" + title + "</strong>" +
        "<div class=\"text-muted\" style=\"font-size:0.82rem;margin:0.35rem 0\">" + preview + (String(p.text || "").length > 120 ? "…" : "") + "</div>" +
        "<div class=\"btn-group\">" +
        "<button type=\"button\" class=\"btn btn--sm btn--secondary\" data-s2-load-prompt=\"" + i + "\">Usar</button>" +
        "<button type=\"button\" class=\"btn btn--sm btn--ghost\" data-s2-del-prompt=\"" + i + "\">Eliminar</button>" +
        "</div></li>"
      );
    }).join("");
    list.querySelectorAll("[data-s2-load-prompt]").forEach(btn => {
      btn.addEventListener("click", () => {
        const i = +btn.getAttribute("data-s2-load-prompt");
        const item = (state.s2SavedPrompts || [])[i];
        const out = document.getElementById("s2BuiltPrompt");
        if (item && out) {
          out.textContent = item.text || "";
          toast("Prompt cargado");
        }
      });
    });
    list.querySelectorAll("[data-s2-del-prompt]").forEach(btn => {
      btn.addEventListener("click", () => {
        const i = +btn.getAttribute("data-s2-del-prompt");
        state.s2SavedPrompts = (state.s2SavedPrompts || []).filter((_, idx) => idx !== i);
        saveState();
        renderS2SavedPrompts();
        toast("Prompt eliminado", "trash-2");
      });
    });
  }

  function initS2PromptLab() {
    const buildBtn = document.getElementById("s2BuildPrompt");
    const saveBtn = document.getElementById("s2SavePrompt");
    const clearBtn = document.getElementById("s2ClearPrompts");
    const out = document.getElementById("s2BuiltPrompt");
    if (!buildBtn || buildBtn.dataset.bound) return;
    if (buildBtn) buildBtn.dataset.bound = "1";
    if (buildBtn && out) {
      buildBtn.addEventListener("click", () => {
        out.textContent = buildS2PromptFromFields();
        toast("Prompt construido", "sparkles");
      });
    }
    if (saveBtn) {
      saveBtn.addEventListener("click", () => {
        const text = out ? out.textContent.trim() : "";
        if (!text || text.indexOf("Completa los campos") === 0) {
          toast("Construye un prompt antes de guardar", "alert-triangle");
          return;
        }
        const titleEl = document.getElementById("s2pb-objetivo");
        const title = (titleEl && titleEl.value.trim()) || ("Prompt " + new Date().toLocaleString());
        state.s2SavedPrompts = state.s2SavedPrompts || [];
        state.s2SavedPrompts.unshift({ title: title.slice(0, 80), text: text, at: Date.now() });
        state.s2SavedPrompts = state.s2SavedPrompts.slice(0, 20);
        saveState();
        renderS2SavedPrompts();
        toast("Prompt guardado en LocalStorage", "save");
      });
    }
    if (clearBtn) {
      clearBtn.addEventListener("click", () => {
        state.s2SavedPrompts = [];
        saveState();
        renderS2SavedPrompts();
        toast("Prompts borrados", "eraser");
      });
    }
    // Persist notes / improved prompt textareas
    document.querySelectorAll("[data-s2-note]").forEach(el => {
      if (el.dataset.boundNote) return;
      el.dataset.boundNote = "1";
      const key = el.getAttribute("data-s2-note");
      state.s2Notes = state.s2Notes || {};
      if (state.s2Notes[key]) el.value = state.s2Notes[key];
      el.addEventListener("input", () => {
        state.s2Notes = state.s2Notes || {};
        state.s2Notes[key] = el.value;
        saveState();
      });
    });
    renderS2SavedPrompts();
  }

'''


def replace_between(text: str, start_marker: str, end_marker: str, new_mid: str, *, include_start=True) -> str:
    a = text.find(start_marker)
    if a < 0:
        raise SystemExit(f"No se encontró inicio: {start_marker[:60]}")
    b = text.find(end_marker, a + len(start_marker))
    if b < 0:
        raise SystemExit(f"No se encontró fin tras: {start_marker[:60]}")
    if include_start:
        return text[:a] + new_mid + text[b:]
    return text[: a + len(start_marker)] + new_mid + text[b:]


def main() -> None:
    t = INDEX.read_text(encoding="utf-8")
    section = SECTION.read_text(encoding="utf-8").rstrip() + "\n"

    # Fix: mention Power Automate as unavailable (allowed as restriction)
    section = section.replace(
        "<li>Automatizaciones empresariales fuera del alcance de esta sesión.</li>",
        "<li>Power Automate.</li>\n                <li>Automatizaciones empresariales fuera del alcance de esta sesión.</li>",
        1,
    )

    # --- Replace sesion2 inner HTML ---
    s_open = t.find('<section id="sesion2"')
    if s_open < 0:
        raise SystemExit("No sesion2")
    s_gt = t.find(">", s_open) + 1
    s_close = t.find("</section>", s_gt)
    t = t[:s_gt] + "\n" + section + "    " + t[s_close:]

    # --- CSS: replace old S2 PA / caso1 blocks with lighter S2v2 styles ---
    css_new = """
    /* ========== S2 HORIZONTE (Copilot Chat) ========== */
    .s2-route {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 0.65rem;
      margin: 0.75rem 0 1rem;
    }
    .s2-route__step {
      background: var(--bg-elevated);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 0.65rem 0.75rem;
      font-size: 0.86rem;
    }
    .s2-route__step strong { display: block; color: var(--brand-primary); margin-bottom: 0.2rem; }
    .s2- Dual { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }
    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
    .improve-card {
      background: var(--bg-elevated);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 0.85rem 1rem;
      margin: 0.75rem 0;
    }
    .improve-card h5 { margin: 0 0 0.45rem; font-size: 0.95rem; }
    .improve-card .prompt-box { margin: 0.45rem 0; font-size: 0.86rem; white-space: pre-wrap; }
    .prompt-lab {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 0.75rem;
      margin: 0.75rem 0 1rem;
    }
    .prompt-lab__item {
      background: var(--bg-elevated);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 0.75rem;
    }
    .prompt-lab__item--weak { border-left: 4px solid #c0392b; }
    .prompt-lab__item--pro { border-left: 4px solid #2f9e6a; }
    .s2-val-table input[type="text"],
    .s2-val-table textarea,
    .s2-val-table select {
      width: 100%;
      font: inherit;
      font-size: 0.82rem;
      padding: 0.35rem 0.45rem;
      border: 1px solid var(--border);
      border-radius: 6px;
      background: var(--bg);
      color: var(--text);
    }
    @media (max-width: 900px) {
      .grid-2, .s2-Dual, .prompt-lab { grid-template-columns: 1fr; }
    }
    @media print {
      .improve-card, .prompt-lab__item, .s2-route__step { break-inside: avoid; }
    }

"""
    # Fix typo in css
    css_new = css_new.replace(".s2- Dual", ".s2-dual")

    # Remove old S2 CSS blocks if present
    for marker_start, marker_end in [
        ("    /* ========== S2 CASO 1 COPILOT FLOW ========== */", "    /* ========== POWER AUTOMATE FLOW (S2) ========== */"),
        ("    /* ========== POWER AUTOMATE FLOW (S2) ========== */", "    .entregable"),
        ("    /* ========== S2 HORIZONTE (Copilot Chat) ========== */", "    .entregable"),
    ]:
        a = t.find(marker_start)
        b = t.find(marker_end, a) if a >= 0 else -1
        if a >= 0 and b >= 0:
            t = t[:a] + t[b:]

    # Insert new CSS before .entregable or after m365-box
    if "S2 HORIZONTE (Copilot Chat)" not in t:
        anchor = "    .entregable"
        if anchor not in t:
            raise SystemExit("No .entregable CSS anchor")
        t = t.replace(anchor, css_new + anchor, 1)

    # Also strip leftover .pa-flow rules if still present after partial delete
    # (POWER AUTOMATE block may have left pa-flow if marker mismatch)
    if "POWER AUTOMATE FLOW" in t:
        a = t.find("    /* ========== POWER AUTOMATE FLOW (S2) ========== */")
        # find next major comment or .entregable
        b = t.find("    .entregable", a)
        if a >= 0 and b > a:
            t = t[:a] + t[b:]

    if "S2 CASO 1 COPILOT FLOW" in t:
        a = t.find("    /* ========== S2 CASO 1 COPILOT FLOW ========== */")
        b = t.find("    /* ==========", a + 10)
        if a >= 0 and b > a:
            t = t[:a] + t[b:]

    # Re-ensure CSS present
    if "S2 HORIZONTE (Copilot Chat)" not in t:
        t = t.replace("    .entregable", css_new + "    .entregable", 1)

    # --- PROGRESS_KEYS ---
    t = re.sub(
        r'const PROGRESS_KEYS = \[[^\]]+\]',
        'const PROGRESS_KEYS = [\n'
        '    "reto-r1","reto-r2","reto-r3","reto-r4","reto-r5","reto-r6",\n'
        '    "s1-done","s2-done","proyecto-final",\n'
        '    "s2-f0","s2-f1","s2-f2","s2-f3","s2-f4","s2-f5","s2-f6","s2-f7","s2-f8",\n'
        '    "s2-e1","s2-e2","s2-e3","s2-e4","s2-e5","s2-e6","s2-e7","s2-e8","s2-e9","s2-e10"\n'
        '  ]',
        t,
        count=1,
    )

    # --- Remove fase-1..fase-6 from RETO_CASES ---
    # Keep r6 closing, remove from "fase-1" through end of fase-6 before closing of RETO_CASES
    m = re.search(r',\s*"fase-1"\s*:\s*\{', t)
    if m:
        start = m.start()
        end = t.find("\n};\n\n  function buildPromptFromCase", start)
        if end < 0:
            end = t.find("\n};\n\n  function renderDeliverableHtml", start)
        if end < 0:
            raise SystemExit("No se pudo localizar fin de RETO_CASES para borrar fase-*")
        t = t[:start] + t[end:]

    # --- PLANILLAS: replace old s2-* with s2v2-* ---
    for key in ("s2-ficha", "s2-control", "s2-informe-plantilla", "s2-guia-pa", "s2-resultado"):
        # remove block
        pat = rf'    "{key}": \(\) => downloadStaticFile\(\n      "[^"]+",\n      "[^"]+"\n    \),\n\n'
        t2 = re.sub(pat, "", t)
        if t2 == t:
            pat2 = rf'    "{key}": \(\) => downloadStaticFile\(\n      "[^"]+",\n      "[^"]+"\n    \),\n'
            t2 = re.sub(pat2, "", t)
        t = t2

    if "s2v2-correo" not in t:
        # insert before informe-ejecutivo or after priorizacion-practica
        anchor = '    "informe-ejecutivo":'
        if anchor not in t:
            raise SystemExit("No planillas anchor")
        t = t.replace(anchor, NEW_PLANILLAS + anchor, 1)

    # --- TEMPLATES: replace S2 entries ---
    # Remove old S2 template lines
    t = re.sub(
        r'    \{ name: "S2 [^"]+", desc: "[^"]*", key: "s2-[^"]+", type: "[^"]+" \},\n',
        "",
        t,
    )
    if "s2v2-alcance" not in t[t.find("const TEMPLATES"): t.find("const TEMPLATES") + 2500]:
        insert = '''    { name: "S2 Correo Horizonte (PDF)", desc: "Referencia visual del correo de práctica", key: "s2v2-correo", type: "PDF" },
    { name: "S2 Alcance Horizonte", desc: "Word · Documento de alcance ficticio", key: "s2v2-alcance", type: "Word" },
    { name: "S2 Presupuesto y cronograma", desc: "Excel · Datos para validar con Copilot Chat", key: "s2v2-presupuesto", type: "Excel" },
    { name: "S2 Transcripción reunión", desc: "Word · Decisiones vs propuestas", key: "s2v2-transcripcion", type: "Word" },
    { name: "S2 Registro inicial de riesgos", desc: "Excel · Riesgos preliminares", key: "s2v2-riesgos", type: "Excel" },
    { name: "S2 Comentarios interesados", desc: "Word · Comentarios ficticios", key: "s2v2-comentarios", type: "Word" },
    { name: "S2 Plantilla comité", desc: "PowerPoint · 8 diapositivas", key: "s2v2-pptx", type: "PowerPoint" },
    { name: "S2 Guía de validación", desc: "PDF · Verificar resultados de Copilot", key: "s2v2-guia", type: "PDF" },
    { name: "S2 Kit Horizonte (zip)", desc: "Los 8 archivos del caso", key: "s2v2-kit", type: "ZIP" },
'''
        t = t.replace(
            '    { name: "Bitácora de validación"',
            insert + '    { name: "Bitácora de validación"',
            1,
        )

    # --- Remove S2 CASO 1 QUIZ; insert Prompt Lab JS ---
    if "S2 CASO 1 QUIZ" in t:
        a = t.find("  /* ========== S2 CASO 1 QUIZ ========== */")
        b = t.find("  /* ========== BOOT ========== */", a)
        if a >= 0 and b > a:
            t = t[:a] + S2_JS + "\n" + t[b:]
    elif "initS2PromptLab" not in t:
        boot = "  /* ========== BOOT ========== */"
        if boot not in t:
            raise SystemExit("No BOOT")
        t = t.replace(boot, S2_JS + boot, 1)

    # Boot calls
    t = t.replace("    initS2Caso1Quiz();\n", "", 1)
    if "initS2PromptLab();" not in t:
        t = t.replace(
            "    initRetoEngine();\n",
            "    initRetoEngine();\n    initS2PromptLab();\n",
            1,
        )

    # Ensure initCopyButtons runs after (already does earlier) - re-call after S2 mount is fine
    # Re-bind copy after prompt lab - already on DOMContentLoaded before/after

    INDEX.write_text(t, encoding="utf-8")

    # --- app.py: add s2 email + version ---
    app = APP.read_text(encoding="utf-8")
    if "_s2_horizonte_email_content" not in app:
        helper = '''
def _s2_horizonte_email_content() -> tuple[str, str]:
    subject = "SOLICITUD DE ANÁLISIS | Proyecto Horizonte"
    body = """Buenos días,

Solicitamos realizar la revisión inicial del Proyecto Horizonte, iniciativa orientada a la modernización de infraestructura energética urbana.

Para este análisis se adjuntan los siguientes documentos:

- Documento preliminar de alcance.
- Presupuesto y cronograma.
- Transcripción de la reunión inicial.
- Registro preliminar de riesgos.
- Comentarios de los interesados.

El comité requiere recibir:

1. Resumen ejecutivo.
2. Alcance consolidado.
3. Hallazgos presupuestales.
4. Riesgos prioritarios.
5. Compromisos identificados.
6. Información faltante.
7. Decisiones requeridas.
8. Presentación ejecutiva.

Por favor, no asuma que la iniciativa está aprobada. Diferencie claramente la información confirmada, las propuestas y los elementos pendientes de validación.

Cordialmente,

Laura Méndez
Dirección de Infraestructura
"""
    return subject, body


'''
        app = app.replace(
            "def _reto1_email_content(to_email: str, name: str, smtp_email: str) -> tuple[str, str]:",
            helper + "def _reto1_email_content(to_email: str, name: str, smtp_email: str) -> tuple[str, str]:",
            1,
        )
        app = app.replace(
            '    if reto_id in ("r1", "reto1", "reto-1"):\n        subject, body = _reto1_email_content(to_email, name, smtp_email)\n        return subject, body, "Laura Méndez · Coordinación de Campo"',
            '    if reto_id in ("r1", "reto1", "reto-1"):\n        subject, body = _reto1_email_content(to_email, name, smtp_email)\n        return subject, body, "Laura Méndez · Coordinación de Campo"\n\n    if reto_id in ("s2", "s2-horizonte", "horizonte", "sesion2"):\n        subject, body = _s2_horizonte_email_content()\n        return subject, body, "Laura Méndez · Dirección de Infraestructura"',
            1,
        )
        app = app.replace(
            '    return ["r1", "r2", "r2-all"] + [p["id"] for p in get_reto_r2_parts()]',
            '    return ["r1", "r2", "r2-all", "s2"] + [p["id"] for p in get_reto_r2_parts()]',
            1,
        )

    app = re.sub(
        r'APP_CODE_VERSION = "[^"]+"',
        'APP_CODE_VERSION = "2026-08-04-s2-horizonte-copilot-chat-v1"',
        app,
        count=1,
    )
    APP.write_text(app, encoding="utf-8")

    # --- Verification ---
    tt = INDEX.read_text(encoding="utf-8")
    s2a = tt.find('id="sesion2"')
    s2b = tt.find('id="prompts"')
    s2 = tt[s2a:s2b]
    checks = {
        "title": "Del documento disperso al comité directivo" in s2,
        "pedagogy": "Copilot organiza, relaciona y propone" in s2,
        "no PA in S2 HTML": "Power Automate" not in s2.replace("Power Automate.", ""),  # allow unavailable list item ending with period only once
        "no SharePoint": "SharePoint" not in s2,
        "no Mantener": "Mantener y continuar" not in s2,
        "planilla kit": "s2v2-kit" in s2,
        "prompt lab": "s2BuildPrompt" in tt,
        "progress keys": '"s2-f0"' in tt and '"s2-e10"' in tt,
        "no fase-1 RETO": '"fase-1"' not in tt[tt.find("RETO_CASES"): tt.find("RETO_CASES") + 8000] if "RETO_CASES" in tt else True,
        "no s2c1 quiz": "initS2Caso1Quiz" not in tt,
        "s2 email app": "_s2_horizonte_email_content" in APP.read_text(encoding="utf-8"),
        "planillas map": "s2v2-alcance" in tt,
    }
    # Stricter PA check: only allowed as "Power Automate." in unavailable list
    pa_hits = [line.strip() for line in s2.splitlines() if "Power Automate" in line]
    print("PA lines in S2:", pa_hits)
    for k, v in checks.items():
        print(("OK" if v else "FAIL"), k)
    # Allow exactly the unavailable bullet
    bad_pa = [x for x in pa_hits if x.strip() != "<li>Power Automate.</li>"]
    if bad_pa:
        print("FAIL unexpected PA:", bad_pa)
        raise SystemExit(1)
    if not all(checks.values()):
        raise SystemExit(1)
    print("OK S2v2 patch aplicado")


if __name__ == "__main__":
    main()
