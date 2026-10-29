# Layout contumeliax: คู่มือการใช้งาน (User Manual)

The style Thai agencies receive: a plain bordered cover, contents, chapters as coloured bars, numbered steps,
a framed screenshot under every step with a short "หน้าจอ…" caption. Read [examples-manual.md](examples-manual.md)
for the tone; write with this system's own labels, never copy the examples.

## Front matter
```
---
brand: contumeliax
cover: manual
title: คู่มือการใช้งาน (User Manual)
system: <ชื่อระบบภาษาไทย>
system_en: (<ชื่อระบบภาษาอังกฤษ>)
version: 1.0
date: <เดือน ปี พ.ศ.>
---
```
Leave out `version` or `date` when the user has not given them (the cover then shows neither). Add
`prepared_by:` when the cover's "จัดทำโดย" is not the brand's company (e.g. the agency's IT office),
`client_logo:` for the agency's emblem beside the company logo, `title: คู่มือสำหรับผู้ดูแลระบบ (Administrator
Manual)` for an admin book. Do not write the cover or contents yourself.

## Chapters
- `# 1. ข้อมูลทั่วไปของระบบ` with `## 1.1 การเข้าสู่ระบบ` (who can sign in, the URL, what to enter, the button),
  `## 1.2 หน้าหลัก` (the parts of the main screen as a list: "ทางด้านซ้ายมือ จะแสดง…"), `## 1.3 การออกจากระบบ`.
  Add `## ความต้องการของระบบ` (browsers, screen size) only when the sources state it.
- One `# n. การ<ทำอะไร>` per task, in the order a user meets them. Open with one sentence: "ผู้ใช้งานสามารถ<…>
  โดยดำเนินการตามขั้นตอนต่อไปนี้". When the task has variants, say how many ("สามารถดำเนินการได้ 2 กรณี ดังนี้")
  and give each its section `## n.1 กรณี<…>`.
- Admin tasks (users, roles, master data, settings) as their own chapters after the user tasks, or a separate
  manual.
- An optional last chapter `# n. ปัญหาที่พบบ่อยและวิธีแก้ไข` with `| ปัญหา / ข้อความที่พบ | สาเหตุ | วิธีแก้ไข |`,
  from the error messages the sources list.

## Steps
- A step is a plain paragraph starting with its number: `2.1 เข้าเมนู “จองห้องประชุม”` in a chapter without
  sections, `3.1.2 …` inside section 3.1. Steps are not headings (the contents lists chapters and sections only).
- One step, one thing: a user action ("คลิกปุ่ม “ยืนยัน”", "ระบุ PIN ใหม่") or what the system does ("ระบบจะแสดง
  หน้าจอ…", "ระบบแสดงข้อความ “…”", "ระบบส่งอีเมลแจ้ง…"). Begin later steps with "จากนั้น" where it reads naturally.
- Labels as the screen shows them, in “ ” quotes and bold: คลิกปุ่ม **“ขอใบรับรอง”**, เมนู **“ตั้งค่า”**.
- Under a step that shows a screen: the image (with boxes on what the step clicks or fills), then the caption
  `ภาพ: หน้าจอ<ชื่อหน้าจอ>`; an email or a form uses `ภาพ: ภาพอีเมล…` / `ภาพ: ภาพตัวอย่างแบบฟอร์ม…`.
- Field rules from the SRS go in the step as a note: "(หมายเหตุ : PIN ใช้ตัวอักษร ตัวเลข และอักขระพิเศษ ยาว 6 ถึง
  12 ตัวอักษร)".
- A screen with several outputs or fields to explain: a lead-in ending "ดังนี้", then a list
  `- **ชื่อช่อง** คือ <ความหมาย>`; allowed values each in quotes with their meaning.
- Things the user prepares beforehand (files, size limits, file-name patterns) as a list after "ต้องเตรียมข้อมูล
  ดังนี้", with the exact limits.
- Status marks and what changes after a step ("เมนู … จะเปลี่ยนเป็น …") are said in the step that causes them.
- Rejection, error and timeout paths get their own steps: "ในกรณีที่คำขอถูกปฏิเสธ ระบบจะแสดง…".

## Style
- Polite instructional Thai, second person implied: "ให้คลิก…", "ระบุ…", "จากนั้นคลิก…". Call the reader
  "ผู้ใช้งาน" (or the role name). No requirement language ("ระบบต้อง…") and no internal codes (SCR-, FR-, API).
- Short steps; a paragraph of explanation only where the screen needs it (the main screen's parts, a result).
- Markdown the converter reads: `#`/`##` headings with numbers, paragraphs, `- ` lists, pipe tables, images with
  `{box=…}`, `[ภาพหน้าจอ: …]`, `ภาพ:` caption lines, **bold** for labels. No HTML, no inline code.

## Checklist
- Front matter has `cover: manual`, `system`, and a brand or company keys.
- Chapters in user order; every task from the outline present; sign-in, main screen and sign-out in chapter 1.
- Every step numbered in sequence within its chapter or section; every screen step has an image or placeholder
  and a `ภาพ:` caption; clicked controls boxed.
- Every label matches the screens; every rule and limit matches the SRS numbers.
