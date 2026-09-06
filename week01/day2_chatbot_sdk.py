"""
参考代码 A —— 用 OpenAI SDK（兼容性写法）调 DeepSeek

这是你在网上找的版本（2026-09-04 跑通过）。逻辑清晰，好读。

它做了一件关键的事：OpenAI 客户端对象帮你封装了所有"看不见"的东西
    1. URL 是固定的，藏在 base_url
    2. 鉴权头 Authorization: Bearer xxx 也帮你构造好
    3. 请求体序列化（dict → JSON 字符串）
    4. 响应解析（JSON 文本 → dict）
    5. 重试 / 限流 / 超时处理（默认带）

代价是你看不见这几层。这就是你"看得懂流程、语法不熟"的原因 —— 你看到的版本里
那些事被 SDK 藏起来了，所以 requests 那一层你接触不到。

Day 2 任务：自己手动用 requests 把这个程序重写一遍（合上这文件别看）。
重写完跑通后，再打开 day2_chatbot_requests.py 对照。
"""

import os  # ← 我加的：让密钥从 .env 读，不硬编码

from dotenv import load_dotenv  # ← 我加的
from openai import OpenAI

load_dotenv()  # ← 我加的

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),  # ← 我改的：原来是 "你的密钥"
    base_url="https://api.deepseek.com",
)

messages = [
    {"role": "system", "content": "你是一个乐于助人的助手。"}
]

while True:
    user_input = input("你: ")
    if user_input == "退出":
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
    )

    ai_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ai_reply})

    print("AI:", ai_reply)