# Step C: Hand-in SRS and SDS documents (เอกสารส่งมอบ)

Two customer documents for the acceptance committee: `srs-doc.md` (เอกสารข้อกำหนดความต้องการซอฟต์แวร์) then
`sds-doc.md` (เอกสารการออกแบบสถาปัตยกรรมและการออกแบบซอฟต์แวร์). They are rewritten from `srs.md`, `design.md`
and `schema.sql`; nothing may be added, dropped or renamed. The layout follows the contractor hand-in style used
for government projects (cover, revision and approval tables, contents, numbered chapters, tables everywhere).

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
Use these names and codes exactly in both documents.

Working files from an older run may lack some codes (no U-/NFR- ids in `srs.md`, no M/SCR/TBL/API/ADR codes or
screens table in `design.md`). Then assign the codes yourself in the facts list: a code is a label, not a rename,
so this does not break "nothing added or renamed". Keep FR ids exactly as `srs.md` has them (FR-01 stays FR-01).
Screens missing from `design.md`: derive one per user job from the FRs and APIs. Module names that differ
between `srs.md` and `design.md`: the SRS name wins. List every code and screen you assigned in your reply.

## 2. Front matter (both documents)
Start each file with this block; the converter turns it into the cover, revision history, approval and
reference tables, the table of contents, the page header and the footer. Do not write those pages yourself.
```
---
company: บริษัท <ชื่อ> จำกัด
company_en: <NAME> CO., LTD.
address: <ที่อยู่บริษัท>
contact: โทร. <เบอร์>  |  <อีเมล>  |  <เว็บไซต์>
logo: logo.png
title: เอกสารข้อกำหนดความต้องการซอฟต์แวร์
title_en: Software Requirements Specification (SRS)
project: <ชื่อโครงการตาม TOR>
contract: <เลขที่สัญญา>
client: <หน่วยงานผู้ว่าจ้าง>
doc_code: SRS-001
version: 1.0
date: <วัน เดือน ปี พ.ศ.>
classification: ใช้ภายในโครงการ (Project Internal Use)
author: <ผู้จัดทำ>
revision: จัดทำเอกสารข้อกำหนดความต้องการซอฟต์แวร์
ref: TOR | ขอบเขตของงาน (TOR) <ชื่อโครงการ> | - | <วันที่>
note: เอกสารฉบับนี้เมื่อได้รับการลงนามรับรองแล้วจะถูกตรึงเป็น Requirement Baseline การเปลี่ยนแปลงหลังจากนั้นต้องผ่านกระบวนการควบคุมการเปลี่ยนแปลง
---
```
SDS: `title: เอกสารการออกแบบสถาปัตยกรรมและการออกแบบซอฟต์แวร์`, `title_en: System Architecture & Software
Design Document (SDD)`, `doc_code: SDD-001`, a `ref:` line for the SRS, no `note`. Omit a key you do not know;
`logo` is a PNG path relative to the markdown file.

## 3. srs-doc.md
Chapter (`#`) and section (`##`) headings carry their numbers and an English name in brackets:
`# 1. บทนำ (Introduction)`, `## 1.1 วัตถุประสงค์ของเอกสาร (Purpose)`, `### 6.6.1 …`. Item headings start with their
code instead (`### M01: …`, `### SCR-01 …`), and headings inside an appendix have no number. Number the
sections you keep in sequence: when a listed section does not apply (no performance requirement in the TOR),
drop it and number the next one in its place. Chapters in this order:

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

## 4. sds-doc.md
Same heading style. Chapters in this order:

1. บทนำ (Introduction): 1.1 วัตถุประสงค์ของเอกสาร (one paragraph: turns the requirements into a buildable design,
   baseline for developers and QA); 1.2 ขอบเขตของเอกสาร (what it covers: architecture, UI, database, API,
   security, operation; what it does not: business analysis in the SRS, user manual, project plan);
   1.3 กลุ่มผู้ใช้เอกสารและวิธีการอ่าน `| กลุ่มผู้อ่าน | วัตถุประสงค์ในการใช้ | หมวดที่ควรอ่าน |`;
   1.4 นิยามศัพท์และคำย่อทางเทคนิค `| คำย่อ | คำเต็ม | ความหมายในบริบทของระบบนี้ |`.
