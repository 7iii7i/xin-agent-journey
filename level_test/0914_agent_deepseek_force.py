# ⑤-4 验证脚本：强制让模型调 add 工具（证明三件套链路真工作，不是模型自答）
import os, json
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com")

def 加法(num1, num2):
    return f"{num1} + {num2} = {num1 + num2}"

工具清单 = [{"type":"function","function":{"name":"add","description":"计算两个数字相加的和",
    "parameters":{"type":"object","properties":{"num1":{"type":"number"},"num2":{"type":"number"}},"required":["num1","num2"]}}}]

def 跑_agent(问题):
    历史 = [{"role":"user","content":问题}]
    轮次 = 0
    while 轮次 < 10:
        轮次 += 1
        # 第一轮强制调 add 证明链路；之后交回 auto 让模型自己决定何时停
        tc = {"type":"function","function":{"name":"add"}} if 轮次 == 1 else "auto"
        resp = client.chat.completions.create(
            model="deepseek-chat", messages=历史, tools=工具清单, tool_choice=tc,
        )
        回复 = resp.choices[0].message
        历史.append(回复)
        if 回复.tool_calls:
            for 调用 in 回复.tool_calls:
                参数 = json.loads(调用.function.arguments)
                if 调用.function.name == "add":
                    结果 = 加法(参数["num1"], 参数["num2"])
                    print(f"  ↳ [第{轮次}轮] 模型要求调 add({参数['num1']}, {参数['num2']})，工具返回：{结果}")
                历史.append({"role":"tool","tool_call_id":调用.id,"content":str(结果)})
            continue
        else:
            return 回复.content
    return "⚠️ 达到最大轮次"

if __name__ == "__main__":
    print("问题：帮我算 3 加 5 等于多少")
    print("回答：", 跑_agent("帮我算 3 加 5 等于多少"))
