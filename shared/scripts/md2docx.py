#!/usr/bin/env python3
"""Converts an SRS/SDS markdown file from this skill into a Word file (and optionally PDF).

    python3 md2docx.py srs-doc.md                 -> srs-doc.docx          (Windows: py md2docx.py ...)
    python3 md2docx.py srs-doc.md --pdf           -> srs-doc.docx + srs-doc.pdf (needs LibreOffice)
    python3 md2docx.py srs-doc.md -o out/x.docx --font "TH SarabunPSK" --size 16

Understands the skill's restricted markdown: # to #### headings, "- " lists, pipe tables, ```mermaid blocks,
![alt](image.png), [ภาพหน้าจอ: name] placeholders, **bold**, and caption lines "ภาพ: ..." (after a figure) and
"ตาราง: ..." (before a table), which are numbered รูปภาพที่ N / ตารางที่ N.

A front matter block (--- key: value --- at the top) adds the hand-in front pages: a cover with the company
logo and a project table, revision history, approval and reference tables, a table of contents, a header with
the logo, company and document code, and a footer with the classification and "หน้า X จาก Y". Keys: brand,
company, company_en, address, contact, logo, header_logo, client_logo, title, title_en, project, contract,
client, doc_code, version, date, classification, author, revision, note, and repeated
"ref: code | name | version | date" lines. "brand: <name>" fills in the keys the document leaves out from
brands/<name>/brand.yaml (company details, logo, colours); the document's own keys win.

Run setup.py once first: it installs python-docx, mermaid-cli and the Sarabun font where missing. Without
mermaid-cli a diagram is kept as text with a note; without LibreOffice there is no PDF.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import env  # noqa: E402

try:
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.section import WD_SECTION
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT, WD_TAB_LEADER
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.image.image import Image as DocxImage
    from docx.shared import Cm, Pt, RGBColor, Twips
except ImportError:
    # setup.py puts python-docx in the skill's own venv when the system Python lacks it
    py = env.venv_python()
    if py and os.path.abspath(sys.executable) != os.path.abspath(py):
        sys.exit(subprocess.run([py, os.path.abspath(__file__)] + sys.argv[1:]).returncode)
    sys.exit("python-docx is missing: run scripts/setup.py (or pip install python-docx)")

HEADING_SIZES = {1: 2, 2: 0, 3: 0, 4: 0}  # points added to a 16 pt body, scaled with the body size
NAVY, GREY = "1F3864", "D9D9D9"  # default front-page table headers / body table headers
BLANK = "..................................."
LOGO_KEYS = ("logo", "header_logo", "client_logo")
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


def field(par, code, font, size, shown="1", color=None):
    """Appends a Word field (PAGE, SECTIONPAGES, TOC ...) whose cached result is `shown`."""
    run = par.add_run()
    set_font(run, font, size)
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    for kind, text in (("begin", None), ("instr", code), ("separate", None), ("text", shown), ("end", None)):
        if kind == "instr":
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
        elif kind == "text":
            el = OxmlElement("w:t")
        else:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), kind)
        if text is not None:
            el.text = text
        run._element.append(el)


def border(par, side, color, size=8):
    ppr = par._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    el = OxmlElement(f"w:{side}")
    for k, v in (("val", "single"), ("sz", str(size)), ("space", "1"), ("color", color)):
        el.set(qn(f"w:{k}"), v)
    bdr.append(el)
    ppr.append(bdr)


def right_tab(par, sec):
    """One right tab at the margin; the Header/Footer styles' own centre and right stops are cleared."""
    stops = par.paragraph_format.tab_stops
    for pos in (Twips(4680), Twips(9360)):
        stops.add_tab_stop(pos, WD_TAB_ALIGNMENT.CLEAR)
    stops.add_tab_stop(sec.page_width - sec.left_margin - sec.right_margin, WD_TAB_ALIGNMENT.RIGHT)


def col_widths(rows, total=16.7):
    """Column widths in cm from the text length: short code columns stay narrow, prose columns get the rest."""
    cols = range(max(len(r) for r in rows))
    cell = [[r[j] if j < len(r) else "" for r in rows] for j in cols]
    longest = [max(len(c) for c in col) for col in cell]
    weights = [min(max(n, 4), 60) for n in longest]
    # a column never breaks inside its longest word (an id such as FR-BK-01): about 0.25 cm a character
    floor = [min(max(max((len(w) for c in col for w in c.split()), default=0) * 0.25 + 0.4, 1.6), 5) for col in cell]
    widths = [max(total * w / sum(weights), f) for w, f in zip(weights, floor)]
    scale = total / sum(widths)
    return [w * scale for w in widths]


