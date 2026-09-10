import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

# 对话历史：一个列表，装着之前所有轮次。空着开始，后面一点点往里加。
历史 = [
    {"role": "user", "content": "我叫忻，请记住我的名字"},
]

# 第 1 轮：把历史发过去
回1 = client.chat.completions.create(model="deepseek-chat", messages=历史).choices[0].message.content
print("AI 第1轮：", 回1)

# 关键：把 AI 的回复也记进历史（这样下一轮它才看得到自己说过啥）
历史.append({"role": "assistant", "content": 回1})

# 第 2 轮：接着问，这次没提名字，看它记不记得
历史.append({"role": "user", "content": "我刚说我叫什么名字？"})
回2 = client.chat.completions.create(model="deepseek-chat", messages=历史).choices[0].message.content
print("AI 第2轮：", 回2)
