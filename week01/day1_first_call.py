"""
Day 1 —— 第一次真正调用 LLM API

这条脚本只讲一件事：
    一次 API 调用，从头到尾只有一件事在发生 —— 同一个数据不停地变形态。

    第 1 步  你有话要说          str      (你的想法)
    第 2 步  组装成消息列表      list[dict]  ← Python 的数据结构
    第 3 步  组装成请求体        dict     ← 加上模型、温度等参数
    第 4 步  发送  requests.post(json=payload)
                                       ↑ 这里 requests 偷偷帮你做了 json.dumps()
                                       dict → str（JSON 文本），变成字节流发出去
    第 5 步  收到响应            str     ← 网络上跑的全是文本/字节
             response.json()    → dict   ← 把 JSON 文本还原成 dict
    第 6 步  从嵌套 dict 里掏出你要的内容

没有 API Key 也能跑：会走离线演示模式，把同样的六步用假数据演一遍。
有 API Key：把 .env.example 复制成 .env 填入 Key，脚本会自动切到真实调用。

运行：
    uv run python week01/day1_first_call.py
"""

import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()  # 读取 .env 里的环境变量

API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com").strip()

SEP = "─" * 58


def title(n: int, text: str) -> None:
    print(f"\n{SEP}\n第 {n} 步  {text}\n{SEP}")


# ────────────────────────────────────────────────────────────────
# 真实调用部分
# ────────────────────────────────────────────────────────────────

def call_llm(messages: list[dict], model: str = "deepseek-chat") -> str:
    """
    给模型发一组消息，返回它说的话（纯字符串）。

    注意 messages 的类型：list[dict]
    每一条消息都是一个 dict，必须有 role 和 content 两个键。
    """
    title(1, "你的原始输入")
    user_text = messages[-1]["content"]
    print(f"  {user_text!r}")
    print(f"  类型: {type(user_text).__name__}")

    title(2, "组装成消息列表 list[dict]")
    print(json.dumps(messages, ensure_ascii=False, indent=2))
    print(f"  类型: {type(messages).__name__}，长度 {len(messages)}")
    print(f"  第 0 个元素类型: {type(messages[0]).__name__}")

    title(3, "组装成请求体 dict")
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "stream": False,
    }
    print(f"  请求体的键: {list(payload.keys())}")
    print(f"  类型: {type(payload).__name__}")

    title(4, "发送 —— requests 偷偷帮你 json.dumps()")
    print("  requests.post(url, json=payload)")
    print("  等价于: requests.post(url, data=json.dumps(payload),")
    print("                        headers={'Content-Type': 'application/json'})")
    print("  很多人'会用但说不清为什么'，根源就在这一步。")

    url = f"{BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=60)

    # 状态码不是 2xx 就抛异常，不要静默失败
    resp.raise_for_status()

    title(5, "收到响应 —— str 变回 dict")
    raw_text = resp.text
    print(f"  resp.text 前 120 字符:\n  {raw_text[:120]}...")
    print(f"  resp.text 类型: {type(raw_text).__name__}   ← 网络上跑的是文本")
    data = resp.json()  # ← 这一步就是 json.loads(resp.text)
    print(f"  resp.json() 之后类型: {type(data).__name__}   ← 变回 dict 了")

    title(6, "从嵌套 dict 里掏内容（一层一层来，别一口吃）")
    print("  data                              →", type(data).__name__)
    print("  data['choices']                   →", type(data["choices"]).__name__)
    print("  data['choices'][0]                →", type(data["choices"][0]).__name__)
    print("  data['choices'][0]['message']     →", type(data["choices"][0]["message"]).__name__)

    # ⚠️ 生产代码必须判空：真实接口偶尔会返回空的 choices
    choices = data.get("choices")
    if not choices:
        raise RuntimeError(f"接口返回空的 choices，完整响应: {data}")

    content = choices[0]["message"]["content"]
    print(f"\n  最终拿到的 content:\n  {content}")
    print(f"  类型: {type(content).__name__}")

    # 顺带看一下花了多少 token —— 后面做成本控制时这是核心指标
    usage = data.get("usage", {})
    print(f"\n  token 消耗: 输入 {usage.get('prompt_tokens')} / "
          f"输出 {usage.get('completion_tokens')} / 共 {usage.get('total_tokens')}")

    return content


