# ⑤-4 真实 DeepSeek 调用版（对照 echo demo，只改"生成回复"那一行）
# 和 api_service.py 同源：用 OpenAI 兼容客户端调 DeepSeek
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # 从同目录 .env 读取 DEEPSEEK_API_KEY（若没装 python-dotenv 先 pip install）

# ① 客户端（跟 api_service.py 一模一样）
client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

# ② 工具：加法（跟 api_service.py 一样，工具名用英文 add）
def 加法(num1, num2):
    return f"{num1} + {num2} = {num1 + num2}"

# 工具清单 = 告诉模型"你有什么工具可用"（JSON 格式，照模板改）
工具清单 = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "计算两个数字相加的和",
            "parameters": {
                "type": "object",
                "properties": {
                    "num1": {"type": "number", "description": "第一个加数"},
                    "num2": {"type": "number", "description": "第二个加数"}
                },
                "required": ["num1", "num2"]
            }
        }
    }
]

# ③ Agent 循环三件套（和 echo demo 一样结构，只是"回复"来自真模型）
def 跑_agent(问题: str) -> str:
    历史 = [{"role": "user", "content": 问题}]
    轮次 = 0
    while 轮次 < 10:
        轮次 += 1
        # ↓↓↓ 这一行就是和 echo demo 唯一不同的地方：真调 DeepSeek ↓↓↓
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=历史,
            tools=工具清单,
            tool_choice="auto",   # auto = 让模型自己决定要不要调工具
        )
        回复 = resp.choices[0].message

        # 把模型回复加进历史（真实 SDK 对象直接 append 即可）
        历史.append(回复)

        if 回复.tool_calls:
            for 调用 in 回复.tool_calls:
                函数名 = 调用.function.name
                参数 = json.loads(调用.function.arguments)   # 参数是 JSON 字符串，必须解析
                if 函数名 == "add":
                    结果 = 加法(参数["num1"], 参数["num2"])
                # 工具结果也要加进历史，且要带 tool_call_id 跟前面的调用配对
                历史.append({"role": "tool", "tool_call_id": 调用.id, "content": str(结果)})
            continue   # 调了工具就再循环一轮，让模型看到结果后给最终答案
        else:
            return 回复.content   # 模型直接给答案，结束

    return "⚠️ 达到最大轮次"

# ④ 跑一下（想问别的就改这行问题）
if __name__ == "__main__":
    问题 = "帮我算 3 加 5 等于多少"
    print("问题：", 问题)
    print("回答：", 跑_agent(问题))
