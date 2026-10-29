# Screenshots for the UAT document

Every test case shows the screen the tester should see when the case passes (the expected result). Pick the first route that works:

## 1. The user's own images
The user gives a folder of screenshots (or a prototype export). Match each image to a test case of the screenshot
list by opening it; rename or copy it to `screens/<nn>-<slug>.png` so the order is visible. An image that fits
no test case is reported, not used; files in the folder that are not images are ignored.
- One image per screen state. When two test cases show the same state (the main screen before two different menus),
  the same image may serve both, each with its own box.
- Images that already carry the taker's red marks keep them: add no box on top. Marks that point at the wrong
  control are reported, and a clean image asked for.

## 2. Capture from the running system
Only when a browser tool is available in this session and the user gives the URL.
- Sign-in: the user signs in themselves in the browser, or gives a test account for a test or staging system.
  Never type a real person's password, and never sign in to a production system with your own guesses.
- Use test data only. Do not submit anything that sends real email, real approvals or real payments; for a case
  that would, ask the user to do it or leave a placeholder.
- One capture per test case, the browser window at a steady size (about 1440 × 900) so the screens look alike. Capture
  the page area, not the whole desktop. Hide or blur personal data that is not test data.
- When you can read an element's position (a DOM bounding box), note it for the box on that test case.

## 3. Placeholders
No images and no running system: write `[ภาพหน้าจอ: <ชื่อหน้าจอ>]` where the image goes, keep the caption line,
and give the user the screenshot list (file name, screen, state, control to box) so the images can be added and
the document converted again.

A placeholder means "this screen exists, the picture is missing". A test step that happens outside the system
(preparing files, a staff member doing it on the user's behalf, waiting for an approval) has no screen: write it
as text only, without a placeholder.

## Images inside the test table
The image goes inside the Test Description cell as one of its "<br>" lines; it is printed at the cell's width.
A red box works there too. Write it after the image path:
```
| 1 | เข้าสู่ระบบ | หน้าเข้าสู่ระบบ | 1.การเข้าสู่ระบบ<br>…<br>![หน้าจอเข้าสู่ระบบ](screens/01-login.png){box=820,410,160,48}<br>… | [ ] ผ่าน<br>[ ] ไม่ผ่าน | |
```
- `x,y,width,height` in the image's pixels (check the size with the image open), or in % of the width and
  height: `{box=51%,45%,10%,5%}`. Several boxes: `{box=…; box=…}`.
- Box the one or two controls the test case names, never the whole screen. A screen the case only shows (a result,
  a message) needs no box.
- A popup or small dialog inside a full-window capture prints too small to read: add `crop=x,y,w,h` (same units,
  the area of the dialog plus a margin) so only that part is printed: `{box=…; crop=320,150,700,420}`. Box
  coordinates stay those of the original image.
- The converter draws the box on a copy; the file in `screens/` stays clean.
