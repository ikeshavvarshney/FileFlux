#!/usr/bin/env python3
import os,sys,shutil,json,mimetypes,argparse,subprocess;from colorama import Fore,Style,init;init(autoreset=True)
VERSION="1.1";AUTHOR="Keshav Varshney";REPO="https://github.com/ikeshavvarshney/FileFlux"
HOME,DB=os.path.expanduser("~"),os.path.join(os.path.expanduser("~"),".fileflux.json")
SUGGEST={"image/jpeg":"View image","image/png":"View image","image/gif":"View image","image/svg+xml":"Vector editor","video/mp4":"Media player","audio/mpeg":"Music player","application/pdf":"PDF reader","application/zip":"Unzip","application/x-tar":"Extract archive","application/gzip":"Extract archive","text/plain":"Text editor","text/markdown":"Markdown editor","text/x-python":"Python IDE","text/x-c":"C compiler","text/x-c++":"C++ compiler","text/x-java-source":"Java IDE","application/javascript":"Node.js / Browser","application/json":"JSON viewer","text/html":"Web browser","text/css":"CSS editor","application/xml":"XML editor","application/sql":"SQL client","application/x-yaml":"YAML config","application/vnd.ms-excel":"Excel","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":"Excel","application/vnd.openxmlformats-officedocument.wordprocessingml.document":"Word","application/vnd.openxmlformats-officedocument.presentationml.presentation":"PowerPoint","application/x-sh":"Shell script","application/x-bash":"Bash script","application/x-powershell":"PowerShell","application/x-msdownload":"Windows executable","application/x-dosexec":"Windows executable","application/octet-stream":"Binary file","application/x-executable":"Executable","inode/directory":"Directory browser"}
def load_db():
    try: return json.load(open(DB)) if os.path.exists(DB) else {}
    except: return {}
def save_db(d): json.dump(d,open(DB,"w"))
def human_size(n):
    for u in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024:
            return f"{n:.1f} {u}"
        n /= 1024
    return f"{n:.1f} PB"
def detect(path):
    if not os.path.exists(path): return f"{Fore.RED}❌ Not found{Style.RESET_ALL}"
    if os.path.isdir(path): return f"{Fore.BLUE}[DIR]{Style.RESET_ALL} {path}"
    size,mime=os.path.getsize(path),mimetypes.guess_type(path)[0] or "binary"
    info=[f"{Fore.CYAN}{path}{Style.RESET_ALL}",f"- Size: {Fore.YELLOW}{human_size(size)}{Style.RESET_ALL}",f"- Type: {Fore.MAGENTA}{mime}{Style.RESET_ALL}",f"- Suggestion: {Fore.GREEN}{SUGGEST.get(mime,'Unknown')}{Style.RESET_ALL}"]
    try:
        details=subprocess.check_output(["file","-b",path],text=True).strip();info.append(f"- Details: {Fore.WHITE}{details}{Style.RESET_ALL}")
    except: pass
    return "\n".join(info)
# file ops compact
def copy(s,d): shutil.copy2(s,d); print(f"[COPIED] {s} -> {d}")
def cut(s,d): shutil.move(s,d); print(f"[MOVED] {s} -> {d}")
def delete(p): (os.remove(p) if os.path.isfile(p) else shutil.rmtree(p)); print(f"[DELETED] {p}")
def mkdir(p): os.makedirs(p,exist_ok=True); print(f"[MKDIR] {p}")
def rename(s,d): os.rename(s,d); print(f"[RENAMED] {s} -> {d}")
# search
def searchtext(path,query,all=False,ignore=True):
    path=os.path.abspath(path);files=[]
    for root,_,fs in os.walk(path):
        for f in fs:
            if ignore and os.path.exists(os.path.join(root,".gitignore")): continue
            fp=os.path.join(root,f)
            try:
                with open(fp,'r',errors='ignore') as fi:
                    for i,l in enumerate(fi):
                        if query in l: files.append((fp,i+1,l.strip()));
                        if files and not all: break
            except: pass
            if files and not all: break
    return files
def searchfile(path,pattern,exclude=[]):
    path=os.path.abspath(path);res=[]
    for root,_,fs in os.walk(path):
        for f in fs:
            if pattern in f and not any(e in root for e in exclude): res.append(os.path.join(root,f))
    return res
