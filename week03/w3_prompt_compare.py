import os
from openai import OpenAI

# 建好电话机（和之前一样）
client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

# 封装：把"发问→拿回答"包成一个函数，避免重复写那段长代码
def 问(提示词):
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": 提示词}],
    )
    return resp.choices[0].message.content

# 同一个意思，三种问法
实验 = [
    ("① 朴素问法", "什么是 API？"),
    ("② 加角色+受众", "你是一个给8岁小孩讲课的老师，用比喻解释什么是 API。"),
    ("③ 加格式约束", "用不超过15个字解释什么是 API，只给定义不要举例子。"),
    ("④ 程序员口吻", "用一行代码注释的风格解释什么是 API"),
]

for 名称, 提示词 in 实验:
    print(f"\n===== {名称} =====")
    print(f"问：{提示词}")
    print(f"答：{问(提示词)}")
