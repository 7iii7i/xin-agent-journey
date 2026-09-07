# ===== Day3：交互式对话机器人（终端实时聊天 + 记住上下文）=====
# 目标：把 Day2「写死的 messages 列表」升级成「你打字、AI 回、连续多轮」的真实对话。
# 新语法：while 循环 / input() / list.append() / break
# 复用：Day2 的 requests 发请求 + .get 安全解析链

import os
import requests
from dotenv import load_dotenv

load_dotenv()  # 从 .env 读 DEEPSEEK_API_KEY，绝不硬编码在代码里
api_key = os.getenv("DEEPSEEK_API_KEY")

# 对话历史。每一轮的 user / assistant 消息都会被 append 进来，
# 下次请求时整份 messages 发给模型，它就能"看见"前面的话 → 记住上下文。
# 第一条是 system：给 AI 设定人设/规则（可选，但强烈建议有）。
messages = [
    {"role": "system", "content": "你是一个简洁、友好的中文助手，回答尽量短。"}
]

print("=== Day3 交互式对话（输入 exit / quit / 退出 结束）===")

# while True：死循环，不断等用户输入，直到遇到 break 才停。
while True:
    user_input = input("你: ")  # input() 在终端打印提示并等你敲一行，返回字符串

    # 统一转小写、去首尾空格后判断是不是退出指令
    if user_input.strip().lower() in ("exit", "quit", "退出"):
        print("再见 👋")
        break  # 跳出 while 循环，程序结束

    # ① 把用户这句加进历史（append = 在列表末尾追加一个元素）
    messages.append({"role": "user", "content": user_input})

    # ② 调模型，带上【完整】messages 历史 → 模型才能记住前面聊了啥
    resp = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": "deepseek-chat", "messages": messages},
    )

    # ③ 安全解析（复习 Day2：字典用 .get，列表 [0] 要手动判空防崩）
    if resp.status_code == 200:
        data = resp.json()
        choices = data.get("choices", [])          # 字典层安全取，缺失给空列表
        first = choices[0] if choices else {}       # 列表层手动判空：空则给 {}
        content = first.get("message", {}).get("content")  # 又回到字典层安全取

        if content:
            print("AI:", content)
            # ④ 把 AI 的回复也加进历史，下一轮用户说话时模型才看得到
            messages.append({"role": "assistant", "content": content})
        else:
            print("AI 回复为空，再试一次")
    else:
        print("请求出错：", resp.status_code, resp.text)
