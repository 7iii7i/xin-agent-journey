# 提示词里写明"只输出 JSON，不要任何多余文字"，字段用：姓名 / 性别 / 年龄 / 擅长 / 出处
# 调用时加 response_format={"type":"json_object"}（强制纯 JSON）
# 用 json.loads(...) 把模型返回的字符串解析成字典
# 用 数据.get("年龄", 0) 安全取值，判断：年龄 ≥ 18 打印"已成年"，否则"未成年"
# 额外打印一行：姓名：楚尘，年龄：18
import os
from openai import OpenAI
import json

资料=[]
资料.append({"role":"user","content":"只输出 JSON，不要任何多余文字,楚尘，男，18岁，擅长剑法，来自诸天塔，字段用：姓名 / 性别 / 年龄 / 擅长 / 出处"})
client=OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"],base_url="https://api.deepseek.com")
resp=client.chat.completions.create(model="deepseek-chat",messages=资料,response_format={"type":"json_object"})
print(resp.choices[0].message.content)
信息=json.loads(resp.choices[0].message.content)
print(信息.get("年龄", 0))
age=信息.get("年龄", 0)
if age >=18:
    print("已成年")
else:
    print("未成年")
print(f"姓名:{信息.get('姓名')},年龄:{信息.get('年龄')}")

