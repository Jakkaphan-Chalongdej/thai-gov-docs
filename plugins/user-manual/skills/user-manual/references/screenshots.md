# Screenshots for the manual

Every step shows the screen the user sees at that moment. Pick the first route that works:

## 1. The user's own images
The user gives a folder of screenshots (or a prototype export). Match each image to a step of the screenshot
list by opening it; rename or copy it to `screens/<nn>-<slug>.png` so the order is visible. An image that fits
no step is reported, not used; files in the folder that are not images are ignored.
- One image per screen state. When two steps show the same state (the main screen before two different menus),
  the same image may serve both, each with its own box.
- Sharp pictures come from 2× captures: a Retina Mac (Cmd+Shift+4, or Cmd+Shift+5 for a window) or Windows at
  200 % display scaling. The converter reads the density from the file and warns about any picture that will print
  below 200 ppi; ask for those to be taken again rather than enlarging them, which adds no detail.
- Images that already carry the taker's red marks keep them: add no box on top. Marks that point at the wrong
  control are reported, and a clean image asked for.

## 2. Capture from the running system
When the user gives the URL of a test or staging system. Capture with the bundled script, which draws the page in
Chrome at 2× pixel density (as a Retina screen) and records it in the file, so the converter prints it sharp and at
its natural size:
```
python3 <skill-dir>/scripts/capture.py <URL> screens/01-login.png            # 2880 × 1800 from a 1440 × 900 window
python3 <skill-dir>/scripts/capture.py <URL> screens/05-report.png --scale 3 # dense tables or small text
```
- Sign-in: `capture.py <sign-in URL> --login` opens a Chrome window on the capture profile; the user signs in there
  themselves and closes it, and later captures are signed in. Or the user gives a test account for a test or
  staging system. Never type a real person's password, and never sign in to a production system with your own
  guesses.
- A screen that needs clicks to reach (a dialog, a filled form, a second tab) cannot be reached by the script: use a
  browser tool when this session has one and the user's own capture otherwise (route 1), or leave a placeholder.
  Never save the scaled-down preview a browser tool shows you as the picture.
- Use test data only. Do not submit anything that sends real email, real approvals or real payments; for a step
  that would, ask the user to do it or leave a placeholder.
- One capture per step, the same `--size` (default 1440x900) for all so the screens look alike. Pages follow
  light mode unless `--dark`. Hide or blur personal data that is not test data.
- A step about one part of a busy screen: add `crop=` around that part (see Boxes) so its text prints larger.
- When you can read an element's position (a DOM bounding box), note it for the box on that step; in a 2×
  capture the box's pixel numbers are twice the page's CSS pixels.

## 3. Placeholders
No images and no running system: write `[ภาพหน้าจอ: <ชื่อหน้าจอ>]` where the image goes, keep the caption line,
and give the user the screenshot list (file name, screen, state, control to box) so the images can be added and
the manual converted again.

A placeholder means "this screen exists, the picture is missing". A step that happens outside the system
(preparing files, a staff member doing it on the user's behalf, waiting for an approval) has no screen: write it
as text only, without a placeholder.

## Boxes
The control the step tells the user to click or fill gets a red box. Write it after the image line:
```
![หน้าจอเข้าสู่ระบบ](screens/01-login.png){box=820,410,160,48}
```
- `x,y,width,height` in the image's pixels (check the size with the image open), or in % of the width and
  height: `{box=51%,45%,10%,5%}`. Several boxes: `{box=…; box=…}`.
- Box the one or two controls the step names, never the whole screen. A screen the step only shows (a result,
  a message) needs no box.
- A popup or small dialog inside a full-window capture prints too small to read: add `crop=x,y,w,h` (same units,
  the area of the dialog plus a margin) so only that part is printed: `{box=…; crop=320,150,700,420}`. Box
  coordinates stay those of the original image.
- The converter draws the box on a copy; the file in `screens/` stays clean.
