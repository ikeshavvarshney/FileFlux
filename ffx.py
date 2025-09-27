#!/usr/bin/env python3
import os, sys, shutil, json, mimetypes, argparse, subprocess
from colorama import Fore, Style, init

# Init colorama (Windows safe)
init(autoreset=True)

VERSION = "1.0"
HOME, DB = os.path.expanduser("~"), os.path.join(os.path.expanduser("~"), ".fileflux.json")
SUGGEST = {
    "image/jpeg": "View image", "image/png": "View image",
    "application/pdf": "PDF reader", "application/zip": "Unzip",
    "text/plain": "Text editor"
}

def load_db(): return json.load(open(DB)) if os.path.exists(DB) else {}
def save_db(d): json.dump(d, open(DB,"w"))
def human_size(n):
    for u in ["B","KB","MB","GB","TB"]:
        if n < 1024: return f"{n:.1f} {u}"
        n /= 1024
    return f"{n:.1f} PB"

def detect(path):
    if not os.path.exists(path): return f"{Fore.RED}❌ Not found{Style.RESET_ALL}"
    if os.path.isdir(path): return f"{Fore.BLUE}📁 Directory:{Style.RESET_ALL} {path}"
    size, mime = os.path.getsize(path), mimetypes.guess_type(path)[0] or "binary"
    info = [
        f"{Fore.CYAN}🔍 {path}{Style.RESET_ALL}",
        f"— Size: {Fore.YELLOW}{human_size(size)}{Style.RESET_ALL}",
        f"— Type: {Fore.MAGENTA}{mime}{Style.RESET_ALL}",
        f"— Suggestion: {Fore.GREEN}{SUGGEST.get(mime,'Unknown')}{Style.RESET_ALL}"
    ]
    try:
        details = subprocess.check_output(["file","-b",path], text=True).strip()
        info.append(f"— Details: {Fore.WHITE}{details}{Style.RESET_ALL}")
    except: pass
    return "\n".join(info)

def copy(s,d): shutil.copy2(s,d); print(f"{Fore.GREEN}📄 Copied{Style.RESET_ALL} {s} → {d}")
def cut(s,d): shutil.move(s,d); print(f"{Fore.YELLOW}✂️ Moved{Style.RESET_ALL} {s} → {d}")
def delete(p): (os.remove(p) if os.path.isfile(p) else shutil.rmtree(p)); print(f"{Fore.RED}🗑️ Deleted{Style.RESET_ALL} {p}")
def mkdir(p): os.makedirs(p,exist_ok=True); print(f"{Fore.BLUE}📁 Created{Style.RESET_ALL} {p}")
def rename(s,d): os.rename(s,d); print(f"{Fore.CYAN}✏️ Renamed{Style.RESET_ALL} {s} → {d}")

def main():
    parser=argparse.ArgumentParser(
        prog=f"{Fore.CYAN}ffx{Style.RESET_ALL}",
        description=f"{Fore.YELLOW}FileFlux (ffx){Style.RESET_ALL} - A modern CLI tool for file and path management."
    )
    parser.add_argument("-v","--version",action="version",
        version=f"{Fore.GREEN}ffx version {VERSION}{Style.RESET_ALL}")
    sub=parser.add_subparsers(dest="cmd",help="Available commands")

    sub.add_parser("info",help=f"{Fore.MAGENTA}Show file/folder info{Style.RESET_ALL}").add_argument("file")
    for cmd in ["copy","cut","rename"]:
        s=sub.add_parser(cmd,help=f"{Fore.MAGENTA}{cmd.capitalize()} file/folder{Style.RESET_ALL}")
        s.add_argument("src"); s.add_argument("dst")
    sub.add_parser("delete",help=f"{Fore.MAGENTA}Delete file/folder{Style.RESET_ALL}").add_argument("path")
    sub.add_parser("mkdir",help=f"{Fore.MAGENTA}Create directory{Style.RESET_ALL}").add_argument("path")
    sp=sub.add_parser("save",help=f"{Fore.MAGENTA}Save an alias for path{Style.RESET_ALL}")
    sp.add_argument("alias"); sp.add_argument("path")
    jp=sub.add_parser("jump",help=f"{Fore.MAGENTA}Jump to saved alias{Style.RESET_ALL}")
    jp.add_argument("alias")

    args,db=parser.parse_args(),load_db()
    if args.cmd=="info": print(detect(args.file))
    elif args.cmd=="copy": copy(args.src,args.dst)
    elif args.cmd=="cut": cut(args.src,args.dst)
    elif args.cmd=="delete": delete(args.path)
    elif args.cmd=="mkdir": mkdir(args.path)
    elif args.cmd=="rename": rename(args.src,args.dst)
    elif args.cmd=="save": db[args.alias]=os.path.abspath(os.path.expanduser(args.path)); save_db(db); print(f"{Fore.GREEN}💾 Saved{Style.RESET_ALL} {db[args.alias]} as {Fore.YELLOW}{args.alias}{Style.RESET_ALL}")
    elif args.cmd=="jump": path=db.get(args.alias); print(f"{Fore.CYAN}{path}{Style.RESET_ALL}") if path and os.path.exists(path) else print(f"{Fore.RED}❌ Alias not found or path missing{Style.RESET_ALL}")
    else: parser.print_help()

if __name__=="__main__": main()
