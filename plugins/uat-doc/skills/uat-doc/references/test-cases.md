# Deriving UAT test cases

A UAT case is what an agency tester does at the screen and what must happen, written so a non-developer can
follow it and tick ผ่าน or ไม่ผ่าน. It proves a requirement to the person who will accept the system, so every
case traces to an acceptance criterion (SRS) or to a screen behaviour (SDS), and nothing is tested that the
sources do not promise.

## 1. Functions
One function per menu item or screen group the tester recognises ("Admin Overview", "จัดการผู้ใช้งาน",
"รายการต้องสงสัย"). From an SDS take the screens (SCR-…) of the module in scope; from an SRS take the FRs of the
module; from a manual take its chapters. Order the functions as the tester meets them: sign-in first when it is
in scope, list before detail, create before edit, edit before delete, admin settings last.

## 2. Cases per function
Write the cases each function needs, in this order, and only those the sources support:
1. Display: the tester opens the menu; the screen shows its parts. List every displayed item, column or panel the
   sources name, as dash items under "ประกอบด้วยข้อมูลที่แสดงดังนี้".
2. Each action, the normal path: search and filter (one case per filter group, partial and full search when the
   SRS asks), create, edit, delete or cancel, export (one case per file format group), workflow actions (submit,
   approve, send back, close). State what the tester enters and what the system shows after it.
3. Validation: one case per rule group of a form (required fields, format or length limits with the SRS
   numbers, duplicate values), with the message or behaviour the sources give. A rule with no stated message is
   written as the behaviour ("ระบบไม่บันทึกและแจ้งให้กรอกช่อง …") and the exact message goes to the user as a
   question.
4. Permission: a role without access does not see the menu or the button (from the SRS role matrix), one case
   per function where the matrix differs between roles.
5. Status: each state change the tester can cause, and what it shows elsewhere (the list, a notification, the
   dashboard).

A case is one tester goal, so a create case includes filling the form and saving; split cases when the expected
results differ, not per click. Background behaviour the tester cannot see (replication, a scheduled job) is tested
through what the screen shows of it (the job status, the run log), never by inspecting the database.

## 3. Writing a case
Each case is one row of the function's table (see the layout):
- Number: the row's No runs 1, 2, 3 within the function; the Test Description starts with the same number and the
  case name: "1.การแสดงเมนู Admin Overview", "2.การค้นหาผู้ใช้งาน".
- Then one or two sentences in the sample's voice: "เมื่อผู้ใช้งานต้องการ<เป้าหมาย> ให้เลือกเมนู “<เมนู>” จากนั้น<การ
  กระทำ> ระบบจะ<ผลที่เห็น>ดังภาพ". Preconditions the tester must set up come first ("ลงชื่อเข้าใช้งานด้วยบทบาท
  ผู้ดูแลระบบ", "มีรายการสถานะใหม่อย่างน้อย 1 รายการ").
- Test data the tester types goes in the sentence in quotes, invented as test values only ("ทดสอบ01"), never a real
  person's data.
- Then the image line of the expected screen (or the placeholder), then the displayed items or the checks as dash
  items under a lead-in ending "ดังนี้".
- Menu holds the menu path or the flow name the tester sees ("Admin Overview Flow", "ดูแลระบบ > จัดการผู้ใช้งาน").
- Result is always `[ ] ผ่าน<br>[ ] ไม่ผ่าน`; Remark stays empty for the tester.

## 4. Coverage
When the source is an SRS, every acceptance criterion of the FRs in scope is covered by at least one case; keep
the map for chapter 3 of the layout (FR id, criterion, function and case number). A criterion no screen can show
(an uptime figure, a load test) is not a UAT case: list it to the user as belonging to another test (Operational
Test, Security Test).
