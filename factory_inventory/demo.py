"""验证脚本：用 TestClient 发几个真实工厂问题，确认 Agent 真调工具查/改库。"""
from fastapi.testclient import TestClient
from main import app

c = TestClient(app)

问题列表 = [
    "有没有不锈钢螺丝？",
    "轴承 6204 还有多少？",
    "给冷轧钢板入库 100 公斤",
    "铜线出库 5 卷后还剩多少？",
]

for 问 in 问题列表:
    r = c.post("/ask", json={"问题": 问})
    print(f"问：{问}")
    print(f"答：{r.json().get('answer', '')}")
    print("-" * 50)
