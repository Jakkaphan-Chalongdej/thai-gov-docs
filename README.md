# thai-gov-docs: Claude Code marketplace

| plugin | ใช้ทำอะไร |
|---|---|
| tor | ร่างขอบเขตของงาน (TOR) จัดจ้างระบบสารสนเทศของหน่วยงานรัฐ ตามโครงที่ใช้จริง พร้อมข้อความมาตรฐาน เลขไทย และช่องลงนามคณะกรรมการทุกหน้า ออกเป็น Word และ PDF |
| srs-sds | เขียน SRS และ/หรือ SDS ภาษาไทยแบบหน่วยงานรัฐจาก TOR: ความต้องการ, เอกสารออกแบบระบบกับ schema และเอกสารส่งมอบตามแบรนด์บริษัท ออกเป็น markdown, Word และ PDF |
| user-manual | เขียนคู่มือการใช้งานระบบทีละขั้นพร้อมภาพหน้าจอและกรอบเน้นจุดที่ต้องคลิก จาก SRS/SDS ต้นแบบ หรือระบบที่รันอยู่ ออกเป็น Word และ PDF ตามแบรนด์บริษัท |

## ติดตั้งใน Claude Code
พิมพ์ใน Claude Code ครั้งเดียว

```
/plugin install tor --marketplace Jakkaphan-Chalongdej/thai-gov-docs
/plugin install srs-sds --marketplace Jakkaphan-Chalongdej/thai-gov-docs
/plugin install user-manual --marketplace Jakkaphan-Chalongdej/thai-gov-docs
```

Claude Code ที่เก่ากว่า 2.1.275 ใช้บรรทัดเหล่านี้แทน

```
/plugin marketplace add Jakkaphan-Chalongdej/thai-gov-docs
/plugin install tor@thai-gov-docs
/plugin install srs-sds@thai-gov-docs
/plugin install user-manual@thai-gov-docs
```

รับรุ่นใหม่ได้ด้วย

```
/plugin marketplace update thai-gov-docs
```

ถ้าเคยแตก zip ไว้ที่ `~/.claude/skills/srs-sds` ให้ลบโฟลเดอร์นั้นออก ไม่อย่างนั้น skill จะซ้ำกันสองชุด

ครั้งแรกที่ขอ Word/PDF Claude จะรัน `setup.py` ของ skill เพื่อเตรียมเครื่อง (python-docx, mermaid-cli, ฟอนต์ Sarabun) และบอกคำสั่งติดตั้งสิ่งที่ต้องลงเอง (Node.js, LibreOffice)
รายละเอียดอยู่ใน [plugins/srs-sds/skills/srs-sds/README.md](plugins/srs-sds/skills/srs-sds/README.md)

## ใช้บน claude.ai
plugin marketplace ใช้ได้เฉพาะ Claude Code บน claude.ai ให้ใช้ไฟล์ zip ของ skill แทน

```bash
scripts/build-zip.sh
```

แล้วอัปโหลด `dist/<skill>.zip` (เช่น `dist/tor.zip`, `dist/srs-sds.zip`, `dist/user-manual.zip`) ที่ Settings → Capabilities → Skills (ต้องเปิด code execution) หรือให้ admin ของแผน Team/Enterprise
อัปโหลดให้ทั้งองค์กร บน claude.ai แผนภาพอาจยังเป็นข้อความ เพราะ sandbox ดาวน์โหลด Chrome ของ mermaid-cli ไม่ได้

## โครงสร้าง
```
shared/                    ต้นฉบับที่ทุก skill ใช้ร่วม (แก้ที่นี่ที่เดียว)
  scripts/                 md2docx.py (markdown → Word/PDF), setup.py, env.py
  fonts/                   Sarabun (OFL)
  brands/<บริษัท>/         brand.yaml (ชื่อ ที่อยู่ ติดต่อ สี layout) + logo.png
plugins/<plugin>/skills/<skill>/
  SKILL.md, references/    ขั้นตอนของเอกสารชนิดนั้น
  layouts/<layout>/        โครงบทและตัวอย่างสำนวนของแต่ละแบบ
  scripts/ fonts/ brands/  สำเนาจาก shared/ (สร้างด้วย sync-shared.sh ห้ามแก้ตรงนี้)
scripts/sync-shared.sh     คัดลอก shared/ เข้าทุก skill (--check ตรวจว่าตรงกัน)
scripts/build-zip.sh       sync แล้วสร้าง dist/<skill>.zip
```
แต่ละ skill ต้องมีสำเนาของตัวเอง เพราะการติดตั้ง plugin และ zip บน claude.ai ใช้เฉพาะโฟลเดอร์ของ skill นั้น

### เพิ่มบริษัท (แบรนด์)
สร้าง `shared/brands/<ชื่อ>/` ที่มี `brand.yaml` (คัดลอกจาก contumeliax แล้วแก้) และ `logo.png`
จากนั้นรัน `scripts/sync-shared.sh` เอกสารที่ใส่ `brand: <ชื่อ>` จะใช้ปก หัวกระดาษ และโลโก้ของบริษัทนั้น

### เพิ่มแบบเอกสาร (layout)
คัดลอก `plugins/srs-sds/skills/srs-sds/layouts/contumeliax/` เป็นชื่อใหม่ แก้โครงบทและตัวอย่าง แล้วตั้ง
`layout: <ชื่อ>` ใน brand.yaml ของบริษัทที่ใช้แบบนั้น

## ออกรุ่นใหม่
1. แก้ไฟล์ใน `shared/` หรือใน skill (ยกเว้นโฟลเดอร์สำเนา scripts/ fonts/ brands/) แล้วรัน `scripts/sync-shared.sh`
2. เพิ่ม `version` ใน `plugins/<plugin>/.claude-plugin/plugin.json` และใน `.claude-plugin/marketplace.json` ให้ตรงกัน
3. `scripts/sync-shared.sh --check` และ `claude plugin validate .` แล้ว commit และ push
