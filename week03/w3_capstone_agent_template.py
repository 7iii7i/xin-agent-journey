import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

# ===== 填空①：写一个真实函数（模型"调工具"时，真正干活的是它）=====
def 你的函数(参数名):
    # TODO: 写你的真实逻辑，最后 return 一段文字
    # 例：return "小雨 23度"
    pass   # ← 删掉这行，换成你的 return


# ===== 填空②：把上面的函数写成"工具说明书"告诉模型 =====
工具清单 = [
    {
        "type": "function",
        "function": {
            "name": "你的函数名",                       # ← 必须和 def 的名字一模一样
            "description": "这个函数干嘛用（模型靠这句决定调不调）",  # ← 写清楚用途
            "parameters": {
                "type": "object",
                "properties": {
                    "参数名": {"type": "string", "description": "参数说明"}   # ← 改成你的参数
                },
                "required": ["参数名"]                   # ← 必填参数写这里
            }
        }
    }
]


# ===== 记忆：历史列表（多轮对话靠它，每轮都 append）=====
历史 = []


# ===== 填空③：你要问模型的问题（写好几个可演示"记忆"）=====
问题列表 = [
    "在这里写第一个问题",
    # "在这里写第二个问题（可选，演示它记得前文）",
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
            if 函数名 == "你的函数名":
                结果 = 你的函数(参数["参数名"])
            # elif 函数名 == "第二个函数": 结果 = 第二个函数(参数["xxx"])
            历史.append({"role": "tool", "tool_call_id": 调用.id, "content": str(结果)})
        # 带工具结果再问一次，模型给最终回答
        resp2 = client.chat.completions.create(model="deepseek-chat", messages=历史)
        print("模型：" + resp2.choices[0].message.content)
    else:
        print("模型：" + 回复.content)
