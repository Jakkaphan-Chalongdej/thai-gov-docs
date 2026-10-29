# Layout standard: เอกสาร UAT (User Acceptance Test Documents)

The style of the agency sample "เมนู Admin Overview": an English title block on the cover, English chapter and
table headings, Thai body text, and one six-column test table per function with the expected screen inside the
Test Description cell. Read [examples-uat.md](examples-uat.md) for the tone; write with this system's own
labels, never copy the examples.

## Front matter
```
---
cover: uat
title: User Acceptance Test Documents
system: <ชื่อระบบภาษาอังกฤษ ตามที่หน่วยงานใช้>
subtitle: (<เมนูหรือโมดูลที่ทดสอบ>)
author: <ผู้จัดทำ>
date: <วว/ดด/ปปปป ตามที่ผู้ใช้ให้>
version: 0.1
revision: จัดทำเอกสาร UAT
test_rows: 4
---
```
The cover prints title, "for", system and subtitle right-aligned; the converter then adds the contents, the
Revision History table (author, date, revision, version) and a blank Test History table with `test_rows` lines
for the testers. Leave out `author`, `date` or `version` when the user has not given them (the cells stay blank
for handwriting). Add `brand:` (logo and company on the cover) only when the user asks for it. Do not write the
cover, contents or history tables yourself.

## Chapters
1. `# 1. Introduction`
   - `## 1.1 Purpose`: one paragraph, the standard wording adapted to the system: "วัตถุประสงค์ของการทดสอบระบบ
     เพื่อตรวจสอบว่าระบบที่พัฒนาขึ้นสามารถทำงานตรงตามความต้องการที่ระบุในเอกสารกำหนดความต้องการ และเพื่อตรวจสอบ
     ความน่าจะเป็นของการเกิดข้อผิดพลาดที่เกิดขึ้นภายในระบบ และรายงานจำนวนข้อผิดพลาดที่พบให้มากที่สุดเท่าที่จะเป็นไปได้
     เพื่อใช้สำหรับการปรับปรุงแก้ไขระบบให้มีประสิทธิภาพยิ่งขึ้นก่อนนำไปใช้งานจริง" Name the SRS document when there
     is one ("ตามที่ระบุในเอกสารข้อกำหนดความต้องการซอฟต์แวร์ (SRS-001)").
   - `## 1.2 Test Execution`: one paragraph, the pass/fail rule: the actual result is compared with the expected
     result; matching means ผ่านการทดสอบ (Pass), not matching means ไม่ผ่านการทดสอบ (Fail) and a defect exists.
     Add the roles and test environment (UAT) the sources name, one sentence.
   - `## 1.3 Test Scope`: "ขอบเขตของการทดสอบการใช้ระบบ <เมนู/โมดูล> ครอบคลุมฟังก์ชันและคุณลักษณะ ดังนี้", then
     `| No. | Function | Detail for System |`, one row per function of chapter 2; the detail cell is a dash
     list (`- การแสดงผลเมนู …<br>- การค้นหา …`).
2. `# 2. User Acceptance Test`
   - Per function `## 2.n <Function>` (the same names as the scope table), then the table
     `| No | Function | Menu | Test Description | Result | Remark |`, one row per test case (see
     [../../references/test-cases.md](../../references/test-cases.md)).
   - Test Description cell, lines joined by `<br>`: `n.<ชื่อกรณีทดสอบ>`, the narrative sentence ending "ดังภาพ"
     when a screen follows, the image line or `[ภาพหน้าจอ: <ชื่อหน้าจอ>]`, a lead-in ending "ดังนี้", then the
     displayed items or checks as `- ` lines.
   - Result cell: `[ ] ผ่าน<br>[ ] ไม่ผ่าน`. Remark cell: empty.
3. `# 3. Requirement Traceability` (only when the cases come from an SRS): "กรณีทดสอบในเอกสารนี้ครอบคลุมความต้องการ
   ดังนี้", then `| FR | Acceptance Criteria | Function | Test Case |` (Test Case as "2.1 ข้อ 1"), every
   acceptance criterion of the FRs in scope. Criteria tested elsewhere (Operational, Security) are listed with
   that test's name in the Test Case cell.

## Markdown the converter reads
`#`/`##` headings with their numbers, paragraphs, `- ` lists, pipe tables (one row per line; inside a cell
`<br>` breaks lines, `- ` starts a dash item, `[ ]` is a check box, an image line or placeholder is printed at
the cell's width), images with `{box=…}`. No other HTML, no bold inside cells, no inline code, no `ภาพ:` captions
(the sample has none).

## Style
- English for headings and table headers as in the sample; Thai for every sentence the tester reads.
- The tester is "ผู้ใช้งาน"; sentences say what to do and what the system shows: "ให้เลือกเมนู “…” จากนั้นระบบจะ
  ปรากฏ…". Labels in “ ” quotes exactly as on the screen.
- No requirement language ("ระบบต้อง…") inside test descriptions and no internal codes (SCR-, API-) outside
  chapter 3.

## Checklist
- Front matter has `cover: uat`, `system` and `subtitle`.
- Scope table rows and chapter 2 sections are the same functions in the same order.
- Every row has No, Function, Menu, a numbered Test Description and the two check boxes.
- Chapter 3 present and complete when the source is an SRS.
