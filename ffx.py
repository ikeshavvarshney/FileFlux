#!/usr/bin/env python3
import os,sys,shutil,json,mimetypes,argparse,subprocess,zipfile;from colorama import Fore,Style,init;init(autoreset=True)
VERSION="1.2";AUTHOR="Keshav Varshney";REPO="https://github.com/ikeshavvarshney/FileFlux"
HOME,DB=os.path.expanduser("~"),os.path.join(os.path.expanduser("~"),".fileflux.json")
SUGGEST={"image/jpeg":"View image","image/png":"View image","image/gif":"View image","image/svg+xml":"Vector editor","video/mp4":"Media player","audio/mpeg":"Music player","application/pdf":"PDF reader","application/zip":"Unzip","application/x-tar":"Extract archive","application/gzip":"Extract archive","text/plain":"Text editor","text/markdown":"Markdown editor","text/x-python":"Python IDE","text/x-c":"C compiler","text/x-c++":"C++ compiler","text/x-java-source":"Java IDE","application/javascript":"Node.js / Browser","application/json":"JSON viewer","text/html":"Web browser","text/css":"CSS editor","application/xml":"XML editor","application/sql":"SQL client","application/x-yaml":"YAML config","application/vnd.ms-excel":"Excel","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":"Excel","application/vnd.openxmlformats-officedocument.wordprocessingml.document":"Word","application/vnd.openxmlformats-officedocument.presentationml.presentation":"PowerPoint","application/x-sh":"Shell script","application/x-bash":"Bash script","application/x-powershell":"PowerShell","application/x-msdownload":"Windows executable","application/x-dosexec":"Windows executable","application/octet-stream":"Binary file","application/x-executable":"Executable","inode/directory":"Directory browser"}
def load_db(): 
    try:return json.load(open(DB)) if os.path.exists(DB) else {}
    except:return {}
def save_db(d): json.dump(d,open(DB,"w"))
def human_size(n):
    for u in ["B","KB","MB","GB","TB"]:
        if n<1024:return f"{n:.1f} {u}"
        n/=1024
    return f"{n:.1f} PB"
def free_space(path): return shutil.disk_usage(path).free # check free disk space
def detect(path):
    if not os.path.exists(path):return f"{Fore.RED}!! Not found !!{Style.RESET_ALL}"
    if os.path.isdir(path):return f"{Fore.BLUE}[DIR]{Style.RESET_ALL} {path}"
    size,mime=os.path.getsize(path),mimetypes.guess_type(path)[0] or "binary"
    info=[f"{Fore.CYAN}{path}{Style.RESET_ALL}",f"- Size: {Fore.YELLOW}{human_size(size)}{Style.RESET_ALL}",f"- Type: {Fore.MAGENTA}{mime}{Style.RESET_ALL}",f"- Suggestion: {Fore.GREEN}{SUGGEST.get(mime,'Unknown')}{Style.RESET_ALL}"]
    try:details=subprocess.check_output(["file","-b",path],text=True).strip();info.append(f"- Details: {Fore.WHITE}{details}{Style.RESET_ALL}")
    except:pass
    return "\n".join(info)
# file ops
def copy(s,d):
    sz=os.path.getsize(s);free=free_space(os.path.dirname(d) or ".")
    if sz>free:print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Not enough space to copy {s}");return
    if sz>100*1024*1024 and free<2*sz:print(f"{Fore.YELLOW}[WARN]{Style.RESET_ALL} Low storage, moving large file")
    shutil.copy2(s,d);print(f"[COPIED] {s} -> {d}")
def cut(s,d):
    sz=os.path.getsize(s);free=free_space(os.path.dirname(d) or ".")
    if sz>free:print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Not enough space to move {s}");return
    if sz>100*1024*1024 and free<2*sz:print(f"{Fore.YELLOW}[WARN]{Style.RESET_ALL} Low storage, moving large file")
    shutil.move(s,d);print(f"[MOVED] {s} -> {d}")
