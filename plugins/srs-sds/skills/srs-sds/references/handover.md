# Step C: Hand-in documents (เอกสารส่งมอบ)

Customer documents for the acceptance committee, rewritten from `srs.md`, `design.md` and `schema.sql`; nothing
may be added, dropped or renamed. Two documents, each its own job:
- `srs-doc.md` (เอกสารข้อกำหนดความต้องการซอฟต์แวร์), from `srs.md` only.
- `sds-doc.md` (เอกสารการออกแบบสถาปัตยกรรมและการออกแบบซอฟต์แวร์), from `design.md`, `schema.sql` and the SRS (its FR
  and NFR ids feed the traceability chapter). The SRS may be this skill's `srs.md` or a finished SRS the user
  hands in (.md, .docx, .pdf): read its ids and role names from it.

The chapter structure and tone come from a layout: `layouts/<layout>/srs-doc.md` or `sds-doc.md`, plus the
examples in the same folder. The layout is the brand's `layout` key (brands/<brand>/brand.yaml), else the one
the user names, else ask; with one layout only, use it.

## 1. Build the facts list first
Before writing, list for yourself (not in the documents):
- TOR item numbers and the FR / NFR ids each maps to (SRS section 8).
- User groups with their codes U-01, U-02 … (ผู้ดูแลระบบ keeps its name as its code) and modules M01, M02 …
  with the short code used in FR ids (FR-BK-01 → module code BK).
- Screens SCR-01 …, tables TBL-01 … with their columns from `schema.sql`, APIs API-01 …, decisions ADR-01 …
- Company and project details for the cover. Ask the user once for what the sources do not give (company name
  and address, logo file, contract number, author, date); leave out what they do not know: the converter prints
  dotted lines or blank cells for the agency to fill in by hand. Never invent a contract number or a person's
  name.
Use these names and codes exactly in every document of the project.

Working files from an older run may lack some codes (no U-/NFR- ids in `srs.md`, no M/SCR/TBL/API/ADR codes or
screens table in `design.md`). Then assign the codes yourself in the facts list: a code is a label, not a rename,
so this does not break "nothing added or renamed". Keep FR ids exactly as `srs.md` has them (FR-01 stays FR-01).
Screens missing from `design.md`: derive one per user job from the FRs and APIs. Module names that differ
between `srs.md` and `design.md`: the SRS name wins. List every code and screen you assigned in your reply.

## 2. Front matter and brand
Start each file with a front matter block; the converter turns it into the cover, revision history, approval and
reference tables, the table of contents, the page header and the footer. Do not write those pages yourself.
`brand: <name>` fills in company name, address, contact, logo and colours from `brands/<name>/brand.yaml`
(list the folders in `brands/` to see the names). A key written in the document overrides the brand's value.
```
---
brand: contumeliax
title: เอกสารข้อกำหนดความต้องการซอฟต์แวร์
title_en: Software Requirements Specification (SRS)
project: <ชื่อโครงการตาม TOR>
contract: <เลขที่สัญญา>
client: <หน่วยงานผู้ว่าจ้าง>
doc_code: SRS-001
version: 1.0
date: <วัน เดือน ปี พ.ศ.>
author: <ผู้จัดทำ>
revision: จัดทำเอกสารข้อกำหนดความต้องการซอฟต์แวร์
ref: TOR | ขอบเขตของงาน (TOR) <ชื่อโครงการ> | - | <วันที่>
note: เอกสารฉบับนี้เมื่อได้รับการลงนามรับรองแล้วจะถูกตรึงเป็น Requirement Baseline การเปลี่ยนแปลงหลังจากนั้นต้องผ่านกระบวนการควบคุมการเปลี่ยนแปลง
---
```
SDS: `title: เอกสารการออกแบบสถาปัตยกรรมและการออกแบบซอฟต์แวร์`, `title_en: System Architecture & Software
Design Document (SDD)`, `doc_code: SDD-001`, a `ref:` line for the SRS, no `note`. Omit a key you do not know.

Without a brand, or for another company, write the company keys yourself: `company`, `company_en`, `address`,
`contact`, `logo`. Logos (PNG or JPEG, paths relative to the markdown file):
- `logo:` the company logo on the cover and in the header; overrides the brand's logo (a project or a sister
  company's logo).
- `header_logo:` a different, smaller logo for the page header only.
- `client_logo:` the agency's emblem, placed beside the company logo on the cover.
The converter fits each logo in its box (cover 6.6 × 2.5 cm, header 4 × 1 cm) and reports a missing file.

## 3. Markdown the converter reads
- `#` to `###` headings, `- ` lists, pipe tables with a `|---|` row, mermaid blocks, images, caption lines, the
  front matter. No bold, HTML, inline code, footnotes. A literal "|" inside a table cell is written `\|`
  (mode=partial\|full).
- Mermaid: node ids in English letters, Thai text only inside quotes: `user["เจ้าหน้าที่"]`; `erDiagram` with
  English table/column names from the schema.
- Captions: a line starting `ภาพ: ` right after a diagram or image (numbered รูปภาพที่ N), a line starting
  `ตาราง: ` right before a table that needs a name (numbered ตารางที่ N). Never type the numbers yourself.

## Checklist (every hand-in document)
- Front matter present; no cover, revision, approval or contents pages written by hand.
- Every role, module, screen, table, column and API name matches the facts list; codes (U-, M, FR-, NFR-, SCR-,
  TBL-, API-, ADR-, DC-) are unique and every code cited somewhere is defined somewhere.
- Every image/diagram has a `ภาพ:` line after it.
- The layout's own checklist passes.
