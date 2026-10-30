# Layout contumeliax: คู่มือการใช้งาน (User Manual)

The same contractor hand-in form as the project's SRS and SDS (srs-sds layout contumeliax): the company cover
with the project table, revision history, approval and reference tables, contents, a header with the logo and
document code, a footer with the classification and "หน้า X จาก Y", numbered chapters in Thai with the English
name in brackets. Inside the task chapters it reads as a manual: numbered steps and a framed screenshot under
every step. Read [examples-manual.md](examples-manual.md) for the tone; write with this system's own labels,
never copy the examples.

## Front matter
```
---
brand: contumeliax
cover: manual
title: คู่มือการใช้งาน
title_en: User Manual
system: <ชื่อระบบภาษาไทย>
system_en: <ชื่อระบบภาษาอังกฤษ>
project: <ชื่อโครงการตาม TOR, ตรงกับปก SRS>
contract: <เลขที่สัญญา>
client: <หน่วยงานผู้ว่าจ้าง>
doc_code: UM-001
version: 1.0
date: <วัน เดือน ปี พ.ศ.>
author: <ผู้จัดทำ>
revision: จัดทำคู่มือการใช้งาน
ref: SRS-001 | เอกสารข้อกำหนดความต้องการซอฟต์แวร์ (SRS) | 1.0 | <วันที่>
ref: SDD-001 | เอกสารการออกแบบสถาปัตยกรรมและการออกแบบซอฟต์แวร์ (SDD) | 1.0 | <วันที่>
---
```
Take `project`, `contract`, `client` and the `ref` lines' codes, versions and dates from the SRS/SDS front
matter or cover, so the three documents name the project the same way; add a `ref:` for a UAT document when
there is one. Omit a key nobody knows (the converter prints dotted lines or blank cells for the agency to fill
in); never invent a contract number or a person's name. An admin book: `title: คู่มือสำหรับผู้ดูแลระบบ`,
`title_en: Administrator Manual`, `doc_code: UM-002`. Logos (PNG or JPEG, paths relative to the markdown file):
`logo:` replaces the brand's logo on the cover and in the header, `header_logo:` puts a different, smaller logo
in the header only, `client_logo:` adds the agency's emblem beside the company logo on the cover. Do not write the cover, history, approval, reference or contents pages yourself.

## Chapters
1. `# 1. บทนำ (Introduction)`
   - `## 1.1 วัตถุประสงค์ของเอกสาร (Purpose)`: one paragraph naming the system, the project and the agency, that
     this manual explains how <กลุ่มผู้ใช้> use the system step by step according to the SRS (name its code,
     "เอกสารข้อกำหนดความต้องการซอฟต์แวร์ (SRS-001)"), ending "ทั้งนี้เพื่อวัตถุประสงค์ดังต่อไปนี้", then a list
     (a guide for users to work in the system correctly, a reference for training, a reference for the
     acceptance committee and the UAT).
   - `## 1.2 ขอบเขตของคู่มือ (Scope)`: "ชื่อระบบ:" line, then "คู่มือฉบับนี้ครอบคลุมการใช้งาน ดังนี้" and
     `| ลำดับ | งาน / เมนู | รายละเอียด | บทที่ |`, one row per task chapter (บทที่ as "3"), the detail cell a
     short phrase of what the reader does there.
   - `## 1.3 กลุ่มผู้ใช้งาน (User Classes)`: a lead-in, then `| รหัส | กลุ่มผู้ใช้งาน | งานที่ใช้คู่มือนี้ |` with
     the SRS role codes and names exactly (U-01 …, ผู้ดูแลระบบ), only the roles this book is for.
   - `## 1.4 สภาพแวดล้อมการใช้งาน (Operating Environment)`: `| องค์ประกอบ | ข้อกำหนด |` (browser, screen size,
     network or VPN, sign-in method) from SRS 2.4; drop the section when the sources state nothing.
2. `# 2. ข้อมูลทั่วไปของระบบ (General Information)` with `## 2.1 การเข้าสู่ระบบ (Sign In)` (who can sign in, the
   URL, what to enter, the button), `## 2.2 หน้าหลัก (Main Screen)` (the parts of the main screen as a list:
   "ทางด้านซ้ายมือ จะแสดง…"), `## 2.3 การออกจากระบบ (Sign Out)`.
3. One `# n. การ<ทำอะไร> (<English>)` per task from chapter 3 on, in the order a user meets them. Open with one
   sentence: "ผู้ใช้งานสามารถ<…> โดยดำเนินการตามขั้นตอนต่อไปนี้". When the task has variants, say how many
   ("สามารถดำเนินการได้ 2 กรณี ดังนี้") and give each its section `## n.1 กรณี<…>` (English name optional on
   sections below chapter level).
4. Admin tasks (users, roles, master data, settings) as their own chapters after the user tasks, or a separate
   manual.
