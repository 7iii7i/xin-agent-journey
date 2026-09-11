import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

# ===== 填空①：写一个真实函数（模型"调工具"时，真正干活的是它）=====
def 加法(num1, num2):
    # 真实逻辑：两数相加，返回一段文字
    return f"{num1} + {num2} = {num1 + num2}"


# ===== 填空②：把上面的函数写成"工具说明书"告诉模型 =====
# ⚠️ 注意：工具名(name)和参数名必须英文/数字/下划线/横线，这是 API 硬性规定，不能用中文
工具清单 = [
    {
        "type": "function",
        "function": {
            "name": "add",                                 # ← 工具名必须英文（和下面派发对应）
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


# ===== 记忆：历史列表（多轮对话靠它，每轮都 append）=====
历史 = []


# ===== 填空③：你要问模型的问题（写好几个可演示"记忆"）=====
问题列表 = [
    "帮我算一下 3 加 5 等于多少",
    "我刚才让你算的是什么算式？结果是多少？",   # 第二问演示"记忆"：模型从历史里看到上一轮调了加法
]


# ===== 主循环：把"记忆"和"工具"揉一起跑 =====
for 问题 in 问题列表:
    历史.append({"role": "user", "content": 问题})
    print(f"\n你：{问题}")

    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=历史,
        tools=工具清单,
        tool_choice="auto",
    )
    回复 = resp.choices[0].message

    if 回复.tool_calls:
        # 模型决定调工具 → 你的代码真执行 → 结果喂回历史
        历史.append(回复)
        for 调用 in 回复.tool_calls:
            函数名 = 调用.function.name
            参数 = json.loads(调用.function.arguments)
            # ===== 填空④：按函数名派发执行（有几个工具就写几行 if）=====
            if 函数名 == "add":                      # ← 这里对应工具名 "add"
                结果 = 加法(参数["num1"], 参数["num2"])
            # elif 函数名 == "第二个函数": 结果 = 第二个函数(参数["xxx"])
            历史.append({"role": "tool", "tool_call_id": 调用.id, "content": str(结果)})
        # 带工具结果再问一次，模型给最终回答
        resp2 = client.chat.completions.create(model="deepseek-chat", messages=历史)
        print("模型：" + resp2.choices[0].message.content)
    else:
        print("模型：" + 回复.content)