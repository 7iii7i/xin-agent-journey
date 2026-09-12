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


# ===== 工具说明书（name / 参数必须英文）=====
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


历史 = []   # ← 整个对话历史，跨所有问题保留（记忆的来源）

# ===== 问题列表：第 1 个是多步推理，第 2 个考跨轮记忆 =====
问题列表 = [
    "帮我算一下，先算 3 加 5，再用这个结果加 10，最后是多少",
    "我刚才让你算的第一个算式是什么？最后结果是多少？",
]

# ===== 外层 for：一个问题一个问题地聊（多轮）=====
for 问题 in 问题列表:
    历史.append({"role": "user", "content": 问题})
    print(f"\n你：{问题}")

    轮次 = 0
    最大轮次 = 10            # 每个问题最多推理 10 步

    # ===== 内层 while：针对当前问题做多步推理，直到模型给最终答案 =====
    while 轮次 < 最大轮次:
        轮次 += 1
        print(f"--- 第 {轮次} 轮 ---")

        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=历史,
            tools=工具清单,
            tool_choice="auto",
        )
        回复 = resp.choices[0].message

        if 回复.tool_calls:
            # 模型要调工具 → 执行 → 结果喂回历史 → 继续循环（不退出）
            历史.append(回复)
            for 调用 in 回复.tool_calls:
                函数名 = 调用.function.name
                参数 = json.loads(调用.function.arguments)
                if 函数名 == "add":
                    结果 = 加法(参数["num1"], 参数["num2"])
                    print(f"  [执行工具] add({参数['num1']}, {参数['num2']}) -> {结果}")
                历史.append({"role": "tool", "tool_call_id": 调用.id, "content": str(结果)})
            continue
        else:
            # 模型给了最终文字 → 任务完成 → 跳出内层循环，进入下一个问题
            print("模型：" + 回复.content)
            break

    if 轮次 >= 最大轮次:
        print("⚠️ 达到最大轮次，强制结束（防止死循环）")

print("\n=== 全部问题处理完毕 ===")
