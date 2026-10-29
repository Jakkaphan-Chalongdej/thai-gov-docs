---
name: uat-doc
description: เขียนเอกสารทดสอบการยอมรับระบบ (User Acceptance Test: UAT) ภาษาไทยแบบที่ผู้รับจ้างส่งมอบหน่วยงานรัฐ จาก SRS/SDS คู่มือการใช้งาน ต้นแบบหน้าจอ หรือระบบที่รันอยู่ ได้แก่ ปก UAT Documents ประวัติการแก้ไขและประวัติการทดสอบ บทนำ (Purpose, Test Execution, Test Scope) และตารางกรณีทดสอบรายฟังก์ชัน (No, Function, Menu, Test Description พร้อมภาพหน้าจอในตาราง, Result ช่องติ๊กผ่าน/ไม่ผ่าน, Remark) ออกเป็น Word/PDF ใช้เมื่อผู้ใช้ขอเอกสาร UAT, User Acceptance Test, แบบทดสอบการยอมรับระบบ, test script/test case สำหรับตรวจรับ หรือเอกสารทดสอบรายเมนู
---
# UAT documents for Thai government systems

Writes the User Acceptance Test document the agency's testers fill in during acceptance: a cover, revision and
test history, an introduction with the pass/fail rule and the scope, then one table of test cases per function,
each case describing what the tester does and what the screen must show, with a screenshot of the expected screen
and ผ่าน / ไม่ผ่าน check boxes. Output is markdown converted to Word/PDF.

## 1. Sources and facts
Read every source the user gives: SRS/SDS (this plugin family's `srs.md`, `srs-doc.md`, `design.md`,
`sds-doc.md`, or any .docx/.pdf), a user manual, a prototype, a running system (URL), screenshots, notes, an
earlier UAT document to follow. Then list for yourself:
- The scope: which menus or modules this document covers. The usual unit is one document per menu or module
  ("(Admin Overview)", "(Web Portal)"); ask when the user has not said, and propose one per module.
- Per function in scope: the menu path, the screens (SDS SCR-…), what each screen displays, its fields with their
  rules (required, format, length: copy the SRS numbers exactly), its buttons, its messages, the roles that may
  use it, the status changes, and the FR ids and acceptance criteria it covers.
- Labels exactly as the screens show them; when the SRS/SDS words a label differently from the screen, the
  screen wins and you tell the user. Never invent a menu, field, button, message or displayed item: anything you
  cannot confirm is a question to the user, and a test case states only what is confirmed.

## 2. Test cases
Follow [references/test-cases.md](references/test-cases.md): derive the cases from the acceptance criteria and the
screens (display, each action, validation, permission, status), number them, and write each in the narrative
style of the layout. Propose the list of functions and cases to the user before writing the document when there
are more than about ten cases, so wrong or missing cases are caught early.

## 3. Screenshots
Follow [references/screenshots.md](references/screenshots.md): use the user's images when they exist, capture
them from a running test system when a browser tool and a test account are available, otherwise leave
`[ภาพหน้าจอ: …]` placeholders and hand the user the screenshot list. Each image shows the screen as it must look
when the case passes.

## 4. Write the document
Follow the layout `layouts/<layout>/uat.md` and its examples (only [standard](layouts/standard/uat.md) today,
the style of the agency sample "เมนู Admin Overview"). Save as `uat-<เมนูหรือโมดูล>.md` in a folder the user names,
else `./uat-<ชื่อระบบสั้น>/`, with images in `screens/` beside it. Ask once for what the cover needs and the
sources do not give (the system's English name, who prepared it, the date, the version); leave out what the user
does not know.

## 5. Word / PDF
Convert with the bundled scripts (`<skill-dir>` is this skill's folder; on Windows use `py`):
```
python3 <skill-dir>/scripts/setup.py                       # once per machine; prints what is missing
python3 <skill-dir>/scripts/md2docx.py uat-admin.md --size 14 --pdf
```
`--size 14` matches the agency sample (TH Sarabun 14 pt). The front matter (`cover: uat` …) gives the cover,
contents, Revision History and Test History tables and the page numbers. In table cells, `<br>` separates lines,
`- ` lines are dash items, `[ ]` becomes a Word check box, and image or `[ภาพหน้าจอ: …]` lines are printed inside the
cell. Report what stderr says was missing (an image not found, an empty contents page, no PDF) instead of hiding
it. Brands (`brand: <name>`, `brands/<name>/`) add a logo and the company line to the cover only when the user
wants them; the sample style has none.

## Final check
- Every function in the scope table has its own section and at least one test case; every case is numbered in
  sequence within its function and has ผ่าน / ไม่ผ่าน boxes.
- Every acceptance criterion of the FRs in scope is covered by a case (chapter 3 when the source is an SRS).
- Menu, field, button, message and displayed-item labels match the screens and the SRS/SDS exactly; rules carry
  the SRS numbers.
- Every case that shows a screen has an image or a placeholder inside its Test Description cell.
- Open questions and missing screenshots are listed in your reply.
