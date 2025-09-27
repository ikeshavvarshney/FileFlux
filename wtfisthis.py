#!/usr/bin/env python3
import argparse, os, sys, mimetypes, subprocess

# Common magic numbers
MAGIC = {
    b"\x89PNG": ("image/png", "PNG image"),
    b"\xFF\xD8\xFF": ("image/jpeg", "JPEG image"),
    b"%PDF": ("application/pdf", "PDF document"),
    b"PK": ("application/zip", "ZIP archive"),
    b"7z\xBC\xAF\x27\x1C": ("application/x-7z-compressed", "7z archive"),
    b"Rar!": ("application/x-rar-compressed", "RAR archive"),
    b"\x1F\x8B": ("application/gzip", "GZIP archive"),
    b"\x7FELF": ("application/x-executable", "ELF binary"),
}

SUGGEST = {
    "image/jpeg": "Open with any image viewer",
    "image/png": "Open with any image viewer",
    "application/pdf": "Open with a PDF reader",
    "application/zip": "Extract with unzip/WinRAR",
    "application/x-7z-compressed": "Extract with 7zip",
    "application/x-rar-compressed": "Extract with WinRAR/7zip",
    "application/gzip": "Extract with gunzip",
    "application/x-executable": "Run on Linux/Unix systems",
    "text/plain": "Open with a text editor",
}

def human_size(n):
    for unit in ["B","KB","MB","GB","TB"]:
        if n < 1024: return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"

def detect_magic(path):
    with open(path, 'rb') as f:
        head = f.read(16)
    for sig,(mime,desc) in MAGIC.items():
        if head.startswith(sig):
            return mime,desc
    return None,None

def detect_mime(path):
    mime, _ = mimetypes.guess_type(path)
    return mime or "application/octet-stream"

def detect_encoding(path):
    try:
        with open(path,'rb') as f:
            raw=f.read(2048)
        raw.decode('utf-8')
        return 'utf-8'
    except:
        return 'binary'

def fallback_file(path):
    try:
        out = subprocess.check_output(["file","-b",path],text=True)
        return out.strip()
    except: return None

def analyze(path,details=False):
    if not os.path.exists(path):
        print(f"❌ {path}: File not found")
        return
    if os.path.isdir(path):
        print(f"📁 {path}: directory")
        return
    size=os.path.getsize(path)
    mime_guess,desc=detect_magic(path)
    if not mime_guess:
        mime_guess=detect_mime(path)
        desc=os.path.splitext(path)[1].lstrip('.') or "Unknown"
    encoding=detect_encoding(path)
    suggestion=SUGGEST.get(mime_guess,"No suggestion available")
    print(f"\n🔍 {path}")
    print(f"— Size: {human_size(size)}")
    print(f"— Type: {desc}")
    print(f"— MIME: {mime_guess}")
    print(f"— Encoding: {encoding}")
    print(f"— Suggestion: {suggestion}")
    if details:
        extra=fallback_file(path)
        if extra: print(f"— Details: {extra}")

def main():
    p=argparse.ArgumentParser(description="wtfisthis: Universal File Detective")
    p.add_argument("files",nargs="+",help="File(s) to analyze")
    p.add_argument("--details",action="store_true",help="Show extra info using system 'file'")
    args=p.parse_args()
    for f in args.files: analyze(f,args.details)

if __name__=="__main__":
    main()
