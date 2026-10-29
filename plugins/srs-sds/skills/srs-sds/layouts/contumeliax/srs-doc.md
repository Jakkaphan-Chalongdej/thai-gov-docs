# Layout contumeliax: SRS (เอกสารข้อกำหนดความต้องการซอฟต์แวร์)

Contractor hand-in style for government projects: numbered chapters in Thai with the English name in brackets,
almost everything in tables. Read [examples-srs.md](examples-srs.md) for the tone; write with this project's
own names, never copy the examples.

## Chapters
1. บทนำ (Introduction): 1.1 วัตถุประสงค์ของเอกสาร (Purpose) — a paragraph naming the project, the TOR and the
   agency, ending "ทั้งนี้เพื่อวัตถุประสงค์ดังต่อไปนี้", then a list (reference between agency and contractor,
   requirement baseline for design/test/acceptance, shared understanding, UAT criteria); 1.2 ขอบเขตของระบบ
   (Scope) — "ชื่อระบบ:" line, "ขอบเขตโดยสังเขป:" paragraph (purpose, contract period from the TOR),
   "สิ่งที่ระบบนี้ทำ:" then one list item per module.
2. ภาพรวมของระบบ (Overall Description): 2.1 บริบทของระบบ (System Context) — two or three paragraphs on data
   sources, processing and who sees the results, citing the TOR item; 2.2 กลุ่มผู้ใช้งานและคุณลักษณะ (User
   Classes & Characteristics) — lead-in, then `| รหัส | กลุ่มผู้ใช้งาน | หน้าที่หลักในระบบ |`;
   2.3 ตารางสิทธิ์การเข้าถึงตามบทบาท (Role Permission Matrix) — `| ฟังก์ชัน / โมดูล | U-01 | … | ผู้ดูแลระบบ |`
   with C R U D A or - per cell, then the line "หมายเหตุ: C = สร้าง, R = อ่าน, U = แก้ไข, D = ลบ, A = อนุมัติ,
   - = ไม่มีสิทธิ์"; 2.4 สภาพแวดล้อมการทำงานของระบบ (Operating Environment) — `| องค์ประกอบ | ข้อกำหนด |
   หมายเหตุ |` (site, infrastructure, browsers, encryption, sign-in; หมายเหตุ "ตาม TOR ข้อ …");
   2.5 ข้อจำกัดในการออกแบบและพัฒนา (Design & Implementation Constraints) — a list, each ending "ตาม TOR ข้อ …";
   2.6 สมมติฐานและการพึ่งพา (Assumptions & Dependencies) — `| ประเภท | รายละเอียด | ผลกระทบหากไม่เป็นไปตามที่ระบุ |`.
3. ข้อกำหนดความต้องการเชิงฟังก์ชัน (Functional Requirements): a lead-in naming the modules and saying each
   requirement has an id for traceability; then per module `## 3.n <ชื่อโมดูล>` and
   `| รหัส | ชื่อความต้องการ | รายละเอียด / ที่มา (อ้างอิง TOR) |`, one row per FR, the detail ending
   "(TOR 6.9.1.1)". Every FR of `srs.md` appears once, with its acceptance criteria folded into the detail.
4. ข้อกำหนดความต้องการที่ไม่ใช่เชิงฟังก์ชัน (Non-Functional Requirements): 4.1 ประสิทธิภาพ (Performance),
   4.2 ความมั่นคงปลอดภัย (Security), 4.3 ความพร้อมใช้งานและความน่าเชื่อถือ (Availability & Reliability),
   4.4 ความสามารถในการรองรับการขยายตัว (Scalability), 4.5 การใช้งานง่าย (Usability), 4.6 การบำรุงรักษา
   (Maintainability); each `| รหัส | รายละเอียดความต้องการ | อ้างอิง TOR |` with ids NFR-PF-01, NFR-SC-01,
   NFR-AV-01, NFR-SL-01, NFR-US-01, NFR-MT-01. Drop a subsection the TOR says nothing about rather than invent one.
5. ข้อกำหนดส่วนต่อประสานภายนอก (External Interface Requirements): 5.1 ส่วนต่อประสานผู้ใช้ (User Interfaces)
   `| ส่วนต่อประสาน | รายละเอียด | อ้างอิง TOR |`; 5.2 ส่วนต่อประสานซอฟต์แวร์ (Software Interfaces)
   `| ระบบที่เชื่อมโยง | รายละเอียดการเชื่อมโยง | อ้างอิง TOR |`; 5.3 ส่วนต่อประสานการสื่อสาร (Communication
   Interfaces) `| โปรโตคอล/มาตรฐาน | วัตถุประสงค์การใช้งาน | อ้างอิง TOR |`.
6. ข้อกำหนดด้านข้อมูล (Data Requirements): a paragraph on what data the system keeps and that the full data
   dictionary is in the SDS, then `| รหัส | ชื่อชุดข้อมูล |` (DS-01 …) or `| ข้อมูล | ฟิลด์สำคัญ | หมายเหตุ |`
   from SRS section 4, and the state cycles as `| สถานะ | ใครทำต่อ | ไปสถานะ | ถ้าค้าง |`.
7. ตารางสอบทานย้อนกลับ (Traceability Matrix): `| ข้อ TOR | รหัสความต้องการ | ชื่อความต้องการ |`, one row per TOR
   item, every TOR number and every FR/NFR id present. A TOR item met by a deliverable rather than a function
   (a design document, training) gets "-" as its code and the deliverable as its name ("เอกสารออกแบบระบบ (SDD)").
   TOR items cited by NFRs belong here too, even when `srs.md` section 8 left them out.
8. ภาคผนวก ก: อภิธานศัพท์ (Glossary): `| คำศัพท์ / คำย่อ | คำอธิบาย |` ("CIP | Customs Intelligence Platform -
   …" style: English expansion, a dash, the Thai meaning).

Open questions from SRS section 7 go to the user, not into this document.

## Headings
Chapter (`#`) and section (`##`) headings carry their numbers and an English name in brackets:
`# 1. บทนำ (Introduction)`, `## 1.1 วัตถุประสงค์ของเอกสาร (Purpose)`, `### 6.6.1 …`. Item headings start with their
code instead (`### M01: …`, `### SCR-01 …`), and headings inside an appendix have no number. Number the
sections you keep in sequence: when a listed section does not apply (no performance requirement in the TOR),
drop it and number the next one in its place.

## Style
- Formal Thai with the English term in brackets the first time: "ฐานข้อมูลกลาง (Data Lake House)". Requirements:
  "ระบบต้อง…" / "ระบบต้องสามารถ…ได้"; cite sources as "(TOR 6.9.1.1)" in FR rows, "ตาม TOR ข้อ 3.3.1" in prose.
- Mostly tables: a paragraph only where the chapter list above asks for one. A lead-in ending "ดังนี้" or
  "ดังต่อไปนี้" before a list.
- Call the customer by the name in the TOR (e.g. กรมศุลกากร) or "หน่วยงาน"; the contractor "ผู้พัฒนาระบบ".

## Checklist
- Every TOR item number in chapter 7; every FR of `srs.md` in chapter 3 once; every NFR in chapter 4.
- Role codes in 2.2 are the column heads of 2.3.
