# 把 术语表.md 转成中文 PDF（微信可直接预览）
import os, re
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Preformatted, Table,
                                TableStyle, Spacer, ListFlowable, ListItem)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE = os.path.dirname(__file__)
SRC = os.path.join(BASE, "术语表.md")
OUT = os.path.join(BASE, "术语表.pdf")

# 注册中文字体（黑体，单 TTF，中文显示最稳）
pdfmetrics.registerFont(TTFont("cn", r"C:\Windows\Fonts\simhei.ttf"))

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r'<font color="#d63384">\1</font>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    return s

CN = "cn"
H1 = ParagraphStyle("H1", fontName=CN, fontSize=17, leading=22, spaceAfter=10, textColor=colors.HexColor("#1f2328"))
H2 = ParagraphStyle("H2", fontName=CN, fontSize=14, leading=18, spaceBefore=14, spaceAfter=6, textColor=colors.HexColor("#0969da"))
H3 = ParagraphStyle("H3", fontName=CN, fontSize=11.5, leading=15, spaceBefore=8, spaceAfter=3, textColor=colors.HexColor("#0969da"))
BODY = ParagraphStyle("BODY", fontName=CN, fontSize=9.5, leading=14, spaceAfter=4)
QUOTE = ParagraphStyle("QUOTE", parent=BODY, leftIndent=10, textColor=colors.HexColor("#57606a"))
CODE = ParagraphStyle("CODE", fontName=CN, fontSize=8.5, leading=12, backColor=colors.HexColor("#f6f8fa"),
                      borderPadding=5, leftIndent=4, spaceAfter=4, wordWrap="CJK")
CELL = ParagraphStyle("CELL", fontName=CN, fontSize=8.5, leading=12)

# ---- 解析 markdown 源，按 ## / ### 切分 ----
with open(SRC, encoding="utf-8") as f:
    lines = f.read().split("\n")

groups, cur_g, cur_t = [], None, None
for line in lines:
    if line.startswith("## "):
        cur_g = {"title": line[3:].strip(), "intro": [], "terms": []}
        cur_t = None
        groups.append(cur_g)
    elif line.startswith("### "):
        cur_t = {"title": line[4:].strip(), "body": []}
        cur_g["terms"].append(cur_t)
    else:
        if cur_t is not None:
            cur_t["body"].append(line)
        elif cur_g is not None:
            cur_g["intro"].append(line)

def split_row(r):
    return [c.strip() for c in r.strip().strip("|").split("|")]

def parse_blocks(body):
    """把一组 markdown 行变成 reportlab flowables。"""
    flow, i, n = [], 0, len(body)
    while i < n:
        prev = i
        line = body[i]
        if line.strip() in ("---", "***", "___"):
            i += 1
            continue
        if line.strip().startswith("```"):
            code = []
            i += 1
            while i < n and not body[i].strip().startswith("```"):
                code.append(body[i]); i += 1
            i += 1
            flow.append(Preformatted(esc("\n".join(code)), CODE))
        elif line.strip().startswith("|") and i + 1 < n and body[i + 1].strip().startswith("|"):
            rows = []
            while i < n and body[i].strip().startswith("|"):
                rows.append(body[i]); i += 1
            header = split_row(rows[0])
            data = [split_row(r) for r in rows[2:]]  # 跳过分隔行
            table_data = [[Paragraph(inline(c), CELL) for c in header]] + \
                         [[Paragraph(inline(c), CELL) for c in r] for r in data]
            t = Table(table_data, colWidths=[None] * len(header))
            t.setStyle(TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d0d7de")),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#fafbfc")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            flow.append(t)
        elif line.strip().startswith("> "):
            quote = []
            while i < n and body[i].strip().startswith(">"):
                quote.append(body[i].strip()[2:]); i += 1
            flow.append(Paragraph(inline(" ".join(quote)), QUOTE))
        elif line.strip().startswith("- "):
            items = []
            while i < n and body[i].strip().startswith("- "):
                items.append(ListItem(Paragraph(inline(body[i].strip()[2:]), BODY))); i += 1
            flow.append(ListFlowable(items, bulletType="bullet", start="•"))
        elif line.strip() == "":
            i += 1
        else:
            para = []
            while i < n and body[i].strip() and not body[i].strip().startswith(("|", ">", "-", "```")):
                para.append(body[i]); i += 1
            flow.append(Paragraph(inline(" ".join(para)), BODY))
        if i == prev:
            i += 1  # 安全兜底：任何未预期行都跳过，避免死循环
    return flow

# ---- 组装文档 ----
doc = SimpleDocTemplate(OUT, pagesize=A4,
                        leftMargin=16 * mm, rightMargin=16 * mm,
                        topMargin=16 * mm, bottomMargin=16 * mm,
                        title="术语表（忻的学习词典）")
story = [Paragraph("术语表 · 忻的学习词典", H1)]
for gi, g in enumerate(groups):
    story.append(Paragraph(g["title"], H2))
    intro = [l for l in g["intro"] if l.strip()]
    if intro:
        story += parse_blocks(intro)
    for t in g["terms"]:
        story.append(Paragraph(t["title"], H3))
        story += parse_blocks(t["body"])

print("building...", flush=True)
try:
    doc.build(story)
    print("PDF 生成成功：", OUT, "大小", os.path.getsize(OUT), "字节", flush=True)
except Exception as e:
    import traceback
    traceback.print_exc()
