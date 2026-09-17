# ===== 接口层（main.py）Tier 2：async + SSE 流式 + CORS + lifespan =====
import os
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from db import 商品库实例, 会话库实例
from agent import 跑_agent
from config import 配置, 日志


# 🟢 懂框架：lifespan 是 FastAPI 的"启动/关闭钩子"。
# 原来 __init__ 里不能 await，所以把"建表+播种"挪到这儿，服务起来时 await 一次。
@asynccontextmanager
async def lifespan(app):
    await 商品库实例.初始化()
    await 会话库实例.初始化()
    日志.info("数据库初始化完成，服务就绪")
    yield


app = FastAPI(lifespan=lifespan)

# CORS：允许前端从别的端口/域名访问本接口（🟢懂框架，生产要收紧 allow_origins）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# 请求体多了 session_id：区分"是谁在聊"，实现多用户各自上下文
class 提问体(BaseModel):
    session_id: str
    question: str


@app.post("/ask")
async def ask(提问: 提问体):
    # 1) 先把用户这句存进他的会话
    await 会话库实例.追加(提问.session_id, "user", 提问.question)
    # 2) 取出这个 session 的全部历史（多轮上下文）
    历史 = await 会话库实例.取历史(提问.session_id)

    # 3) 用 StreamingResponse 把 Agent 的输出一截一截推给前端（SSE 协议）
    async def 事件流():
        完整 = ""
        try:
            async for token in 跑_agent(历史):
                完整 += token
                # SSE 格式：每行 "data: <内容>\n\n"。用 json.dumps 包住，特殊字符不会炸。
                yield f"data: {json.dumps(token, ensure_ascii=False)}\n\n"
        except Exception as e:
            日志.exception("Agent 执行出错")
            yield f"data: {json.dumps('⚠️ 服务出错：' + str(e), ensure_ascii=False)}\n\n"
        finally:
            # 4) 流结束后，把完整回答存进会话（下一轮才能接上）
            if 完整.strip():
                await 会话库实例.追加(提问.session_id, "assistant", 完整)

    return StreamingResponse(事件流(), media_type="text/event-stream")


@app.get("/history")
async def 历史(session_id: str):
    return {"history": await 会话库实例.取历史(session_id)}


@app.get("/")
def 首页():
    前端路径 = os.path.join(os.path.dirname(__file__), "index.html")
    with open(前端路径, encoding="utf-8") as f:
        return HTMLResponse(f.read())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=配置.端口)