# clipboard helper: tries pbcopy, xclip/xsel, clip; returns True on success
def copy_to_clipboard(text):
    try:
        if shutil.which('pbcopy'):
            p=subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE); p.communicate(input=text.encode()); return True
        if shutil.which('xclip'):
            p=subprocess.Popen(['xclip','-selection','clipboard'], stdin=subprocess.PIPE); p.communicate(input=text.encode()); return True
        if shutil.which('xsel'):
            p=subprocess.Popen(['xsel','--clipboard','--input'], stdin=subprocess.PIPE); p.communicate(input=text.encode()); return True
        if os.name=='nt':
            p=subprocess.Popen(['clip'], stdin=subprocess.PIPE); p.communicate(input=text.encode()); return True
    except: pass
    try:
        import pyperclip; pyperclip.copy(text); return True
    except: return False
# file listing (pretty compact)
def list_files(path=None):
    p=os.path.abspath(path or os.getcwd())
    try:
        entries=list(os.scandir(p))
    except Exception as e:
        print(f"[ERROR] {e}"); return
    # header
    print(f"{Fore.CYAN}Listing: {p}{Style.RESET_ALL}")
    # compute widths
    names=[e.name for e in entries]
    namew=max((len(n) for n in names),default=10);sizew=12
    for e in entries:
        try:
            if e.is_dir(): ftype='Directory'
            else:
                mt=mimetypes.guess_type(e.path)[0] or ''
                if mt.startswith('image'): ftype='Image'
                elif e.name.endswith('.py'): ftype='Python'
                elif e.name.endswith('.md'): ftype='Markdown'
                elif mt.startswith('video'): ftype='Video'
                elif mt.startswith('text'): ftype='Text'
                elif e.name.endswith('.zip') or e.name.endswith('.tar') or e.name.endswith('.gz'): ftype='Archive'
                else: ftype=mt.split('/')[-1] or 'Binary'
            sz=(os.path.getsize(e.path) if e.is_file() else 0)
        except: ftype='Unknown'; sz=0
        name=f"{Fore.GREEN}{e.name}{Style.RESET_ALL}".ljust(namew+len(Fore.GREEN)+len(Style.RESET_ALL))
        sizecol=str(human_size(sz)).center(sizew)
        typecol=f"{Fore.BLUE}{ftype}{Style.RESET_ALL}"
        print(f"{name} {sizecol} {typecol}")
# password manager: stores under key '__passwords__' in DB; storing prints confirmation; retrieving copies to clipboard and prints short msg only
def pass_store(alias,password,db):
    db.setdefault('__passwords__',{})[alias]=password; save_db(db); print(f"[SAVED] password for '{alias}'")
def pass_get(alias,db):
    pwd=db.get('__passwords__',{}).get(alias)
    if not pwd: print(f"[ERROR] no password found for '{alias}'"); return
    ok=copy_to_clipboard(pwd)
    if ok: print(f"[CLIP] password for '{alias}' copied to clipboard")
    else: print(f"[WARN] could not copy to clipboard, password stored in DB (use ffx pass {alias} to view it)")
# banner
def show_logo():
    logo=f"\n{Fore.CYAN}██████╗██╗██╗     ██████╗██████╗██╗    ██╗   ██╗██╗  ██╗{Style.RESET_ALL}\n{Fore.YELLOW}██╔═══╝██║██║     ██╔═══╝██╔═══╝██║    ██║   ██║╚██╗██╔╝{Style.RESET_ALL}\n{Fore.MAGENTA}████╗  ██║██║     ████╗  ████╗  ██║    ██║   ██║ ╚███╔╝{Style.RESET_ALL}\n{Fore.GREEN}██╔═╝  ██║██║     ██╔═╝  ██╔═╝  ██║    ██║   ██║ ██╔██╗{Style.RESET_ALL}\n{Fore.CYAN}██║    ██║██████╗ ██████╗██║    ██████╗╚██████╔╝██╔╝ ██╗{Style.RESET_ALL}\n{Fore.YELLOW}╚═╝    ╚═╝╚═════╝ ╚═════╝╚═╝    ╚═════╝ ╚═════╝ ╚═╝  ╚═╝{Style.RESET_ALL}\n{Fore.CYAN}Repo: {REPO}{Style.RESET_ALL}\n"
    print(logo)
