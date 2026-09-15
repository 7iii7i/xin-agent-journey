# 用 TestClient 在内存里发请求，验证 Agent 真调工具查库 + 真实 DeepSeek 回答
# 运行：python demo.py
from fastapi.testclient import TestClient
from main import app

客户端 = TestClient(app)

问题列表 = [
    "你们有耳机吗？多少钱？",
    "充电宝还有货吗？",
    "推荐一个显示器",
]

for 问题 in 问题列表:
    print("用户：", 问题)
    响应 = 客户端.post("/ask", json={"question": 问题})
    数据 = 响应.json()
    print("客服：", 数据.get("answer", 数据))
    print("-" * 40)