def delete(p):(os.remove(p) if os.path.isfile(p) else shutil.rmtree(p));print(f"[DELETED] {p}")
def mkdir(p):os.makedirs(p,exist_ok=True);print(f"[MKDIR] {p}")
def rename(s,d):os.rename(s,d);print(f"[RENAMED] {s} -> {d}")
# search unified
def search(path,text=None,ext=None,pattern=None):
    path=os.path.abspath(path);res=[]
    for root,_,fs in os.walk(path):
        for f in fs:
            if pattern and pattern in f:res.append(os.path.join(root,f));continue
            if text:
                if ext and not f.endswith(ext):continue
                fp=os.path.join(root,f)
                try:
                    with open(fp,'r',errors='ignore') as fi:
                        for i,l in enumerate(fi):
                            if text in l:res.append(f"{fp}:{i+1}:{l.strip()}");break
                except:pass
    return res
# convert
def convert(fmt,src,dst=None):
    try:
        if fmt=="json":
            text=open(src).read();out=json.dumps({"content":text},indent=2)
        elif fmt=="txt":
            data=json.load(open(src));out=str(data)
        else:print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Unknown format");return
        dst=dst or f"{os.path.splitext(src)[0]}.{fmt}"
        open(dst,"w").write(out);print(f"[CONVERTED] {src} -> {dst}")
    except Exception as e:print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {e}")
# archive/extract
def archive(src,dst=None): # safe archive: avoids overwriting src if dst==src
    try:
        abs_src=os.path.abspath(src)
        if not dst: dst=os.path.splitext(abs_src)[0]+'.zip' # default dst
        abs_dst=os.path.abspath(dst)
        if abs_dst==abs_src: dst=abs_dst+'.zip'; abs_dst=os.path.abspath(dst) # avoid same-name overwrite
        os.makedirs(os.path.dirname(abs_dst) or '.',exist_ok=True) # ensure dest dir exists
        with zipfile.ZipFile(abs_dst,'w',zipfile.ZIP_DEFLATED) as z:
            if os.path.isdir(abs_src):
                for root,_,files in os.walk(abs_src):
                    for f in files:
                        full=os.path.join(root,f)
                        arc=os.path.relpath(full,start=os.path.dirname(abs_src)) # keep relative paths
                        z.write(full,arc)
            else:
                z.write(abs_src,os.path.basename(abs_src))
        print(f"{Fore.GREEN}[ARCHIVED]{Style.RESET_ALL} {src} -> {dst}")
    except Exception as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} archiving failed: {e}")
def extract(src,dst=None): # safe extract: default dir and avoid clobbering file paths
    try:
        if dst is None: dst=os.path.splitext(src)[0] # default to filename without ext
        abs_dst=os.path.abspath(dst)
        if os.path.exists(abs_dst) and os.path.isfile(abs_dst): abs_dst=abs_dst+'_extracted' # avoid writing into a file
        os.makedirs(abs_dst,exist_ok=True)
        with zipfile.ZipFile(src,'r') as z: z.extractall(abs_dst)
        print(f"{Fore.GREEN}[EXTRACTED]{Style.RESET_ALL} {src} -> {abs_dst}")
    except Exception as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} extraction failed: {e}")
# clipboard
def copy_to_clipboard(text):
    try:
        if shutil.which('pbcopy'):p=subprocess.Popen(['pbcopy'],stdin=subprocess.PIPE);p.communicate(input=text.encode());return True
        if shutil.which('xclip'):p=subprocess.Popen(['xclip','-selection','clipboard'],stdin=subprocess.PIPE);p.communicate(input=text.encode());return True
        if shutil.which('xsel'):p=subprocess.Popen(['xsel','--clipboard','--input'],stdin=subprocess.PIPE);p.communicate(input=text.encode());return True
        if os.name=='nt':p=subprocess.Popen(['clip'],stdin=subprocess.PIPE);p.communicate(input=text.encode());return True
    except:pass
    try:import pyperclip;pyperclip.copy(text);return True
    except:return False
