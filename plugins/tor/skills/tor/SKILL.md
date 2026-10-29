---
name: tor
description: ร่างขอบเขตของงาน (TOR / Terms of Reference) ภาษาไทยสำหรับจัดจ้างพัฒนาหรือจัดหาระบบสารสนเทศของหน่วยงานรัฐ จากความต้องการ บันทึกการประชุม หรือ TOR เดิม ตามโครงที่ใช้จริง (หลักการและเหตุผล วัตถุประสงค์ คุณสมบัติผู้ยื่นข้อเสนอ ขอบเขตของงาน ระยะเวลา วงเงิน งวดงานและการจ่ายเงิน ค่าปรับ การรับประกัน ข้อสงวนสิทธิ์ ภาคผนวกบุคลากรและการฝึกอบรม) เขียนข้อกำหนดที่วัดได้และไม่ล็อกยี่ห้อ ออกเป็น Word/PDF มีเลขหน้าและช่องลงนามคณะกรรมการทุกหน้า ใช้เมื่อผู้ใช้ขอร่าง TOR ขอบเขตของงาน ร่างขอบเขตงาน spec จัดซื้อจัดจ้างระบบ หรือแก้ไข TOR
---
# Drafting a Thai government TOR

Drafts the ขอบเขตของงาน an agency publishes to hire a contractor for an information system, in the shape real
signed TORs use. The draft is the committee's working text: the agency's procurement officer checks it against
the current regulations and templates before it is published.

## 1. Facts first
Read what the user gives (a brief, meeting notes, an old TOR, an SRS, a budget request). Then ask once, in one
list, for what is missing; offer a sensible default in brackets for each so the user can just confirm:
- Agency (full name and short name used in the text), project name, fiscal year, the seal image if any.
- Budget in baht and its source (งบประมาณรายจ่ายประจำปี …), procurement method (e-bidding, วิธีคัดเลือก,
  เฉพาะเจาะจง), award criterion: price only (เกณฑ์ราคา), or price performance and its criteria.
- Duration (days from contract signing), place of work and installation.
- Scope: the users and what the system must do, data, integrations with existing systems, the hardware or
  licences to supply, numbers that matter (users, records, reports, response time), security needs.
- Deliverables and instalments (how many, % each, deadline in days), training (courses, days, trainees),
  documents and copies, warranty period and response times, late fine rate, past-work and personnel rules.
- Drafting committee: names and positions for the signature lines.
Never invent a budget, a legal threshold, a person or an existing system. A value the user leaves open goes into
the draft as `[ระบุ…]` and into the list you report.

## 2. Outline, then write
Follow the layout `layouts/<layout>/tor.md` (only [standard](layouts/standard/tor.md) today) and its
[examples](layouts/standard/examples-tor.md). Show the section list with the scope sub-sections to the user
first, then write `tor.md` in a folder the user names, else `./tor-<ชื่อโครงการสั้น>/`.
- Standard clauses (qualifications, general terms, fines, warranty, reservation of rights, IT security,
  copyright): [references/clauses.md](references/clauses.md). Fill every `[…]`; keep the wording.
- The scope and specifications: [references/requirements.md](references/requirements.md). Every requirement is
  checkable at acceptance and open to more than one product.

## 3. Word / PDF
```
python3 <skill-dir>/scripts/setup.py          # once per machine
python3 <skill-dir>/scripts/md2docx.py tor.md --pdf
```
`<skill-dir>` is this skill's folder (Windows: `py`). The front matter (`cover: tor`) gives the title block,
page numbers at the top from page 2 and the committee's signature lines on every page; `thai_digits: yes` prints
the numbers as ๑๒๓. Report what stderr says was missing.

## Final check
- All sections of the layout present and numbered in sequence; sub-items numbered under their section.
- Every `[…]` filled or reported; budget, duration, instalment % (sum 100) and deadlines agree everywhere they
  appear (sections on duration, budget, instalments and the deliverables table).
- Scope items are measurable, name no brand except a stated existing system, and each deliverable named in the
  instalments exists in the scope.
- Tell the user the draft must be checked by the agency's procurement officer against the current regulations,
  and that its scope numbers (๖.x.x) are the TOR item numbers an SRS will cite later (the srs-sds skill).
