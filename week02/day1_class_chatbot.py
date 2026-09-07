# week02/day1：面向对象入门 —— 把之前的聊天机器人重构成「类」
# 新概念：class / __init__ / self / 实例方法 / 属性 / if __name__ == "__main__"
# 复习：messages 历史记忆（day3）、requests 调 API（day1/day2）

import os
import requests
from dotenv import load_dotenv

load_dotenv()


class ChatBot:
    def __init__(self, model="deepseek-chat"):
        # __init__ 是「构造方法」：创建对象时自动运行，用来做初始化
        # self 指向「这个对象自己」；挂在 self 上的变量属于这个对象（叫「属性」）
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.model = model
        self.messages = []  # 对话历史，初始为空列表（每个对象的独立记忆）

    def ask(self, user_text):
        # 实例方法：第一个参数永远是 self，调用时不用手写
        self.messages.append({"role": "user", "content": user_text})  # 用户的话进历史
        resp = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": self.model, "messages": self.messages},
        )
        if resp.status_code == 200:
            data = resp.json()
            reply = data["choices"][0]["message"]["content"]
            self.messages.append({"role": "assistant", "content": reply})  # 回答也进历史
            return reply
        return f"出错：{resp.status_code}"

    def chat_loop(self):
        # 交互循环：和 day3 的 while 一样，只是逻辑包在了类里
        print("（输入 exit 退出）")
        while True:
            user_text = input("你：")
            if user_text.lower() == "exit":
                break
            print("AI：", self.ask(user_text))


if __name__ == "__main__":
    # 直接运行 python day1_class_chatbot.py 时，__name__ 是 "__main__"，这行执行
    # 被别的文件 import 时，__name__ 是模块名，这行不执行（不会自动弹输入）
    bot = ChatBot()      # 创建对象（自动调用 __init__）
    bot.chat_loop()      # 调实例方法
