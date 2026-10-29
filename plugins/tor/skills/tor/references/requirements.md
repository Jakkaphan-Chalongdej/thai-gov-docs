# Writing the scope (ขอบเขตของงาน)

The scope is what the contractor prices and what the inspection committee checks. Each item must be checkable
on the delivered system and open to any product that meets it.

## Structure
- Group the scope by work stream, in the order the work happens: การศึกษาและวิเคราะห์ความต้องการ → การออกแบบ →
  การพัฒนาระบบ (one sub-section per subsystem) → การติดตั้งและทดสอบ → การฝึกอบรม → เอกสารและคู่มือ → (เลือก)
  การจัดหาฮาร์ดแวร์/ซอฟต์แวร์ลิขสิทธิ์ → การรับประกันและบำรุงรักษา.
- Number to at most four levels (6.4.1.1); deeper lists use 1) 2) and then (1) (2). One requirement per item.
- Lead-ins end "ดังนี้" / "อย่างน้อยดังนี้"; an item that lists examples ends "เป็นต้น" or "หรือตามที่[หน่วยงาน]กำหนด".

## One requirement, one check
- System behaviour: "ระบบต้องสามารถ…ได้", "ระบบต้องรองรับ…"; contractor work: "ผู้รับจ้างต้อง…".
- Put the number in when the sources give it: "ไม่น้อยกว่า 200 ผู้ใช้งานพร้อมกัน", "แสดงผลภายใน 3 วินาที", "ไม่น้อยกว่า 16 Dashboard และไม่น้อยกว่า
  11 รายงาน", "จัดเก็บไม่น้อยกว่า 90 วัน". Words like รวดเร็ว, ทันสมัย, ใช้งานง่าย never stand alone: replace them with
  the measure or drop them. A number the sources do not give is not invented: write the requirement without it
  and list "ควรกำหนดตัวเลข: …" to the user (users at once, response time, data volume, retention).
- Ignore TOR item numbers quoted in an SRS or old document: the new TOR numbers its own items.
- Data rules copy the agency's numbers (เลขประจำตัวผู้เสียภาษี 13 หลัก, ไฟล์ไม่เกิน 10 MB).
- Deliverable documents name their content: "เอกสารการออกแบบระบบ (System Design Specification) ประกอบด้วย
  สถาปัตยกรรมระบบ แผนภาพความสัมพันธ์ของข้อมูล (ER Diagram) และพจนานุกรมข้อมูล (Data Dictionary)".
- Training: course, days, trainees and their number: "หลักสูตรการใช้งานสำหรับผู้ดูแลระบบ จำนวนไม่น้อยกว่า 2 วัน
  ให้กับเจ้าหน้าที่ไม่น้อยกว่า 10 คน"; details per course in an appendix (objective, trainees, prerequisites,
  materials received, what trainees can do afterwards).

## Fair competition
- No brand, model or single vendor's feature names. Hardware and software specs state the minimum and add
  "หรือดีกว่า": "หน่วยประมวลผลกลางจำนวนไม่น้อยกว่า 16 แกน (Core) หรือดีกว่า".
- A named product only when the system must work with something the agency already owns, and the sentence says
  so (tools a source mentions in passing, such as a scheduler or a desktop utility, are written by function): "ต้องสามารถเชื่อมต่อกับฐานข้อมูล PostgreSQL ที่[หน่วยงาน]ใช้งานอยู่เดิมได้".
- No requirement that only one vendor can meet (a specific certificate held by one company, an exact model
  number, a dimension that fits one product). If the user asks for one, tell them it narrows competition and
  write the measurable need instead.
- Licences: quantity and type ("ลิขสิทธิ์แบบ Subscription ระยะเวลา 3 ปี จำนวนไม่น้อยกว่า 5 ผู้ใช้งาน").

## Personnel appendix
Table `| ลำดับ | ตำแหน่ง | วุฒิการศึกษา (ขั้นต่ำ) | จำนวน (คน) | ประสบการณ์ (ปี) |`, introduced by "ผู้รับจ้างจะต้องมี
บุคลากรที่มีคุณสมบัติและประสบการณ์ ดังนี้เป็นอย่างน้อย". Typical roles: ผู้จัดการโครงการ, นักวิเคราะห์ระบบ,
นักออกแบบ UX/UI, นักพัฒนาระบบ, นักออกแบบฐานข้อมูล, นักทดสอบระบบ, ผู้เชี่ยวชาญด้านความมั่นคงปลอดภัย. Size it to
the project; the user decides the numbers.
