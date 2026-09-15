"""工厂库存查询 Agent —— 简历项目 v1（基础·企业场景）
整体数据流（背这个流程就行）：
  浏览器发问 → FastAPI /ask → 跑_agent() 三件套 → DeepSeek 决定调哪个工具
  → 工具真正操作「库存库」SQLite（查/改）→ 结果塞回历史 → 模型组织成中文回答
"""
import os
import json
import sqlite3
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

load_dotenv()
# 🟢懂框架：这里的 client 就是"调 DeepSeek 的电话"，base_url 指向 DeepSeek 的接口
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

# ========== 库存库 class（SQLite 封装，线程安全：每个方法自己开关连接）==========
class 库存库:
    def __init__(self, 库名="factory.db"):
        self.库名 = 库名
        conn = sqlite3.connect(库名)
        conn.execute("""CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            编号 TEXT,
            名称 TEXT,
            类别 TEXT,
            规格 TEXT,
            数量 INTEGER,
            单位 TEXT,
            安全库存 INTEGER,
            库位 TEXT,
            更新时间 TEXT
        )""")
        conn.commit()
        conn.close()
        if not self._有数据():
            self._塞种子()

    def _有数据(self):
        conn = sqlite3.connect(self.库名)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM inventory")
        数 = c.fetchone()[0]
        conn.close()
        return 数 > 0

    def _塞种子(self):
        # 真实感的工厂库存（成品/原料/备件 混在一张表，靠「类别」区分）
        种子 = [
            ("P-001", "不锈钢法兰 DN50", "成品", "PN16", 120, "个", 30, "A区-1架"),
            ("P-002", "铝合金外壳 A型", "成品", "400×300", 80, "件", 20, "A区-2架"),
            ("R-001", "冷轧钢板 1.2mm", "原料", "1.2×1250", 500, "公斤", 100, "B区-1架"),
            ("R-002", "不锈钢螺丝 M6", "原料", "M6×20", 3000, "个", 500, "B区-2架"),
            ("R-003", "铜线 2.5mm²", "原料", "100米/卷", 60, "卷", 15, "B区-3架"),
            ("R-004", "PP塑料粒子", "原料", "25kg/包", 200, "包", 50, "B区-4架"),
            ("S-001", "三相电机 0.75kW", "备件", "卧式", 12, "台", 4, "C区-1架"),
            ("S-002", "轴承 6204", "备件", "内径20", 240, "个", 60, "C区-2架"),
            ("S-003", "传送带皮带", "备件", "宽500", 18, "条", 5, "C区-3架"),
            ("S-004", "空气滤芯", "备件", "Φ100", 90, "个", 20, "C区-4架"),
        ]
        conn = sqlite3.connect(self.库名)
        for 编号, 名称, 类别, 规格, 数量, 单位, 安全库存, 库位 in 种子:
            conn.execute(
                "INSERT INTO inventory (编号,名称,类别,规格,数量,单位,安全库存,库位,更新时间) VALUES (?,?,?,?,?,?,?,?,?)",
                (编号, 名称, 类别, 规格, 数量, 单位, 安全库存, 库位, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            )
        conn.commit()
        conn.close()

    def 搜物品(self, 关键词):
        conn = sqlite3.connect(self.库名)
        c = conn.cursor()
        like = f"%{关键词}%"
        c.execute("SELECT 编号,名称,类别,规格,数量,单位,库位 FROM inventory WHERE 名称 LIKE ? OR 编号 LIKE ? OR 类别 LIKE ?", (like, like, like))
        行 = c.fetchall()
        conn.close()
        return [{"编号": r[0], "名称": r[1], "类别": r[2], "规格": r[3], "数量": r[4], "单位": r[5], "库位": r[6]} for r in 行]

    def 查库存(self, 编号或名称):
        conn = sqlite3.connect(self.库名)
        c = conn.cursor()
        like = f"%{编号或名称}%"
        c.execute("SELECT 编号,名称,数量,单位,安全库存,库位 FROM inventory WHERE 名称 LIKE ? OR 编号 LIKE ?", (like, like))
        行 = c.fetchall()
        conn.close()
        return [{"编号": r[0], "名称": r[1], "数量": r[2], "单位": r[3], "安全库存": r[4], "库位": r[5]} for r in 行]

    def 入库(self, 编号或名称, 数量):
        conn = sqlite3.connect(self.库名)
        c = conn.cursor()
        like = f"%{编号或名称}%"
        c.execute("SELECT id, 数量, 名称 FROM inventory WHERE 名称 LIKE ? OR 编号 LIKE ?", (like, like))
        r = c.fetchone()
        if not r:
            conn.close()
            return f"没找到「{编号或名称}」，无法入库"
        new = r[1] + 数量
        c.execute("UPDATE inventory SET 数量=?, 更新时间=? WHERE id=?", (new, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), r[0]))
        conn.commit()
        conn.close()
        return f"「{r[2]}」入库 +{数量}，当前库存 {new}"

    def 出库(self, 编号或名称, 数量):
        conn = sqlite3.connect(self.库名)
        c = conn.cursor()
        like = f"%{编号或名称}%"
        c.execute("SELECT id, 数量, 名称 FROM inventory WHERE 名称 LIKE ? OR 编号 LIKE ?", (like, like))
        r = c.fetchone()
        if not r:
            conn.close()
            return f"没找到「{编号或名称}」，无法出库"
        new = r[1] - 数量
        c.execute("UPDATE inventory SET 数量=?, 更新时间=? WHERE id=?", (new, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), r[0]))
        conn.commit()
        conn.close()
        return f"「{r[2]}」出库 -{数量}，当前库存 {new}"