2. หลักการและข้อจำกัดในการออกแบบ (Design Principles & Constraints): 2.1 หลักการออกแบบที่ยึดถือ
   `| หลักการ | คำอธิบาย | ผลต่อการออกแบบ |`; 2.2 ข้อจำกัดในการออกแบบ `| รหัส | ข้อจำกัด | ที่มาและผลต่อการออกแบบ |`
   (DC-01 …, "ตามข้อ … ของ TOR"); 2.3 บันทึกการตัดสินใจเชิงสถาปัตยกรรม (Architecture Decision Records) — per
   decision a `| หัวข้อ | รายละเอียด |` table with rows รหัส ADR, หัวข้อการตัดสินใจ, สถานะ, บริบท (Context),
   ทางเลือกที่พิจารณา, การตัดสินใจ, เหตุผลประกอบ, ผลที่ตามมา (Consequences), ข้อกำหนด/ข้อจำกัดที่เกี่ยวข้อง;
   2.4 ตารางสรุปการตัดสินใจเชิงสถาปัตยกรรม `| รหัส | หัวข้อการตัดสินใจ | ทางเลือกที่เลือก | สถานะ |`.
3. การออกแบบสถาปัตยกรรมระบบ (System Architecture Design): 3.1 ภาพรวมสถาปัตยกรรม — lead-in, a mermaid
   flowchart, `ภาพ: ภาพรวมสถาปัตยกรรมของระบบ`; 3.2 มุมมองเชิงตรรกะ (Logical View) `| ชั้น (Layer) |
   ความรับผิดชอบ | เทคโนโลยีที่ใช้ |`; 3.3 มุมมองเชิงกระบวนการ (Process View) `| กระบวนการ |
   องค์ประกอบที่เกี่ยวข้อง | ประเด็นสำคัญในการออกแบบ |`; 3.4 มุมมองการติดตั้งใช้งาน (Deployment View)
   `| องค์ประกอบ | หน้าที่ | ข้อกำหนดทรัพยากร | จำนวน |`; 3.5 มุมมองการพัฒนา (Development View) `| องค์ประกอบ |
   โครงสร้างโปรเจกต์ | หมายเหตุ |`; 3.6 สภาพแวดล้อมของระบบ (Environments) `| สภาพแวดล้อม | วัตถุประสงค์ |
   ผู้มีสิทธิ์เข้าถึง | ข้อมูลที่ใช้ |` (DEV, Test/SIT, UAT, PROD).
4. การออกแบบรายละเอียดระดับโมดูล (Detailed Module Design): 4.1 แผนผังการแบ่งโมดูลและความสัมพันธ์ `| รหัสโมดูล |
   ชื่อโมดูล | ความรับผิดชอบ | โมดูลที่พึ่งพา |`; 4.2 รายละเอียดการออกแบบรายโมดูล — per module
   `### M01: <ชื่อ>` and `| หัวข้อ | รายละเอียด |` (วัตถุประสงค์ citing the TOR item, หน้าที่หลัก, FR ที่รองรับ,
   then the rows that fit: ข้อมูลที่ใช้, ลักษณะการประมวลผล, ผลลัพธ์, ซอฟต์แวร์ที่ใช้, ความมั่นคงปลอดภัย);
   4.3 การออกแบบองค์ประกอบร่วม (Cross-cutting Components) `| องค์ประกอบ | หน้าที่ | แนวทางการออกแบบ |`.
5. การออกแบบส่วนติดต่อผู้ใช้ (User Interface Design): 5.1 แนวคิดและหลักการออกแบบประสบการณ์ผู้ใช้งานและส่วนติดต่อ
   ผู้ใช้งาน — three or four paragraphs (user-centred design, layout and visual hierarchy, design system, responsive)
   written for this system's users; 5.2 โครงสร้างการนำทางและผังหน้าจอ (Navigation & Sitemap) `| รหัสหน้าจอ |
   ชื่อหน้าจอ | โมดูล | กลุ่มผู้ใช้ที่เข้าถึงได้ |`, every screen; 5.3 รายละเอียดการออกแบบหน้าจอ — per screen
   `### SCR-01 <ชื่อหน้าจอ>`, the screen image (`![…](screens/x.png)` or `[ภาพหน้าจอ: <ชื่อหน้าจอ>]`), a caption
   `ภาพ: หน้าจอ<ชื่อหน้าจอ>`, then `| หัวข้อ | รายละเอียด |` with rows รหัสหน้าจอ, ชื่อหน้าจอ, โมดูล, วัตถุประสงค์,
   กลุ่มผู้ใช้, องค์ประกอบหลัก (UI Components), ข้อมูลที่แสดง, การกระทำที่รองรับ (Actions), กฎการตรวจสอบ/เงื่อนไข,
   การเชื่อมโยง API, การรองรับภาษา / Responsive.