def demo_multi_turn(messages: list[dict]) -> None:
    """多轮对话的本质：把历史消息一直往下拼。"""
    title("附", "多轮对话 = 历史消息不断追加")
    history = [{"role": "system", "content": "你是一个简洁的助手，回答不超过两句话。"}]

    for turn in [
        "我叫忻，浙江台州人。",
        "我刚才说我叫什么？",
        "我老家在哪？",
    ]:
        history.append({"role": "user", "content": turn})
        print(f"\n  >>> 用户: {turn}")
        reply = call_llm(history)
        # 关键：把模型的回复也 append 进 history，下一轮它才"记得"
        history.append({"role": "assistant", "content": reply})
        print(f"  <<< 模型: {reply}")
        print(f"  （当前 history 长度: {len(history)} 条）")


# ────────────────────────────────────────────────────────────────
# 离线演示部分（没有 Key 也能看懂全流程）
# ────────────────────────────────────────────────────────────────

def offline_demo() -> None:
    print("\n" + "═" * 58)
    print("未检测到 DEEPSEEK_API_KEY —— 进入离线演示模式")
    print("═" * 58)
    print("下面的数据结构和真实 DeepSeek 返回完全一致，只是数据是假的。\n")

    title(1, "你的原始输入")
    user_text = "用一句话解释什么是 JSON"
    print(f"  {user_text!r}  类型: {type(user_text).__name__}")

    title(2, "组装成消息列表 list[dict]")
    messages = [{"role": "user", "content": user_text}]
    print(json.dumps(messages, ensure_ascii=False, indent=2))

    title(3, "组装成请求体 dict")
    payload = {"model": "deepseek-chat", "messages": messages, "temperature": 0.7}
    print(json.dumps(payload, ensure_ascii=False, indent=2))

    title(4, "requests 偷偷做的那一步 —— dict → str")
    wire = json.dumps(payload, ensure_ascii=False)
    print(f"  发送出去的真实文本:\n  {wire}")
    print(f"  类型: {type(wire).__name__}   ← 网络只能传文本/字节")

    title(5, "收到响应 —— str 变回 dict")
    fake_response_text = json.dumps(
        {
            "id": "demo",
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "JSON 是一种轻量级的文本数据交换格式。"},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 12, "completion_tokens": 18, "total_tokens": 30},
        },
        ensure_ascii=False,
    )
    print(f"  收到的文本: {fake_response_text[:80]}...")
    data = json.loads(fake_response_text)
    print(f"  json.loads() 之后类型: {type(data).__name__}")

    title(6, "一层一层掏")
    print("  data['choices']                →", type(data["choices"]).__name__)
    print("  data['choices'][0]             →", type(data["choices"][0]).__name__)
    print("  data['choices'][0]['message']  →", type(data["choices"][0]["message"]).__name__)
    print("  data['choices'][0]['message']['content']")
    print("      →", data["choices"][0]["message"]["content"])

    print("\n" + "═" * 58)
    print("想要跑真实调用：")
    print("  1. 复制 .env.example 为 .env")
    print("  2. 去 platform.deepseek.com 注册，充 10 块钱，拿 API Key")
    print("  3. 填进 .env 的 DEEPSEEK_API_KEY")
    print("  4. 重新运行本脚本")
    print("═" * 58)


def main() -> None:
    if API_KEY:
        print("检测到 API Key，进行真实调用。\n")
        # 第一次调用：单轮
        call_llm([{"role": "user", "content": "用一句话解释什么是 JSON"}])
        # 第二次调用：多轮，看它怎么"记住"上下文
        demo_multi_turn([])
    else:
        offline_demo()


if __name__ == "__main__":
    main()
