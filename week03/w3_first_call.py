import os
from openai import OpenAI

# 从环境变量读 key，不写死在代码里（防泄露）
client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "用一句话解释什么是 API"}],
)

print("模型回答：")
print(resp.choices[0].message.content)
