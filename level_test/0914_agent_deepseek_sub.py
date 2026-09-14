# ⑤-4 真实 DeepSeek 调用版 · 减法工具对照版（只把"加法"换成"减法"，其余和加版一模一样）
# 作用：给你当对照样板，证明"换工具"只是改 ② 工具定义 + ⑥ 调用判断，三件套不动
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

# ② 工具：减法（换成 sub，函数体改成相减）
def 减法(num1, num2):
    return f"{num1} - {num2} = {num1 - num2}"

# 工具清单：把 name 改成 sub、description 改成"相减"，参数结构不变
工具清单 = [
    {
        "type": "function",
        "function": {
            "name": "sub",
            "description": "计算两个数字相减的差",
            "parameters": {
                "type": "object",
                "properties": {
                    "num1": {"type": "number", "description": "被减数"},
                    "num2": {"type": "number", "description": "减数"}
                },
                "required": ["num1", "num2"]
            }
        }
    }
]

# ③ Agent 循环三件套（结构完全不动，只把"add"判断改成"sub"）
def 跑_agent(问题: str) -> str:
    历史 = [{"role": "user", "content": 问题}]
    轮次 = 0
    while 轮次 < 10:
        轮次 += 1
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=历史,
            tools=工具清单,
            tool_choice="auto",
        )
        回复 = resp.choices[0].message
        历史.append(回复)

        if 回复.tool_calls:
            for 调用 in 回复.tool_calls:
                函数名 = 调用.function.name
                参数 = json.loads(调用.function.arguments)
                if 函数名 == "sub":          # ← 这里从 "add" 改成 "sub"
                    结果 = 减法(参数["num1"], 参数["num2"])
                历史.append({"role": "tool", "tool_call_id": 调用.id, "content": str(结果)})
            continue
        else:
            return 回复.content

    return "⚠️ 达到最大轮次"

# ④ 跑一下（问题也改成减法）
if __name__ == "__main__":
    问题 = "帮我算 10 减 3 等于多少"
    print("问题：", 问题)
    print("回答：", 跑_agent(问题))