# argparser (compact)
def main():
    p=argparse.ArgumentParser(prog=f"{Fore.CYAN}ffx{Style.RESET_ALL}",add_help=False);p.add_argument('-v','--version',action='version',version=VERSION);p.add_argument('-h','--help',action='store_true');sub=p.add_subparsers(dest='cmd')
    sub.add_parser('info').add_argument('file')
    for c in ['copy','cut','rename']: s=sub.add_parser(c); s.add_argument('src'); s.add_argument('dst')
    sub.add_parser('delete').add_argument('path'); sub.add_parser('mkdir').add_argument('path')
    sp=sub.add_parser('save'); sp.add_argument('alias'); sp.add_argument('path', nargs='+')
    jp=sub.add_parser('jump'); jp.add_argument("alias")
    sub.add_parser('unsave').add_argument('alias')
    sub.add_parser('showpaths')
    st=sub.add_parser('searchtext'); st.add_argument('query'); st.add_argument('path',nargs='?',default=os.getcwd()); st.add_argument('--all','-a',action='store_true'); st.add_argument('--in-ignore',action='store_true')
    sf=sub.add_parser('searchfile'); sf.add_argument('pattern'); sf.add_argument('path',nargs='?',default=os.getcwd()); sf.add_argument('--exclude','-e',nargs='*')
    ls=sub.add_parser('ls'); ls.add_argument('path',nargs='?')
    pp=sub.add_parser('pass'); pp.add_argument('alias'); pp.add_argument('password',nargs='?')

    args,db=p.parse_args(),load_db()
    if len(sys.argv)==1: show_logo(); return
    if args.help:
        show_logo(); print(f"{Fore.YELLOW}DESCRIPTION:{Style.RESET_ALL}\n• FileFlux is a modern CLI for managing files and paths.\n• Save and jump to frequently used paths.\n• Search text inside files with searchtext.\n• Find files by name with searchfile.\n• Password manager: 'ffx pass <alias> [password]'.\n• {Fore.GREEN}Author{Style.RESET_ALL}: {Fore.CYAN}{AUTHOR}{Style.RESET_ALL}\n• {Fore.GREEN}Version{Style.RESET_ALL}: {Fore.CYAN}{VERSION}{Style.RESET_ALL}\n• {Fore.GREEN}Repo{Style.RESET_ALL}: {Fore.CYAN}{REPO}{Style.RESET_ALL}\n")
        p.print_help(); return
    if args.cmd=='info': print(detect(args.file))
    elif args.cmd=='copy': copy(args.src,args.dst)
    elif args.cmd=='cut': cut(args.src,args.dst)
    elif args.cmd=='delete': delete(args.path)
    elif args.cmd=='mkdir': mkdir(args.path)
    elif args.cmd=='rename': rename(args.src,args.dst)
    elif args.cmd=="save": db[args.alias]=os.path.abspath(os.path.expanduser(' '.join(args.path).rstrip("/\\"))); save_db(db); print(f"[SAVED] {db[args.alias]} as {args.alias}")
    elif args.cmd=='jump': path=db.get(args.alias); print(os.path.abspath(os.path.expanduser(path.rstrip("/\\"))) if path and os.path.exists(os.path.abspath(os.path.expanduser(path.rstrip("/\\")))) else "[ERROR] Alias not found or path missing")
    elif args.cmd=='unsave':
        if args.alias in db: db.pop(args.alias,None); save_db(db); print(f"[REMOVED] alias {args.alias}")
        else: print(f"[ERROR] Alias not found")
    elif args.cmd=='showpaths':
        if db: print('[PATHS]'); [print(f"  {k} -> {v}") for k,v in db.items() if k!='__passwords__']
        else: print('[NONE] No saved paths')
    elif args.cmd=='searchtext':
        files=searchtext(args.path,args.query,all=args.all,ignore=not args.in_ignore)
        if files:
            for fp,ln,txt in files: print(f"{fp}\nLine {ln}\n{txt}\n")
        else: print('[NONE] No matches found')
    elif args.cmd=='searchfile':
        res=searchfile(args.path,args.pattern,exclude=args.exclude or [])
        if res: [print(p) for p in res]
        else: print('[NONE] No files found')
    elif args.cmd=='ls': list_files(args.path)
    elif args.cmd=='pass':
        if args.password: pass_store(args.alias,args.password,db)
        else: pass_get(args.alias,db)
    else: p.print_help()

if __name__=="__main__": main()
