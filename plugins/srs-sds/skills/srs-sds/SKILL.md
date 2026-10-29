---
name: srs-sds
description: เขียนเอกสาร SRS และ/หรือ SDS ภาษาไทยแบบหน่วยงานรัฐจาก TOR หรือบรีฟ (ทำ SRS อย่างเดียว, SDS อย่างเดียวจาก SRS ที่มีอยู่ หรือทั้งคู่) ได้แก่ ความต้องการพร้อม acceptance criteria, เอกสารออกแบบระบบกับ schema PostgreSQL และเอกสารส่งมอบ SRS/SDD แบบผู้รับจ้าง (ปกบริษัท ประวัติการแก้ไข ตารางอนุมัติ สารบัญ, FR/NFR แยกโมดูลอ้างอิงข้อ TOR, ตารางสิทธิ์ตามบทบาท, ADR, มุมมองสถาปัตยกรรม, หน้าจอ, ตารางข้อมูล, API, ความปลอดภัย, ตารางสอบทานย้อนกลับ) ตามแบรนด์บริษัท (ชื่อ ที่อยู่ โลโก้ เปลี่ยนได้) ออกเป็น Word/PDF ใช้เมื่อผู้ใช้ขอ SRS, SDS, SDD, เอกสารความต้องการ, เอกสารออกแบบระบบ, ตารางสืบย้อน TOR หรือเอกสารส่งมอบให้คณะกรรมการตรวจรับ
---
# SRS / SDS for Thai government software projects

Turns a TOR (ขอบเขตของงาน) or a short brief into the requirement and design documents a Thai agency's acceptance
committee expects. Written from the AI Factory pipeline (BA → Architect → Doc agents), packaged to run alone.

## Pick the job from the request

| The user asks for | Do | Output files |
|---|---|---|
| SRS / เอกสารความต้องการ (ฉบับส่งมอบ) | A → C-SRS | `srs.md`, `srs-doc` .md/.docx/.pdf |
| SDS / SDD / เอกสารออกแบบระบบ (ฉบับส่งมอบ) | SRS in hand (else A first) → B → C-SDS | `design.md`, `schema.sql`, `sds-doc` .md/.docx/.pdf |
| SRS และ SDS / "ทำให้ครบ" / เอกสารตรวจรับ | A → B → C-SRS → C-SDS | all of the above |
| only working files: ความต้องการ, user stories, schema | A, or B | `srs.md`, or `design.md` + `schema.sql` |

An SRS-only job never runs Step B. Reuse files that already exist instead of redoing a step. An SDS job may start
from a finished SRS the user gives (.md, .docx, .pdf, also one made elsewhere): Step B reads its FR/NFR ids and
roles from it, and the SDS cites those ids unchanged.

Write the files into a folder the user names, else `./srs-sds-<ชื่อระบบสั้น>/`. Show each file to the user before
starting the next step when the job has more than one step, so they can correct requirements early.

## Inputs
1. Read every source the user gives (TOR .docx/.pdf/.md, brief, meeting notes). For .docx/.pdf use the tools you
   have (pandoc, pdftotext, a docx/pdf skill). Quote the TOR's item numbers exactly (e.g. 4.2.1.1).
2. No TOR: number the brief's lines yourself and say so in the documents ("ความต้องการ" instead of "ข้อ TOR").
3. Never invent a requirement. Guesses go in "สมมติฐานและคำถามถึงลูกค้า" (SRS section 7) and are listed to the user.

## Step A: SRS (working requirements)
Follow [references/srs.md](references/srs.md). One document, about 1,000 words: roles, FRs as user stories with
2–4 checkable acceptance criteria, data, state cycles, non-functional, out of scope, questions, TOR → FR table and
the "เรื่องพื้นฐาน" table.

## Step B: System design + schema
Follow [references/design.md](references/design.md); its input is `srs.md` or the SRS the user gave. `design.md` (architecture, modules, tables, API, rules,
workflows, security, roles) and `schema.sql` (PostgreSQL DDL with Thai COMMENT ON TABLE). Every FR lands in a module,
a table and an API row.

## Step C: Hand-in documents for the committee
Follow [references/handover.md](references/handover.md) (facts list, front matter, brand and logos), then the
layout for the document being written: `layouts/<layout>/srs-doc.md` for C-SRS, `layouts/<layout>/sds-doc.md` for
C-SDS, and that folder's examples. Only layout today: [contumeliax](layouts/contumeliax/srs-doc.md).

Brands live in `brands/<name>/` (brand.yaml with company details and colours, logo.png); today `contumeliax`.
Ask the user once which brand to use (or the company details if none fits), plus the contract number, author and
date if they want them on the cover; leave out what they do not know. A different logo for one project goes in
the front matter (`logo:`), the agency's emblem in `client_logo:`.

## Final check (every job)
- Every TOR item / brief line maps to at least one FR; every FR id cited later exists in the SRS.
- Every code (U-, M, FR-, NFR-, SCR-, TBL-, API-, ADR-, DC-) cited anywhere is defined once.
- Role names, screen names, table and column names are spelled the same in every file.
- Nothing invented: open questions are listed in the SRS and in your reply.
- Mermaid blocks parse (node ids in English letters, Thai only inside quotes).

## Word / PDF
When the user wants .docx or .pdf (or after Step C unless they said markdown only), convert each document with the
bundled scripts. `<skill-dir>` is this skill's folder; on Windows use `py` instead of `python3`.

1. Once per machine (later runs are quick), prepare and check the tools:
   ```
   python3 <skill-dir>/scripts/setup.py
   ```
   It installs what it can inside the skill folder (python-docx in `.venv`, mermaid-cli in `.tools`) and the bundled
   Sarabun font into the user's font folder when no Thai font is installed. For a MISSING line it cannot fix
   (Node.js, LibreOffice) it prints the install command: tell the user that command, and ask before running a
   package manager yourself. Continue with what works: .docx needs only the first line.
2. Convert each document:
   ```
   python3 <skill-dir>/scripts/md2docx.py srs-doc.md --pdf
   ```
   It writes `srs-doc.docx` (A4, numbered รูปภาพที่/ตารางที่ captions, mermaid rendered to images) and, with
   `--pdf`, `srs-doc.pdf` through LibreOffice with the table of contents filled in. A front matter block gives the
   cover, revision/approval/reference tables, contents, the header (logo, company, document code) and the footer
   (classification, "หน้า X จาก Y"); see handover.md section 2. Font: TH Sarabun New 16 when installed, else
   Sarabun 11 (same look); `--font "TH SarabunPSK"` switches it. Report what its stderr says was missing (a diagram
   left as text, an empty table of contents, no PDF) instead of hiding it. Word asks to update fields when the
   .docx opens: answering yes fills in the contents page numbers.

Screenshots: put PNGs in `screens/` and reference them as `![ชื่อหน้าจอ](screens/x.png)`; `[ภาพหน้าจอ: …]` lines
become grey boxes to paste into later. Logo files named in the front matter are paths relative to the markdown
file; a brand's own logo needs nothing.
