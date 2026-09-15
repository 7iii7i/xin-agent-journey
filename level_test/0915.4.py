# 你好接口 —— 用"访客"命名，更好对应"你好"场景
# 骨架（🔴死记）：app=FastAPI() / @app.post("/路径")不带冒号 / return 用 {} 不是 ()
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

# 访客资料 = 请求体的"说明书/模具"：规定客户端要发来一个 名字 字段（字符串）
# 🟢懂框架：class 名字(BaseModel): 里面的字段就是接口要收的数据形状
class 访客资料(BaseModel):
    名字: str

# @app.post("/你好") 装饰下面的函数，让它变成 POST /你好 接口
# 你好(访客: 访客资料)：访客 = 装数据的盒子（参数），访客资料 = 盒子的类型标签
# 🔴死记：冒号后面跟 pydantic 类，FastAPI 就自动把请求体按它解析
@app.post("/你好")
def 你好(访客: 访客资料):
    return {"消息": f"你好，{访客.名字}！"}   # 🔴死记：return 用 {} 包字典

# ===== 下面这段是"亲眼看看"的演示（不是骨架必须背的）=====
# 用 TestClient 在本地模拟一次请求，并让你用 input 输入名字，看清 输入→请求体→响应 的全过程
if __name__ == "__main__":
    from fastapi.testclient import TestClient
    客户端 = TestClient(app)
    输入的名字 = input("请输入你的名字（直接回车默认=小明）：") or "小明"
    # 把你输入的名字，打包成接口要的 JSON 请求体（对应 访客资料 的 名字 字段）
    响应 = 客户端.post("/你好", json={"名字": 输入的名字})
    print("你输入的是：", 输入的名字)
    print("发出的请求体：", {"名字": 输入的名字})
    print("服务器回：", 响应.json())
