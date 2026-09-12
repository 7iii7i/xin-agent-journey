import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

# ===== 真实函数：模型调工具时真正干活的 =====
def 加法(num1, num2):
    return f"{num1} + {num2} = {num1 + num2}"


# ===== 工具说明书（name / 参数必须英文，这是 API 硬性规定）=====
工具清单 = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "计算两个数字相加的和，当用户问加法、求和、几加几时用",
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


历史 = []

# ===== 通用 Agent 循环：用 while，而不是写死的 for =====
问题 = "帮我算一下 3 加 5 等于多少"
历史.append({"role": "user", "content": 问题})
print(f"你：{问题}")

轮次 = 0
最大轮次 = 10            # ← 防死循环：最多跑 10 轮就强制停

while 轮次 < 最大轮次:
    轮次 += 1
    print(f"\n--- 第 {轮次} 轮 ---")

    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=历史,
        tools=工具清单,
        tool_choice="auto",
    )
    回复 = resp.choices[0].message

    if 回复.tool_calls:
        # 模型要调工具 → 你的代码执行 → 结果喂回历史 → 继续循环（不退出）
        历史.append(回复)
        for 调用 in 回复.tool_calls:
            函数名 = 调用.function.name
            参数 = json.loads(调用.function.arguments)
            if 函数名 == "add":
                结果 = 加法(参数["num1"], 参数["num2"])
            历史.append({"role": "tool", "tool_call_id": 调用.id, "content": str(结果)})
        continue            # ← 关键：回去再问模型，让它看到工具结果后决定下一步
    else:
        # 模型给了最终文字 → 任务完成 → 跳出循环
        print("模型：" + 回复.content)
        break

if 轮次 >= 最大轮次:
    print("⚠️ 达到最大轮次，强制结束（防止 Agent 陷入死循环）")
