import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel


def 跑agent(问题):
    历史=[{"role":"user","content":问题}]
    while 轮次 < 10:
        resp=client.chat.comleptions.create(model="deepseek-chat",messages=历史,tools=工具清单,tool_choice="auto")
        回复=resp.choices[0].message
        if 回复.tool_calls:
            历史.append(回复)
            for 调用 in 回复.tool_calls:
                函数名=调用.function.name
                参数=json.loads(调用.function.arguments)
                if 函数名=="add":
                    结果=加法(参数["num1"],参数["num2"])
                    历史.append({"role":"tool","tool_call_id":调用.id,"content":str(结果)})
            continue

    return 回复.content

app=FastAPI()

class 提问体(BaseModel):
    question:str


@app.post("/ask")
def ask(提问,提问体):
    return{"answer":"...."}


conn=sqlite3.connect("test.db")
cur=conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS t(id INTEGER name TEXT)")
cur.execute("INSERT INTO t values(1,'小明')")
rows=cur.fetchall()
conn.commit()
conn.close()

