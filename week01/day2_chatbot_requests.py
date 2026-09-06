"""
参考代码 B —— 用 requests 手动重写 SDK 版

把 SDK 替你藏起来的事一层层打开。**核心不是代码，是注释。**

任务（先合上这个文件）：
    1. 不看这个文件，把 day2_chatbot_sdk.py 用 requests 重新敲一遍
    2. 跑通后，再打开这个文件对比
    3. 找出两版的 5 处差异：注释里都标了 SDK 帮你做了哪几件事
"""

import os

import requests
from dotenv import load_dotenv

load_dotenv()

# ▼ SDK 帮你做的事 #1+#2：固定 URL 路径 + 构造鉴权头
BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com").strip()
API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

messages = [
    {"role": "system", "content": "你是一个乐于助人的助手。"},
]

while True:
    user_input = input("你: ")
    if user_input == "退出":
        break

    messages.append({"role": "user", "content": user_input})

    # ▼ SDK 帮你做的事 #3：把 dict 自动变成 JSON 字节流
    #   requests.post(..., json=xxx) 里这个 json= 参数会偷偷做 json.dumps()
    resp = requests.post(
        f"{BASE_URL}/chat/completions",         # 事情 #1 的展开
        headers=HEADERS,                         # 事情 #2 的展开
        json={"model": "deepseek-chat",
              "messages": messages},
        timeout=60,
    )

    # ▼ SDK 帮你做的事 #4：把 JSON 文本还原成 dict
    data = resp.json()

    # ▼ SDK 帮你做的事 #5：内置重试 / 限流 / 异常类
    #   我们这里只做最基本的：异常时打印原文，break 退出
    if "choices" not in data or not data["choices"]:
        print("接口返回异常，原文：", data)
        break

    # ▼ SDK 的 create() 调用里有一个你看不见的属性：finish_reason
    #   它是字符串："stop" 正常结束 / "length" 被截断 / "content_filter" 被拦
    #   教程不爱讲这个，但生产代码必须判 —— 不判就是给用户发半句话
    finish_reason = data["choices"][0].get("finish_reason")
    if finish_reason != "stop":
        print(f"⚠️ 模型没正常说完，finish_reason = {finish_reason}")

    ai_reply = data["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ai_reply})

    print("AI:", ai_reply)