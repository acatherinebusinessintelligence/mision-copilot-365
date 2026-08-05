# -*- coding: utf-8 -*-
"""Inserta Caso 1 Copilot PA SharePoint y renumera los retos S2 existentes."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CASE = Path(__file__).with_name("_s2_caso1_copilot.html")

CSS = r'''
    /* ========== S2 CASO 1 COPILOT FLOW ========== */
    .pa-vflow {
      display: flex;
      flex-direction: column;
      align-items: stretch;
      gap: 0.35rem;
      margin: 0.75rem 0 1rem;
      max-width: 720px;
    }
    .pa-vflow__node {
      background: var(--bg-elevated);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 0.7rem 0.85rem;
      font-size: 0.88rem;
      box-shadow: 0 1px 4px rgba(34, 30, 64, 0.06);
    }
    .pa-vflow__node strong { display: block; margin-bottom: 0.15rem; }
    .pa-vflow__node span { color: var(--text-muted); font-size: 0.82rem; }
    .pa-vflow__arrow {
      text-align: center;
      color: var(--brand-primary);
      font-weight: 700;
      line-height: 1;
    }
    .pa-vflow__label {
      margin: 0.35rem 0;
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--text-muted);
    }
    .pa-vflow__cols {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.75rem;
      margin-top: 0.5rem;
    }
    .pa-vflow__node--ask {
      border-left: 4px solid var(--brand-primary);
      background: color-mix(in srgb, var(--brand-primary) 10%, var(--bg-elevated));
    }
    .pa-vflow__node--warn {
      border-left: 4px solid #c0392b;
      background: color-mix(in srgb, #c0392b 8%, var(--bg-elevated));
    }
    .pa-vflow__node--ok {
      border-left: 4px solid #2f9e6a;
      background: color-mix(in srgb, #2f9e6a 10%, var(--bg-elevated));
    }
    .improve-card {
      background: var(--bg-elevated);
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 0.85rem 1rem;
      margin: 0.75rem 0;
    }
    .improve-card h5 { margin: 0 0 0.45rem; font-size: 0.95rem; }
    .improve-card .prompt-box { margin: 0.45rem 0; font-size: 0.86rem; white-space: pre-wrap; }
    .audit-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 0.75rem;
    }
    .audit-grid .improve-card { margin: 0; }
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
    .s2c1-q { margin: 0.85rem 0; padding-bottom: 0.65rem; border-bottom: 1px dashed var(--border); }
    .s2c1-q .quiz-option { display: flex; gap: 0.5rem; align-items: flex-start; margin: 0.35rem 0; font-size: 0.9rem; cursor: pointer; }
    @media (max-width: 900px) {
      .pa-vflow__cols { grid-template-columns: 1fr; }
      .audit-grid { grid-template-columns: 1fr; }
      .prompt-lab { grid-template-columns: 1fr; }
    }
    @media print {
      .improve-card, .pa-vflow__node, .prompt-lab__item { break-inside: avoid; }
    }

'''

QUIZ_JS = r'''
  /* ========== S2 CASO 1 QUIZ ========== */
  const S2C1_QUIZ = [
    { answer: 1, ok: "Correcto. El desencadenador es la creación de un elemento en SharePoint.", bad: "Revisa la Fase 1: el evento inicial es un nuevo elemento en SharePoint." },
    { answer: 1, ok: "Correcto. Obtener mi perfil recupera datos de la cuenta conectada.", bad: "Esa acción no borra listas ni crea columnas." },
    { answer: 1, ok: "Correcto. El contenido dinámico toma valores del elemento; el texto fijo no cambia.", bad: "Los corchetes deben resolverse con contenido dinámico, no como texto literal." },
    { answer: 1, ok: "Correcto. Tras cada cambio de Copilot hay que validar campos, ramas y conexiones.", bad: "Copilot no garantiza una configuración perfecta." },
    { answer: 1, ok: "Correcto. Un cambio a la vez facilita aislar errores y validar.", bad: "Conviene no mezclar todas las mejoras en un solo prompt." },
    { answer: 1, ok: "Correcto. Un Update mal configurado puede sobrescribir datos.", bad: "Siempre verifica sitio, lista, ID y campos obligatorios." },
    { answer: 0, ok: "Correcto. El campo debe ser numérico y el umbral sin puntos ni símbolos.", bad: "Antes de comparar, revisa el tipo de dato y el formato del umbral." },
    { answer: 1, ok: "Correcto. Copilot no reemplaza la prueba humana del flujo.", bad: "Siempre debes ejecutar y validar el flujo." }
  ];

  function initS2Caso1Quiz() {
    const root = document.getElementById("s2c1Quiz");
    if (!root || root.dataset.bound) return;
    root.dataset.bound = "1";
    const scoreEl = document.getElementById("s2c1QuizScore");
    const syncScore = () => {
      let n = 0;
      S2C1_QUIZ.forEach((q, i) => {
        const sel = root.querySelector('input[name="s2c1q' + i + '"]:checked');
        if (sel && +sel.value === q.answer) n++;
      });
      if (scoreEl) scoreEl.textContent = String(n);
      state.s2c1Quiz = state.s2c1Quiz || {};
      state.s2c1Quiz.score = n;
      saveState();
    };
    root.querySelectorAll("input[type=radio]").forEach(inp => {
      inp.addEventListener("change", () => {
        const qi = +inp.name.replace("s2c1q", "");
        const q = S2C1_QUIZ[qi];
        const fb = document.getElementById("s2c1f" + qi);
        const ok = +inp.value === q.answer;
        if (fb) {
          fb.textContent = ok ? q.ok : q.bad;
          fb.style.color = ok ? "#2f9e6a" : "#c0392b";
          fb.style.fontSize = "0.86rem";
          fb.style.marginTop = "0.35rem";
        }
        syncScore();
      });
    });
    // restore
    const saved = (state.s2c1Quiz && state.s2c1Quiz.answers) || {};
    Object.keys(saved).forEach(k => {
      const el = root.querySelector('input[name="s2c1q' + k + '"][value="' + saved[k] + '"]');
      if (el) {
        el.checked = true;
        el.dispatchEvent(new Event("change"));
      }
    });
    root.querySelectorAll("input[type=radio]").forEach(inp => {
      inp.addEventListener("change", () => {
        state.s2c1Quiz = state.s2c1Quiz || {};
        state.s2c1Quiz.answers = state.s2c1Quiz.answers || {};
        state.s2c1Quiz.answers[inp.name.replace("s2c1q", "")] = inp.value;
        saveState();
      });
    });
    syncScore();
  }

'''


def main():
    t = INDEX.read_text(encoding="utf-8")
    case = CASE.read_text(encoding="utf-8").rstrip() + "\n\n"

    if 'data-reto="s2-caso1"' in t:
        print("Caso 1 ya insertado; actualizar contenido...")
        # replace existing article
        a = t.find('<!-- CASO 1 · COPILOT')
        if a < 0:
            a = t.find('<article class="reto is-open" data-reto="s2-caso1">')
        b = t.find('<!-- RETO 1 -->', a) if a >= 0 else -1
        if a < 0 or b < 0:
            # find between s2-caso1 and next reto fase-1
            a = t.find('<article class="reto is-open" data-reto="s2-caso1">')
            if a < 0:
                a = t.find('<article class="reto" data-reto="s2-caso1">')
            b = t.find('<!-- RETO 1 -->', a)
        if a < 0 or b < 0:
            raise SystemExit("No se pudo localizar bloque caso 1 existente")
        t = t[:a] + case + t[b:]
    else:
        marker = "          <!-- RETO 1 -->"
        if marker not in t:
            raise SystemExit("No se encontró RETO 1")
        t = t.replace(marker, case + marker, 1)

    # Renumber display numbers for fase articles: Outlook becomes 2..7
    # Current structure after insert: caso1=1, then RETO 1 with num 1 still - fix those
    # Replace reto nums inside sesion2 for data-reto="fase-N"
    def renum(m):
        n = int(m.group(1))
        return f'<span class="reto__num">{n + 1}</span>'

    # Only within sesion2 section for fase-* articles - careful global replace of reto__num near fase
    s2a = t.find('id="sesion2"')
    s2b = t.find('id="prompts"')
    s2 = t[s2a:s2b]
    # Fix Outlook case: remove is-open if present on fase-1
    s2 = s2.replace(
        '<article class="reto is-open" data-reto="fase-1">',
        '<article class="reto" data-reto="fase-1">',
        1,
    )
    s2 = s2.replace(
        'aria-expanded="true">\n              <span class="reto__title-wrap">\n                <span class="reto__num">1</span>\n                <span>\n                  <strong>Proyecto integrador:',
        'aria-expanded="false">\n              <span class="reto__title-wrap">\n                <span class="reto__num">2</span>\n                <span>\n                  <strong>Caso 2 · Proyecto integrador:',
        1,
    )
    # If title already has Caso 2, skip; if still Proyecto without Caso 2 prefix after num change:
    if 'Caso 2 · Proyecto integrador' not in s2 and 'Proyecto integrador: del correo' in s2:
        s2 = s2.replace(
            '<strong>Proyecto integrador: del correo recibido al informe ejecutivo</strong>',
            '<strong>Caso 2 · Proyecto integrador: del correo recibido al informe ejecutivo</strong>',
            1,
        )

    # Map fase-2..6 display numbers 3..7 by walking articles
    for old_n, new_n, title_old, title_new in [
        (2, 3, "Extracción de información del Word", "Caso 3 · Extracción de información del Word"),
        (3, 4, "Presupuesto del proyecto", "Caso 4 · Presupuesto del proyecto"),
        (4, 5, "Matriz de riesgos", "Caso 5 · Matriz de riesgos"),
        (5, 6, "Informe y aprobación", "Caso 6 · Informe y aprobación"),
        (6, 7, "Presentación ejecutiva", "Caso 7 · Presentación ejecutiva"),
    ]:
        # update num immediately before each title if present
        s2 = s2.replace(
            f'<span class="reto__num">{old_n}</span>\n                <span>\n                  <strong>{title_old}</strong>',
            f'<span class="reto__num">{new_n}</span>\n                <span>\n                  <strong>{title_new}</strong>',
            1,
        )
        # if already Caso N · title
        s2 = s2.replace(
            f'<span class="reto__num">{old_n}</span>\n                <span>\n                  <strong>Caso {new_n} · {title_old}</strong>',
            f'<span class="reto__num">{new_n}</span>\n                <span>\n                  <strong>Caso {new_n} · {title_old}</strong>',
            1,
        )
        # fallback: only title prefix
        if f'Caso {new_n} · {title_old}' not in s2:
            s2 = s2.replace(f'<strong>{title_old}</strong>', f'<strong>Caso {new_n} · {title_old}</strong>', 1)

    t = t[:s2a] + s2 + t[s2b:]

    # CSS insert once
    if "S2 CASO 1 COPILOT FLOW" not in t:
        anchor = "    /* ========== POWER AUTOMATE FLOW (S2) ========== */"
        if anchor not in t:
            raise SystemExit("No CSS anchor")
        t = t.replace(anchor, CSS + anchor, 1)

    # PROGRESS_KEYS
    if '"s2-caso1"' not in t[t.find("PROGRESS_KEYS"): t.find("PROGRESS_KEYS") + 400]:
        t = t.replace(
            '"fase-1","fase-2","fase-3","fase-4","fase-5","fase-6","fase-7","fase-8"',
            '"s2-caso1","fase-1","fase-2","fase-3","fase-4","fase-5","fase-6","fase-7","fase-8"',
            1,
        )

    # Quiz JS + boot call
    if "initS2Caso1Quiz" not in t:
        boot_anchor = "  /* ========== BOOT ========== */"
        if boot_anchor not in t:
            raise SystemExit("No boot anchor")
        t = t.replace(boot_anchor, QUIZ_JS + boot_anchor, 1)
        t = t.replace(
            "    initRetoEngine();\n",
            "    initRetoEngine();\n    initS2Caso1Quiz();\n",
            1,
        )

    # Version
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    app = re.sub(
        r'APP_CODE_VERSION = "[^"]+"',
        'APP_CODE_VERSION = "2026-08-04-s2-caso1-copilot-pa-v1"',
        app,
        count=1,
    )
    (ROOT / "app.py").write_text(app, encoding="utf-8")

    INDEX.write_text(t, encoding="utf-8")

    # verify
    tt = INDEX.read_text(encoding="utf-8")
    checks = {
        "caso1": 'data-reto="s2-caso1"' in tt,
        "outlook kept": "del correo recibido al informe ejecutivo" in tt,
        "fase-6 kept": 'data-reto-enhance="fase-6"' in tt,
        "no html download button": 'data-planilla="s2-correo"' not in tt,
        "quiz": "initS2Caso1Quiz" in tt,
        "mejora6": "Información incompleta" in tt and "s2c1-p6" in tt,
        "lab pro": "s2c1-lab-p" in tt,
        "mensaje pedagógico": "Copilot propone y modifica el flujo" in tt,
    }
    for k, v in checks.items():
        print(("OK" if v else "FAIL"), k)
    if not all(checks.values()):
        raise SystemExit("Verificación incompleta")
    print("OK patch aplicado")


if __name__ == "__main__":
    main()