def style_font(style, font, size, bold, color="000000"):
    """Makes a built-in style (Heading 1 ...) use the Thai font, black, without its theme fonts."""
    style.font.name, style.font.size, style.font.bold = font, Pt(size), bold
    style.font.italic = False
    style.font.color.rgb = RGBColor.from_string(color)
    rpr = style.element.get_or_add_rPr()
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:
        fonts = OxmlElement("w:rFonts")
        rpr.insert(0, fonts)
    for attr in list(fonts.attrib):
        del fonts.attrib[attr]
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        fonts.set(qn(attr), font)
    for tag, val in (("w:szCs", str(int(round(size * 2)))), ("w:bCs", None)):
        el = rpr.find(qn(tag))
        if el is None:
            el = OxmlElement(tag)
            rpr.append(el)
        if val:
            el.set(qn("w:val"), val)
        elif not bold:
            rpr.remove(el)


def parse_keys(lines, meta):
    """Reads "key: value" lines (# starts a comment) into meta; repeated "ref:" lines collect as rows."""
    for line in lines:
        m = re.match(r"^\s*([a-z_]+)\s*:\s*(.*?)\s*(#.*)?$", line)
        if m and m.group(1) == "ref":
            meta.setdefault("ref", []).append([c.strip() for c in m.group(2).split("|")])
        elif m:
            meta[m.group(1)] = m.group(2).strip().strip('"')
    return meta


def read_front_matter(lines, base_dir):
    """Returns ({key: value, "ref": [rows]}, remaining lines) for a leading --- block, with the brand's keys
    filled in and logo paths made absolute."""
    if not lines or lines[0].strip() != "---":
        return {}, lines
    for n, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            meta = parse_keys(lines[1:n], {"ref": []})
            break
    else:
        return {}, lines  # no closing ---: treat as body
    for key in LOGO_KEYS:
        if meta.get(key) and not os.path.isabs(meta[key]):
            meta[key] = os.path.join(base_dir, meta[key])
    brand = meta.get("brand")
    if brand:
        folder = os.path.join(env.BRANDS_DIR, brand)
        conf = os.path.join(folder, "brand.yaml")
        if os.path.exists(conf):
            with open(conf, encoding="utf-8") as f:
                defaults = parse_keys(f.read().splitlines(), {})
            for key in LOGO_KEYS:
                if defaults.get(key) and not os.path.isabs(defaults[key]):
                    defaults[key] = os.path.join(folder, defaults[key])
            meta = dict(defaults, **{k: v for k, v in meta.items() if v not in ("", [])})
        else:
            known = sorted(d for d in os.listdir(env.BRANDS_DIR)) if os.path.isdir(env.BRANDS_DIR) else []
            print(f"brand {brand!r} not found (have: {', '.join(known) or 'none'}); using the front matter only",
                  file=sys.stderr)
    for key in LOGO_KEYS:
        if meta.get(key) and not os.path.exists(meta[key]):
            print(f"{key} not found: {meta[key]} (left out)", file=sys.stderr)
            del meta[key]
    return meta, lines[n + 1:]


def image_size(path):
    """(width, height) in pixels of a PNG/JPEG/GIF/BMP, else None."""
    try:
        img = DocxImage.from_file(path)
        return img.px_width, img.px_height
    except Exception:
        return None


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
    if cells.endswith("|") and not cells.endswith("\\|"):
        cells = cells[:-1]
    # "\|" is a literal pipe inside a cell (mode=partial\|full)
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", cells)]


