#!/usr/bin/env python3
"""Captures a web page as a sharp, high-density screenshot for a manual or a UAT document.

    python3 capture.py https://staging.example.go.th/login screens/01-login.png
    python3 capture.py URL out.png --scale 3 --size 1440x900 --wait 8
    python3 capture.py URL --login                    # opens Chrome to sign in once; close it when done

The page is drawn by headless Chrome at --scale pixels per screen point (default 2, as a Retina screen), so a
1440 x 900 window gives a 2880 x 1800 picture whose text stays crisp when printed at 16.5 cm. The file records
144 dpi (72 x scale), which md2docx.py reads to print it at its natural size.

Sign-in: --login opens a normal Chrome window on a separate profile (--profile, default .capture-profile beside
the output, or in the current folder); the user signs in there themselves and closes the window. Later captures
use the same profile, so they see the signed-in pages. Use test or staging systems and test accounts only.

Needs Chrome, Chromium or Edge (or the Chrome that mermaid-cli downloaded); set CHROME to choose one.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import env  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("url")
    ap.add_argument("out", nargs="?", help="PNG to write (not needed with --login)")
    ap.add_argument("--scale", type=float, default=2, help="pixels per screen point (2 = Retina, 3 = sharper)")
    ap.add_argument("--size", default="1440x900", help="browser window in screen points, WIDTHxHEIGHT")
    ap.add_argument("--wait", type=float, default=5, help="seconds the page may take to finish drawing")
    ap.add_argument("--profile", help="Chrome profile folder that keeps the sign-in")
    ap.add_argument("--login", action="store_true", help="open a visible Chrome to sign in, then close it")
    ap.add_argument("--dark", action="store_true", help="the page's dark mode (default: light, whatever the OS uses)")
    args = ap.parse_args()

    chrome = env.find_chrome()
    if not chrome:
        sys.exit("Chrome, Chromium or Edge not found: install Chrome, run scripts/setup.py (mermaid-cli brings one), "
                 "or set CHROME to the browser's path")
    base = os.path.dirname(os.path.abspath(args.out)) if args.out else os.getcwd()
    profile = os.path.abspath(args.profile or os.path.join(base, ".capture-profile"))
    os.makedirs(profile, exist_ok=True)
    common = [f"--user-data-dir={profile}", "--no-first-run", "--no-default-browser-check"]

    if args.login:
        print(f"Sign in in the Chrome window, then close it. Profile: {profile}")
        subprocess.run([chrome] + common + ["--new-window", args.url])
        return
    if not args.out:
        sys.exit("give the PNG to write, e.g. screens/01-login.png")

    width, height = (int(x) for x in args.size.lower().split("x"))
    out = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="capture-")
    shot = os.path.join(tmp, "shot.png")
    cmd = [chrome] + common + [
        "--headless=new", "--hide-scrollbars", "--disable-gpu", f"--window-size={width},{height}",
        f"--force-device-scale-factor={args.scale}", f"--blink-settings=preferredColorScheme={0 if args.dark else 1}", f"--virtual-time-budget={int(args.wait * 1000)}",
        f"--screenshot={shot}", args.url]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120 + args.wait)
    if not os.path.exists(shot):
        sys.exit(f"no screenshot taken: {(r.stderr or r.stdout).strip()[-400:]}")
    try:
        from PIL import Image
        im = Image.open(shot)
        # the dpi tells md2docx.py the pixel density, so the picture prints at its natural size
        im.save(out, dpi=(72 * args.scale, 72 * args.scale))
        size = im.size
    except ImportError:
        os.replace(shot, out)
        size = None
        print("Pillow missing (run scripts/setup.py): the density is not recorded, md2docx.py guesses it",
              file=sys.stderr)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"{out}" + (f"  {size[0]} x {size[1]} px" if size else ""))


if __name__ == "__main__":
    main()
