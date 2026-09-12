# ===== Step 3：pytest 测试 =====
# 作用：不启动真服务器、不联网、不花 DeepSeek key，
#       用 FastAPI 自带的 TestClient 直接测接口逻辑。
#
# 为什么用假数据（mock）？
#   /ask 内部会真的调 DeepSeek（跑_agent）。单测不该依赖外网/真实 key，
#   所以用 monkeypatch 把 跑_agent 换成"返回假答案"的函数，只验证：
#     ① 路由接得到请求  ② 返回格式对  ③ 会存进"库"  ④ 异常能兜底
#
# 运行（在 week04 目录下）：
#   python -m pytest test_api.py -v

# ⚠️ 必须在 import api_service 之前设好 key，
#    因为 api_service.py 在导入时就读 DEEPSEEK_API_KEY 建客户端，否则直接 KeyError 崩
import os
os.environ.setdefault("DEEPSEEK_API_KEY", "sk-test-fake-key")

import pytest
from fastapi.testclient import TestClient

import api_service
from api_service import app


# ---- 用内存字典假装是数据库，隔离真实 qa.db，不污染文件 ----
@pytest.fixture
def 假库():
    数据 = []                                   # 列表当"数据库表"

    def 存(问题, 答案):
        数据.append({"问题": 问题, "答案": 答案, "时间": "2026-09-12 00:00:00"})

    def 取():
        return list(reversed(数据))             # 仿原逻辑：新→旧

    # 把模块里的真函数替换成内存版
    api_service.存问答 = 存
    api_service.取历史 = 取
    return 数据


# ---- 客户端：把"真调 DeepSeek"换成"假回答" ----
@pytest.fixture
def 客户端(假库, monkeypatch):
    def 假跑_agent(问题: str) -> str:
        return f"[测试假答案] {问题}"

    monkeypatch.setattr(api_service, "跑_agent", 假跑_agent)
    return TestClient(app)


# ① 正常：POST /ask 返回 200 且答案正确
def test_ask_正常返回(客户端):
    响应 = 客户端.post("/ask", json={"question": "3加5"})
    assert 响应.status_code == 200
    assert 响应.json()["answer"] == "[测试假答案] 3加5"


# ② 缺字段：pydantic 校验 question 必填，缺了返回 422
def test_ask_缺字段返回422(客户端):
    响应 = 客户端.post("/ask", json={})        # 没给 question
    assert 响应.status_code == 422


# ③ 会存库：调一次 /ask，内存库里应有 1 条
def test_ask_会存入历史(客户端, 假库):
    客户端.post("/ask", json={"question": "你好"})
    assert len(假库) == 1
    assert 假库[0]["问题"] == "你好"


# ④ 查历史：GET /history 能查到刚存的问题
def test_history_能查到(客户端, 假库):
    客户端.post("/ask", json={"question": "今天天气"})
    响应 = 客户端.get("/history")
    assert 响应.status_code == 200
    历史 = 响应.json()["history"]
    assert any(h["问题"] == "今天天气" for h in 历史)


# ⑤ 异常兜底：跑_agent 抛错时接口应返回 500（而不是整个进程崩）
def test_ask_内部异常返回500(客户端, monkeypatch):
    def 会炸(问题):
        raise RuntimeError("DeepSeek 挂了")

    monkeypatch.setattr(api_service, "跑_agent", 会炸)
    响应 = 客户端.post("/ask", json={"question": "x"})
    assert 响应.status_code == 500
