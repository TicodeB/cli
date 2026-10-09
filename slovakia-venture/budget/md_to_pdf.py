#!/usr/bin/env python3
"""Render a Markdown dossier to PDF for offline reading.

Handles the subset used in this repo: headings, tables, blockquotes, lists,
rules, bold/italic/code. No external binaries needed.

IMPORTANT: embeds DejaVu Sans. The built-in Helvetica uses WinAnsi encoding,
which has no glyphs for c-caron, t-caron, d-caron, l-caron or n-caron, so
Slovak text renders with those letters SILENTLY DROPPED ("den" for "deon").
Any document here containing Slovak must use the embedded font.

    python3 md_to_pdf.py DOSSIER-slovakia-trip.md DOSSIER-slovakia-trip.pdf
"""
from __future__ import annotations

import re
import sys
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (HRFlowable, KeepTogether, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

NAVY = colors.HexColor("#1F3864")
SLATE = colors.HexColor("#44546A")
RULE = colors.HexColor("#BFBFBF")
BAND = colors.HexColor("#EAF1F8")
QUOTE_BG = colors.HexColor("#FFF8E1")

# --- Unicode fonts, required for Slovak diacritics ---------------------------
FONT_DIRS = ["/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/dejavu"]
FACES = {
    "Body": "DejaVuSans.ttf",
    "Body-Bold": "DejaVuSans-Bold.ttf",
    "Body-Oblique": "DejaVuSans-Oblique.ttf",
    "Body-Mono": "DejaVuSansMono.ttf",
}


def register_fonts() -> bool:
    """Register DejaVu. Returns False if unavailable (then Slovak will break)."""
    import os
    found = {}
    for name, filename in FACES.items():
        for d in FONT_DIRS:
            path = os.path.join(d, filename)
            if os.path.exists(path):
                found[name] = path
                break
    if "Body" not in found or "Body-Bold" not in found:
        return False
    for name, path in found.items():
        pdfmetrics.registerFont(TTFont(name, path))
    # registerFontFamily takes registered FONT NAMES, not file paths.
    pdfmetrics.registerFontFamily(
        "Body", normal="Body",
        bold="Body-Bold" if "Body-Bold" in found else "Body",
        italic="Body-Oblique" if "Body-Oblique" in found else "Body",
        boldItalic="Body-Bold" if "Body-Bold" in found else "Body")
    return True


UNICODE_OK = register_fonts()
if not UNICODE_OK:
    sys.stderr.write(
        "WARNING: DejaVu not found. Falling back to Helvetica, which DROPS "
        "Slovak diacritics (c/t/d/l/n-caron). Do not ship a Slovak PDF "
        "built this way.\n")

REG = "Body" if UNICODE_OK else "Helvetica"
BLD = "Body-Bold" if UNICODE_OK else "Helvetica-Bold"
MNO = "Body-Mono" if UNICODE_OK else "Courier"

ss = getSampleStyleSheet()
S = {
    "h1": ParagraphStyle("h1", parent=ss["Heading1"], fontName=BLD,
                         fontSize=20, leading=25, textColor=NAVY, spaceAfter=10),
    "h2": ParagraphStyle("h2", parent=ss["Heading2"], fontName=BLD,
                         fontSize=14, leading=18, textColor=NAVY,
                         spaceBefore=16, spaceAfter=7),
    "h3": ParagraphStyle("h3", parent=ss["Heading3"], fontName=BLD,
                         fontSize=11.5, leading=15, textColor=SLATE,
                         spaceBefore=11, spaceAfter=5),
    "body": ParagraphStyle("body", parent=ss["BodyText"], fontName=REG,
                           fontSize=10.2, leading=14.6, alignment=TA_LEFT,
                           spaceAfter=7),
    "bullet": ParagraphStyle("bullet", parent=ss["BodyText"], fontName=REG,
                             fontSize=10.2, leading=14.6, leftIndent=12,
                             bulletIndent=3, spaceAfter=3),
    "quote": ParagraphStyle("quote", parent=ss["BodyText"], fontName=REG,
                            fontSize=10.2, leading=14.6, leftIndent=9,
                            rightIndent=6, spaceBefore=4, spaceAfter=4),
    "cell": ParagraphStyle("cell", parent=ss["BodyText"], fontName=REG,
                           fontSize=8.8, leading=11.6, spaceAfter=0),
    "cellh": ParagraphStyle("cellh", parent=ss["BodyText"], fontName=BLD,
                            fontSize=8.8, leading=11.6, textColor=colors.white,
                            spaceAfter=0),
}


def inline(text: str) -> str:
    """Markdown inline -> reportlab mini-HTML."""
    text = escape(text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<font color="#1F3864">\1</font>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"`([^`]+)`", rf'<font face="{MNO}" size="9">\1</font>', text)
    text = text.replace("~~", "")
    return text


def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def build_table(rows: list[list[str]], width: float) -> Table:
    head, body = rows[0], rows[1:]
    ncols = len(head)
    data = [[Paragraph(inline(c), S["cellh"]) for c in head]]
    for r in body:
        r = (r + [""] * ncols)[:ncols]
        data.append([Paragraph(inline(c), S["cell"]) for c in r])

    # first column wider; remainder shared
    if ncols == 1:
        widths = [width]
    else:
        first = width * (0.42 if ncols <= 3 else 0.30)
        widths = [first] + [(width - first) / (ncols - 1)] * (ncols - 1)

    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), BAND))
    t.setStyle(TableStyle(style))
    return t


