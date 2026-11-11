"""Genera caso-horizonte.html: página pública, solo texto, con los documentos 02 a 06 del caso.

Uso:  python scripts/build_caso_horizonte.py
Lee planillas/02..06 y escribe caso-horizonte.html en la raíz del repo.
La página la sirve app.py en /caso-horizonte (sin login) para que el Agente PMO
pueda usarla como conocimiento web cuando Bing la indexe.
"""
from __future__ import annotations

import html
import sys
from pathlib import Path

import docx
import openpyxl
from docx.table import Table
from docx.text.paragraph import Paragraph

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "planillas"
OUT = ROOT / "caso-horizonte.html"

AVISO = "Proyecto Horizonte es un caso académico ficticio."

DOCS = [
    ("doc-02", "02 · Alcance preliminar", "02_Alcance_Proyecto_Horizonte.docx"),
    ("doc-03", "03 · Presupuesto y cronograma", "03_Presupuesto_y_Cronograma_Horizonte.xlsx"),
    ("doc-04", "04 · Transcripción de la reunión inicial", "04_Transcripcion_Reunion_Horizonte.docx"),
    ("doc-05", "05 · Registro inicial de riesgos", "05_Registro_Inicial_Riesgos_Horizonte.xlsx"),
    ("doc-06", "06 · Comentarios de interesados", "06_Comentarios_Interesados_Horizonte.docx"),
]

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def e(s: str) -> str:
    return html.escape(s, quote=False)


def fmt(v) -> str:
    if v is None:
        return ""
    if hasattr(v, "strftime"):
        return v.strftime("%Y-%m-%d")
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    if isinstance(v, int) and abs(v) >= 10000:
        return f"{v:,}".replace(",", ".")
    return str(v).strip()


def table_html(rows: list[list[str]], header: bool = True) -> str:
    if not rows:
        return ""
    out = ["<table>"]
    for i, r in enumerate(rows):
        tag = "th" if header and i == 0 else "td"
        cells = "".join(f"<{tag}>{e(c)}</{tag}>" for c in r)
        out.append(f"<tr>{cells}</tr>")
    out.append("</table>")
    return "\n".join(out)


def docx_html(path: Path) -> str:
    d = docx.Document(path)
    parts: list[str] = []
    list_open = None  # "ul" | "ol" | None
    first_title = True

    def close_list():
        nonlocal list_open
        if list_open:
            parts.append(f"</{list_open}>")
            list_open = None

    for el in d.element.body.iterchildren():
        tag = el.tag.split("}")[1]
        if tag == "p":
            p = Paragraph(el, d)
            txt = p.text.strip()
            if not txt:
                continue
            style = (p.style.name or "").lower()
            numbered = el.find(f".//{W_NS}numPr") is not None
            bullet_char = txt.startswith("•")
            if style.startswith("title"):
                close_list()
                if first_title:  # el título del documento ya va en el <h2>
                    first_title = False
                    continue
                parts.append(f"<h3>{e(txt)}</h3>")
            elif style.startswith("heading"):
                close_list()
                parts.append(f"<h3>{e(txt)}</h3>")
            elif "list" in style or numbered or bullet_char:
                kind = "ol" if "number" in style else "ul"
                if list_open != kind:
                    close_list()
                    parts.append(f"<{kind}>")
                    list_open = kind
                parts.append(f"<li>{e(txt.lstrip('• ').strip())}</li>")
            else:
                close_list()
                parts.append(f"<p>{e(txt)}</p>")
        elif tag == "tbl":
            close_list()
            t = Table(el, d)
            rows = []
            for r in t.rows:
                cells: list[str] = []
                for c in r.cells:
                    v = c.text.strip()
                    if not cells or cells[-1] != v:  # celdas combinadas
                        cells.append(v)
                rows.append(cells)
            if len(rows) == 1 and len(rows[0]) == 1:
                # Recuadro de una celda: "Título\ntexto"
                head, _, body = rows[0][0].partition("\n")
                parts.append(f"<p><strong>{e(head)}.</strong> {e(body.strip())}</p>")
            else:
                parts.append(table_html(rows))
    close_list()
    return "\n".join(parts)


