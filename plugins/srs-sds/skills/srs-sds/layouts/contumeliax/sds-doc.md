# Layout contumeliax: SDS / SDD (เอกสารการออกแบบสถาปัตยกรรมและการออกแบบซอฟต์แวร์)

Contractor hand-in style for government projects: numbered chapters in Thai with the English name in brackets,
almost everything in tables. Read [examples-sds.md](examples-sds.md) for the tone; write with this project's
own names, never copy the examples.

## Chapters
Chapters in this order:

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
- Chapters 1–11 in order; every table of `schema.sql` in 6.2, 6.3 and an ER diagram; every FR and NFR id of the
  SRS in chapter 10.
- Every screen in 5.2 has a 5.3 entry; every API cited by a screen is in 8.2.