class Writer:
    def __init__(self, font, size, base_dir):
        self.doc = Document()
        self.font, self.size, self.base = font, size, base_dir
        self.figures = self.tables = 0
        self.primary, self.table_fill = NAVY, GREY
        sec = self.doc.sections[0]
        sec.page_width, sec.page_height = Cm(21), Cm(29.7)
        sec.top_margin, sec.bottom_margin = Cm(2.65), Cm(2.29)
        sec.left_margin, sec.right_margin = Cm(2.12), Cm(2.12)
        sec.header_distance = sec.footer_distance = Cm(0.88)
        normal = self.doc.styles["Normal"]
        style_font(normal, font, size, False)
        # headings use Word's styles so the table of contents picks them up
        for level in range(1, 5):
            style = self.doc.styles[f"Heading {level}"]
            style_font(style, font, size + HEADING_SIZES[level] * size / 16, True)
            pf = style.paragraph_format
            pf.space_before, pf.space_after = Pt(12 if level == 1 else 6), Pt(4)
            pf.keep_with_next = True
        for level in (1, 2, 3):
            style_font(self.doc.styles[f"toc {level}"] if f"toc {level}" in self.doc.styles
                       else self.doc.styles.add_style(f"toc {level}", 1), font, size, level == 1)
            self.doc.styles[f"toc {level}"].paragraph_format.left_indent = Cm(0.5 * (level - 1))

    # front pages -----------------------------------------------------------------------------------------
    def logo(self, par, path, max_w, max_h):
        """Adds the image scaled to fit max_w x max_h cm, keeping its shape. False when there is none."""
        if not path:
            return False
        size = image_size(path)
        if not size:
            print(f"logo not readable (use PNG or JPEG): {path}", file=sys.stderr)
            return False
        w, h = size
        if w / h > max_w / max_h:
            par.add_run().add_picture(path, width=Cm(max_w))
        else:
            par.add_run().add_picture(path, height=Cm(max_h))
        return True

    def toc(self, entries):
        """A TOC field listing the level 1-2 headings; Word and the PDF step fill in the page numbers."""
        width = self.doc.sections[0].page_width - self.doc.sections[0].left_margin - self.doc.sections[0].right_margin
        pars = []
        for level, text in entries or [(1, "คลิกขวาแล้วเลือก Update Field เพื่อปรับปรุงสารบัญ")]:
            p = self.doc.add_paragraph(style=f"toc {level}")
            p.paragraph_format.tab_stops.add_tab_stop(width, WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
            pars.append((p, text))
        first, last = pars[0][0], pars[-1][0]
        for kind, text in (("begin", None), ("instr", 'TOC \\o "1-2" \\h \\z \\u'), ("separate", None)):
            run = first.add_run()
            el = OxmlElement("w:instrText" if kind == "instr" else "w:fldChar")
            if text:
                el.set(qn("xml:space"), "preserve")
                el.text = text
            else:
                el.set(qn("w:fldCharType"), kind)
            run._element.append(el)
        for p, text in pars:
            set_font(p.add_run(text), self.font, self.size, p.style.name == "toc 1")
        end = OxmlElement("w:fldChar")
        end.set(qn("w:fldCharType"), "end")
        last.add_run()._element.append(end)

    def front_pages(self, meta, toc=None):
        self.primary = meta.get("color_primary", NAVY).lstrip("#")
        self.table_fill = meta.get("color_table", GREY).lstrip("#")
        center = WD_ALIGN_PARAGRAPH.CENTER
        p = self.doc.add_paragraph()
        p.alignment = center
        p.paragraph_format.space_before = Pt(36)
        if meta.get("client_logo"):
            # contractor and agency side by side
            self.logo(p, meta.get("logo"), 5, 2.5)
            p.add_run("\u2003\u2003")
            self.logo(p, meta["client_logo"], 5, 2.5)
        else:
            self.logo(p, meta.get("logo"), 6.6, 2.5)
        for key, bold, scale in (("company", True, 1.1), ("company_en", False, 1)):
            if meta.get(key):
                self.para(meta[key], bold=bold, align=center, space_after=0, scale=scale)
        self.para("", space_after=24)
        self.para(meta.get("title", ""), bold=True, align=center, space_after=0, scale=1.4)
        if meta.get("title_en"):
            self.para(meta["title_en"], bold=True, align=center, space_after=24, scale=1.2)
        version = meta.get("version", "1.0")
        rows = [["รายการ", "รายละเอียด"],
                ["ชื่อโครงการ", meta.get("project", BLANK)],
                ["เลขที่สัญญา", meta.get("contract", BLANK)],
                ["หน่วยงานผู้ว่าจ้าง", meta.get("client", BLANK)],
                ["จัดทำโดย", meta.get("company", BLANK)],
                ["รหัสเอกสาร / เวอร์ชัน", f"{meta.get('doc_code', BLANK)} / Version {version}"],
                ["วันที่จัดทำ", meta.get("date", "___ / ___ / ______")],
                ["ชั้นความลับ", "ชั้นความลับ: " + meta.get("classification", "ใช้ภายในโครงการ (Project Internal Use)")]]
        self.table(rows, header=self.primary, widths=(5, 11.5))
        for key in ("address", "contact"):
            if meta.get(key):
                self.para(meta[key], align=center, space_after=0, scale=0.8)
        self.page_break()

        self.heading(1, "ประวัติการแก้ไขและการอนุมัติเอกสาร", toc=False)
        self.heading(2, "ตารางประวัติการแก้ไข (Revision History)", toc=False)
        first = [f"V.{version}", meta.get("date", ""), meta.get("author", ""),
                 meta.get("revision", "จัดทำ" + meta.get("title", "เอกสาร"))]
        self.table([["เวอร์ชัน", "วันที่", "ผู้แก้ไข", "สาระสำคัญที่แก้ไข"], first] + [[""] * 4] * 3,
                   header=self.primary, widths=(2.5, 3.5, 4.5, 6))
        self.heading(2, "ตารางการอนุมัติเอกสาร (Approval Table)", toc=False)
        self.table([["บทบาท", "ชื่อ-นามสกุล", "ตำแหน่ง", "ลายมือชื่อ / วันที่"]] + [[""] * 4] * 4,
                   header=self.primary, widths=(3.5, 4.5, 4, 4.5))
        self.heading(2, "เอกสารอ้างอิง (Reference Documents)", toc=False)
        refs = [(r + [""] * 4)[:4] for r in meta.get("ref", [])]
        self.table([["รหัส", "ชื่อเอกสาร", "เวอร์ชัน", "วันที่"]] + (refs or [[""] * 4] * 4),
                   header=self.primary, widths=(2.5, 8.5, 2.5, 3))
        if meta.get("note"):
            self.para("หมายเหตุ: " + meta["note"])
        self.page_break()

        self.heading(1, "สารบัญ", toc=False)
        self.toc(toc)
        # ask Word to refresh the table of contents and page counts when the file opens
        upd = OxmlElement("w:updateFields")
        upd.set(qn("w:val"), "true")
        self.doc.settings.element.append(upd)

        body = self.doc.add_section(WD_SECTION.NEW_PAGE)
        pg = OxmlElement("w:pgNumType")
        pg.set(qn("w:start"), "1")
        body._sectPr.append(pg)
        self.header(self.doc.sections[0], meta)
        self.footer(body, meta)

    def header(self, sec, meta):
        """Logo, company name and document code over a navy rule; the body section inherits it."""
        p = sec.header.paragraphs[0]
        right_tab(p, sec)
        small = self.size * 0.7
        if self.logo(p, meta.get("header_logo") or meta.get("logo"), 4, 1):
            set_font(p.add_run("  "), self.font, small)
        run = p.add_run(meta.get("company_en") or meta.get("company", ""))
        set_font(run, self.font, small, True)
        run.font.color.rgb = RGBColor.from_string(self.primary)
        version = meta.get("version", "1.0")
        run = p.add_run(f"\t{meta.get('doc_code', '')}  Version {version}")
        set_font(run, self.font, small)
        run.font.color.rgb = RGBColor.from_string("666666")
        border(p, "bottom", self.primary)

    def footer(self, sec, meta):
        sec.footer.is_linked_to_previous = False
        p = sec.footer.paragraphs[0]
        right_tab(p, sec)
        small, grey = self.size * 0.75, "888888"
        run = p.add_run("ชั้นความลับ: " + meta.get("classification", "ใช้ภายในโครงการ (Project Internal Use)") + "\tหน้า ")
        set_font(run, self.font, small)
        run.font.color.rgb = RGBColor.from_string(grey)
        field(p, "PAGE", self.font, small, color=grey)
        run = p.add_run(" จาก ")
        set_font(run, self.font, small)
        run.font.color.rgb = RGBColor.from_string(grey)
        field(p, "SECTIONPAGES", self.font, small, color=grey)
        border(p, "top", "BFBFBF", 4)

    def plain_footer(self):
        """Without front matter: a centred page number."""
        p = self.doc.sections[0].footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        field(p, "PAGE", self.font, self.size)

    def page_break(self):
        self.doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    # body ------------------------------------------------------------------------------------------------
    def para(self, text, bold=False, align=None, indent=None, space_after=4, scale=1):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_after = Pt(space_after)
        if align is not None:
            p.alignment = align
        if indent is not None:
            p.paragraph_format.first_line_indent = indent
        add_runs(p, text, self.font, self.size * scale, bold)
        return p

    def body_para(self, text):
        p = self.para(text, indent=Cm(1.25))
        # Thai has no spaces between words; thaiDistribute justifies it the way Word does for Thai documents
        jc = OxmlElement("w:jc")
        jc.set(qn("w:val"), "thaiDistribute")
        p._p.get_or_add_pPr().append(jc)

    def heading(self, level, text, toc=True):
        p = self.doc.add_paragraph(style=f"Heading {min(level, 4)}" if toc else None)
        if not toc:  # front-page headings stay out of the table of contents
            p.paragraph_format.space_before = Pt(12 if level == 1 else 6)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            if level == 1:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_runs(p, text, self.font, self.size + HEADING_SIZES.get(level, 0) * self.size / 16, True)

    def bullet(self, text):
        p = self.doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1.75)
        p.paragraph_format.first_line_indent = Cm(-0.5)
        p.paragraph_format.space_after = Pt(0)
        add_runs(p, "• " + text, self.font, self.size)

    def table(self, rows, header=None, widths=None):
        header = header or self.table_fill
        width = max(len(r) for r in rows)
        t = self.doc.add_table(rows=len(rows), cols=width)
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        widths = widths or col_widths(rows)
        for j, col in enumerate(t._tbl.tblGrid.findall(qn("w:gridCol"))):
            col.set(qn("w:w"), str(int(Cm(widths[j]).twips)))
        for i, row in enumerate(rows):
            tr = t.rows[i]._tr.get_or_add_trPr()
            if i == 0:
                # repeat the header row on every page the table runs onto
                tr.append(OxmlElement("w:tblHeader"))
            cant = OxmlElement("w:cantSplit")
            tr.append(cant)
            for j in range(width):
                cell = t.cell(i, j)
                cell.width = Cm(widths[j])
                par = cell.paragraphs[0]
                par.paragraph_format.space_after = Pt(0)
                if i == 0:
                    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
                add_runs(par, row[j] if j < len(row) else "", self.font, self.size, i == 0)
                if i == 0:
                    shade(cell, header)
                    if header == self.primary:
                        for run in par.runs:
                            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        self.doc.add_paragraph().paragraph_format.space_after = Pt(0)

    def image(self, path):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.keep_with_next = True
        # fit 15 x 20 cm so a tall diagram (an ER chart) stays on one page
        size = image_size(path)
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
        self.para(f"รูปภาพที่ {self.figures} {text}", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)

    def table_caption(self, text):
        self.tables += 1
        p = self.para(f"ตารางที่ {self.tables} {text}", bold=True, space_after=2)
        p.paragraph_format.keep_with_next = True


