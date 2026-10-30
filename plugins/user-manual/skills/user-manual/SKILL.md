---
name: user-manual
description: เขียนคู่มือการใช้งานระบบ (User Manual) ภาษาไทยแบบที่หน่วยงานรัฐใช้ส่งมอบ จาก SRS/SDS ต้นแบบหน้าจอ ระบบที่รันอยู่ หรือภาพหน้าจอที่มี เขียนเป็นบทตามงานของผู้ใช้ ขั้นตอนมีเลขกำกับ ภาพหน้าจอทุกขั้นพร้อมกรอบสีแดงเน้นจุดที่ต้องคลิก ในรูปแบบเอกสารส่งมอบชุดเดียวกับ SRS/SDS (ปกบริษัทพร้อมตารางโครงการ ประวัติการแก้ไข ตารางอนุมัติ เอกสารอ้างอิง สารบัญ บทนำ อภิธานศัพท์ หัว/ท้ายกระดาษตามแบรนด์ โลโก้เปลี่ยนได้) ออกเป็น Word/PDF ใช้เมื่อผู้ใช้ขอคู่มือการใช้งาน คู่มือผู้ใช้ คู่มือผู้ดูแลระบบ user manual หรือเอกสารส่งมอบประเภทคู่มือ
---
# User manual for Thai government systems

Writes the คู่มือการใช้งาน an agency receives with a system: one chapter per thing a user does, numbered steps
in the order the user meets the screens, and a screenshot after every step with the control to click boxed in
red. It is handed in with the SRS/SDS and the UAT, so it has their form: the company cover with the project
table, revision history, approval and reference tables, contents, an introduction (purpose, scope, user
classes) and a glossary. Output is markdown converted to Word/PDF with the brand's cover, header and footer.

## 1. Sources and facts
Read every source the user gives: SRS/SDS (this plugin family's `srs-doc.md` / `sds-doc.md`, or any .docx/.pdf),
a prototype, a running system (URL), existing screenshots, notes. Then list for yourself:
- Audiences: the roles (ผู้ใช้งาน, เจ้าหน้าที่, ผู้อนุมัติ, ผู้ดูแลระบบ …) and the tasks each does. From an SRS: the
  FRs and use cases; from an SDS: the screen list (SCR-…) with menus, fields, buttons, rules and messages.
- Per task: the menu path, every screen in order, each field with its rule (required, format, length: copy the
  SRS numbers exactly, e.g. PIN 6–12 ตัวอักษร), each button label, each system message, status changes, emails
  or notifications sent, and the alternative paths (rejected, cancelled, forgotten password).
- Use the labels exactly as the screens show them; when the brief or the SRS words a name differently (the
  system's own name, a menu), the screen wins and you tell the user about the difference. Never invent a menu,
  field, button or message: anything you cannot confirm goes to the user as a question, and the manual says only
  what is confirmed. A label you cannot read is described without quotes ("คลิกปุ่มขออนุมัติที่มุมขวาล่าง") and
  listed as a question.
- A task the sources name but show no screens for (an admin approving, done in another system) is written from
  what the reader sees of it (status changes, emails) in the reader's manual, and listed to the user as a gap;
  never make up its screens.
- From the SRS/SDS cover and chapters, for chapter 1 and the front matter: the project name, contract number,
  agency, the documents' codes, versions and dates (SRS-001, SDD-001, a UAT), the role codes and names (SRS
  2.2), the operating environment (SRS 2.4) and the glossary terms. Without an SRS, ask once for what the cover
  needs (project, agency, contract, author, date, version) and leave out what the user does not know.
- The sign-in URL is the one the user types; when it leads to a central sign-in page (SSO), say so in the
  sign-in step ("ระบบจะพาไปยังหน้าลงชื่อเข้าใช้ของ …").

## 2. Outline first
Propose the outline and get the user's OK before writing:
- One manual per audience when the roles see different menus (คู่มือสำหรับผู้ใช้งาน, คู่มือสำหรับผู้ดูแลระบบ),
  unless the user wants one book; then the admin tasks come last as their own chapters.
- Chapter 1 บทนำ (purpose, scope table of the task chapters, user classes, operating environment), chapter 2
  ข้อมูลทั่วไปของระบบ (sign-in, the main screen and its parts, sign-out), then one chapter per task in the order a
  user meets them (register before use, set before change), each with its alternative cases, and the glossary
  appendix last.
- The screenshot list: `screens/<nn>-<slug>.png` per step, what state the screen must be in, which control to box.

## 3. Screenshots
Follow [references/screenshots.md](references/screenshots.md): use the user's images when they exist, capture
them from the running system when a browser tool and a test account are available, otherwise leave
`[ภาพหน้าจอ: …]` placeholders and hand the user the screenshot list.

## 4. Write the manual
Follow the layout: `layouts/<layout>/manual.md` and its examples (the brand's `layout` key, else the one the user
names; only [contumeliax](layouts/contumeliax/manual.md) today). Save as `manual.md` (or `manual-<audience>.md`)
in a folder the user names, else `./manual-<ชื่อระบบสั้น>/`, with the images in `screens/` beside it.

## 5. Word / PDF
Convert with the bundled scripts (`<skill-dir>` is this skill's folder; on Windows use `py`):
```
python3 <skill-dir>/scripts/setup.py          # once per machine: python-docx, Pillow, fonts; prints what is missing
python3 <skill-dir>/scripts/md2docx.py manual.md --pdf
```
The front matter (`cover: manual`, `brand:` …) gives the SRS-style cover with the project table, revision
history, approval and reference tables, contents, the header with logo and document code, and the footer with
"หน้า X จาก Y"; `cover_style: bordered` gives the older bordered manual cover with chapter bars instead; boxes written after an image line are drawn on the picture. Report what stderr says
was missing (an image not found, boxes not drawn, an empty contents page, no PDF) instead of hiding it.
Brands live in `brands/<name>/` (company details, logo, colours); a different logo for one manual goes in the
front matter (`logo:`), the agency's emblem in `client_logo:`.

## Final check
- Chapter 1 (purpose, scope, user classes) and the glossary appendix are present; project, agency, document
  references and role names match the SRS.
- Every task of the outline is a chapter; every step has one action or one system response, and a screenshot or
  a placeholder with a caption.
- Menu, field, button and message labels match the screens and the SRS/SDS exactly; field rules carry the SRS
  numbers.
- Every alternative path the sources mention (rejected, cancelled, forgotten) is written.
- Open questions and missing screenshots are listed in your reply.
