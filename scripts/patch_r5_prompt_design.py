# -*- coding: utf-8 -*-
"""Replace Reto 5 buildPromptR5Text + fields with design-focused generate-from-scratch prompt."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
PROMPT_JS = Path(__file__).with_name("_r5_prompt_design_js.txt")

R5_FIELDS = r'''    "fields": [
      ["caso", "Caso", "MCP-365-P05 · Comparación documental de PRO-OPS-12, versiones 3.1 y 4.0."],
      ["rol", "Rol de Copilot", "Analista senior de procesos, control documental y transición operativa, con capacidad para comparar normas, identificar cambios textuales y de significado, detectar requisitos nuevos/eliminados/modificados, contradicciones, impactos operativos, acciones de transición verificables y crear Excel ejecutivos con presentación profesional."],
      ["doc_anterior", "Documento anterior", "PRO-OPS-12 · Versión 3.1, vigente hasta el 28/02/2026 (archivo PRO-OPS-12_Version_3_1.pdf)."],
      ["doc_vigente", "Documento vigente", "PRO-OPS-12 · Versión 4.0, vigente desde el 01/03/2026 (archivo PRO-OPS-12_Version_4_0.pdf)."],
      ["temas", "Temas de comparación", "1. Anticipación a usuarios.\n2. Autorización de inicio.\n3. Registro de hallazgos.\n4. Horario y cierre.\n5. Clasificación de impacto.\n6. Confirmación de recursos.\n7. Criterios de detención.\n8. Evidencia y trazabilidad.\n9. Conservación de registros.\n10. Responsabilidad del contratista.\n11. Indicadores.\n12. Régimen de transición."],
      ["vacio", "Respuesta cuando no exista información", "No especificado."],
      ["salida", "Archivo de salida", "MCP365_P05_Comparacion_documental_completada.xlsx"]
    ],'''


def replace_prompt(text: str) -> str:
    start = text.find("  /** Prompt Reto 5:")
    if start < 0:
        start = text.find("  function buildPromptR5Text(f)")
    end = text.find("\n\n  /* ========== RETO ENGINE", start)
    if start < 0 or end < 0:
        raise SystemExit("prompt block not found")
    return text[:start] + PROMPT_JS.read_text(encoding="utf-8").rstrip() + text[end:]


def replace_fields(text: str) -> str:
    r5 = text.find('  "r5": {')
    r6 = text.find('  "r6": {', r5)
    block = text[r5:r6]
    f0 = block.find('    "fields": [')
    f1 = block.find('    "checklist": [', f0)
    if f0 < 0 or f1 < 0:
        raise SystemExit("fields/checklist not found")
    new_block = block[:f0] + R5_FIELDS + "\n" + block[f1:]
    return text[:r5] + new_block + text[r6:]


def main():
    text = INDEX.read_text(encoding="utf-8")
    text = replace_prompt(text)
    print("Prompt replaced")
    text = replace_fields(text)
    print("Fields replaced")
    # sanity
    assert "REGLA FUNDAMENTAL DE DISEÑO" in text
    assert "Lista de propuestas no aprobadas" in text
    assert "CRITERIO DE RECHAZO" in text
    assert "MCP365_P05_Comparacion_documental.xlsx" not in text or "completada" in text
    # ensure no plantilla flow language returned
    assert "No utilices una plantilla previa" in text
    INDEX.write_text(text, encoding="utf-8")
    print(f"OK -> {INDEX}")


if __name__ == "__main__":
    main()
