# Step A: SRS (เอกสารความต้องการระบบ)

The SRS is the base every later document builds on (design, build, test), so it must be complete against the
brief/TOR and precise.

## Steps
1. Read the TOR/brief and any notes. Number every requirement line; each becomes at least one functional
   requirement (FR).
2. Find the roles (ผู้ใช้งาน, เจ้าหน้าที่, หัวหน้า/ผู้อนุมัติ …) and what each may do. Add "ผู้ดูแลระบบ" (manages
   users, roles, settings) unless the user says the system has none. Later documents use these role names exactly.
3. Write each FR as a user story with 2–4 checkable acceptance criteria: "เมื่อ … แล้ว ระบบ …".
   Every data rule in the TOR (required fields, formats, password length/characters, OTP) gets its own FR or AC
   with the TOR's numbers copied exactly.
4. For every record with a status (คำขอ, ใบสั่งซื้อ, ข่าว …) write its state cycle in section 4.1: state | who
   acts next | next states | what happens when nobody acts. Name the end states, undoing after approval and who
   approves it, an acting approver when the approver is away, and side effects (หักวันลา, ออกเลขที่).
5. Basics most systems need, each its own FR: sign-in, the first admin account, users and roles, password
   reset/change, audit log; notifications and date format if the TOR mentions them. List them in the
   "## เรื่องพื้นฐาน" table: one row per topic with FR ids that exist. "ไม่มี <เหตุผล>" only for แจ้งเตือน and วันที่.
6. Write what is out of scope and the questions to ask the customer instead of guessing silently.
7. About 1,000 words: short sentences, tables, no repeats. Save as `srs.md`.

## Template
```
# เอกสารความต้องการระบบ (SRS): <ชื่อระบบ>

## 1. บทนำ
- วัตถุประสงค์: <หนึ่งถึงสองประโยค>
- ขอบเขต: <โมดูลที่รวม>
- คำศัพท์: <คำเฉพาะของหน่วยงาน ถ้ามี>

## 2. ผู้ใช้และบทบาท
| บทบาท | หน้าที่ | สิทธิ์หลัก |
|---|---|---|
| ผู้ดูแลระบบ | <จัดการผู้ใช้ บทบาท และตั้งค่า> | <สิทธิ์ทั้งหมดของการดูแลระบบ> |

## 3. ความต้องการเชิงฟังก์ชัน
### 3.1 <ชื่อโมดูล>
**FR-01 <ชื่อสั้น>** (TOR <ข้อ>)
ในฐานะ <บทบาท> ต้องการ <สิ่งที่ทำ> เพื่อ <ประโยชน์>
- AC1: เมื่อ <เงื่อนไข> แล้ว ระบบ <ผลที่ตรวจได้>
- AC2: …

## 4. ข้อมูลหลัก
| ข้อมูล | ฟิลด์สำคัญ | หมายเหตุ |
|---|---|---|

### 4.1 วงจรสถานะ
| สถานะ | ใครทำต่อ | ไปสถานะ | ถ้าค้าง |
|---|---|---|---|

## 5. ความต้องการที่ไม่ใช่ฟังก์ชัน
- ความปลอดภัย: สิทธิ์ตามบทบาท, บันทึกการใช้งาน (audit log), ข้อมูลส่วนบุคคลตาม PDPA
- การใช้งาน: เบราว์เซอร์ที่รองรับ, ภาษาไทย, วันที่แบบ พ.ศ.
- ประสิทธิภาพและการสำรองข้อมูล: <ตาม TOR หรือสมมติฐาน>

## 6. นอกขอบเขต
## 7. สมมติฐานและคำถามถึงลูกค้า
## 8. ตารางโยง TOR → FR
| TOR | FR |
|---|---|

## เรื่องพื้นฐาน
| หัวข้อ | FR / ข้อ |
|---|---|
| การเข้าสู่ระบบ | FR-01 |
| ช่องทางแจ้งเตือน | ไม่มี <เหตุผล เช่น TOR ไม่พูดถึงการแจ้ง> |
```

## Checklist
- Every requirement line of the TOR/brief appears in the TOR → FR table; none is left without an FR.
- "ผู้ดูแลระบบ" in section 2; the เรื่องพื้นฐาน table points at FRs with ACs.
- Every FR has a role, a goal and checkable acceptance criteria (no "ใช้งานง่าย" without a measure).
- Approval, search/filter, reports/export, notifications and data rules from the TOR each have their own FR.
- Validation rules (required fields, formats, lengths) are in the acceptance criteria.
- Every status has an owner and a next state; end states and "ถ้าค้าง" are written, nothing waits forever.
- Nothing is invented as a requirement; guesses are in section 7.
- FR ids are unique, in order, each starting its own line or heading (not a table row).