6. การออกแบบฐานข้อมูล (Database Design): two or three paragraphs (logical then physical model, normalised to at
   least 3NF, keys and constraints, access control and audit); 6.1 แบบจำลองข้อมูลเชิงตรรกะ (Logical Data Model) —
   a paragraph naming the central entities and relations, then a mermaid `erDiagram` built from `schema.sql`
   (every table, every FK), `ภาพ: แผนภาพความสัมพันธ์ของข้อมูล (ER Diagram)`. More than 12 tables do not fit a page
   legibly: draw one `erDiagram` per module or table group instead (at most about 12 tables each, a table from
   another group shown only when a FK points at it), each with a lead-in and its own caption
   `ภาพ: แผนภาพความสัมพันธ์ของข้อมูล: <กลุ่ม>`; together they cover every table and every FK; 6.2 รายการตารางในฐานข้อมูล
   (Table Inventory) `| รหัสตาราง | ชื่อตาราง | วัตถุประสงค์ |` with "bookings (การจองห้อง)" names;
   6.3 รายละเอียดโครงสร้างตาราง (Table Specification) — per table a caption `ตาราง: <ชื่อไทย> (<table>)` and
   `| ชื่อฟิลด์ | ประเภทข้อมูล | คำอธิบายและกฎการตรวจสอบ |`, column names and types exactly as in `schema.sql`,
   the description saying Primary Key / Foreign Key to which table, required, unique and every allowed value;
   6.4 กลยุทธ์การจัดทำดัชนีและการปรับแต่งสมรรถนะ `| ตาราง | ฟิลด์ที่ทำดัชนี | ประเภทดัชนี | เหตุผล |`;
   6.5 กลยุทธ์การแบ่งพาร์ทิชันและการเก็บถาวร `| ตาราง | กลยุทธ์ | เงื่อนไขและรอบการดำเนินการ |` (only tables that
   grow large); 6.6 การออกแบบการย้ายข้อมูล (Data Migration Design) with 6.6.1 Field Mapping, 6.6.2 Cleansing
   Rules (CR-01 …), 6.6.3 Reconciliation — whenever the system loads data from an existing system (one-off
   migration, ETL or replication); skip it only for a system that starts empty.
7. การออกแบบด้านความมั่นคงปลอดภัย (Security Design): 7.1 สถาปัตยกรรมความมั่นคงปลอดภัยและการแบ่งโซน `| โซน |
   องค์ประกอบที่อยู่ในโซน | การควบคุมการเข้าถึง |`; 7.2 การพิสูจน์ตัวตนและการให้สิทธิ์ `| ประเด็น | การออกแบบ |
   ข้อกำหนดที่รองรับ |` (sign-in, session/token, authorisation, MFA, password policy, lockout); 7.3 ตารางสิทธิ์การ
   เข้าถึงระดับเทคนิค (Technical RBAC Matrix) `| ทรัพยากร / API Endpoint | U-01 | … | ผู้ดูแลระบบ |` with อนุญาต /
   ไม่อนุญาต / อ่าน / อ่าน/เขียน; 7.4 การเข้ารหัสข้อมูล `| ข้อมูล | วิธีการเข้ารหัส | การจัดการกุญแจ | ข้อกำหนด |`;
   7.5 การออกแบบการบันทึกร่องรอยการใช้งาน `| เหตุการณ์ที่บันทึก | ข้อมูลที่บันทึก | ระยะเวลาจัดเก็บ | ผู้เข้าถึงได้ |`;
   7.6 การออกแบบด้านการคุ้มครองข้อมูลส่วนบุคคล (Privacy by Design) `| ประเด็น | การออกแบบรองรับ |`.
8. การออกแบบส่วนเชื่อมต่อระบบ (Interface & API Design): 8.1 หลักการออกแบบ API — paragraphs (REST, JSON, HTTP
   methods, endpoint naming, response format and status codes, authentication, versioning); 8.2 รายการ API
   ภายในระบบ (Internal API Inventory) `| รหัส | Endpoint | หน้าที่ | โมดูล |`, every API of `design.md`;
   8.3 รายละเอียด API รายรายการ — for the main APIs (at least one per module) `| หัวข้อ | รายละเอียด |` with rows
   รหัส API, Endpoint, หน้าที่, HTTP Method, การพิสูจน์ตัวตน (Authentication), Request (Body), Response (Success 200),
   การจัดการข้อผิดพลาด (Error Handling), Rate Limit / Timeout, โมดูลที่เกี่ยวข้อง; 8.4 การเชื่อมต่อกับระบบภายนอก
   `| หัวข้อ | รายละเอียด |`.
