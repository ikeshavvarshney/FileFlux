#!/usr/bin/env python3
import os, sys, shutil, json, mimetypes, argparse, subprocess
from colorama import Fore, Style, init; init(autoreset=True)

VERSION = "1.0"
AUTHOR = "Keshav Varshney"
REPO = "https://github.com/ikeshavvarshney/FileFlux"
HOME, DB = os.path.expanduser("~"), os.path.join(os.path.expanduser("~"), ".fileflux.json")
SUGGEST = {"image/jpeg":"View image","image/png":"View image","application/pdf":"PDF reader",
           "application/zip":"Unzip","text/plain":"Text editor"}

def load_db(): return json.load(open(DB)) if os.path.exists(DB) else {}
def save_db(d): json.dump(d, open(DB,"w"))
def human_size(n):
    for u in ["B","KB","MB","GB","TB"]:
        if n<1024: return f"{n:.1f} {u}"; n/=1024
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
def delete(p):(os.remove(p) if os.path.isfile(p) else shutil.rmtree(p)); print(f"{Fore.RED}🗑️ Deleted{Style.RESET_ALL} {p}")
def mkdir(p): os.makedirs(p,exist_ok=True); print(f"{Fore.BLUE}📁 Created{Style.RESET_ALL} {p}")
def rename(s,d): os.rename(s,d); print(f"{Fore.CYAN}✏️ Renamed{Style.RESET_ALL} {s} → {d}")

def searchtext(path, query, all=False, ignore=True):
    path = os.path.abspath(path)
    files=[]
    for root,_,fs in os.walk(path):
        for f in fs:
            if ignore and os.path.exists(os.path.join(root,".gitignore")): continue
            fp = os.path.join(root,f)
            try:
                with open(fp,"r",errors="ignore") as fi:
                    for i, l in enumerate(fi):
                        if query in l:
                            files.append((fp, i+1, l.strip()))
                            if not all: break
            except: pass
            if files and not all: break
    return files

def searchfile(path, pattern, exclude=[]):
    path = os.path.abspath(path)
    res=[]
    for root,_,fs in os.walk(path):
        for f in fs:
            if pattern in f and not any(e in root for e in exclude):
                res.append(os.path.join(root,f))
    return res

def show_logo():
    logo = f"""
{Fore.CYAN}███████╗██╗ ██████╗██╗ ██████╗██╗     ██╗██╗  ██╗{Style.RESET_ALL}
{Fore.YELLOW}██╔════╝██║██╔════╝██║██╔════╝██║     ██║╚██╗██╔╝{Style.RESET_ALL}
{Fore.MAGENTA}█████╗  ██║██║     ██║██║     ██║     ██║ ╚███╔╝{Style.RESET_ALL}
{Fore.GREEN}██╔══╝  ██║██║     ██║██║     ██║     ██║ ██╔██╗{Style.RESET_ALL}
{Fore.CYAN}██║     ██║╚██████╗██║╚██████╗███████╗██║██╔╝ ██╗{Style.RESET_ALL}
{Fore.YELLOW}╚═╝     ╚═╝ ╚═════╝╚═╝ ╚═════╝╚══════╝╚═╝╚═╝  ╚═╝{Style.RESET_ALL}
{Fore.MAGENTA}Author: Keshav Varshney | Version: 1.0{Style.RESET_ALL}
{Fore.CYAN}Repo: https://github.com/ikeshavvarshney/FileFlux{Style.RESET_ALL}
"""
    print(logo)

