# ===== Agent 层（agent.py）Tier 2：异步 + 流式 =====
# 这一层只关心"对话怎么流转"，工具/数据库细节都不管。
import json
from config import client, 配置, 日志
from tools import 注册表

SYSTEM = "你是小店智能客服，语气亲切，能用工具查商品/价格/库存，回答简洁有条理。"


# 🔴 死记骨架：Agent 三件套（和之前学的逻辑一字不差，只是整体 async + 加流式）
# 关键设计（🟢懂框架）：为什么"工具轮用非流式、最终轮用流式"？
#   - 工具轮要判断调哪个工具、拿参数，非流式一次拿全最省心，不用去拼流式的碎片 tool_calls。
#   - 最终轮要打字机效果，所以 stream=True，逐 chunk 把 delta.content 吐出去。
#   - 这样避开了"流式里 tool_calls 也是碎片、还得手动拼"这个大坑，教学最清楚。
async def 跑_agent(历史: list):
    # 历史 = [{"role":"user"/"assistant", "content":"..."}]，由会话库按 session 提供
    消息 = [{"role": m["role"], "content": m["content"]} for m in 历史]
    消息.insert(0, {"role": "system", "content": SYSTEM})
    轮次 = 0
    while 轮次 < 10:
        轮次 += 1
        # ① 工具轮：非流式，干净拿到要调的工具和参数
        resp = await client.chat.completions.create(
            model=配置.MODEL,
            messages=消息,
            tools=注册表.清单(),
            tool_choice="auto",
        )
        回复 = resp.choices[0].message
        if 回复.tool_calls:
            消息.append(回复)  # 把 assistant 这条（含 tool_calls）原样存回上下文
            for 调用 in 回复.tool_calls:
                函数名 = 调用.function.name
                参数 = json.loads(调用.function.arguments or "{}")
                日志.info("调用工具 %s 参数=%s", 函数名, 参数)
                # 🟢 懂框架：一行查字典执行，替代原来的 if 函数名=="search_product"
                结果 = await 注册表.调用(函数名, 参数)
                消息.append({"role": "tool", "tool_call_id": 调用.id, "content": str(结果)})
            continue
        # ② 最终轮：流式，逐 token 推给前端（打字机）
        stream = await client.chat.completions.create(
            model=配置.MODEL,
            messages=消息,
            stream=True,
        )
        async for chunk in stream:
            d = chunk.choices[0].delta
            if d.content:
                yield d.content
        return
    yield "⚠️ 达到最大轮次"