def convert(md_path, out_path, font, size):
    with open(md_path, encoding="utf-8") as f:
        meta, lines = read_front_matter(f.read().splitlines(), os.path.dirname(os.path.abspath(md_path)))
    w = Writer(font, size, os.path.dirname(os.path.abspath(md_path)))
    if meta:
        headings = [re.match(r"^(#{1,2})\s+(.*)$", ln.strip()) for ln in lines]
        w.front_pages(meta, [(len(m.group(1)), m.group(2).strip()) for m in headings if m])
    else:
        w.plain_footer()
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
        w.body_para(" ".join(text))
    w.doc.save(out_path)
    shutil.rmtree(workdir, ignore_errors=True)


LIBRARY = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE library:library PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "library.dtd">
<library:library xmlns:library="http://openoffice.org/2000/library" library:name="Standard"
 library:readonly="false" library:passwordprotected="false">
 <library:element library:name="SrsSds"/>
</library:library>
"""
# Basic, not Python-UNO: LibreOffice's bundled Python is not usable everywhere (macOS kills it)
MACRO = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE script:module PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "module.dtd">
<script:module xmlns:script="http://openoffice.org/2000/script" script:name="SrsSds" script:language="StarBasic">
Sub ExportPdf(src As String, dst As String)
  Dim args(0) As New com.sun.star.beans.PropertyValue
  args(0).Name = &quot;Hidden&quot;
  args(0).Value = True
  doc = StarDesktop.loadComponentFromURL(ConvertToURL(src), &quot;_blank&quot;, 0, args())
  For k = 1 To 2
    idx = doc.getDocumentIndexes()
    For i = 0 To idx.getCount() - 1
      idx.getByIndex(i).update()
    Next i
    doc.getTextFields().refresh()
  Next k
  SetPageTotals(doc)
  Dim out(0) As New com.sun.star.beans.PropertyValue
  out(0).Name = &quot;FilterName&quot;
  out(0).Value = &quot;writer_pdf_Export&quot;
  doc.storeToURL(ConvertToURL(dst), out())
  doc.close(True)
  StarDesktop.terminate()
End Sub

Rem LibreOffice keeps Word&apos;s SECTIONPAGES as an unknown field showing its cached value; write in the body
Rem section&apos;s page count (pages from the first paragraph of that section&apos;s page style to the end)
Sub SetPageTotals(doc)
  styles = doc.getStyleFamilies().getByName(&quot;PageStyles&quot;)
  vc = doc.getCurrentController().getViewCursor()
  total = doc.getCurrentController().getPropertyValue(&quot;PageCount&quot;)
  For i = 0 To styles.getCount() - 1
    st = styles.getByIndex(i)
    If st.FooterIsOn Then
      first = 0
      en = doc.getText().createEnumeration()
      Do While en.hasMoreElements() And first = 0
        par = en.nextElement()
        If par.supportsService(&quot;com.sun.star.text.Paragraph&quot;) Then
          If par.PageDescName = st.Name Then
            vc.gotoRange(par.getStart(), False)
            first = vc.getPage()
          End If
        End If
      Loop
      If first &gt; 0 Then
        inField = False
        fe = st.FooterText.createEnumeration()
        Do While fe.hasMoreElements()
          pe = fe.nextElement().createEnumeration()
          Do While pe.hasMoreElements()
            po = pe.nextElement()
            If po.TextPortionType = &quot;TextFieldSeparator&quot; Then inField = True
            If po.TextPortionType = &quot;TextFieldEnd&quot; Then inField = False
            If inField And po.TextPortionType = &quot;Text&quot; Then po.setString(CStr(total - first + 1))
          Loop
        Loop
      End If
    End If
  Next i
End Sub
</script:module>
"""