def main():
    parser = argparse.ArgumentParser(prog=f"{Fore.CYAN}ffx{Style.RESET_ALL}", add_help=False)
    parser.add_argument("-v","--version", action="version", version=VERSION)
    parser.add_argument("-h","--help", action="store_true")
    sub = parser.add_subparsers(dest="cmd")

    # standard commands
    sub.add_parser("info").add_argument("file")
    for cmd in ["copy","cut","rename"]: s=sub.add_parser(cmd); s.add_argument("src"); s.add_argument("dst")
    sub.add_parser("delete").add_argument("path"); sub.add_parser("mkdir").add_argument("path")
    sp=sub.add_parser("save"); sp.add_argument("alias"); sp.add_argument("path")
    jp=sub.add_parser("jump"); jp.add_argument("alias"); us=sub.add_parser("unsave"); us.add_argument("alias")
    sub.add_parser("showpaths")

    # search commands
    st=sub.add_parser("searchtext"); st.add_argument("query"); st.add_argument("path", nargs="?", default=os.getcwd())
    st.add_argument("--all","-a",action="store_true"); st.add_argument("--in-ignore",action="store_true")
    sf=sub.add_parser("searchfile"); sf.add_argument("pattern"); sf.add_argument("path", nargs="?", default=os.getcwd())
    sf.add_argument("--exclude","-e", nargs="*")

    args, db = parser.parse_args(), load_db()

    if len(sys.argv)==1: show_logo(); return
    if args.help: 
        show_logo()
        print(f"{Fore.YELLOW}DESCRIPTION:{Style.RESET_ALL}\n"
              "• FileFlux is a modern CLI for managing files and paths.\n"
              "• Save and jump to frequently used paths.\n"
              "• Search text inside files with searchtext.\n"
              "• Find files by name with searchfile.\n"
              f"• Author: {AUTHOR}\n• Version: {VERSION}\n• Repo: {Fore.CYAN}{REPO}{Style.RESET_ALL}\n")
        parser.print_help()
        return

    if args.cmd=="info": print(detect(args.file))
    elif args.cmd=="copy": copy(args.src,args.dst)
    elif args.cmd=="cut": cut(args.src,args.dst)
    elif args.cmd=="delete": delete(args.path)
    elif args.cmd=="mkdir": mkdir(args.path)
    elif args.cmd=="rename": rename(args.src,args.dst)
    elif args.cmd=="save": db[args.alias]=os.path.abspath(os.path.expanduser(args.path)); save_db(db); print(f"{Fore.GREEN}💾 Saved{Style.RESET_ALL} {db[args.alias]} as {Fore.YELLOW}{args.alias}{Style.RESET_ALL}")
    elif args.cmd=="jump": path=db.get(args.alias); print(f"{Fore.CYAN}{path}{Style.RESET_ALL}") if path and os.path.exists(path) else print(f"{Fore.RED}❌ Alias not found or path missing{Style.RESET_ALL}")
    elif args.cmd=="unsave": db.pop(args.alias,None); save_db(db); print(f"{Fore.RED}🗑️ Removed alias{Style.RESET_ALL} {Fore.YELLOW}{args.alias}{Style.RESET_ALL}") if args.alias in db else print(f"{Fore.RED}❌ Alias not found{Style.RESET_ALL}")
    elif args.cmd=="showpaths": print(f"{Fore.CYAN}📂 Saved paths:{Style.RESET_ALL}"); [print(f"  {Fore.YELLOW}{k}{Style.RESET_ALL} → {Fore.GREEN}{v}{Style.RESET_ALL}") for k,v in db.items()] if db else print(f"{Fore.RED}❌ No saved paths found{Style.RESET_ALL}")
    elif args.cmd=="searchtext":
        files=searchtext(args.path,args.query,all=args.all,ignore=not args.in_ignore)
        if files: 
            for fp,ln,txt in files: 
                print(f"{Fore.CYAN}{fp}{Style.RESET_ALL} {Fore.MAGENTA}\nLine {ln}{Style.RESET_ALL}\n{Fore.YELLOW}{txt}{Style.RESET_ALL}")
        else: print(f"{Fore.RED}❌ No matches found{Style.RESET_ALL}")
    elif args.cmd=="searchfile":
        res=searchfile(args.path,args.pattern,exclude=args.exclude or [])
        if res: [print(f"{Fore.GREEN}{p}{Style.RESET_ALL}") for p in res]
        else: print(f"{Fore.RED}❌ No files found{Style.RESET_ALL}")
    else: parser.print_help()

if __name__=="__main__": main()
