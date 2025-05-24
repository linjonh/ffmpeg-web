import glob
import os
from markdownify import markdownify as md
def checkDir(dir: str):
    print("checkDir =" + dir)
    if not dir.endswith(os.sep):
        dir = dir[: dir.rfind(os.sep) + 1]
    os.makedirs(dir, exist_ok=True)
    return

        
if __name__=='__main__':
    dir="../ffmpeg-docs-website\\ffmpeg-docs_volcan_translate"
    
    docs=glob.glob(f"{dir}/*.html", recursive=False)
    print(f"{dir} docs size: {len(docs)}")
    for doc in docs:
        print(f"Processing {doc}")
        with open(doc, 'r', encoding='utf-8') as f:
            html = f.read()
            md_str=md(html,heading_style="atx")
            path = os.path.join(dir,"md_docs",os.path.splitext(os.path.basename(doc))[0]+".md")
            print(path)
            checkDir(path)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(md_str)
                print(f"Saved {doc} as markdown")