def pdf_with_toc(exe, docx_path, pdf, run_env):
    """Exports through a Basic macro in a throwaway LibreOffice profile, so the table of contents and the
    page fields are filled in (a plain --convert-to leaves the contents empty). Returns True on success."""
    profile = tempfile.mkdtemp(prefix="srs-sds-lo-")
    url = "file:///" + profile.replace(os.sep, "/").lstrip("/")
    base = [exe, "--headless", "--norestore", "--nologo", f"-env:UserInstallation={url}"]
    try:
        # the first start writes a fresh profile (and its Standard library); the macro goes in afterwards
        subprocess.run(base + ["--terminate_after_init"], capture_output=True, timeout=300, env=run_env)
        lib = os.path.join(profile, "user", "basic", "Standard")
        if not os.path.isdir(lib):
            return False
        with open(os.path.join(lib, "script.xlb"), "w", encoding="utf-8") as f:
            f.write(LIBRARY)
        with open(os.path.join(lib, "SrsSds.xba"), "w", encoding="utf-8") as f:
            f.write(MACRO)
        if os.path.exists(pdf):
            os.remove(pdf)
        src, dst = (os.path.abspath(p).replace('"', "") for p in (docx_path, pdf))
        subprocess.run(base + [f'macro:///Standard.SrsSds.ExportPdf("{src}","{dst}")'],
                       capture_output=True, timeout=600, env=run_env)
        return os.path.exists(pdf)
    except (subprocess.SubprocessError, OSError):
        return False
    finally:
        shutil.rmtree(profile, ignore_errors=True)


def to_pdf(docx_path):
    exe = env.find_soffice()
    if not exe:
        sys.exit("PDF needs LibreOffice (run scripts/setup.py for the install command); the .docx was written. "
                 "Or open it in Word and Save As PDF.")
    outdir = os.path.dirname(os.path.abspath(docx_path))
    pdf = os.path.splitext(docx_path)[0] + ".pdf"
    run_env, fc = env.fontconfig_env(os.environ)
    try:
        if pdf_with_toc(exe, docx_path, pdf, run_env):
            return pdf
        print("table of contents not filled in the PDF (LibreOffice macro failed); open the .docx in Word, "
              "update the fields and save as PDF", file=sys.stderr)
        subprocess.run([exe, "--headless", "--convert-to", "pdf", "--outdir", outdir, os.path.abspath(docx_path)],
                       check=True, capture_output=True, timeout=300, env=run_env)
    finally:
        if fc:
            shutil.rmtree(fc, ignore_errors=True)
    return pdf


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
