#!/usr/bin/env python3
"""Typeset a MAIM manuscript markdown file into a 6x9 review-proof interior PDF.

Companion to the maim-integrity-publishing-design skill's build_covers.py, which
handles covers. This handles the text block.

This produces a REVIEW PROOF, not a print-ready interior. It does not place the
MD mark or the author portrait — those are hash-verified assets under the design
lock, and this script will not substitute approximations for them.

Usage:
    python3.13 scripts/build_interior.py --input <manuscript.md> --output <out.pdf>

Requires: reportlab, Pillow. On this container the interpreter is python3.13.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch as INCH
from reportlab.platypus import (
    BaseDocTemplate,
    Image,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

# ---------------------------------------------------------------- brand

PAGE_W, PAGE_H = 6 * inch, 9 * inch

GROUND = colors.HexColor("#111111")
GOLD = colors.HexColor("#C9931A")
GREEN = colors.HexColor("#1F8A4C")
RULE = colors.HexColor("#C9C4B8")
MUTED = colors.HexColor("#5A5650")

# DejaVu ships with the container. Georgia is the brand body face and is not
# available here, so the proof is set in DejaVu Serif and the substitution is
# declared on the colophon rather than hidden.
BODY_FONT = "Times-Roman"
BODY_BOLD = "Times-Bold"
BODY_ITAL = "Times-Italic"
DISPLAY = "Helvetica-Bold"
MONO = "Courier"

ASSETS = Path(__file__).resolve().parent.parent / "assets" / "brand"
MARK = ASSETS / "MD-Circle-Original.png"
PORTRAIT = ASSETS / "Major-Author-Photo.JPG"

TITLE = "You Are the System"
SERIES = "MAJOR MOVES · VOLUME ONE"
AUTHOR = "Major Dream Williams"

# ---------------------------------------------------------------- styles


def styles() -> dict[str, ParagraphStyle]:
    s = {}
    s["body"] = ParagraphStyle(
        "body", fontName=BODY_FONT, fontSize=10.5, leading=15.5,
        alignment=TA_JUSTIFY, spaceAfter=7, textColor=GROUND,
    )
    s["first"] = ParagraphStyle("first", parent=s["body"], firstLineIndent=0)
    s["cont"] = ParagraphStyle("cont", parent=s["body"], firstLineIndent=12)
    s["h1"] = ParagraphStyle(
        "h1", fontName=DISPLAY, fontSize=19, leading=23, spaceBefore=0,
        spaceAfter=16, textColor=GROUND, alignment=TA_LEFT,
    )
    s["h2"] = ParagraphStyle(
        "h2", fontName=DISPLAY, fontSize=12.5, leading=16, spaceBefore=16,
        spaceAfter=7, textColor=GROUND,
    )
    s["h3"] = ParagraphStyle(
        "h3", fontName=BODY_BOLD, fontSize=11, leading=14, spaceBefore=12,
        spaceAfter=5, textColor=GROUND,
    )
    s["quote"] = ParagraphStyle(
        "quote", fontName=BODY_ITAL, fontSize=10.5, leading=15.5,
        leftIndent=16, rightIndent=10, spaceBefore=4, spaceAfter=8,
        textColor=GROUND, alignment=TA_LEFT,
    )
    s["voicelabel"] = ParagraphStyle(
        "voicelabel", fontName=MONO, fontSize=7, leading=10, leftIndent=16,
        spaceBefore=10, spaceAfter=3, textColor=GOLD,
    )
    s["bullet"] = ParagraphStyle(
        "bullet", parent=s["body"], leftIndent=16, bulletIndent=5,
        alignment=TA_LEFT, spaceAfter=4,
    )
    s["epigraph"] = ParagraphStyle(
        "epigraph", fontName=BODY_ITAL, fontSize=12, leading=18,
        alignment=TA_CENTER, leftIndent=28, rightIndent=28,
        spaceBefore=30, spaceAfter=30, textColor=GROUND,
    )
    s["ttl"] = ParagraphStyle(
        "ttl", fontName=DISPLAY, fontSize=30, leading=34, alignment=TA_CENTER,
        textColor=GROUND, spaceAfter=10,
    )
    s["series"] = ParagraphStyle(
        "series", fontName=MONO, fontSize=8.5, leading=12, alignment=TA_CENTER,
        textColor=GOLD, spaceAfter=28,
    )
    s["byline"] = ParagraphStyle(
        "byline", fontName=BODY_FONT, fontSize=12, leading=16,
        alignment=TA_CENTER, textColor=GROUND, spaceBefore=16,
    )
    s["note"] = ParagraphStyle(
        "note", fontName=BODY_FONT, fontSize=8, leading=11.5,
        alignment=TA_LEFT, textColor=MUTED,
    )
    s["cell"] = ParagraphStyle(
        "cell", fontName=BODY_FONT, fontSize=8.5, leading=12, textColor=GROUND,
    )
    s["cellh"] = ParagraphStyle(
        "cellh", fontName=BODY_BOLD, fontSize=8.5, leading=12, textColor=GROUND,
    )
    return s


# ---------------------------------------------------------------- inline md

def inline(text: str) -> str:
    """Convert the inline markdown this manuscript actually uses."""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<b><i>\1</i></b>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"`(.+?)`", r'<font face="Courier" size="9">\1</font>', text)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r"\1", text)
    text = text.replace("—", "—").replace("·", "·")
    return text


def is_table_row(line: str) -> bool:
    return line.strip().startswith("|") and line.strip().endswith("|")


def is_divider(line: str) -> bool:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c)


# ---------------------------------------------------------------- parse

def build_story(md: str, S: dict) -> list:
    story: list = []
    lines = md.split("\n")
    i = 0
    para: list[str] = []
    first_after_head = True

    # The manuscript file carries production scaffolding the reader must never
    # see: the approval record at the top and the production status at the end.
    # The book proper runs from "A Word from Major" to the workbook's end.
    def find(pattern: str, default: int) -> int:
        for n, ln in enumerate(lines):
            if re.match(pattern, ln.strip()):
                return n
        return default

    start = find(r"^##\s+A Word from Major", 0)
    end = find(r"^##\s+Production status", len(lines))
    lines = lines[start:end]

    def flush():
        nonlocal para, first_after_head
        if not para:
            return
        txt = inline(" ".join(para).strip())
        if txt:
            story.append(Paragraph(txt, S["first"] if first_after_head else S["cont"]))
            first_after_head = False
        para = []

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped:
            flush()
            i += 1
            continue

        # horizontal rule -> small breathing space
        if re.fullmatch(r"-{3,}|\*{3,}", stripped):
            flush()
            story.append(Spacer(1, 9))
            i += 1
            continue

        # headings
        m = re.match(r"^(#{1,4})\s+(.*)", stripped)
        if m:
            flush()
            level, text = len(m.group(1)), m.group(2).strip()
            if level == 1:
                story.append(PageBreak())
                story.append(Spacer(1, 42))
                story.append(Paragraph(inline(text), S["h1"]))
            elif level == 2:
                story.append(Paragraph(inline(text), S["h2"]))
            else:
                story.append(Paragraph(inline(text), S["h3"]))
            first_after_head = True
            i += 1
            continue

        # blockquote run — the author-voice blocks
        if stripped.startswith(">"):
            flush()
            block: list[str] = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                block.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            chunk: list[str] = []
            flowed: list = []
            for bl in block + [""]:
                if bl.strip():
                    chunk.append(bl.strip())
                elif chunk:
                    text = " ".join(chunk)
                    if "[MAJOR'S WORDS]" in text or "MAJOR'S WORDS" in text:
                        label = text.replace("**", "").strip()
                        flowed.append(Paragraph(inline(label), S["voicelabel"]))
                    else:
                        flowed.append(Paragraph(inline(text), S["quote"]))
                    chunk = []
            story.append(KeepTogether(flowed) if len(flowed) <= 4 else flowed[0])
            if len(flowed) > 4:
                story.extend(flowed[1:])
            first_after_head = True
            continue

        # table
        if is_table_row(stripped):
            flush()
            rows: list[list[str]] = []
            while i < len(lines) and is_table_row(lines[i].strip()):
                cur = lines[i].strip()
                if not is_divider(cur):
                    rows.append([c.strip() for c in cur.strip("|").split("|")])
                i += 1
            if rows:
                ncols = max(len(r) for r in rows)
                data = []
                for ri, r in enumerate(rows):
                    r = r + [""] * (ncols - len(r))
                    sty = S["cellh"] if ri == 0 else S["cell"]
                    data.append([Paragraph(inline(c), sty) for c in r])
                avail = PAGE_W - 1.95 * INCH
                t = Table(data, colWidths=[avail / ncols] * ncols, hAlign="LEFT")
                t.setStyle(TableStyle([
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("LINEBELOW", (0, 0), (-1, 0), 0.6, GROUND),
                    ("LINEBELOW", (0, 1), (-1, -2), 0.25, RULE),
                ]))
                story.append(Spacer(1, 5))
                story.append(t)
                story.append(Spacer(1, 9))
                first_after_head = True
            continue

        # bullets / numbered
        m = re.match(r"^[-*]\s+(.*)", stripped)
        if m:
            flush()
            story.append(Paragraph(inline(m.group(1)), S["bullet"], bulletText="•"))
            i += 1
            continue
        m = re.match(r"^(\d+)[.)]\s+(.*)", stripped)
        if m:
            flush()
            story.append(Paragraph(inline(m.group(2)), S["bullet"],
                                   bulletText=f"{m.group(1)}."))
            i += 1
            continue

        # code fence — skip the fence markers, keep contents as mono
        if stripped.startswith("```"):
            flush()
            i += 1
            buf = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            for b in buf:
                if b.strip():
                    story.append(Paragraph(
                        inline(b), ParagraphStyle("c", parent=S["note"],
                                                  fontName=MONO, fontSize=8.5)))
            story.append(Spacer(1, 6))
            continue

        para.append(stripped)
        i += 1

    flush()
    return story


# ---------------------------------------------------------------- front matter

def front_matter(S: dict) -> list:
    out: list = [Spacer(1, 1.15 * INCH)]
    if MARK.is_file():
        # Scaled proportionately. Never redrawn, never regenerated.
        out.append(Image(str(MARK), width=1.05 * INCH, height=1.05 * INCH,
                         hAlign="CENTER"))
        out.append(Spacer(1, 0.4 * INCH))
    else:
        out.append(Spacer(1, 1.45 * INCH))
    out += [
        Paragraph(SERIES, S["series"]),
        Paragraph(TITLE, S["ttl"]),
        Paragraph(AUTHOR, S["byline"]),
        PageBreak(),
        Spacer(1, 1.2 * INCH),
        Paragraph("If everything stops when you stop&nbsp;&mdash; what exactly "
                  "have you built?", S["epigraph"]),
        PageBreak(),
    ]
    return out


def about_author(S: dict) -> list:
    """Bio drawn from Major's own Startup Qatar Founder Profile — his document,
    his wording. No biography is invented here."""
    out: list = [PageBreak(), Spacer(1, 0.75 * INCH),
                 Paragraph("About the Author", S["h2"]), Spacer(1, 10)]
    if PORTRAIT.is_file():
        # Proportionate framing only; the supplied likeness is never synthesized.
        from PIL import Image as PILImage
        w, h = PILImage.open(PORTRAIT).size
        tw = 1.85 * INCH
        out.append(Image(str(PORTRAIT), width=tw, height=tw * h / w, hAlign="LEFT"))
        out.append(Spacer(1, 12))
    for para in [
        "<b>Major Dream Williams</b> was born in New York City, raised in The Bronx "
        "and Mount Vernon, and shaped by a Jamaican immigrant family.",
        "He worked as a licensed financial advisor holding Series 7, 6 and 63 "
        "credentials. He entered cryptocurrency in 2012 and moved into Web3 "
        "development in 2017, then expanded into AI, automation, data systems and "
        "agentic workforces.",
        "He is the founder of AMA Solutions Corp and the architect of Foundry OS, "
        "building digital infrastructure for founders, creators, students and "
        "emerging markets \u2014 work organised around one principle: "
        "<b>ownership over dependency</b>.",
    ]:
        out.append(Paragraph(para, S["body"]))
    out.append(Spacer(1, 8))
    out.append(Paragraph("\u201cFinance exposed the mechanics of capital. Web3 opened "
                         "new models for ownership. AI made it possible to organize "
                         "those ideas into practical systems.\u201d", S["quote"]))
    return out


def colophon(S: dict) -> list:
    notes = [
        "<b>Review proof &mdash; not print-ready.</b>",
        "",
        "This proof carries the approved manuscript text only. It is produced for "
        "reading and review, and a physical spine cannot be calculated until final "
        "page count, printer trim, paper, binding, bleed and barcode specifications "
        "are fixed.",
        "",
        "<b>Marks and likeness:</b>",
        "The MD/woven-hat mark and the author photograph are the approved v0.4 "
        "originals, restored 23 October 2026 and verified byte-for-byte against the "
        "checksums in the MAIM Integrity design lock. They are placed unaltered "
        "except for proportionate scaling. Nothing here is redrawn, traced or "
        "regenerated.",
        "",
        "<b>Cover:</b> this proof is the text block only. Covers build separately "
        "from the approved v0.4 cover family.",
        "",
        "<b>Typeface substitution:</b>",
        "The brand body face is Georgia, which is not installed on the build "
        "machine. This proof is set in a serif substitute. Final typesetting should "
        "use Georgia for body and Arial Narrow for display.",
        "",
        "Author sections are assembled from recorded intake sessions of 14 and 23 "
        "October 2026 and were approved by Major Dream Williams on 23 October 2026.",
    ]
    out = [PageBreak(), Spacer(1, 0.9 * INCH)]
    for n in notes:
        out.append(Paragraph(n, S["note"]) if n else Spacer(1, 7))
    return out


# ---------------------------------------------------------------- doc

class Book(BaseDocTemplate):
    def __init__(self, path: str, **kw):
        super().__init__(path, pagesize=(PAGE_W, PAGE_H),
                         leftMargin=0.95 * INCH, rightMargin=1.0 * INCH,
                         topMargin=0.85 * INCH, bottomMargin=0.9 * INCH,
                         title=f"{TITLE} — {SERIES.title()}", author=AUTHOR, **kw)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width,
                      self.height, id="text")
        self.addPageTemplates([PageTemplate(id="main", frames=[frame],
                                            onPage=self._furniture)])

    def _furniture(self, canv, doc):
        canv.saveState()
        n = doc.page
        if n > 2:
            canv.setFont(MONO, 7)
            canv.setFillColor(MUTED)
            head = TITLE if n % 2 == 0 else "MAJOR MOVES · VOLUME ONE"
            canv.drawCentredString(PAGE_W / 2, PAGE_H - 0.55 * INCH, head.upper())
            canv.setFillColor(GOLD)
            canv.drawCentredString(PAGE_W / 2, 0.58 * INCH, str(n))
        canv.restoreState()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    a = ap.parse_args()

    src = Path(a.input)
    if not src.is_file():
        print(f"error: no manuscript at {src}", file=sys.stderr)
        return 1

    S = styles()
    story = front_matter(S) + build_story(src.read_text(encoding="utf-8"), S)
    story += about_author(S) + colophon(S)

    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    doc = Book(str(out))
    doc.build(story)

    print(f"wrote {out}  ({out.stat().st_size // 1024} KB)")
    print("REVIEW PROOF — text block only; covers build separately. See colophon.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
