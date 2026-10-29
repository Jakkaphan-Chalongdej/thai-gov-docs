#!/usr/bin/env python3
"""Gets this machine ready to turn the skill's markdown into Word/PDF, then reports what works.

    python3 setup.py           install what it can, then report   (Windows: py setup.py)
    python3 setup.py --check   report only

Installs only inside the skill folder or the user's own font folder, never system-wide:
  python-docx      -> <skill>/.venv (only when the current Python lacks it)
  mermaid-cli      -> <skill>/.tools (needs Node.js; downloads a headless Chrome once, ~150 MB)
  Sarabun font     -> the user's font folder (only when neither TH Sarabun New nor Sarabun is installed)
LibreOffice (for PDF) and Node.js cannot be installed from here: the report prints the command for this OS.
Exit code 0 when .docx output works.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import venv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import env  # noqa: E402

MERMAID_CLI = "@mermaid-js/mermaid-cli@11.4.2"

HINTS = {
    "node": {"win32": "winget install OpenJS.NodeJS.LTS", "darwin": "brew install node",
             "linux": "sudo apt install nodejs npm   (or your distro's package)"},
    "soffice": {"win32": "winget install TheDocumentFoundation.LibreOffice",
                "darwin": "brew install --cask libreoffice",
                "linux": "sudo apt install libreoffice-writer   (or your distro's package)"},
}


def hint(tool):
    key = sys.platform if sys.platform in ("win32", "darwin") else "linux"
    return HINTS[tool][key]


def has_docx(python):
    return subprocess.run([python, "-c", "import docx"], capture_output=True).returncode == 0


def setup_docx(check):
    if has_docx(sys.executable):
        return True, "python-docx in " + sys.executable
    py = env.venv_python()
    if py and has_docx(py):
        return True, "python-docx in " + env.VENV_DIR
    if check:
        return False, "python-docx missing (run setup.py without --check)"
    print("installing python-docx into", env.VENV_DIR, flush=True)
    try:
        venv.create(env.VENV_DIR, with_pip=True, clear=True)
        py = env.venv_python()
        subprocess.run([py, "-m", "pip", "install", "--quiet", "--disable-pip-version-check", "python-docx"], check=True)
    except (OSError, subprocess.CalledProcessError) as e:
        return False, f"python-docx install failed: {e}"
    return True, "python-docx in " + env.VENV_DIR


def install_fonts():
    dest = env.user_font_dir()
    os.makedirs(dest, exist_ok=True)
    files = [f for f in os.listdir(env.FONTS_DIR) if f.endswith(".ttf")]
    for f in files:
        shutil.copy2(os.path.join(env.FONTS_DIR, f), os.path.join(dest, f))
    if env.WINDOWS:
        # a per-user font needs its registry entry before Word and LibreOffice list it
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows NT\CurrentVersion\Fonts", 0,
                            winreg.KEY_SET_VALUE) as key:
            for f in files:
                name = os.path.splitext(f)[0].replace("-", " ") + " (TrueType)"
                winreg.SetValueEx(key, name, 0, winreg.REG_SZ, os.path.join(dest, f))
    elif not env.MAC and shutil.which("fc-cache"):
        subprocess.run(["fc-cache", "-f", dest], capture_output=True)
    return dest


def setup_fonts(check):
    font = env.installed_font()
    if font:
        return True, font + " installed"
    if check:
        return False, "no Thai font (setup installs the bundled Sarabun)"
    try:
        dest = install_fonts()
    except OSError as e:
        return False, f"font install failed: {e}"
    return True, "Sarabun installed into " + dest + " (open Word again to see it)"


def npm_install(npm, cache=None):
    cmd = [npm, "install", "--prefix", env.TOOLS_DIR, "--no-audit", "--no-fund", "--loglevel", "error", MERMAID_CLI]
    e = dict(os.environ)
    if cache:
        e["npm_config_cache"] = cache
    return subprocess.run(cmd, env=e, capture_output=True, text=True, errors="replace")


def try_render(cmd):
    tmp = tempfile.mkdtemp(prefix="srs-sds-check-")
    try:
        src, out = os.path.join(tmp, "t.mmd"), os.path.join(tmp, "t.png")
        with open(src, "w", encoding="utf-8") as f:
            f.write('flowchart LR\n  a["ทดสอบ"] --> b["ระบบ"]\n')
        e, fc = env.fontconfig_env(os.environ)
        r = subprocess.run(cmd + ["-i", src, "-o", out], env=e, capture_output=True, text=True, errors="replace",
                           timeout=300)
        if fc:
            shutil.rmtree(fc, ignore_errors=True)
        return os.path.exists(out), (r.stderr or r.stdout).strip()[-300:]
    except (OSError, subprocess.SubprocessError) as e:
        return False, str(e)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def setup_mermaid(check):
    cmd = env.find_mmdc()
    if cmd and cmd[0].endswith(("mmdc", "mmdc.cmd")):
        ok, err = try_render(cmd)
        return ok, "mermaid-cli works" if ok else "mermaid-cli fails: " + err
    npm = shutil.which("npm")
    if not npm:
        return False, "Node.js missing: diagrams stay as text. Install: " + hint("node")
    if check:
        return False, "mermaid-cli not installed (run setup.py without --check)"
    print("installing mermaid-cli into", env.TOOLS_DIR, "(first time downloads Chrome, a few minutes)", flush=True)
    r = npm_install(npm)
    if r.returncode != 0:
        # a broken ~/.npm cache (wrong owner) is common; a private cache sidesteps it
        r = npm_install(npm, tempfile.mkdtemp(prefix="srs-sds-npm-"))
    if r.returncode != 0:
        return False, "mermaid-cli install failed: " + (r.stderr or r.stdout).strip()[-300:]
    ok, err = try_render(env.find_mmdc())
    return ok, "mermaid-cli works" if ok else "mermaid-cli installed but fails: " + err


def setup_pdf():
    exe = env.find_soffice()
    if exe:
        return True, "LibreOffice at " + exe
    return False, "LibreOffice missing: no PDF (or open the .docx in Word and Save As PDF). Install: " + hint("soffice")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    ap = argparse.ArgumentParser(description="prepare Word/PDF output for the srs-sds skill")
    ap.add_argument("--check", action="store_true", help="report only, install nothing")
    a = ap.parse_args()
    rows = [("docx", *setup_docx(a.check)), ("font", *setup_fonts(a.check)),
            ("diagrams", *setup_mermaid(a.check)), ("pdf", *setup_pdf())]
    print()
    for name, ok, msg in rows:
        print(f"{'ok' if ok else 'MISSING':8} {name:9} {msg}")
    sys.exit(0 if rows[0][1] else 1)


if __name__ == "__main__":
    main()
