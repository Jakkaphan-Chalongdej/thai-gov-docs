#!/usr/bin/env python3
"""Converts an SRS/SDS markdown file from this skill into a Word file (and optionally PDF).

    python3 md2docx.py srs-doc.md                 -> srs-doc.docx          (Windows: py md2docx.py ...)
    python3 md2docx.py srs-doc.md --pdf           -> srs-doc.docx + srs-doc.pdf (needs LibreOffice)
    python3 md2docx.py srs-doc.md -o out/x.docx --font "TH SarabunPSK" --size 16

Understands the skill's restricted markdown: # to #### headings, "- " lists, pipe tables, ```mermaid blocks,
![alt](image.png), [ภาพหน้าจอ: name] placeholders, **bold**, and caption lines "ภาพ: ..." (after a figure) and
"ตาราง: ..." (before a table), which are numbered ภาพที่ N / ตารางที่ N.

Run setup.py once first: it installs python-docx, mermaid-cli and the Sarabun font where missing. Without
mermaid-cli a diagram is kept as text with a note; without LibreOffice there is no PDF.
"""
import argparse
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import env  # noqa: E402

try:
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor
except ImportError:
    # setup.py puts python-docx in the skill's own venv when the system Python lacks it
    py = env.venv_python()
    if py and os.path.abspath(sys.executable) != os.path.abspath(py):
        sys.exit(subprocess.run([py, os.path.abspath(__file__)] + sys.argv[1:]).returncode)
    sys.exit("python-docx is missing: run scripts/setup.py (or pip install python-docx)")

HEADING_SIZES = {1: 4, 2: 2, 3: 1, 4: 0}  # points added to a 16 pt body, scaled with the body size
TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$")
TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")
IMAGE = re.compile(r"^!\[(.*?)\]\((.+?)\)\s*$")
PLACEHOLDER = re.compile(r"^\[ภาพหน้าจอ:\s*(.+?)\]\s*$")


def set_font(run, font, size, bold=None):
    size = round(size * 2) / 2  # Word stores half-points
    run.font.name = font
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    rpr = run._element.get_or_add_rPr()
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        rpr.insert(0, fonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        fonts.set(qn(attr), font)
    # Thai is a complex script: Word sizes it with szCs and bolds it with bCs
    szcs = rpr.find(qn("w:szCs"))
    if szcs is None:
        szcs = OxmlElement("w:szCs")
        rpr.append(szcs)
    szcs.set(qn("w:val"), str(int(size * 2)))
    if bold:
        rpr.append(OxmlElement("w:bCs"))


def add_runs(par, text, font, size, bold=False):
    """Adds text to a paragraph, honouring **bold** spans."""
    for i, part in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        if part:
            set_font(par.add_run(part), font, size, bold or i % 2 == 1)


def shade(cell, color):
    tcpr = cell._element.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color)
    tcpr.append(shd)


def page_number(section, font, size):
    par = section.header.paragraphs[0]
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = par.add_run()
    set_font(run, font, size)
    for kind, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if kind:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), kind)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = text
        run._element.append(el)


def png_size(path):
    """(width, height) of a PNG, else None."""
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24])


def render_mermaid(code, workdir, n, font):
    cmd = env.find_mmdc()
    if not cmd:
        print(f"mermaid diagram {n} not rendered: no Node.js/mermaid-cli (run scripts/setup.py)", file=sys.stderr)
        return None
    src = os.path.join(workdir, f"d{n}.mmd")
    out = os.path.join(workdir, f"d{n}.png")
    cfg = os.path.join(workdir, "mermaid.json")
    with open(src, "w", encoding="utf-8") as f:
        f.write(code)
    with open(cfg, "w", encoding="utf-8") as f:
        f.write('{"theme":"neutral","themeVariables":{"fontFamily":"%s, Sarabun, sans-serif"}}' % font)
    run_env, fc = env.fontconfig_env(os.environ)
    if cmd[0].endswith(("npx", "npx.cmd")):
        # npx downloads into the npm cache; a private one avoids a broken ~/.npm
        run_env = dict(run_env, npm_config_cache=os.path.join(workdir, "npm"))
    try:
        subprocess.run(cmd + ["-i", src, "-o", out, "-c", cfg, "-s", "2", "-b", "white"],
                       check=True, capture_output=True, timeout=300, env=run_env)
    except (subprocess.SubprocessError, OSError) as e:
        err = getattr(e, "stderr", b"") or b""
        print(f"mermaid diagram {n} not rendered: {err.decode(errors='replace')[-300:] or e}", file=sys.stderr)
        return None
    finally:
        if fc:
            shutil.rmtree(fc, ignore_errors=True)
    return out if os.path.exists(out) else None


