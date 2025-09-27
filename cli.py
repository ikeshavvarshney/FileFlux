#!/usr/bin/env python3
import argparse, os, mimetypes, subprocess

# Suggestions for common file types
SUGGEST = {
    "image/jpeg": "Open with any image viewer",
    "image/png": "Open with any image viewer",
    "application/pdf": "Open with a PDF reader",
    "application/zip": "Extract with unzip/WinRAR",
    "text/plain": "Open with a text editor",
}

def human_size(n):
    for unit in ["B","KB","MB","GB"]:
        if n < 1024: return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"

def analyze(path, details=False):
    if not os.path.exists(path):
        return f"❌ File not found: {path}"
    if os.path.isdir(path):
        return f"📁 {path} is a directory"
    size = os.path.getsize(path)
    mime, _ = mimetypes.guess_type(path)
    mime = mime or "application/octet-stream"
    info = [
        f"🔍 {path}",
        f"— Size: {human_size(size)}",
        f"— Type: {mime}",
        f"— Suggestion: {SUGGEST.get(mime,'No suggestion available')}"
    ]
    if details:
        try:
            out = subprocess.check_output(["file","-b",path], text=True)
            info.append(f"— Details: {out.strip()}")
        except:
            info.append("— Details: N/A")
    return "\n".join(info)

def main():
    p = argparse.ArgumentParser(prog="wtfisthis", description="Universal File Detective")
    p.add_argument("files", nargs="+", help="File(s) to analyze")
    p.add_argument("--details", action="store_true", help="Show extra info using system 'file'")
    args = p.parse_args()
    for f in args.files:
        print(analyze(f, args.details))

if __name__ == "__main__":
    main()
