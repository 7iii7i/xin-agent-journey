import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

# 让模型把一句话"抽取"成结构化 JSON
提示词 = """请把这句话提取成 JSON：
楚尘是诸天塔主，年龄18岁，擅长剑法。
只返回 JSON，格式：{"名字": "", "称号": "", "年龄": 0, "擅长": ""}"""

resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": 提示词}],
    response_format={"type": "json_object"},   # 强制模型只输出合法 JSON，不废话
)

文本 = resp.choices[0].message.content
数据 = json.loads(文本)        # 字符串 → 字典（你 W2 学过的 json 模块）

# 用 .get 安全取值（W2 链式 .get，键缺失返回 None 不崩）
print("名字：", 数据.get("名字"))
print("称号：", 数据.get("称号"))
print("年龄：", 数据.get("年龄"))
print("擅长：", 数据.get("擅长"))

# 结构化之后程序就能直接拿值做判断，比如：
if 数据.get("年龄", 0) >= 18:
    print("已成年，可独立执行任务")