9. การออกแบบด้านการดำเนินงานและการติดตั้ง (Operational Design): 9.1 กลยุทธ์การนำระบบขึ้นใช้งาน `| ประเด็น |
   แนวทาง | หมายเหตุ |` (server check → database → application → web server → domain/SSL → UAT → go live);
   9.2 การเฝ้าระวังและสังเกตการณ์ระบบ `| สิ่งที่เฝ้าระวัง | ตัวชี้วัด | เกณฑ์แจ้งเตือน | ผู้รับการแจ้งเตือน |`;
   9.3 การสำรองและกู้คืนข้อมูล `| ข้อมูลที่สำรอง | ความถี่ | ระยะเวลาเก็บย้อนหลัง | สถานที่จัดเก็บ |`;
   9.4 การจัดการค่าตั้งค่าและความลับของระบบ — a paragraph.
10. ตารางสอบทานย้อนกลับจากข้อกำหนดสู่การออกแบบ: 10.1 Requirement-to-Design `| รหัสข้อกำหนด | โมดูล |
    หัวข้อในเอกสารฉบับนี้ | ตาราง/API ที่เกี่ยวข้อง | สถานะ |`, every FR id; 10.2 NFR กับการออกแบบที่รองรับ
    `| รหัส NFR | ข้อกำหนด | การออกแบบที่รองรับ | หัวข้อ |`, every NFR id; 10.3 การส่งต่อสู่การทดสอบ
    (Design-to-Test) `| ส่วนของการออกแบบ | ประเภทการทดสอบที่เกี่ยวข้อง | หลักฐานที่ต้องจัดทำ |`.
11. ภาคผนวก (Appendices): `| ภาคผนวก | รายการ | สถานะ |` (ADR form, full data dictionary, OpenAPI, network
    diagram, UI prototype, test plan, DR plan: "มี" or "จัดทำภายหลัง"), then `## แบบฟอร์มบันทึกการตัดสินใจเชิง
    สถาปัตยกรรม (ADR Form)` as a blank `| หัวข้อ | รายละเอียด |` table with "(ระบุ…)" hints.

Facts the sources do not give (server sizes, versions, retention periods, backup frequency) are written as a
reasonable default marked "(เสนอ)" in the cell, and listed to the user as things to confirm.

## Diagrams (mermaid)
- Node ids in English letters; Thai text only inside quotes: `user["เจ้าหน้าที่"]`.
- ER: `erDiagram` with English table/column names from the schema.
- Captions: a line starting `ภาพ: ` right after a diagram or image (numbered รูปภาพที่ N), a line starting
  `ตาราง: ` right before a table that needs a name (numbered ตารางที่ N). Never type the numbers yourself.

## Style
- Formal Thai with the English term in brackets the first time: "ฐานข้อมูลกลาง (Data Lake House)". Requirements:
  "ระบบต้อง…" / "ระบบต้องสามารถ…ได้"; cite sources as "(TOR 6.9.1.1)" in FR rows, "ตาม TOR ข้อ 3.3.1" in prose.
- Mostly tables: a paragraph only where the chapter list above asks for one. A lead-in ending "ดังนี้" or
  "ดังต่อไปนี้" before a list.
- Restricted markdown only: `#` to `###` headings, `- ` lists, pipe tables with a `|---|` row, mermaid blocks,
  images, caption lines, the front matter. No bold, HTML, inline code, footnotes. A literal "|" inside a table
  cell is written `\|` (mode=partial\|full).
- Call the customer by the name in the TOR (e.g. กรมศุลกากร) or "หน่วยงาน"; the contractor "ผู้พัฒนาระบบ".
- Read [examples-srs.md](examples-srs.md) and [examples-sds.md](examples-sds.md) for the tone; write with this
  project's own names, never copy the examples.

## Checklist
- Front matter present in both files; no cover, revision, approval or contents pages written by hand.
- SRS: every TOR item number in chapter 7; every FR of `srs.md` in chapter 3 once; every NFR in chapter 4.
- Every role, module, screen, table, column and API name matches the facts list; codes (U-, M, FR-, NFR-, SCR-,
  TBL-, API-, ADR-, DC-) are unique and every code cited somewhere is defined somewhere.
- SDS: chapters 1–11 in order; every table of `schema.sql` in 6.2, 6.3 and an ER diagram; every FR and NFR id in
  chapter 10.
- Every image/diagram has a `ภาพ:` line after it.
