# Layout standard: ขอบเขตของงาน (TOR) for an IT project

The flat shape of a signed ministry TOR: a title block on page 1, numbered sections 1–17 in the body (printed
๑.–๑๗.), appendices after. Read [examples-tor.md](examples-tor.md) for the tone; write with this project's own facts.

## Front matter
```
---
cover: tor
title: (ร่าง) ขอบเขตของงาน (Terms of Reference: TOR)
project: <โครงการ…>
client: <ชื่อเต็มของหน่วยงาน>
fiscal_year: <พ.ศ.>
logo: <ตราหน่วยงาน.png>          # optional
thai_digits: yes                  # no for Arabic digits
committee: <ชื่อ> | ประธานกรรมการ
committee: <ชื่อ> | กรรมการ
committee: <ชื่อ> | กรรมการและเลขานุการ
---
```
Names unknown: write `committee: | ประธานกรรมการ` (the line stays blank to sign). A large TOR with a contents page:
add `toc: yes`. Write numbers with Arabic digits in the markdown; `thai_digits: yes` converts them.

## Sections
Each `# n. <หัวข้อ>`; sub-items as paragraphs starting with their number (`6.4.1 …`), not headings, except the
scope's work streams, which are `## 6.n <หัวข้อ>` so they show in a contents page.
1. หลักการและเหตุผล — the agency's current situation, the problem with numbers, why the system is needed;
   two or three paragraphs.
2. วัตถุประสงค์ — items each starting "เพื่อ…".
3. คำจำกัดความ — ผู้ว่าจ้าง, ผู้ยื่นข้อเสนอ, ผู้รับจ้าง, คณะกรรมการตรวจรับพัสดุ, ระบบ, plus terms of this project:
   "3.1 ผู้ว่าจ้าง หมายถึง <หน่วยงาน>".
4. คุณสมบัติผู้ยื่นข้อเสนอ — clauses.md.
5. ข้อกำหนดทั่วไป — clauses.md, plus the project's general terms.
6. ขอบเขตของงาน — requirements.md; the bulk of the TOR.
7. ระยะเวลาดำเนินการ — "ระยะเวลาดำเนินการ 180 วัน (หนึ่งร้อยแปดสิบวัน) นับถัดจากวันลงนามในสัญญา".
8. สถานที่ดำเนินการ — the agency's address and installation site.
9. วงเงินงบประมาณ — "วงเงินงบประมาณ 1,105,000 บาท (หนึ่งล้านหนึ่งแสนห้าพันบาทถ้วน) ซึ่งเป็นราคาที่รวมภาษีมูลค่าเพิ่ม
   ภาษีอื่น ค่าขนส่ง ค่าจดทะเบียน และค่าใช้จ่ายอื่นทั้งปวงไว้แล้ว" — the amount in words must match the figure.
10. หลักเกณฑ์การพิจารณาคัดเลือกข้อเสนอ — clauses.md.
11. การส่งมอบงาน — what is delivered, how many copies, in which formats.
12. งวดงานและการจ่ายเงิน — clauses.md; a table per instalment of its deliverables, each citing its scope item.
13. อัตราค่าปรับ — clauses.md.
14. การรับประกันผลงานและบำรุงรักษา — clauses.md.
15. ข้อปฏิบัติด้านความมั่นคงปลอดภัยเทคโนโลยีสารสนเทศ — clauses.md.
16. การละเมิดลิขสิทธิ์ — clauses.md.
17. ข้อสงวนสิทธิ์ — clauses.md.
Training is a work stream of section 6 (courses, days, trainees), with course details in an appendix.
ภาคผนวก: `# ภาคผนวก ก <ชื่อ>` (e.g. รายการ Dashboard/รายงาน, คุณลักษณะเฉพาะ), `# ภาคผนวก ข บุคลากร`,
`# ภาคผนวก ค รายละเอียดหลักสูตรการฝึกอบรม`, an NDA form when section 15 asks for one. Drop a section that does not
apply and renumber the rest in sequence.

## Tables
Caption line `ตาราง: …` before a table (numbered ตารางที่ N): the compliance table, the instalment table, the
personnel table, the training table. Figures (a system diagram) get `ภาพ: …` after them (numbered รูปที่ N).

## Style
- Formal regulatory Thai. The agency by its short name after the first mention (สป.กษ.), the bidder
  "ผู้ยื่นข้อเสนอ", the winner "ผู้รับจ้าง". Obligations "ต้อง…"; English terms in brackets the first time.
- Money with the amount in words in brackets; percentages "ร้อยละ 30"; durations "ภายใน 60 วัน นับถัดจากวัน
  ลงนามในสัญญา".
- Markdown the converter reads: `#`/`##` headings, paragraphs, `- ` lists, pipe tables, `ตาราง:`/`ภาพ:` lines.
  No bold inside clauses, no HTML.

## Checklist
- Sections 1–17 (minus dropped ones) in order and renumbered; appendices referenced from the text exist.
- Duration, budget, instalment % (sum 100) and deadlines consistent across sections 7, 9, 12.
- Every deliverable in section 12 is produced by a scope item in section 6; every training course in the
  appendix is listed in the scope.
- Every `[…]` filled or reported to the user.
