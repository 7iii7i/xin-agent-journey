import os
import json
import sqlite3
from datetime import datetime
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)


# ===== 第 1 层：商品库（SQLite，用 class 封装）=====
# 这就是你学的 SQLite 四步（connect -> execute -> commit/close）的封装版
# 对外只留干净方法：搜商品 / 查价格 / 查库存，业务逻辑一行调用
class 商品库:
    def __init__(self, 库名="shop.db"):
        self.库名 = 库名
        self.建表()
        self.播种()

    def 建表(self):
        conn = sqlite3.connect(self.库名)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT,
                price       REAL,
                stock       INTEGER,
                category    TEXT,
                description TEXT
            )
        """)
        conn.commit()
        conn.close()

    def 播种(self):
        # 只在空表时塞 5 个真实感商品，避免重复运行反复插入
        conn = sqlite3.connect(self.库名)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM products")
        if c.fetchone()[0] == 0:
            c.executemany(
                "INSERT INTO products (name, price, stock, category, description) VALUES (?, ?, ?, ?, ?)",
                [
                    ("无线蓝牙耳机 Pro", 199.0, 50, "耳机", "主动降噪，续航30小时"),
                    ("快充充电宝 20000mAh", 129.0, 30, "充电", "支持22.5W快充"),
                    ("机械键盘 红轴", 299.0, 12, "外设", "RGB背光，热插拔轴"),
                    ("4K显示器 27寸", 999.0, 8, "显示器", "IPS面板，99% sRGB"),
                    ("人体工学椅", 899.0, 5, "家具", "可躺，腰部支撑"),
                ],
            )
            conn.commit()
        conn.close()

    def 搜商品(self, 关键词):
        conn = sqlite3.connect(self.库名)
        行 = conn.execute(
            "SELECT name, price, stock, category, description FROM products WHERE name LIKE ? OR category LIKE ? OR description LIKE ?",
            (f"%{关键词}%", f"%{关键词}%", f"%{关键词}%"),
        ).fetchall()
        conn.close()
        return [{"名称": r[0], "价格": r[1], "库存": r[2], "分类": r[3], "描述": r[4]} for r in 行]

    def 查价格(self, 名称):
        conn = sqlite3.connect(self.库名)
        行 = conn.execute("SELECT price, stock FROM products WHERE name LIKE ?", (f"%{名称}%",)).fetchone()
        conn.close()
        if 行:
            return {"名称": 名称, "价格": 行[0], "库存": 行[1]}
        return {"错误": "没找到该商品"}

    def 查库存(self, 名称):
        conn = sqlite3.connect(self.库名)
        行 = conn.execute("SELECT stock FROM products WHERE name LIKE ?", (f"%{名称}%",)).fetchone()
        conn.close()
        return 行[0] if 行 else 0


商品库实例 = 商品库()


# ===== 第 2 层：给 DeepSeek 看的工具清单（电商版）=====
# 模型读的是这段 JSON 文字说明，自己决定调哪个工具、参数是啥
工具清单 = [
    {
        "type": "function",
        "function": {
            "name": "search_product",
            "description": "按关键词搜索商品（匹配名称/分类/描述），返回商品列表",
            "parameters": {
                "type": "object",
                "properties": {"keyword": {"type": "string", "description": "搜索词，如'耳机'、'充电'"}},
                "required": ["keyword"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_price",
            "description": "查询指定商品的单价和库存",
            "parameters": {
                "type": "object",
                "properties": {"name": {"type": "string", "description": "商品名称（可部分匹配）"}},
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock",
            "description": "查询指定商品的当前库存数量",
            "parameters": {
                "type": "object",
                "properties": {"name": {"type": "string", "description": "商品名称（可部分匹配）"}},
                "required": ["name"],
            },
        },
    },
]


# ===== 第 3 层：Agent 三件套（和你之前写的一字不差）=====
def 跑_agent(问题: str) -> str:
    历史 = [{"role": "user", "content": 问题}]
    轮次 = 0
    while 轮次 < 10:
        轮次 += 1
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=历史,
            tools=工具清单,
            tool_choice="auto",
        )
        回复 = resp.choices[0].message
        if 回复.tool_calls:
            历史.append(回复)
            for 调用 in 回复.tool_calls:
                函数名 = 调用.function.name
                参数 = json.loads(调用.function.arguments)
                if 函数名 == "search_product":
                    结果 = 商品库实例.搜商品(参数["keyword"])
                elif 函数名 == "get_price":
                    结果 = 商品库实例.查价格(参数["name"])
                elif 函数名 == "get_stock":
                    结果 = 商品库实例.查库存(参数["name"])
                历史.append({"role": "tool", "tool_call_id": 调用.id, "content": str(结果)})
            continue
        else:
            return 回复.content
    return "⚠️ 达到最大轮次"


# ===== 第 4 层：FastAPI 把 Agent 暴露成接口 =====
app = FastAPI()

class 提问体(BaseModel):
    question: str

@app.post("/ask")
def ask(提问: 提问体):
    try:
        答案 = 跑_agent(提问.question)
        return {"answer": 答案}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务内部出错：{e}")


# ===== 前端页面：一个服务同时托管聊天界面 + 接口，方便部署 =====
@app.get("/")
def 首页():
    前端路径 = os.path.join(os.path.dirname(__file__), "index.html")
    with open(前端路径, encoding="utf-8") as f:
        return HTMLResponse(f.read())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
