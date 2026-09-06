"""
最小版本 —— 今天只需要看懂这 10 行。

看不懂 week01/day1_first_call.py 很正常，那个是"字典"，留着以后查。
这个才是你第一天要会的东西。
"""

import os

import requests
from dotenv import load_dotenv

load_dotenv()  # 从 .env 读 Key

# 1. 发一个请求出去。json= 这个参数会自动把字典变成 JSON 文本
resp = requests.post(
    "https://api.deepseek.com/chat/completions",
    headers={"Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}"},
    json={
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "用一句话解释什么是 JSON"}],
    },
)

data = resp.json()

# 3. 掏之前先看看有没有。没有就把原文打出来 —— 这习惯能救你无数次
if "choices" not in data:
    print("没拿到回答，接口返回的原文是：")
    print(data)  # 十有八九是 .env 里的 Key 没填对
else:
    print(data["choices"][0]["message"]["content"])