# list files
def list_files(path=None):
    p=os.path.abspath(path or os.getcwd())
    try:entries=list(os.scandir(p))
    except Exception as e:print(f"[ERROR] {e}");return
    print(f"{Fore.CYAN}Listing: {p}{Style.RESET_ALL}")
    names=[e.name for e in entries];namew=max((len(n) for n in names),default=10);sizew=12
    for e in entries:
        try:
            if e.is_dir():ftype='Directory'
            else:
                mt=mimetypes.guess_type(e.path)[0] or ''
                if mt.startswith('image'):ftype='Image'
                elif e.name.endswith('.py'):ftype='Python'
                elif e.name.endswith('.md'):ftype='Markdown'
                elif mt.startswith('video'):ftype='Video'
                elif mt.startswith('text'):ftype='Text'
                elif e.name.endswith(('.zip','.tar','.gz')):ftype='Archive'
                else:ftype=mt.split('/')[-1] or 'Binary'
            sz=(os.path.getsize(e.path) if e.is_file() else 0)
        except:ftype='Unknown';sz=0
        name=f"{Fore.GREEN}{e.name}{Style.RESET_ALL}".ljust(namew+len(Fore.GREEN)+len(Style.RESET_ALL))
        sizecol=str(human_size(sz)).center(sizew);typecol=f"{Fore.BLUE}{ftype}{Style.RESET_ALL}"
        print(f"{name} {sizecol} {typecol}")
# password manager
def pass_store(alias,password,db):db.setdefault('__passwords__',{})[alias]=password;save_db(db);print(f"[SAVED] password for '{alias}'")
def pass_get(alias,db):
    pwd=db.get('__passwords__',{}).get(alias)
    if not pwd:print(f"[ERROR] no password found for '{alias}'");return
    ok=copy_to_clipboard(pwd)
    if ok:print(f"[CLIP] password for '{alias}' copied to clipboard")
    else:print(f"[WARN] could not copy to clipboard, use ffx pass {alias} to view")
# banner
def show_logo():
    logo=f"\n{Fore.CYAN}██████╗██╗██╗     ██████╗██████╗██╗    ██╗   ██╗██╗  ██╗{Style.RESET_ALL}\n{Fore.YELLOW}██╔═══╝██║██║     ██╔═══╝██╔═══╝██║    ██║   ██║╚██╗██╔╝{Style.RESET_ALL}\n{Fore.MAGENTA}████╗  ██║██║     ████╗  ████╗  ██║    ██║   ██║ ╚███╔╝{Style.RESET_ALL}\n{Fore.GREEN}██╔═╝  ██║██║     ██╔═╝  ██╔═╝  ██║    ██║   ██║ ██╔██╗{Style.RESET_ALL}\n{Fore.CYAN}██║    ██║██████╗ ██████╗██║    ██████╗╚██████╔╝██╔╝ ██╗{Style.RESET_ALL}\n{Fore.YELLOW}╚═╝    ╚═╝╚═════╝ ╚═════╝╚═╝    ╚═════╝ ╚═════╝ ╚═╝  ╚═╝{Style.RESET_ALL}\n{Fore.CYAN}Repo: {REPO}{Style.RESET_ALL}\n"
    print(logo)
