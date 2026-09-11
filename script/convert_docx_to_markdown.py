#!/usr/bin/env python3
"""Convert a simple DOCX document to Markdown without external packages."""

import argparse
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree


WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{WORD_NS}}}"


def text_from_run(run):
    parts = []
    for node in run:
        if node.tag == f"{W}t":
            parts.append(node.text or "")
        elif node.tag == f"{W}br":
            parts.append("\n")
    text = "".join(parts)
    if run.find(f"{W}b") is not None:
        text = f"**{text}**"
    if run.find(f"{W}i") is not None:
        text = f"*{text}*"
    return text


def paragraph_to_markdown(paragraph):
    text = "".join(text_from_run(run) for run in paragraph.findall(f"{W}r"))
    text = re.sub(r"[ \t]+", " ", text).strip()
    if not text:
        return ""

    properties = paragraph.find(f"{W}pPr")
    style = properties.find(f"{W}pStyle") if properties is not None else None
    style_name = style.get(f"{W}val", "").lower() if style is not None else ""
    heading_match = re.search(r"(?:heading|t[ií]tulo|encabezado)[ _-]*(\d+)", style_name)
    if heading_match:
        return f"{'#' * min(int(heading_match.group(1)), 6)} {text}"
    if style_name.endswith("listparagraph") or "list" in style_name:
        return f"- {text}"

    detail_headings = (
        "Uso actual y limitaciones del software de Fontana",
        "Proceso de llegada de proyectos y licitaciones",
        "Tipos de proyectos de construcción y control de inventario",
        "Propuesta de integración con Odoo para facturación y cotizaciones",
        "Gestión de gastos por compras urgentes en terreno",
        "Control de bodega central y siguientes pasos del proyecto",
    )
    for heading in detail_headings:
        text = text.replace(f"{heading}:", f"\n\n**{heading}**:")

    return text


def cell_text(cell):
    paragraphs = [paragraph_to_markdown(paragraph) for paragraph in cell.findall(f".//{W}p")]
    return " ".join(value for value in paragraphs if value).replace("|", "\\|")


def table_to_markdown(table):
    rows = [[cell_text(cell) for cell in row.findall(f"{W}tc")] for row in table.findall(f"{W}tr")]
    rows = [row for row in rows if any(row)]
    if not rows:
        return []
    width = max(len(row) for row in rows)
    rows = [row + [""] * (width - len(row)) for row in rows]
    output = ["| " + " | ".join(rows[0]) + " |", "| " + " | ".join("---" for _ in rows[0]) + " |"]
    output.extend("| " + " | ".join(row) + " |" for row in rows[1:])
    return output


def convert(source, destination):
    with zipfile.ZipFile(source) as archive:
        document = ElementTree.fromstring(archive.read("word/document.xml"))

    body = document.find(f"{W}body")
    output = []
    for child in body:
        if child.tag == f"{W}p":
            value = paragraph_to_markdown(child)
            if value:
                output.extend(line.strip() for line in value.splitlines())
                output.append("")
        elif child.tag == f"{W}tbl":
            output.extend(table_to_markdown(child))
            output.append("")

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Convierte un DOCX simple a Markdown.")
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    convert(args.source, args.destination)
    print(f"Markdown generado: {args.destination}")


if __name__ == "__main__":
    main()