def xlsx_html(path: Path) -> str:
    wb = openpyxl.load_workbook(path, data_only=True)
    parts: list[str] = ["<p>" + e("Caso académico ficticio. Hoja de cálculo transcrita como tablas.") + "</p>"]
    for ws in wb:
        rows = []
        for r in ws.iter_rows(values_only=True):
            vals = [fmt(v) for v in r]
            while vals and vals[-1] == "":
                vals.pop()
            if any(vals):
                rows.append(vals)
        if not rows:
            continue
        parts.append(f"<h3>Hoja: {e(ws.title)}</h3>")
        if ws.title.lower() == "resumen":
            # Hoja de resumen: título + pares etiqueta/valor
            title, *rest = rows
            parts.append(f"<p><strong>{e(' '.join(title))}</strong></p>")
            parts.append(table_html(rest, header=False))
        else:
            parts.append(table_html(rows))
    return "\n".join(parts)


def build() -> str:
    sections = []
    toc = []
    for anchor, title, fn in DOCS:
        path = SRC / fn
        body = docx_html(path) if fn.endswith(".docx") else xlsx_html(path)
        toc.append(f'<li><a href="#{anchor}">{e(title)}</a></li>')
        sections.append(f'<section id="{anchor}">\n<h2>{e(title)}</h2>\n{body}\n</section>')

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="index, follow">
<meta name="description" content="Documentos del Proyecto Horizonte, caso académico ficticio: alcance, presupuesto y cronograma, transcripción de reunión, registro de riesgos y comentarios de interesados.">
<title>Proyecto Horizonte · Documentos del caso (caso académico ficticio)</title>
<style>
  body {{ font-family: system-ui, -apple-system, "Segoe UI", sans-serif; max-width: 60rem; margin: 0 auto; padding: 1.5rem; line-height: 1.55; color: #1d1d1f; background: #fff; }}
  .aviso {{ border: 2px solid #b45309; background: #fff7ed; padding: 0.75rem 1rem; font-weight: 700; }}
  h1 {{ font-size: 1.7rem; margin-bottom: 0.3rem; }}
  h2 {{ font-size: 1.35rem; margin-top: 2.5rem; border-bottom: 2px solid #ddd; padding-bottom: 0.3rem; }}
  h3 {{ font-size: 1.05rem; margin-top: 1.4rem; }}
  table {{ border-collapse: collapse; width: 100%; font-size: 0.88rem; margin: 0.6rem 0 1rem; display: block; overflow-x: auto; }}
  th, td {{ border: 1px solid #ccc; padding: 0.3rem 0.45rem; text-align: left; vertical-align: top; }}
  th {{ background: #f3f3f3; }}
</style>
</head>
<body>
<p class="aviso" role="note">{e(AVISO)} Los datos, nombres, cifras y situaciones no corresponden a una operación real.</p>
<h1>Proyecto Horizonte · Documentos del caso</h1>
<p>Modernización de infraestructura energética urbana. Esta página reúne, solo en texto, los cinco documentos que se usan en el curso para analizar el caso. Es material de práctica: el proyecto no está aprobado y aparece como iniciativa en estructuración.</p>
<h2>Contenido</h2>
<ol>
{chr(10).join(toc)}
</ol>
{chr(10).join(sections)}
<p class="aviso" role="note">{e(AVISO)}</p>
</body>
</html>
"""


if __name__ == "__main__":
    OUT.write_text(build(), encoding="utf-8", newline="\n")
    print(f"Escrito {OUT.relative_to(ROOT)} ({OUT.stat().st_size} bytes)", file=sys.stderr)
