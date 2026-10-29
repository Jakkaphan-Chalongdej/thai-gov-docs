# uat-doc: skill เขียนเอกสาร UAT สำหรับ Claude Code

skill นี้ให้ Claude เขียนเอกสารทดสอบการยอมรับระบบ (User Acceptance Test Documents) แบบที่หน่วยงานใช้ตรวจรับ
ตามตัวอย่าง "เมนู Admin Overview" แล้วออกเป็น .md, .docx และ .pdf ใช้ได้ทั้ง Windows, macOS และ Linux

## วิธีใช้
พิมพ์สั่งใน Claude Code เช่น

- "ทำเอกสาร UAT เมนู Admin Overview จาก sds-doc.md ภาพหน้าจออยู่ในโฟลเดอร์ screens"
- "ทำ UAT ของโมดูล Web Portal จาก srs.md และ sds-doc.md ยังไม่มีภาพหน้าจอ"
- "ทำ UAT จากระบบทดสอบ https://staging.example.go.th บัญชีทดสอบอยู่ใน seed.json"

Claude เสนอรายการฟังก์ชันและกรณีทดสอบให้ตรวจก่อน แล้วจึงเขียนเอกสาร

| ไฟล์ | เนื้อหา |
|---|---|
| uat-<เมนู>.md / .docx / .pdf | ปก, สารบัญ, Revision History, Test History, 1. Introduction (Purpose, Test Execution, Test Scope), 2. User Acceptance Test ตารางกรณีทดสอบรายฟังก์ชัน, 3. Requirement Traceability (เมื่อทำจาก SRS) |
| screens/ | ภาพหน้าจอที่ต้องเห็นเมื่อทดสอบผ่าน |

## ตารางกรณีทดสอบ
แต่ละฟังก์ชันมีตาราง No, Function, Menu, Test Description, Result, Remark ในช่อง Test Description มีเลขและชื่อกรณี
ทดสอบ ขั้นตอน ภาพหน้าจอ และรายการที่ต้องตรวจ ช่อง Result เป็นช่องติ๊ก (Check Box) "ผ่าน" และ "ไม่ผ่าน" ที่คลิกได้ใน Word

## ภาพหน้าจอ
- มีภาพอยู่แล้ว: วางไว้ในโฟลเดอร์ `screens/` Claude จะจับคู่ภาพกับกรณีทดสอบให้
- มีระบบทดสอบ: Claude เก็บภาพจากเบราว์เซอร์ได้ (ผู้ใช้ลงชื่อเข้าใช้เองหรือให้บัญชีทดสอบ)
- ยังไม่มีภาพ: เอกสารจะเว้นเป็นกรอบ "ใส่ภาพหน้าจอ" ในตาราง และ Claude ให้รายการภาพที่ต้องถ่ายไว้

## เตรียมเครื่อง
ครั้งแรกที่ขอ Word/PDF Claude จะรัน `scripts/setup.py` (ติดตั้ง python-docx, Pillow และฟอนต์ Sarabun ถ้ายังไม่มี)
PDF ต้องมี LibreOffice ถ้าไม่มีให้เปิด .docx ใน Word แล้ว Save As PDF

```bash
python3 ~/.claude/skills/uat-doc/scripts/md2docx.py uat-admin.md --size 14 --pdf
```
