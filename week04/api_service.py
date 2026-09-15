import os
import json
import sqlite3
from datetime import datetime
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel   # pydantic = 数据校验工具，定义"请求体长什么样"
from dotenv import load_dotenv   # 本地运行时自动读取 .env 里的环境变量（Docker 已自带此能力）

load_dotenv()   # 把 .env 里的 DEEPSEEK_API_KEY 等加载进 os.environ

# ===== 客户端（跟之前一样）=====
client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

# ===== 第 3 层：SQLite 数据库（用 class 封装）=====
# 数据库 = 一个本地文件（qa.db），里面一张表存所有问答。
# 列名用英文（跟 API 字段、工具名同规矩：英文最稳）。
# 👉 关键变化：把"连接 / 建表 / 存 / 取"这套 SQL 脏活，全部打包进 记忆库 这个
#    class。业务逻辑（存问答、取历史）只要一行调用，再也不用碰 SQL 语句。
#    这就是学 class 的意义——让毕业代码变干净、好维护。

class 记忆库:
    def __init__(self, 库名="qa.db"):                    # 🔴 死记骨架：class + __init__
        self.库名 = 库名                                 # 只记住库文件名，连接每次用时再开（线程安全）
        self.建表()                                      # 启动时保证表存在

    def 建表(self):                                      # 🟢 懂框架：每次用都开/关自己的连接（避免跨线程共享连接）
        conn = sqlite3.connect(self.库名)
        # 注意：注释必须写在字符串外，字符串里的 # 是数据不是注释（已踩坑多次）
        conn.execute("""
            CREATE TABLE IF NOT EXISTS qa_log (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,  -- 自增编号，每行唯一
                question TEXT,                               -- 问题（文字）
                answer   TEXT,                               -- 答案（文字）
                time     TEXT                                -- 提问时间（文字）
            )
        """)
        conn.commit()
        conn.close()

    def 存(self, 问题, 答案):                             # 🔴 死记骨架：方法首参永远是 self
        # 每次回答完，开一个自己的连接把问答插进去（? 占位防注入）
        conn = sqlite3.connect(self.库名)
        conn.execute(
            "INSERT INTO qa_log (question, answer, time) VALUES (?, ?, ?)",
            (问题, 答案, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        conn.commit()
        conn.close()                                      # 🟢 用完即关，线程安全

    def 取历史(self):                                   # 🔴 死记骨架
        # 每次查都开自己的连接，读最近 20 条（新→旧）
        conn = sqlite3.connect(self.库名)
        行 = conn.execute("SELECT question, answer, time FROM qa_log ORDER BY id DESC LIMIT 20").fetchall()
        conn.close()
        # 把元组转成 {"问题":..,"答案":..,"时间":..} 字典，方便 JSON 返回
        return [{"问题": r[0], "答案": r[1], "时间": r[2]} for r in 行]

记忆库实例 = 记忆库()    # 程序一启动就建好表（等价于原来的 初始化库()）


# ===== 工具：计算器（用 class 封装）=====
# 把"加/减"打包进 计算器 这个对象（封装），Agent 只管调 .加()/.减()，不碰内部算法。
# 这就是学 class 的意义——和 记忆库 class 同一个套路，工具也干净了。
class 计算器:
    def 加(self, num1, num2):                         # 🔴 死记骨架：方法首参永远是 self
        return f"{num1} + {num2} = {num1 + num2}"     # 🟢 懂框架：内部怎么算藏起来
    def 减(self, num1, num2):                         # 🔴 死记骨架
        return f"{num1} - {num2} = {num1 - num2}"     # 🟢 懂框架

计算器实例 = 计算器()    # 造一个计算器对象备用（等价于原来的 加法 函数）

# 给 DeepSeek 看的工具清单（add + sub 两个 function）
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
    },
    {
        "type": "function",
        "function": {
            "name": "sub",
            "description": "计算两个数字相减的差",
            "parameters": {
                "type": "object",
                "properties": {
                    "num1": {"type": "number", "description": "被减数"},
                    "num2": {"type": "number", "description": "减数"}
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
                    结果 = 计算器实例.加(参数["num1"], 参数["num2"])
                elif 函数名 == "sub":
                    结果 = 计算器实例.减(参数["num1"], 参数["num2"])
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
        记忆库实例.存(提问.question, 答案)   # ← 第 3 层：顺手存进数据库（现在是一行 class 调用）
        return {"answer": 答案}          # 再返回给客户端
    except Exception as e:
        # 兜底：下游（DeepSeek / 网络 / 入库）任何报错都不让接口直接崩，
        #       返回 500 + 错误信息，前端/调用方才好处理
        raise HTTPException(status_code=500, detail=f"服务内部出错：{e}")

@app.get("/history")                # ← 第 3 层新增：查历史的接口
def 历史():
    return {"history": 记忆库实例.取历史()}     # 返回最近 20 条问答（一行 class 调用）


# ===== 直接启动：把"怎么起服务"写进代码（不用记 uvicorn 命令）=====
# 用法：python api_service.py        （key 从同目录 .env 自动读取，无需手动设环境变量）
# 注意 host="0.0.0.0"：允许容器外/局域网访问（写 127.0.0.1 只有本机自己能连）
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