def split_row(line):
    cells = line.strip()
    if cells.startswith("|"):
        cells = cells[1:]
    if cells.endswith("|"):
        cells = cells[:-1]
    return [c.strip() for c in cells.split("|")]


class Writer:
    def __init__(self, font, size, base_dir):
        self.doc = Document()
        self.font, self.size, self.base = font, size, base_dir
        self.figures = self.tables = 0
        sec = self.doc.sections[0]
        sec.page_width, sec.page_height = Cm(21), Cm(29.7)
        sec.top_margin, sec.bottom_margin = Cm(2.5), Cm(2)
        sec.left_margin, sec.right_margin = Cm(3), Cm(2)
        normal = self.doc.styles["Normal"]
        normal.font.name, normal.font.size = font, Pt(size)
        page_number(sec, font, size)

    def para(self, text, bold=False, align=None, indent=None, space_after=4):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        if align is not None:
            p.alignment = align
        if indent is not None:
            p.paragraph_format.first_line_indent = indent
        add_runs(p, text, self.font, self.size, bold)
        return p

    def heading(self, level, text):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12 if level <= 2 else 6)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        if level == 1:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_runs(p, text, self.font, self.size + HEADING_SIZES.get(level, 0) * self.size / 16, True)

    def bullet(self, text):
        p = self.doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1)
        p.paragraph_format.first_line_indent = Cm(-0.5)
        p.paragraph_format.space_after = Pt(0)
        add_runs(p, "- " + text, self.font, self.size)

    def table(self, rows):
        width = max(len(r) for r in rows)
        t = self.doc.add_table(rows=len(rows), cols=width)
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for i, row in enumerate(rows):
            for j in range(width):
                cell = t.cell(i, j)
                cell.paragraphs[0].paragraph_format.space_after = Pt(0)
                add_runs(cell.paragraphs[0], row[j] if j < len(row) else "", self.font, self.size, i == 0)
                if i == 0:
                    shade(cell, "D9E2F3")
        self.doc.add_paragraph().paragraph_format.space_after = Pt(0)

    def image(self, path):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.keep_with_next = True
        # fit 15 x 20 cm so a tall diagram (an ER chart) stays on one page
        size = png_size(path)
        if size and size[1] * 15 > size[0] * 20:
            p.add_run().add_picture(path, height=Cm(20))
        else:
            p.add_run().add_picture(path, width=Cm(15))

    def placeholder(self, name):
        t = self.doc.add_table(rows=1, cols=1)
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = t.cell(0, 0)
        cell.width = Cm(15)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(60)
        p.paragraph_format.space_after = Pt(60)
        run = p.add_run(f"[ใส่ภาพหน้าจอ: {name}]")
        set_font(run, self.font, self.size)
        run.font.color.rgb = RGBColor(0x80, 0x80, 0x80)

    def code(self, text, note):
        self.para(note, align=None)
        for line in text.splitlines():
            p = self.doc.add_paragraph()
            p.paragraph_format.space_after = Pt(0)
            set_font(p.add_run(line), "Courier New", self.size * 0.75)

    def figure_caption(self, text):
        self.figures += 1
        self.para(f"ภาพที่ {self.figures} {text}", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)

    def table_caption(self, text):
        self.tables += 1
        p = self.para(f"ตารางที่ {self.tables} {text}", bold=True, space_after=2)
        p.paragraph_format.keep_with_next = True