库存库实例 = 库存库()

# ========== 工具清单（🟢懂框架：这是"说明书"，模型读了才知道能调啥、参数是啥）==========
工具清单 = [
    {
        "type": "function",
        "function": {
            "name": "search_item",
            "description": "按名称、编号或类别模糊搜索库存物品，返回匹配列表（含编号/名称/类别/数量/库位）。当用户问'有没有XX'、'搜一下XX'时用。",
            "parameters": {
                "type": "object",
                "properties": {"关键词": {"type": "string", "description": "物品名称/编号/类别的关键词，如'螺丝'、'R-002'、'原料'"}},
                "required": ["关键词"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock",
            "description": "查询某个物品的当前库存数量、单位、安全库存和库位。当用户问'XX还有多少'、'XX库存'时用。",
            "parameters": {
                "type": "object",
                "properties": {"编号或名称": {"type": "string"}},
                "required": ["编号或名称"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "record_inbound",
            "description": "登记入库：把指定数量加到某物品库存上。当用户说'进了XX多少'、'XX入库'时用。",
            "parameters": {
                "type": "object",
                "properties": {"编号或名称": {"type": "string"}, "数量": {"type": "integer"}},
                "required": ["编号或名称", "数量"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "record_outbound",
            "description": "登记出库：从某物品库存减去指定数量。当用户说'出了XX多少'、'XX领料'时用。",
            "parameters": {
                "type": "object",
                "properties": {"编号或名称": {"type": "string"}, "数量": {"type": "integer"}},
                "required": ["编号或名称", "数量"],
            },
        },
    },
]

# ========== Agent 三件套（🔴死记骨架：while / if tool_calls / 历史.append）==========
def 跑_agent(问题: str) -> str:
    历史 = [{"role": "user", "content": 问题}]
    轮次 = 0
    while 轮次 < 10:                            # ① while：最多10轮，防死循环
        轮次 += 1
        resp = client.chat.completions.create(   # 🟢懂框架：这行=联网问 DeepSeek
            model="deepseek-chat", messages=历史, tools=工具清单, tool_choice="auto")
        回复 = resp.choices[0].message            # 🔴死记：choices 是列表，取第一条必须 [0]
        if 回复.tool_calls:                      # ② if：模型这回合想调工具？
            历史.append(回复)                     # ③ 历史.append：助手这步塞回历史
            for 调用 in 回复.tool_calls:
                函数名 = 调用.function.name
                参数 = json.loads(调用.function.arguments)
                if 函数名 == "search_item":
                    结果 = json.dumps(库存库实例.搜物品(参数["关键词"]), ensure_ascii=False)
                elif 函数名 == "get_stock":
                    结果 = json.dumps(库存库实例.查库存(参数["编号或名称"]), ensure_ascii=False)
                elif 函数名 == "record_inbound":
                    结果 = 库存库实例.入库(参数["编号或名称"], 参数["数量"])
                elif 函数名 == "record_outbound":
                    结果 = 库存库实例.出库(参数["编号或名称"], 参数["数量"])
                历史.append({"role": "tool", "tool_call_id": 调用.id, "content": str(结果)})  # ③ 工具结果也塞回历史
            continue                              # 🟢懂框架：调完工具回到 while 再问一次
        else:
            return 回复.content                   # 模型不调工具 = 给最终答案
    return "⚠️ 达到最大轮次"

# ========== FastAPI 三件套（🔴死记：app=FastAPI() / @app.post / return 字典）==========
app = FastAPI()

class 提问体(BaseModel):
    问题: str

@app.post("/ask")
def ask(提问: 提问体):
    try:
        答案 = 跑_agent(提问.问题)
        return {"answer": 答案}
    except Exception as e:
        return {"answer": f"出错了：{e}"}

@app.get("/")
def 首页():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        return HTMLResponse("<h1>index.html 没找到</h1>")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
