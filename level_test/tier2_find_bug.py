# ===== 第 2 关：读代码 + 找 bug + 修 =====
# 不要先运行，先读。下面这段的意图是：从一段 JSON 文本里取出城市名并打印。
# 它有两个 bug。找出并修好，然后运行验证。
import os, json

# 假设这是某次接口返回的（注意：是「字符串」，不是字典）
raw = '{"data": {"city": {"name": "玉环", "code": "331083"}}}'

# BUG 1：这里用 resp["data"]["city"]["name"] 硬取值。
#        如果某天返回里没有 "city" 这个 key，会怎样？怎么改得更稳？
resp = json.loads(raw)
name = resp["data"]["city"]["name"]
print("城市：" + name)

# BUG 2：如果 raw 不是合法 JSON（比如网络返回了报错文本），
#        上面 json.loads 会直接崩。请用 try / except 把它包起来，
#        崩了就打印一句"解析失败"。
