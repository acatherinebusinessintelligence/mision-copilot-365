# -*- coding: utf-8 -*-
"""Corrige los Excel del caso para que Copilot (y cualquier lector) vea los resultados.

Problemas que resuelve (archivos generados con openpyxl):
1. Las fórmulas se guardan sin valor calculado (<v></v>). Excel de escritorio
   recalcula al abrir, pero Copilot Chat lee el archivo tal cual y ve celdas vacías
   (p. ej. "Costo total" o el presupuesto total).
2. Fechas guardadas como texto ("2026-08-18"): MIN/MAX las ignoran y el resumen
   muestra fecha inicial/final = 0.

Conserva las fórmulas (para que el estudiante valide en Excel) y agrega el valor.

Uso:
    python scripts/fix_xlsx_cached_values.py planillas/03_...xlsx [otros.xlsx ...]
"""
import re
import sys
import zipfile
from datetime import datetime, date
from pathlib import Path

import openpyxl
from openpyxl.utils import column_index_from_string, get_column_letter

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EXCEL_EPOCH = date(1899, 12, 30)


def serial(v):
    if isinstance(v, datetime):
        v = v.date()
    if isinstance(v, date):
        return (v - EXCEL_EPOCH).days
    return v


def rng(ref):
    a, b = ref.split(":")
    ca, ra = re.match(r"([A-Z]+)(\d+)", a).groups()
    cb, rb = re.match(r"([A-Z]+)(\d+)", b).groups()
    for r in range(int(ra), int(rb) + 1):
        for c in range(column_index_from_string(ca), column_index_from_string(cb) + 1):
            yield f"{get_column_letter(c)}{r}"


def evaluate(wb):
    """Devuelve {(hoja, celda): valor} para todas las celdas con fórmula."""
    vals, formulas = {}, {}
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and c.value.startswith("="):
                    formulas[(ws.title, c.coordinate)] = c.value[1:]
                elif c.value is not None:
                    vals[(ws.title, c.coordinate)] = serial(c.value)

    def get(sheet, ref):
        return vals.get((sheet, ref))

    def num(x):
        return x if isinstance(x, (int, float)) else 0

    def ev(sheet, f):
        m = re.fullmatch(r"([A-Z]+\d+)\*([A-Z]+\d+)", f)
        if m:
            a, b = get(sheet, m[1]), get(sheet, m[2])
            return None if a is None or b is None else num(a) * num(b)
        m = re.fullmatch(r"SUM\(([A-Z]+\d+:[A-Z]+\d+)\)", f)
        if m:
            cells = [get(sheet, r) for r in rng(m[1])]
            if any((sheet, r) in formulas and get(sheet, r) is None for r in rng(m[1])):
                return None
            return sum(num(x) for x in cells if isinstance(x, (int, float)))
        m = re.fullmatch(r"([A-Z]+\d+)-([A-Z]+\d+)(\+1)?", f)
        if m:
            a, b = get(sheet, m[1]), get(sheet, m[2])
            return None if a is None or b is None else num(a) - num(b) + (1 if m[3] else 0)
        m = re.fullmatch(r"([A-Z]+\d+)", f)
        if m:
            return get(sheet, m[1])
        m = re.fullmatch(r"(\w+)!([A-Z]+\d+)", f)
        if m:
            return get(m[1], m[2])
        m = re.fullmatch(r'COUNTIF\((\w+)!([A-Z]+\d+:[A-Z]+\d+),"([^"]*)"\)', f)
        if m:
            return sum(1 for r in rng(m[2]) if get(m[1], r) == m[3])
        m = re.fullmatch(r"(MIN|MAX)\((\w+)!([A-Z]+\d+:[A-Z]+\d+)\)", f)
        if m:
            xs = [get(m[2], r) for r in rng(m[3])]
            xs = [x for x in xs if isinstance(x, (int, float))]
            return (min if m[1] == "MIN" else max)(xs) if xs else 0
        m = re.fullmatch(r'IF\(OR\(([A-Z]+\d+)="Alta",([A-Z]+\d+)="Alta"\),"Alto",IF\(AND\(([A-Z]+\d+)="Media",([A-Z]+\d+)="Media"\),"Medio","Bajo"\)\)', f)
        if m:
            g, h = get(sheet, m[1]), get(sheet, m[2])
            if g == "Alta" or h == "Alta":
                return "Alto"
            return "Medio" if (get(sheet, m[3]) == "Media" and get(sheet, m[4]) == "Media") else "Bajo"
        raise ValueError(f"Fórmula no soportada: {sheet}!{f}")

    pending = dict(formulas)
    for _ in range(10):
        for key, f in list(pending.items()):
            v = ev(key[0], f)
            if v is not None:
                vals[key] = v
                del pending[key]
        if not pending:
            break
    if pending:
        raise ValueError(f"No se pudieron calcular: {pending}")
    return {k: vals[k] for k in formulas}


def fix(path: Path):
    wb = openpyxl.load_workbook(path)
    changed_dates = 0
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and DATE_RE.match(c.value):
                    c.value = datetime.strptime(c.value, "%Y-%m-%d")
                    c.number_format = "yyyy-mm-dd"
                    changed_dates += 1
                elif isinstance(c.value, str) and re.fullmatch(r"=(MIN|MAX)\(\w+!.*\)", c.value):
                    c.number_format = "yyyy-mm-dd"
    values = evaluate(wb)
    wb.save(path)

    # Inyectar valores calculados en el XML (openpyxl no escribe caché de fórmulas).
    names = [ws.title for ws in wb.worksheets]
    src = zipfile.ZipFile(path)
    items = {n: src.read(n) for n in src.namelist()}
    infos = {n: src.getinfo(n) for n in src.namelist()}
    src.close()
    injected = 0
    for idx, sheet in enumerate(names, start=1):
        part = f"xl/worksheets/sheet{idx}.xml"
        xml = items[part].decode("utf-8")

        def repl(m):
            nonlocal injected
            attrs, ref, formula = m.group(1), m.group(2), m.group(3)
            v = values.get((sheet, ref))
            if v is None:
                return m.group(0)
            injected += 1
            if isinstance(v, str):
                attrs = re.sub(r'\st="[^"]*"', "", attrs) + ' t="str"'
                return f"<c{attrs}><f>{formula}</f><v>{v}</v></c>"
            if isinstance(v, float) and v.is_integer():
                v = int(v)
            return f"<c{attrs}><f>{formula}</f><v>{v}</v></c>"

        xml = re.sub(r'<c((?=[^>]*\sr="([A-Z]+\d+)")[^>]*)><f>(.*?)</f>(?:<v>[^<]*</v>|<v/>)?</c>', repl, xml)
        items[part] = xml.encode("utf-8")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as out:
        for n, data in items.items():
            out.writestr(infos[n], data)
    print(f"{path.name}: fechas convertidas={changed_dates}, valores calculados={injected}/{len(values)}")


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        fix(Path(arg))
