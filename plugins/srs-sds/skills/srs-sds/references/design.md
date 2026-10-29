# Step B: System design (เอกสารออกแบบระบบ) + schema

Developers, testers and operators build from this: every FR in the SRS must land in a table and an API, with
nothing left to guess.

## Steps
1. Read `srs.md` in full (FR ids, roles, data). If there is none, write it first (Step A).
2. Choose the stack: the one named in the TOR or by the user; otherwise a plain default (web frontend, REST API,
   PostgreSQL, object storage, reverse proxy, Docker Compose) and say why. Record each significant choice as a
   decision ADR-01 … (context, options, choice, reason, consequences) and each TOR limit on the design as DC-01 …
3. Model the data: one table per managed thing, plus lookup tables for master data. Standard columns on every
   table: id, created_at, created_by, updated_at, updated_by; status for anything with a workflow; soft delete
   (deleted_at) for records the TOR wants kept. Name foreign keys and unique rules.
4. Code the modules M01, M02 … (same order as the SRS modules), the tables TBL-01 …, the screens SCR-01 … (one per
   user job: list, form, detail, approval queue, report, sign-in, users, roles, audit log) and the APIs API-01 …
   List the API per module: list (paging, search, SRS filters), get, create, update, delete or cancel, workflow
   actions (submit, approve, send back), export; the role that may call each.
5. Draw each approval workflow as states and transitions, with who acts.
6. Cover cross-cutting parts once: auth and roles, audit log, file upload, notifications, reports, plus how it
   runs: deployment components with sizes, environments (DEV/SIT/UAT/PROD), monitoring, backup and retention,
   indexes for the main searches. Use the TOR's numbers; otherwise propose values and mark them "(เสนอ)". Login follows
   the stack (own JWT, no outside SSO unless the TOR asks); say which parts are public. The first admin account is
   created at install (seed or setup command) with the SRS role "ผู้ดูแลระบบ". Copy every SRS data rule (required
   fields, formats, password policy, OTP) into the rules table.
7. List the roles the design uses in "## บทบาทที่ใช้", names exactly as in the SRS (or "ทุกบทบาท"). A role or table
   the SRS does not have goes in "## ส่วนที่เพิ่มเพื่อการใช้งาน" with a reason. About 1,000 words. Save as `design.md`.
8. Write the data model as PostgreSQL DDL in `schema.sql` (the SDS data dictionary and ER diagram come from it, so
   it must match section 3): one CREATE TABLE per table with typed columns, PRIMARY KEY, NOT NULL, UNIQUE and
   REFERENCES, and a Thai name for every table: `COMMENT ON TABLE bookings IS 'การจองห้อง';`
   COMMENT ON COLUMN is welcome. Plain SQL only (no functions, DO blocks, psql commands).

## Template
```
# เอกสารออกแบบระบบ: <ชื่อระบบ>

## 1. ภาพรวมสถาปัตยกรรม
<ส่วนประกอบและการเชื่อมต่อ เป็นรายการหรือแผนภาพ mermaid>
เทคโนโลยี: <frontend / backend / database / storage / deploy> — เหตุผล: <สั้นๆ>

## 2. โมดูล
| รหัส | โมดูล | หน้าที่ | FR ที่รองรับ | พึ่งพา |
|---|---|---|---|---|

### หน้าจอ
| รหัส | หน้าจอ | โมดูล | บทบาท | ช่อง / ปุ่มหลัก | API |
|---|---|---|---|---|---|

## 3. โครงสร้างข้อมูล
### TBL-01 <ชื่อตาราง> (<ชื่อไทย>)
| คอลัมน์ | ชนิด | หมายเหตุ |
|---|---|---|
ความสัมพันธ์: <FK, unique, index ที่ต้องมี>

## 4. รายการ API
| รหัส | Method | Path | ใช้ทำอะไร | บทบาทที่เรียกได้ | FR |
|---|---|---|---|---|---|

## 5. กติกาข้อมูล
| ฟิลด์ | กติกา (ตาม SRS) | ตรวจที่ |
|---|---|---|

## 6. Workflow การอนุมัติ
<สถานะ: ร่าง → รออนุมัติ → อนุมัติแล้ว / ส่งกลับแก้ไข / ยกเลิก — ใครเปลี่ยนได้>

## 7. สิทธิ์และความปลอดภัย
- สิทธิ์ตามบทบาท
- รหัสผ่านเก็บแบบ hash, HTTPS, audit log ทุกการเปลี่ยนแปลง, ข้อมูลส่วนบุคคลตาม PDPA

## 8. การเชื่อมต่อระบบอื่น
## 9. ด้านการทำงาน
| เรื่อง | ค่าที่ใช้ | ที่มา |
|---|---|---|
| เครื่อง / container และขนาด | | TOR ข้อ … หรือ (เสนอ) |
| สภาพแวดล้อม DEV / SIT / UAT / PROD | | |
| การเฝ้าระวังและแจ้งเตือน | | |
| สำรองข้อมูล: ความถี่ / เก็บย้อนหลัง | | |
| ดัชนีสำหรับการค้นหาหลัก | | |
## 10. การตัดสินใจสำคัญ
| รหัส | เรื่อง | ทางเลือกที่พิจารณา | ทางที่เลือก | เหตุผล | ผลที่ตามมา |
|---|---|---|---|---|---|

### ข้อจำกัดการออกแบบ
| รหัส | ข้อจำกัด | ที่มา (TOR) |
|---|---|---|

## บทบาทที่ใช้
| บทบาท | สิ่งที่ทำได้ |
|---|---|
| ผู้ดูแลระบบ | <บัญชีแรกสร้างตอนติดตั้ง> |

## ส่วนที่เพิ่มเพื่อการใช้งาน
| สิ่งที่เพิ่ม | เหตุผล |
|---|---|
```
(Last table only if you add something.)

## Checklist
- `schema.sql` has every table of section 3, same columns, and a Thai COMMENT ON TABLE for each.
- Every SRS FR id is in the module table and at least one API row.
- Every SRS list needing search/filter has those parameters on its list API.
- Every workflow has states, transitions and the acting role; every SRS data rule is in the rules table.
- Tables have keys, standard columns and an API that uses them.
- Codes M, SCR, TBL, API, ADR, DC are unique; every screen points at a module and an API that exist.
- Security covers roles, password storage, audit log, personal data; บทบาทที่ใช้ has only SRS roles.
