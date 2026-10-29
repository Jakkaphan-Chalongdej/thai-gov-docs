# thai-gov-docs: Claude Code marketplace

| plugin | ใช้ทำอะไร |
|---|---|
| srs-sds | เขียน SRS และ SDS ภาษาไทยแบบหน่วยงานรัฐจาก TOR: ความต้องการ, เอกสารออกแบบระบบกับ schema และเอกสารส่งมอบ ออกเป็น markdown, Word และ PDF |

## ติดตั้งใน Claude Code
พิมพ์ใน Claude Code ครั้งเดียว

```
/plugin install srs-sds --marketplace <REPO>
```

Claude Code ที่เก่ากว่า 2.1.275 ใช้สองบรรทัดนี้แทน

```
/plugin marketplace add <REPO>
/plugin install srs-sds@thai-gov-docs
```

`<REPO>` คือ `owner/repo` ถ้าอยู่บน GitHub หรือ URL ของ git เต็ม (เช่น `https://gitlab.example.com/team/thai-gov-docs.git`)
สำหรับ GitLab และ git อื่น ถ้า repo เป็น private ต้อง clone ด้วย git ในเครื่องได้ก่อน

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

แล้วอัปโหลด `dist/srs-sds.zip` ที่ Settings → Capabilities → Skills (ต้องเปิด code execution) หรือให้ admin ของแผน Team/Enterprise
อัปโหลดให้ทั้งองค์กร บน claude.ai แผนภาพอาจยังเป็นข้อความ เพราะ sandbox ดาวน์โหลด Chrome ของ mermaid-cli ไม่ได้

## ออกรุ่นใหม่
1. แก้ไฟล์ใน `plugins/srs-sds/skills/srs-sds/`
2. เพิ่ม `version` ใน `plugins/srs-sds/.claude-plugin/plugin.json` และใน `.claude-plugin/marketplace.json` ให้ตรงกัน
3. `claude plugin validate .` แล้ว commit และ push
