import os
from openai import OpenAI
client=OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"],base_url="https://api.deepseek.com")
历史=[]
历史.append({"role":"system","content":"你是一个霸道总裁，用冷漠的话回答我"})
历史.append({"role":"user","content":"老公你好帅"})
resp1=client.chat.completions.create(model="deepseek-chat",messages=历史)
回1=resp1.choices[0].message.content
print(回1)
历史.append({"role":"assistant","content":回1})
历史.append({"role":"user","content":"我刚才说了什么话"})
resp2=client.chat.completions.create(model="deepseek-chat",messages=历史)
print(resp2.choices[0].message.content)
