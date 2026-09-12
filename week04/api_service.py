import os
import json
import sqlite3
from datetime import datetime
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel   # pydantic = 数据校验工具，定义"请求体长什么样"

# ===== 客户端（跟之前一样）=====
client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

# ===== 第 3 层：SQLite 数据库 =====
# 数据库 = 一个本地文件（qa.db），里面一张表存所有问答。
# 列名用英文（跟 API 字段、工具名同规矩：英文最稳）。

def 初始化库():
    # 连数据库文件，没有就自动新建
    conn = sqlite3.connect("qa.db")
    c = conn.cursor()
    # 建表：IF NOT EXISTS 意思是"表已存在就跳过，不报错"
    c.execute("""
        CREATE TABLE IF NOT EXISTS qa_log (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,  -- 自增编号，每行唯一
            question TEXT,                               -- 问题（文字）
            answer   TEXT,                               -- 答案（文字）
            time     TEXT                                -- 提问时间（文字）
        )
    """)
    conn.commit()
    conn.close()

初始化库()   # 程序一启动就把表建好

def 存问答(问题, 答案):
    # 每次回答完，把这一对问答插进表里
    conn = sqlite3.connect("qa.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO qa_log (question, answer, time) VALUES (?, ?, ?)",
        (问题, 答案, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()
    conn.close()

def 取历史():
    # 从表里读最近 20 条（新→旧），返回成列表
    conn = sqlite3.connect("qa.db")
    c = conn.cursor()
    c.execute("SELECT question, answer, time FROM qa_log ORDER BY id DESC LIMIT 20")
    行 = c.fetchall()   # fetchall = 拿到全部行，每行是 (问题, 答案, 时间) 元组
    conn.close()
    # 把元组转成 {"问题":..,"答案":..,"时间":..} 字典，方便 JSON 返回
    return [{"问题": r[0], "答案": r[1], "时间": r[2]} for r in 行]


# ===== 工具：加法 =====
def 加法(num1, num2):
    return f"{num1} + {num2} = {num1 + num2}"

工具清单 = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "计算两个数字相加的和",
            "parameters": {
                "type": "object",
                "properties": {
                    "num1": {"type": "number", "description": "第一个加数"},
                    "num2": {"type": "number", "description": "第二个加数"}
                },
                "required": ["num1", "num2"]
            }
        }
    }
]


# ===== 核心：把之前的 Agent while 循环包成一个函数 =====
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
                if 函数名 == "add":
                    结果 = 加法(参数["num1"], 参数["num2"])
                历史.append({"role": "tool", "tool_call_id": 调用.id, "content": str(结果)})
            continue
        else:
            return 回复.content
    return "⚠️ 达到最大轮次"


# ===== FastAPI：把一个普通函数变成"网络接口" =====
app = FastAPI()

class 提问体(BaseModel):
    question: str

@app.post("/ask")
def ask(提问: 提问体):
    try:
        答案 = 跑_agent(提问.question)   # 先算出答案（内部会调 DeepSeek）
        存问答(提问.question, 答案)      # ← 第 3 层新增：顺手存进数据库
        return {"answer": 答案}          # 再返回给客户端
    except Exception as e:
        # 兜底：下游（DeepSeek / 网络 / 入库）任何报错都不让接口直接崩，
        #       返回 500 + 错误信息，前端/调用方才好处理
        raise HTTPException(status_code=500, detail=f"服务内部出错：{e}")

@app.get("/history")                # ← 第 3 层新增：查历史的接口
def 历史():
    return {"history": 取历史()}     # 返回最近 20 条问答


# ===== 直接启动：把"怎么起服务"写进代码（不用记 uvicorn 命令）=====
# 用法：python api_service.py        （必须先设好 DEEPSEEK_API_KEY 环境变量）
# 注意 host="0.0.0.0"：允许容器外/局域网访问（写 127.0.0.1 只有本机自己能连）
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
