#!/usr/bin/env python3
import os, sys, shutil, json, mimetypes, argparse, subprocess

HOME, DB = os.path.expanduser("~"), os.path.join(os.path.expanduser("~"), ".fileflux.json")
SUGGEST = {"image/jpeg":"View image","image/png":"View image","application/pdf":"PDF reader",
           "application/zip":"Unzip","text/plain":"Text editor"}

def load_db(): return json.load(open(DB)) if os.path.exists(DB) else {}
def save_db(d): json.dump(d, open(DB,"w"))
def human_size(n):
    for u in ["B","KB","MB","GB","TB"]:
        if n<1024: return f"{n:.1f} {u}"
        n/=1024
    return f"{n:.1f} PB"

def detect(path):
    if not os.path.exists(path): return "❌ Not found"
    if os.path.isdir(path): return f"📁 Directory: {path}"
    size, mime = os.path.getsize(path), mimetypes.guess_type(path)[0] or "binary"
    info=[f"🔍 {path}",f"— Size: {human_size(size)}",f"— Type: {mime}",
          "— Suggestion: "+SUGGEST.get(mime,"Unknown")]
    try: info.append("— Details: "+subprocess.check_output(["file","-b",path],text=True).strip())
    except: pass
    return "\n".join(info)

def copy(s,d): shutil.copy2(s,d); print(f"📄 Copied {s}→{d}")
def cut(s,d): shutil.move(s,d); print(f"✂️ Moved {s}→{d}")
def delete(p): (os.remove(p) if os.path.isfile(p) else shutil.rmtree(p)); print(f"🗑️ Deleted {p}")
def mkdir(p): os.makedirs(p,exist_ok=True); print(f"📁 Created {p}")
def rename(s,d): os.rename(s,d); print(f"✏️ Renamed {s}→{d}")

def main():
    p=argparse.ArgumentParser(prog="ffx"); sub=p.add_subparsers(dest="cmd")
    sub.add_parser("info").add_argument("file")
    [sub.add_parser(cmd).add_argument("src").add_argument("dst") for cmd in ["copy","cut","rename"]]
    sub.add_parser("delete").add_argument("path"); sub.add_parser("mkdir").add_argument("path")
    sp=sub.add_parser("save"); sp.add_argument("alias"); sp.add_argument("path")
    jp=sub.add_parser("jump"); jp.add_argument("alias")
    args,db=p.parse_args(),load_db()

    if args.cmd=="info": print(detect(args.file))
    elif args.cmd=="copy": copy(args.src,args.dst)
    elif args.cmd=="cut": cut(args.src,args.dst)
    elif args.cmd=="delete": delete(args.path)
    elif args.cmd=="mkdir": mkdir(args.path)
    elif args.cmd=="rename": rename(args.src,args.dst)
    elif args.cmd=="save": db[args.alias]=os.path.abspath(os.path.expanduser(args.path)); save_db(db); print(f"💾 Saved {db[args.alias]} as {args.alias}")
    elif args.cmd=="jump": path=db.get(args.alias); print(path) if path and os.path.exists(path) else print("❌ Alias not found or path missing")
    else: p.print_help()

if __name__=="__main__": main()
