# 把 术语表.md 转成手机自适应的单文件 HTML（带搜索 + 分组导航）
import os, re
import markdown

SRC = os.path.join(os.path.dirname(__file__), "术语表.md")
OUT = os.path.join(os.path.dirname(__file__), "术语表.html")

with open(SRC, encoding="utf-8") as f:
    text = f.read()

lines = text.split("\n")
groups = []
current_group = None
current_term = None

for line in lines:
    if line.startswith("## "):
        current_group = {"title": line[3:].strip(), "intro": [], "terms": []}
        current_term = None
        groups.append(current_group)
    elif line.startswith("### "):
        current_term = {"title": line[4:].strip(), "body": []}
        current_group["terms"].append(current_term)
    else:
        if current_term is not None:
            current_term["body"].append(line)
        elif current_group is not None:
            current_group["intro"].append(line)

def md(s):
    return markdown.markdown("\n".join(s).strip(), extensions=["tables", "fenced_code"])

# 顶部导航
toc = "".join(
    f'<a class="toc-link" href="#g{i}">{g["title"].split("、",1)[-1] if "、" in g["title"] else g["title"]}</a>'
    for i, g in enumerate(groups)
)

sections = []
for i, g in enumerate(groups):
    intro_html = md(g["intro"]) if any(l.strip() for l in g["intro"]) else ""
    terms_html = ""
    for t in g["terms"]:
        plain = " ".join(t["body"])
        terms_html += (
            f'<section class="term" data-text="{(t["title"]+" "+plain).lower()}">'
            f'<h3>{t["title"]}</h3>{md(t["body"])}</section>'
        )
    sections.append(
        f'<section class="group" id="g{i}"><h2>{g["title"]}</h2>'
        f'{intro_html}{terms_html}</section>'
    )

CSS = """
:root{--bg:#fff;--fg:#1f2328;--muted:#57606a;--line:#d0d7de;--accent:#0969da;--code:#f6f8fa;}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
color:var(--fg);background:var(--bg);line-height:1.7;font-size:16px;padding-bottom:40px;}
header{position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--line);padding:12px 16px;z-index:10;}
header h1{font-size:18px;margin:0 0 8px}
#search{width:100%;padding:10px 12px;font-size:16px;border:1px solid var(--line);border-radius:8px;}
.toc{display:flex;flex-wrap:wrap;gap:6px;padding:10px 16px;border-bottom:1px solid var(--line);background:#fafbfc;}
.toc-link{font-size:13px;color:var(--accent);text-decoration:none;background:#eef3f8;padding:4px 10px;border-radius:999px;}
.group{padding:8px 16px;max-width:760px;margin:0 auto;}
h2{font-size:19px;border-left:4px solid var(--accent);padding-left:10px;margin:28px 0 12px;}
h3{font-size:16px;margin:20px 0 6px;color:var(--accent);}
.term{border-bottom:1px dashed var(--line);padding-bottom:10px;}
code{background:var(--code);padding:2px 6px;border-radius:4px;font-size:14px;font-family:ui-monospace,SFMono-Regular,Consolas,monospace;}
pre{background:var(--code);padding:12px;border-radius:8px;overflow:auto;}
pre code{background:none;padding:0;}
table{border-collapse:collapse;width:100%;font-size:14px;margin:8px 0;}
th,td{border:1px solid var(--line);padding:6px 8px;text-align:left;}
th{background:#fafbfc;}
blockquote{color:var(--muted);border-left:3px solid var(--line);margin:8px 0;padding-left:12px;}
.hidden{display:none}
.empty{text-align:center;color:var(--muted);padding:30px;display:none}
"""

JS = """
const box=document.getElementById('search');
const terms=document.querySelectorAll('.term');
const groups=document.querySelectorAll('.group');
const empty=document.getElementById('empty');
box.addEventListener('input',()=>{
  const q=box.value.trim().toLowerCase();
  let shown=0;
  terms.forEach(t=>{
    const hit=t.dataset.text.includes(q);
    t.classList.toggle('hidden', q && !hit);
    if(hit && q) shown++;
  });
  groups.forEach(g=>{
    const anyTerm=[...g.querySelectorAll('.term')].some(t=>!t.classList.contains('hidden'));
    const hasIntro=g.querySelector('p,ul,blockquote');
    g.classList.toggle('hidden', q && !anyTerm && !hasIntro);
  });
  empty.style.display=(q && shown===0)?'block':'none';
});
"""

html = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>术语表（忻的学习词典）</title><style>{CSS}</style></head>
<body><header><h1>术语表 · 忻的学习词典</h1>
<input id="search" placeholder="搜词，例如：embedding / venv / .get()" autocomplete="off"></header>
<nav class="toc">{toc}</nav>
{''.join(sections)}
<div class="empty" id="empty">没找到，发这个词给我，我补进去 👋</div>
<script>{JS}</script></body></html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print("生成成功：", OUT, "大小", os.path.getsize(OUT), "字节，分组数", len(groups))
