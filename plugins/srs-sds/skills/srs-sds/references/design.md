# Step B: System design (เอกสารออกแบบระบบ) + schema

Developers, testers and operators build from this: every FR in the SRS must land in a table and an API, with
nothing left to guess.

## Steps
1. Read `srs.md` in full (FR ids, roles, data). If there is none, write it first (Step A).
2. Choose the stack: the one named in the TOR or by the user; otherwise a plain default (web frontend, REST API,
   PostgreSQL, object storage, reverse proxy, Docker Compose) and say why.
3. Model the data: one table per managed thing, plus lookup tables for master data. Standard columns on every
   table: id, created_at, created_by, updated_at, updated_by; status for anything with a workflow; soft delete
   (deleted_at) for records the TOR wants kept. Name foreign keys and unique rules.
4. List the API per module: list (paging, search, SRS filters), get, create, update, delete or cancel, workflow
   actions (submit, approve, send back), export; the role that may call each.
5. Draw each approval workflow as states and transitions, with who acts.
6. Cover cross-cutting parts once: auth and roles, audit log, file upload, notifications, reports. Login follows
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
| โมดูล | หน้าที่ | FR ที่รองรับ |
|---|---|---|

## 3. โครงสร้างข้อมูล
### <ชื่อตาราง>
| คอลัมน์ | ชนิด | หมายเหตุ |
|---|---|---|
ความสัมพันธ์: <FK, unique, index ที่ต้องมี>

## 4. รายการ API
| Method | Path | ใช้ทำอะไร | บทบาทที่เรียกได้ | FR |
|---|---|---|---|---|

## 5. กติกาข้อมูล
| ฟิลด์ | กติกา (ตาม SRS) | ตรวจที่ |
|---|---|---|

## 6. Workflow การอนุมัติ
<สถานะ: ร่าง → รออนุมัติ → อนุมัติแล้ว / ส่งกลับแก้ไข / ยกเลิก — ใครเปลี่ยนได้>

## 7. สิทธิ์และความปลอดภัย
- สิทธิ์ตามบทบาท
- รหัสผ่านเก็บแบบ hash, HTTPS, audit log ทุกการเปลี่ยนแปลง, ข้อมูลส่วนบุคคลตาม PDPA

## 8. การเชื่อมต่อระบบอื่น
## 9. ด้านการทำงาน: สำรองข้อมูล, log, ประสิทธิภาพ
## 10. การตัดสินใจสำคัญ
| เรื่อง | ทางที่เลือก | เหตุผล |
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
- Security covers roles, password storage, audit log, personal data; บทบาทที่ใช้ has only SRS roles.
