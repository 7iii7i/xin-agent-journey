# ===== 第 3 关：填空补全一次 API 调用 =====
# 把下面所有的 ___ 换成正确的内容。不要改其它地方。
# 这一关验证你还记不记得「发一次 LLM 请求」的完整骨架。
import os, requests
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
messages = [{"role": "user", "content": "用一句话解释什么是函数"}]

resp = requests.post(
    "https://api.deepseek.com/chat/completions",
    headers={"Authorization": f"Bearer {api_key}"},
    json={"model": "deepseek-chat", "messages": messages},
)

if resp.status_code == 200:
    data = resp.json()
    content = data["choices"][0]["message"]["content"]
    print(content)
else:
    print("出错：", resp.status_code, resp.text)
