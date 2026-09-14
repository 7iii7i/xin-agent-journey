# ============================================================
# 完全版骨架（毕业练习 · W4-5 终极关）
# 目标：把 9 个 TODO 填完，跑通 = FastAPI + while + SQLite 三块全毕业
# 用法：python 完全版_骨架.py   （需先设好 DEEPSEEK_API_KEY 环境变量）
# 深度速查（按你的习惯）：
#   🔵 FastAPI 三件套 = 理解+会改（脚手架，照模板填）
#   🟢 while 大脑     = 必须自己写（核心逻辑）
#   🟠 SQLite 四步     = 必须自己写（核心逻辑）
# ============================================================

import os
import json
import sqlite3
from datetime import datetime
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ----- 客户端（脚手架·照抄，不用背）-----
client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

# ===== 第3层 SQLite（四步：connect→execute→commit→close｜必须自己写）=====
# TODO 1：初始化库 —— 连 qa.db、建表 qa_log(id自增, question, answer, time)、commit、close
def 初始化库():
    pass

初始化库()   # 启动即建表（表已存在时 IF NOT EXISTS 会跳过，不报错）

# TODO 2：存问答(问题, 答案) —— 连、INSERT(用?占位防注入)、commit、close
def 存问答(问题, 答案):
    pass

# TODO 3：取历史() —— 连、SELECT 最近20条(新→旧)、fetchall、转字典列表、close、return
def 取历史():
    pass

# ===== 工具（业务逻辑｜必须自己写）=====
# TODO 4：加法(num1, num2) —— 返回 "a + b = 结果" 字符串
def 加法(num1, num2):
    pass

# TODO 5：工具清单 = [ add 的 JSON schema ]（name / description / parameters）
工具清单 = []

# ===== 核心 while 大脑（必须自己写）=====
# TODO 6：跑_agent(问题) —— 历史=[用户问题]；while 轮次<10；调 DeepSeek(tool_choice="auto")；
#         if 回复.tool_calls: 历史.append(回复) → 遍历执行工具 → 结果带 tool_call_id 回历史 → continue
#         else: return 回复.content
def 跑_agent(问题: str) -> str:
    pass

# ===== FastAPI 三件套（理解+会改）=====
app = FastAPI()

# TODO 7：class 提问体(BaseModel): question: str
class 提问体(BaseModel):
    pass

# TODO 8：@app.post("/ask") def ask(提问):
#         try: 答案=跑_agent(提问.question) → 存问答(提问.question, 答案) → return {"answer": 答案}
#         except: raise HTTPException(status_code=500, detail=f"服务内部出错：{e}")
@app.post("/ask")
def ask(提问: 提问体):
    pass

# TODO 9：@app.get("/history") def 历史(): return {"history": 取历史()}
@app.get("/history")
def 历史():
    pass

# ----- 启动（脚手架·照抄）-----
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