def convert(md_path, out_path, font, size):
    with open(md_path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    w = Writer(font, size, os.path.dirname(os.path.abspath(md_path)))
    workdir = tempfile.mkdtemp(prefix="srs-sds-")
    diagrams = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        if s.startswith("```"):
            lang = s[3:].strip()
            body = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            code = "\n".join(body)
            if lang == "mermaid":
                diagrams += 1
                png = render_mermaid(code, workdir, diagrams, font)
                if png:
                    w.image(png)
                else:
                    w.code(code, "(แผนภาพ mermaid ยังไม่ได้แปลงเป็นภาพ: ติดตั้ง Node.js หรือ mermaid-cli แล้วแปลงใหม่)")
            else:
                w.code(code, "")
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            w.heading(len(m.group(1)), m.group(2).strip())
            i += 1
            continue
        if TABLE_ROW.match(s):
            rows = []
            while i < len(lines) and TABLE_ROW.match(lines[i].strip()):
                if not TABLE_SEP.match(lines[i].strip()):
                    rows.append(split_row(lines[i]))
                i += 1
            w.table(rows)
            continue
        if s.startswith("- "):
            w.bullet(s[2:])
            i += 1
            continue
        m = IMAGE.match(s)
        if m:
            path = m.group(2)
            if not os.path.isabs(path):
                path = os.path.join(w.base, path)
            if os.path.exists(path):
                w.image(path)
            else:
                w.placeholder(m.group(1) or os.path.basename(path))
            i += 1
            continue
        m = PLACEHOLDER.match(s)
        if m:
            w.placeholder(m.group(1))
            i += 1
            continue
        if s.startswith("ภาพ:"):
            w.figure_caption(s[len("ภาพ:"):].strip())
            i += 1
            continue
        if s.startswith("ตาราง:"):
            w.table_caption(s[len("ตาราง:"):].strip())
            i += 1
            continue
        # a paragraph runs until a blank line or a line of another kind
        text = [s]
        i += 1
        while i < len(lines):
            n = lines[i].strip()
            if (not n or n.startswith(("#", "- ", "```", "ภาพ:", "ตาราง:", "![", "[ภาพหน้าจอ:"))
                    or TABLE_ROW.match(n)):
                break
            text.append(n)
            i += 1
        w.para(" ".join(text), indent=Cm(1.25))
    w.doc.save(out_path)
    shutil.rmtree(workdir, ignore_errors=True)


def to_pdf(docx_path):
    exe = env.find_soffice()
    if not exe:
        sys.exit("PDF needs LibreOffice (run scripts/setup.py for the install command); the .docx was written. "
                 "Or open it in Word and Save As PDF.")
    outdir = os.path.dirname(os.path.abspath(docx_path))
    run_env, fc = env.fontconfig_env(os.environ)
    try:
        subprocess.run([exe, "--headless", "--convert-to", "pdf", "--outdir", outdir, os.path.abspath(docx_path)],
                       check=True, capture_output=True, timeout=300, env=run_env)
    finally:
        if fc:
            shutil.rmtree(fc, ignore_errors=True)
    return os.path.splitext(docx_path)[0] + ".pdf"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
        sys.stderr.reconfigure(errors="replace")
    ap = argparse.ArgumentParser(description="SRS/SDS markdown -> .docx (and .pdf)")
    ap.add_argument("markdown")
    ap.add_argument("-o", "--output", help="output .docx (default: next to the markdown)")
    ap.add_argument("--pdf", action="store_true", help="also write a PDF with LibreOffice")
    ap.add_argument("--font", help='default: "TH Sarabun New" when installed, else the bundled "Sarabun"')
    ap.add_argument("--size", type=float, help="body size in pt (default 16 for TH Sarabun, 11 for Sarabun)")
    a = ap.parse_args()
    font = a.font or env.installed_font() or "Sarabun"
    size = a.size or (round(16 * env.SARABUN_SCALE) if font == "Sarabun" else 16)
    out = a.output or os.path.splitext(a.markdown)[0] + ".docx"
    convert(a.markdown, out, font, size)
    print(out)
    if a.pdf:
        print(to_pdf(out))


if __name__ == "__main__":
    main()
