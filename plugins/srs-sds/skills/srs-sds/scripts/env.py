"""Where this skill's tools live on Windows, macOS and Linux. Shared by setup.py and md2docx.py (standard library only)."""
import glob
import os
import shutil
import sys
import tempfile

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS_DIR = os.path.join(SKILL_DIR, "fonts")
BRANDS_DIR = os.path.join(SKILL_DIR, "brands")  # one folder per company: brand.yaml + logo
VENV_DIR = os.path.join(SKILL_DIR, ".venv")
TOOLS_DIR = os.path.join(SKILL_DIR, ".tools")  # npm --prefix for mermaid-cli
WINDOWS = sys.platform == "win32"
MAC = sys.platform == "darwin"

# TH Sarabun New 16 pt looks like Sarabun (Google) at about 11 pt: Thai glyphs are 0.40 vs 0.586 of the em.
SARABUN_SCALE = 0.68


def venv_python():
    p = os.path.join(VENV_DIR, "Scripts", "python.exe") if WINDOWS else os.path.join(VENV_DIR, "bin", "python")
    return p if os.path.exists(p) else None


def font_dirs():
    home = os.path.expanduser("~")
    if WINDOWS:
        return [os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts"),
                os.path.join(os.environ.get("LOCALAPPDATA", home), "Microsoft", "Windows", "Fonts")]
    if MAC:
        return ["/System/Library/Fonts", "/Library/Fonts", os.path.join(home, "Library", "Fonts")]
    return ["/usr/share/fonts", "/usr/local/share/fonts", os.path.join(home, ".local", "share", "fonts"),
            os.path.join(home, ".fonts")]


def user_font_dir():
    home = os.path.expanduser("~")
    if WINDOWS:
        return os.path.join(os.environ.get("LOCALAPPDATA", home), "Microsoft", "Windows", "Fonts")
    if MAC:
        return os.path.join(home, "Library", "Fonts")
    return os.path.join(home, ".local", "share", "fonts")


def _has_font(pattern):
    for d in font_dirs():
        if glob.glob(os.path.join(d, "**", pattern), recursive=True):
            return True
    return False


def installed_font():
    """The Thai font the documents use: "TH Sarabun New" when installed, else "Sarabun", else None."""
    if _has_font("THSarabunNew*.ttf"):
        return "TH Sarabun New"
    if _has_font("Sarabun-Regular.ttf"):
        return "Sarabun"
    return None


def find_soffice():
    names = ["soffice", "libreoffice"]
    paths = ["/Applications/LibreOffice.app/Contents/MacOS/soffice"]
    if WINDOWS:
        names = ["soffice.exe", "soffice.com"]
        for base in (os.environ.get("ProgramFiles", r"C:\Program Files"),
                     os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")):
            paths.append(os.path.join(base, "LibreOffice", "program", "soffice.exe"))
    for n in names:
        if shutil.which(n):
            return shutil.which(n)
    for p in paths:
        if os.path.exists(p):
            return p
    return None


def find_mmdc():
    """Command list for mermaid-cli: the copy setup.py installed, mmdc on PATH, else npx (downloads on first use)."""
    local = os.path.join(TOOLS_DIR, "node_modules", ".bin", "mmdc.cmd" if WINDOWS else "mmdc")
    if os.path.exists(local):
        return [local]
    if shutil.which("mmdc"):
        return [shutil.which("mmdc")]
    if shutil.which("npx"):
        return [shutil.which("npx"), "-y", "@mermaid-js/mermaid-cli"]
    return None


def fontconfig_env(env):
    """LibreOffice and Chrome on macOS/Linux read fontconfig. A user fonts.conf without the system font folders (one
    written for another OS) hides every Thai font, so point them at a config with the system folders and the fonts
    bundled with this skill. Returns (env, temp dir to remove)."""
    if WINDOWS or "FONTCONFIG_FILE" in env:
        return env, None
    tmp = tempfile.mkdtemp(prefix="srs-sds-fc-")
    dirs = "".join(f"<dir>{d}</dir>" for d in font_dirs() + [FONTS_DIR] if os.path.isdir(d))
    conf = os.path.join(tmp, "fonts.conf")
    with open(conf, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd"><fontconfig>'
                f"{dirs}<cachedir>{tmp}/cache</cachedir></fontconfig>")
    env = dict(env)
    env["FONTCONFIG_FILE"] = conf
    return env, tmp