5. Optional `# n. ปัญหาที่พบบ่อยและวิธีแก้ไข (Troubleshooting)` with `| ปัญหา / ข้อความที่พบ | สาเหตุ | วิธีแก้ไข |`,
   from the error messages the sources list.
6. `# ภาคผนวก ก: อภิธานศัพท์ (Glossary)`: `| คำศัพท์ / คำย่อ | คำอธิบาย |`, the terms and abbreviations the reader
   meets in this manual (screen words, statuses, SSO …), written as in the SRS glossary ("SSO | Single Sign-On -
   การลงชื่อเข้าใช้ครั้งเดียว…"); reuse the SRS's wording for terms it already defines.

Number the chapters and sections you keep in sequence: a dropped one gives its number to the next.

## Headings
Chapter (`#`) headings carry their number and an English name in brackets, as in the SRS: `# 3. การจองห้อง
ประชุม (Room Booking)`. Chapter 1's sections carry English names too (`## 1.1 วัตถุประสงค์ของเอกสาร (Purpose)`);
task sections may (`## 3.1 กรณีการจองที่ยังไม่ได้รับการอนุมัติ`). The appendix heading has no number.

## Steps
- A step is a plain paragraph starting with its number: `3.1 เข้าเมนู “จองห้องประชุม”` in a chapter without
  sections, `4.1.2 …` inside section 4.1. Steps are not headings (the contents lists chapters and sections only).
- One step, one thing: a user action ("คลิกปุ่ม “ยืนยัน”", "ระบุ PIN ใหม่") or what the system does ("ระบบจะแสดง
  หน้าจอ…", "ระบบแสดงข้อความ “…”", "ระบบส่งอีเมลแจ้ง…"). Begin later steps with "จากนั้น" where it reads naturally.
- Labels as the screen shows them, in “ ” quotes and bold: คลิกปุ่ม **“ขอใบรับรอง”**, เมนู **“ตั้งค่า”**.
- Under a step that shows a screen: the image (with boxes on what the step clicks or fills), then the caption
  `ภาพ: หน้าจอ<ชื่อหน้าจอ>` (numbered รูปภาพที่ N by the converter, as in the SRS/SDS; never type the number); an
  email or a form uses `ภาพ: ภาพอีเมล…` / `ภาพ: ภาพตัวอย่างแบบฟอร์ม…`.
- Field rules from the SRS go in the step as a note: "(หมายเหตุ : PIN ใช้ตัวอักษร ตัวเลข และอักขระพิเศษ ยาว 6 ถึง
  12 ตัวอักษร)".
- A screen with several outputs or fields to explain: a lead-in ending "ดังนี้", then a list
  `- **ชื่อช่อง** คือ <ความหมาย>`; allowed values each in quotes with their meaning. Many fields: a table
  `| ชื่อช่อง | ความหมาย | กติกา |` with a `ตาราง:` caption line before it.
- Things the user prepares beforehand (files, size limits, file-name patterns) as a list after "ต้องเตรียมข้อมูล
  ดังนี้", with the exact limits.
- Status marks and what changes after a step ("เมนู … จะเปลี่ยนเป็น …") are said in the step that causes them.
- Rejection, error and timeout paths get their own steps: "ในกรณีที่คำขอถูกปฏิเสธ ระบบจะแสดง…".

## Style
- Chapter 1 and the appendix in the SRS's formal tone, mostly tables, the English term in brackets the first
  time; call the customer by its TOR name or "หน่วยงาน", the contractor "ผู้พัฒนาระบบ".
- Task chapters in polite instructional Thai, second person implied: "ให้คลิก…", "ระบุ…", "จากนั้นคลิก…". Call
  the reader "ผู้ใช้งาน" (or the role name). No requirement language ("ระบบต้อง…") and no internal codes (SCR-,
  FR-, API-); role codes appear only in table 1.3.
- Short steps; a paragraph of explanation only where the screen needs it (the main screen's parts, a result).
- Markdown the converter reads: `#`/`##` headings with numbers, paragraphs, `- ` lists, pipe tables, images with
  `{box=…}`, `[ภาพหน้าจอ: …]`, `ภาพ:` caption lines after a figure, `ตาราง:` caption lines before a table,
  **bold** for labels in steps. No HTML, no inline code.

## Checklist
- Front matter has `cover: manual`, `system`, `doc_code`, a brand or company keys, and project/client/refs that
  match the SRS cover.
- Chapter 1 has Purpose, Scope and User Classes; the scope table lists every task chapter with its number; role
  codes and names match the SRS.
- Chapters in user order; every task from the outline present; sign-in, main screen and sign-out in chapter 2.
- Every step numbered in sequence within its chapter or section; every screen step has an image or placeholder
  and a `ภาพ:` caption; clicked controls boxed.
- Every label matches the screens; every rule and limit matches the SRS numbers.
- The glossary appendix is last and defines every abbreviation the manual uses.
