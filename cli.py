#!/usr/bin/env python3
import os, sys, shutil, json, mimetypes, argparse, subprocess

HOME = os.path.expanduser("~")
DB = os.path.join(HOME, ".fileflux.json")
SUGGEST={"image/jpeg":"View image","image/png":"View image","application/pdf":"PDF reader",
         "application/zip":"Unzip","text/plain":"Text editor"}

def load_db(): 
    if os.path.exists(DB): return json.load(open(DB))
    return {}
def save_db(d): json.dump(d, open(DB,"w"))
def human_size(n): 
    for u in ["B","KB","MB","GB"]: 
        if n<1024: return f"{n:.1f} {u}"; n/=1024
    return f"{n:.1f} TB"

def detect(path):
    if not os.path.exists(path): return "❌ Not found"
    if os.path.isdir(path): return f"📁 Directory: {path}"
    size=os.path.getsize(path)
    mime,_=mimetypes.guess_type(path); mime=mime or "binary"
    info=[f"🔍 {path}","— Size: "+human_size(size),
          "— Type: "+mime,"— Suggestion: "+SUGGEST.get(mime,"Unknown")]
    try: info.append("— Details: "+subprocess.check_output(["file","-b",path],text=True).strip())
    except: pass
    return "\n".join(info)

def copy(src,dst): shutil.copy2(src,dst); print(f"📄 Copied {src}→{dst}")
def cut(src,dst): shutil.move(src,dst); print(f"✂️ Moved {src}→{dst}")
def delete(path): os.remove(path) if os.path.isfile(path) else shutil.rmtree(path); print(f"🗑️ Deleted {path}")
def mkdir(path): os.makedirs(path,exist_ok=True); print(f"📁 Created {path}")
def rename(src,dst): os.rename(src,dst); print(f"✏️ Renamed {src}→{dst}")

def main():
    p=argparse.ArgumentParser(prog="fileflux")
    sub=p.add_subparsers(dest="cmd")
    sub.add_parser("info").add_argument("file")
    sub.add_parser("copy").add_argument("src"); sub.add_parser("copy").add_argument("dst")
    sub.add_parser("cut").add_argument("src"); sub.add_parser("cut").add_argument("dst")
    sub.add_parser("delete").add_argument("path")
    sub.add_parser("mkdir").add_argument("path")
    sub.add_parser("rename").add_argument("src"); sub.add_parser("rename").add_argument("dst")
    sub.add_parser("save").add_argument("alias"); sub.add_parser("save").add_argument("path")
    sub.add_parser("jump").add_argument("alias")
    args=p.parse_args(); db=load_db()

    if args.cmd=="info": print(detect(args.file))
    elif args.cmd=="copy": copy(args.src,args.dst)
    elif args.cmd=="cut": cut(args.src,args.dst)
    elif args.cmd=="delete": delete(args.path)
    elif args.cmd=="mkdir": mkdir(args.path)
    elif args.cmd=="rename": rename(args.src,args.dst)
    elif args.cmd=="save": db[args.alias]=args.path; save_db(db); print(f"💾 Saved {args.path} as {args.alias}")
    elif args.cmd=="jump": 
        path=db.get(args.alias)
        if path and os.path.exists(path): os.chdir(path); print(f"📂 Jumped to {path}")
        else: print("❌ Alias not found or path missing")
    else: p.print_help()

if __name__=="__main__": main()
