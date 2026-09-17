# 离线测试（Tier 2 异步版）：用 unittest.mock 把 DeepSeek 客户端"假掉"，
# 不花一分钱 API、不联网，也能验证「异步工具注册表分发」和「异步会话记忆」。
#
# 🟢 懂框架：这就是"mock 掉 LLM 也能测"——面试加分点，说明你懂"可测性"。
#   跑_agent 现在是 async generator，数据库也是 async，所以测试整体用 asyncio + AsyncMock。
import os
import sys
import asyncio
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from unittest.mock import AsyncMock, MagicMock
import agent
from db import 会话库实例


def 造假工具轮(工具名, 参数):
    # 模拟"模型说：我要调这个工具"，对应 agent.py 里的 工具轮（非流式）
    # 注意结构要匹配 agent 里的 resp.choices[0].message.tool_calls
    消息 = MagicMock()
    tc = MagicMock()
    tc.function.name = 工具名
    tc.function.arguments = json.dumps(参数)
    tc.id = "call_1"
    消息.tool_calls = [tc]
    调用 = MagicMock()
    调用.choices = [MagicMock(message=消息)]
    return 调用


def 造假最终轮():
    # 模拟"最终轮的非流式判断"：模型说不用工具（agent 随后会用流式重发拿 token）
    消息 = MagicMock()
    消息.tool_calls = None
    调用 = MagicMock()
    调用.choices = [MagicMock(message=消息)]
    return 调用


async def 造假流(文本):
    # 模拟"最终轮流式输出"，对应 agent.py 里的 async for chunk
    # ⚠️ 必须是真·异步生成器（async def + yield）；同步 iter 不能用于 async for
    chunk = MagicMock()
    chunk.choices = [MagicMock(delta=MagicMock(content=文本))]
    yield chunk


async def 测注册表_异步_带工具():
    agent.client.chat.completions.create = AsyncMock(side_effect=[
        造假工具轮("search_product", {"keyword": "耳机"}),  # 轮1 非流式：要调工具
        造假最终轮(),                                         # 轮2 非流式：不用工具
        造假流("无线蓝牙耳机 Pro 199元，库存50。"),          # 轮2 流式：逐 token
    ])
    out = ""
    async for t in agent.跑_agent([{"role": "user", "content": "有耳机吗"}]):
        out += t
    assert out == "无线蓝牙耳机 Pro 199元，库存50。", out
    print("✓ 异步注册表分发 + 流式最终轮：通过")


async def 测会话库_异步隔离():
    await 会话库实例.初始化()  # 确保表存在
    sid = "测试会话_" + os.urandom(4).hex()
    await 会话库实例.追加(sid, "user", "你好")
    await 会话库实例.追加(sid, "assistant", "您好，想看什么？")
    历史 = await 会话库实例.取历史(sid)
    assert 历史[0]["content"] == "你好"
    assert 历史[-1]["content"] == "您好，想看什么？"
    # 不同 session 互不干扰
    await 会话库实例.追加("另一个会话", "user", "别的话")
    assert await 会话库实例.取历史(sid) == 历史
    print("✓ 会话库异步 + 多轮隔离：通过")


if __name__ == "__main__":
    asyncio.run(测注册表_异步_带工具())
    asyncio.run(测会话库_异步隔离())
    print("\n全部离线测试通过 ✅")