def convert(md_path: str, pdf_path: str) -> None:
    lines = open(md_path, encoding="utf-8").read().split("\n")
    doc = SimpleDocTemplate(
        pdf_path, pagesize=A4,
        leftMargin=18 * mm, rightMargin=16 * mm,
        topMargin=16 * mm, bottomMargin=16 * mm,
        title="Trip Dossier - Slovakia", author="Slovakia venture package",
    )
    avail = doc.width
    flow: list = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        if not line.strip():
            i += 1
            continue

        if re.match(r"^---+$", line.strip()):
            flow.append(Spacer(1, 4))
            flow.append(HRFlowable(width="100%", thickness=0.6, color=RULE))
            flow.append(Spacer(1, 4))
            i += 1
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            key = "h1" if level == 1 else ("h2" if level == 2 else "h3")
            flow.append(Paragraph(inline(m.group(2)), S[key]))
            i += 1
            continue

        # table
        if line.lstrip().startswith("|"):
            block = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                block.append(lines[i])
                i += 1
            rows = [split_row(b) for b in block]
            rows = [r for r in rows
                    if not all(re.fullmatch(r":?-{2,}:?", c or "") for c in r)]
            if rows:
                flow.append(Spacer(1, 3))
                flow.append(build_table(rows, avail))
                flow.append(Spacer(1, 8))
            continue

        # blockquote
        if line.lstrip().startswith(">"):
            block = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                block.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            inner = [Paragraph(inline(b), S["quote"]) for b in block if b.strip()]
            t = Table([[inner]], colWidths=[avail], hAlign="LEFT")
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), QUOTE_BG),
                ("LINEBEFORE", (0, 0), (0, -1), 2.2, NAVY),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]))
            flow.append(KeepTogether([Spacer(1, 3), t, Spacer(1, 8)]))
            continue

        # list item
        m = re.match(r"^\s*(?:[-*]|(\d+)\.)\s+(.*)$", line)
        if m:
            marker = f"{m.group(1)}." if m.group(1) else "•"
            flow.append(Paragraph(inline(m.group(2)), S["bullet"], bulletText=marker))
            i += 1
            continue

        flow.append(Paragraph(inline(line), S["body"]))
        i += 1

    def footer(canvas, docu):
        canvas.saveState()
        canvas.setFont(REG, 7.5)
        canvas.setFillColor(SLATE)
        canvas.drawString(18 * mm, 10 * mm, "Trip Dossier - Slovakia - 09/10/2026")
        canvas.drawRightString(A4[0] - 16 * mm, 10 * mm, f"page {docu.page}")
        canvas.restoreState()

    doc.build(flow, onFirstPage=footer, onLaterPages=footer)
    print(f"written: {pdf_path}")


if __name__ == "__main__":
    convert(sys.argv[1], sys.argv[2])
