import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

# ---- ① 真实工具：你写的普通 Python 函数 ----
def 查天气(城市):
    # 这里用假数据演示；真实场景会去调一个天气 API
    假数据库 = {"北京": "晴 25度", "上海": "多云 28度", "玉环": "小雨 23度"}
    return 假数据库.get(城市, "暂无该城市数据")

# ---- ② 把工具"告诉"模型：用 JSON 描述 名字/干嘛/参数 ----
工具清单 = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",            # 工具名（英文，给模型看的）
            "description": "查询指定城市的当前天气情况",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名，如 玉环"}
                },
                "required": ["city"]
            }
        }
    }
]

# ---- ③ 第1轮：用户提问，把工具也一起发过去 ----
对话 = [{"role": "user", "content": "玉环今天天气怎么样？适合跑步吗？"}]
print("用户：玉环今天天气怎么样？适合跑步吗？\n")

resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=对话,
    tools=工具清单,
    tool_choice="auto",          # 让模型自己决定：调不调工具、调哪个
)
回复 = resp.choices[0].message

# ---- ④ 模型决定：要不要调工具？----
if 回复.tool_calls:
    print(">>> 模型决定调用工具：get_weather\n")
    对话.append(回复)            # 把模型"我要调工具"这句话也记进历史
    for 调用 in 回复.tool_calls:
        函数名 = 调用.function.name
        参数 = json.loads(调用.function.arguments)
        print(f">>> 模型要查的城市：{参数['city']}")
        结果 = 查天气(参数["city"])     # 真正执行你的 Python 函数
        print(f">>> 工具返回：{结果}\n")
        对话.append({                   # 把工具结果喂回去给模型
            "role": "tool",
            "tool_call_id": 调用.id,
            "content": 结果,
        })
    # ---- ⑤ 第2轮：带着工具结果再问一次，模型给最终回答 ----
    resp2 = client.chat.completions.create(
        model="deepseek-chat",
        messages=对话,
    )
    print("模型：" + resp2.choices[0].message.content)
else:
    print("模型：" + 回复.content)
