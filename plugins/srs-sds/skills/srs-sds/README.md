# srs-sds: skill เขียนเอกสาร SRS / SDS สำหรับ Claude Code

skill นี้ให้ Claude เขียนเอกสารความต้องการ (SRS) และเอกสารออกแบบระบบ (SDS) ภาษาไทยแบบที่หน่วยงานรัฐใช้ตรวจรับ จาก TOR หรือบรีฟ
แล้วออกเป็น .md, .docx และ .pdf ได้ ดัดแปลงมาจาก agent BA / Architect / Doc ของ AI Factory
ใช้ได้ทั้ง Windows, macOS และ Linux

## ติดตั้ง
แตก zip ไว้ที่โฟลเดอร์ skill ของ Claude Code แล้วเปิด Claude Code ใหม่

| ระบบ | โฟลเดอร์ |
|---|---|
| macOS / Linux | `~/.claude/skills/` |
| Windows | `%USERPROFILE%\.claude\skills\` |

ถ้าต้องการใช้เฉพาะโปรเจกต์เดียว ให้แตกไว้ที่ `<โปรเจกต์>/.claude/skills/` แทน

แค่นี้ก็สั่ง Claude เขียนเอกสาร .md ได้แล้ว ครั้งแรกที่ขอ Word/PDF Claude จะรัน `scripts/setup.py` เพื่อเตรียมเครื่องให้เอง

| setup.py ทำให้เอง | ต้องติดตั้งเอง (setup.py บอกคำสั่งให้) |
|---|---|
| python-docx (ติดตั้งใน `.venv` ของ skill) | Python 3.9+ (Windows: python.org หรือ `winget install Python.Python.3.12`) |
| mermaid-cli สำหรับแผนภาพ (ติดตั้งใน `.tools` ของ skill) | Node.js สำหรับแผนภาพ (`winget install OpenJS.NodeJS.LTS` / `brew install node`) |
| ฟอนต์ Sarabun (ที่มากับแพ็ก) ถ้าเครื่องยังไม่มีฟอนต์ไทย | LibreOffice สำหรับ PDF (`winget install TheDocumentFoundation.LibreOffice` / `brew install --cask libreoffice`) |

ถ้าไม่มี Node.js เอกสารยังออกได้ แต่แผนภาพจะเป็นข้อความ ถ้าไม่มี LibreOffice ให้เปิด .docx ใน Word แล้ว Save As PDF แทน

จะรันเตรียมเครื่องเองก่อนก็ได้

```bash
python3 ~/.claude/skills/srs-sds/scripts/setup.py
```

บน Windows ใช้ `py "%USERPROFILE%\.claude\skills\srs-sds\scripts\setup.py"` ส่วน `--check` ใช้ดูสถานะโดยไม่ติดตั้งอะไร

## วิธีใช้
พิมพ์สั่งใน Claude Code พร้อมแนบ TOR เช่น

- "ทำ SRS จาก TOR ไฟล์นี้"
- "ออกแบบระบบและ schema จาก srs.md"
- "ทำเอกสารส่งมอบ SRS และ SDS ให้ครบ ออกเป็น Word และ PDF"

Claude ทำงานทีละขั้น (SRS → ออกแบบ → เอกสารส่งมอบ) และให้ตรวจแต่ละขั้นก่อนไปขั้นต่อไป
ไฟล์ทั้งหมดอยู่ในโฟลเดอร์ `srs-sds-<ชื่อระบบ>/`

| ไฟล์ | เนื้อหา |
|---|---|
| srs.md | ความต้องการ (FR พร้อม acceptance criteria) |
| design.md, schema.sql | สถาปัตยกรรม, API, ตารางข้อมูล (PostgreSQL) |
| srs-doc.md / .docx / .pdf | SRS ฉบับส่งมอบ: ปก, ประวัติการแก้ไข, สารบัญ, กลุ่มผู้ใช้และตารางสิทธิ์, FR/NFR แยกโมดูลอ้างอิงข้อ TOR, ส่วนต่อประสาน, ตารางสอบทานย้อนกลับ |
| sds-doc.md / .docx / .pdf | SDD ฉบับส่งมอบ: ADR, มุมมองสถาปัตยกรรม, โมดูล, หน้าจอ, ฐานข้อมูลและ ER, ความปลอดภัย, API, การติดตั้งและสำรองข้อมูล |

ถ้ามีภาพหน้าจอจริง ให้วางไฟล์ PNG ไว้ในโฟลเดอร์ `screens/` แล้วบอก Claude ให้ใช้ ถ้าไม่มี เอกสารจะเว้นเป็นกรอบ
"ใส่ภาพหน้าจอ" ไว้ให้วางภาพเองภายหลัง

ปกและหัวกระดาษใช้ชื่อบริษัท ที่อยู่ โลโก้ และเลขที่สัญญาที่บอก Claude (วางไฟล์โลโก้ `logo.png` ไว้ในโฟลเดอร์เอกสาร)
ส่วนที่ไม่ได้บอกจะเว้นเป็นเส้นประให้กรอกเอง เปิด .docx ใน Word แล้วกด Yes เมื่อถามเรื่อง update fields
เพื่อให้สารบัญมีเลขหน้า (PDF ที่ออกผ่าน LibreOffice มีเลขหน้าในสารบัญอยู่แล้ว)

แปลงไฟล์เองโดยไม่ผ่าน Claude ก็ได้

```bash
python3 ~/.claude/skills/srs-sds/scripts/md2docx.py sds-doc.md --pdf
```

## ฟอนต์
เอกสารใช้ TH Sarabun New 16 ถ้าเครื่องมีฟอนต์นี้ ถ้าไม่มีจะใช้ Sarabun 11 ซึ่งหน้าตาและขนาดใกล้เคียงกัน
ฟอนต์ Sarabun ในโฟลเดอร์ `fonts/` เป็นของ The Sarabun Project ใช้สัญญาอนุญาต SIL Open Font License 1.1 (ดู `fonts/OFL.txt`)
ถ้าหน่วยงานกำหนดให้ใช้ TH Sarabun New ให้ติดตั้งฟอนต์นั้นก่อนแปลงไฟล์

## ข้อควรรู้
- Claude ไม่เติมความต้องการที่ TOR ไม่มี สิ่งที่ไม่ชัดจะถูกรวบไว้ในหัวข้อ "สมมติฐานและคำถามถึงลูกค้า" ให้ไปถามหน่วยงาน
- ควรอ่านทวนเอกสารทุกฉบับก่อนส่งจริง โดยเฉพาะเลขข้อ TOR และชื่อบทบาท
- ถ้าแผนภาพยังเป็นข้อความ ให้รัน `setup.py` แล้วดูบรรทัด diagrams