# argparser
def main():
    p=argparse.ArgumentParser(prog=f"{Fore.CYAN}ffx{Style.RESET_ALL}",add_help=False);p.add_argument('-v','--version',action='version',version=VERSION);p.add_argument('-h','--help',action='store_true');sub=p.add_subparsers(dest='cmd')
    sub.add_parser('info').add_argument('file')
    for c in ['copy','cut','rename']:s=sub.add_parser(c);s.add_argument('src');s.add_argument('dst')
    sub.add_parser('delete').add_argument('path');sub.add_parser('mkdir').add_argument('path')
    sp=sub.add_parser('save');sp.add_argument('alias');sp.add_argument('path',nargs='+')
    jp=sub.add_parser('jump');jp.add_argument("alias")
    sub.add_parser('unsave').add_argument('alias');sub.add_parser('showpaths')
    ls=sub.add_parser('ls');ls.add_argument('path',nargs='?')
    pp=sub.add_parser('pass');pp.add_argument('alias');pp.add_argument('password',nargs='?')
    cv=sub.add_parser('convert');cv.add_argument('--json',action='store_true');cv.add_argument('--txt',action='store_true');cv.add_argument('src');cv.add_argument('dst',nargs='?')
    ar=sub.add_parser('archive');ar.add_argument('src');ar.add_argument('dst')
    ex=sub.add_parser('extract');ex.add_argument('src');ex.add_argument('dst')
    sr=sub.add_parser('search');sr.add_argument('--text');sr.add_argument('--ext');sr.add_argument('pattern',nargs='?');sr.add_argument('path',nargs='?',default=os.getcwd())
    args,db=p.parse_args(),load_db()
    if len(sys.argv)==1:show_logo();return
    if args.help:show_logo(); print(f"{Fore.YELLOW}DESCRIPTION:{Style.RESET_ALL}\n• FileFlux is a modern CLI for managing files and paths.\n• Save and jump to frequently used paths.\n• Search text inside files with searchtext.\n• Find files by name with searchfile.\n• Password manager: 'ffx pass <alias> [password]'.\n• {Fore.GREEN}Author{Style.RESET_ALL}: {Fore.CYAN}{AUTHOR}{Style.RESET_ALL}\n• {Fore.GREEN}Version{Style.RESET_ALL}: {Fore.CYAN}{VERSION}{Style.RESET_ALL}\n• {Fore.GREEN}Repo{Style.RESET_ALL}: {Fore.CYAN}{REPO}{Style.RESET_ALL}\n"); p.print_help(); return
    if args.cmd=='info':print(detect(args.file))
    elif args.cmd=='copy':copy(args.src,args.dst)
    elif args.cmd=='cut':cut(args.src,args.dst)
    elif args.cmd=='delete':delete(args.path)
    elif args.cmd=='mkdir':mkdir(args.path)
    elif args.cmd=='rename':rename(args.src,args.dst)
    elif args.cmd=="save":db[args.alias]=os.path.abspath(os.path.expanduser(' '.join(args.path).rstrip("/\\")));save_db(db);print(f"[SAVED] {db[args.alias]} as {args.alias}")
    elif args.cmd=='jump':path=db.get(args.alias);print(os.path.abspath(os.path.expanduser(path.rstrip("/\\"))) if path and os.path.exists(os.path.abspath(os.path.expanduser(path.rstrip("/\\")))) else "[ERROR] Alias not found or path missing")
    elif args.cmd=='unsave':
        if args.alias in db:db.pop(args.alias,None);save_db(db);print(f"[REMOVED] alias {args.alias}")
        else:print(f"[ERROR] Alias not found")
    elif args.cmd=='showpaths':
        if db:print('[PATHS]');[print(f"  {k} -> {v}") for k,v in db.items() if k!='__passwords__']
        else:print('[NONE] No saved paths')
    elif args.cmd=='ls':list_files(args.path)
    elif args.cmd=='pass':
        if args.password:pass_store(args.alias,args.password,db)
        else:pass_get(args.alias,db)
    elif args.cmd=='convert':fmt="json" if args.json else "txt" if args.txt else None;convert(fmt,args.src,args.dst)
    elif args.cmd=='archive':archive(args.src,args.dst)
    elif args.cmd=='extract':extract(args.src,args.dst)
    elif args.cmd=='search':
        res=search(args.path,text=args.text,ext=args.ext,pattern=args.pattern)
        if res:[print(r) for r in res]
        else:print('[NONE] No matches found')
    else:p.print_help()
if __name__=="__main__":main()
