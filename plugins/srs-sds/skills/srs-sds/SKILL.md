---
name: srs-sds
description: เขียนเอกสาร SRS และ SDS ภาษาไทยแบบหน่วยงานรัฐจาก TOR หรือบรีฟ ได้แก่ ความต้องการพร้อม acceptance criteria, เอกสารออกแบบระบบกับ schema PostgreSQL และเอกสารส่งมอบ SRS/SDS (ตารางสืบย้อน TOR→URS→SRS→FR, use case, หน้าจอ, พจนานุกรมข้อมูล, แผนภาพ mermaid) ใช้เมื่อผู้ใช้ขอ SRS, SDS, เอกสารความต้องการ, เอกสารออกแบบระบบ, ตารางสืบย้อน TOR หรือเอกสารส่งมอบให้คณะกรรมการตรวจรับ
---
# SRS / SDS for Thai government software projects

Turns a TOR (ขอบเขตของงาน) or a short brief into the requirement and design documents a Thai agency's acceptance
committee expects. Written from the AI Factory pipeline (BA → Architect → Doc agents), packaged to run alone.

## Pick the job from the request

| The user asks for | Do | Output files |
|---|---|---|
| SRS / ความต้องการ / user stories | Step A | `srs.md` |
| ออกแบบระบบ / architecture / schema | Step B (needs an SRS: run A first if there is none) | `design.md`, `schema.sql` |
| เอกสารส่งมอบ SRS/SDS / เอกสารตรวจรับ | Steps A → B → C (reuse files that already exist) | `srs-doc.md`, `sds-doc.md` |
| "ทำ SRS SDS ให้ครบ" | A → B → C | all of the above |

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
Follow [references/design.md](references/design.md). `design.md` (architecture, modules, tables, API, rules,
workflows, security, roles) and `schema.sql` (PostgreSQL DDL with Thai COMMENT ON TABLE). Every FR lands in a module,
a table and an API row.

## Step C: Hand-in documents for the committee
Follow [references/handover.md](references/handover.md), then read the style examples before writing:
[references/examples-srs.md](references/examples-srs.md) and [references/examples-sds.md](references/examples-sds.md).
Build the facts list first (TOR items, FR ids, roles, screens and their fields, tables and their columns) from the
files of steps A–B, and use those names exactly in both documents.

## Final check (every job)
- Every TOR item / brief line maps to at least one FR; every FR id cited later exists in the SRS.
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
   It writes `srs-doc.docx` (A4, page numbers, numbered ภาพที่/ตารางที่ captions, mermaid rendered to images) and,
   with `--pdf`, `srs-doc.pdf` through LibreOffice. Font: TH Sarabun New 16 when installed, else Sarabun 11 (same
   look); `--font "TH SarabunPSK"` switches it. Report what its stderr says was missing (a diagram left as text, no
   PDF) instead of hiding it.

Screenshots: put PNGs in `screens/` and reference them as `![ชื่อหน้าจอ](screens/x.png)`; `[ภาพหน้าจอ: …]` lines
become grey boxes to paste into later.
