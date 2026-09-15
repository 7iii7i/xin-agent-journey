# ===== Agent 三件套（基础版 · 不联网 echo 版）=====
# 目标：练会 ① while 轮次  ② if 回复.tool_calls  ③ 历史.append 这三件套
# 用"假客户端"代替真实 DeepSeek，所以不用联网、不用 key，直接跑
# 结构和真实 api_service.py 的 跑_agent 完全相同，只是把联网那行换成了假的
import json

# ---- 假客户端：第一次假装要调 add(3,5)，第二次直接给答案 ----
class _函数:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments
class _调用:
    def __init__(self, id, function):
        self.id = id
        self.function = function
class _消息:
    def __init__(self, content, tool_calls=None):
        self.content = content
        self.tool_calls = tool_calls
class _选择:
    def __init__(self, message):
        self.message = message
class _回复:
    def __init__(self, choices):
        self.choices = choices
class 假客户端:
    def __init__(self):
        self.第几次 = 0
    @property
    def chat(self): return self
    @property
    def completions(self): return self
    def create(self, model, messages, tools, tool_choice):
        self.第几次 += 1
        if self.第几次 == 1:
            调用 = _调用("call_1", _函数("add", '{"num1":3,"num2":5}'))
            return _回复([_选择(_消息("我帮你算一下", [调用]))])
        return _回复([_选择(_消息("3 + 5 = 8"))])
client = 假客户端()

# ---- 计算器（真实版是联网之外的纯计算，这里保留）----
class 计算器:
    def 加(self, a, b): return f"{a} + {b} = {a+b}"
    def 减(self, a, b): return f"{a} - {b} = {a-b}"
计算器实例 = 计算器()

# ===== 下面是 Agent 三件套骨架（🔴死记）=====
def 跑_agent(问题: str) -> str:
    历史 = [{"role": "user", "content": 问题}]   # 先把用户问题放进历史
    轮次 = 0
    while 轮次 < 10:                            # ① while：最多 10 轮，防止死循环
        轮次 += 1
        resp = client.chat.completions.create(  # 🟢懂框架：真实版这里是联网调 DeepSeek
            model="deepseek-chat", messages=历史, tools=[], tool_choice="auto")
        回复 = resp.choices[0].message
        if 回复.tool_calls:                     # ② if：模型想调工具？
            历史.append(回复)                    # ③ 历史.append：把助手这步（含 tool_calls）塞回历史
            for 调用 in 回复.tool_calls:
                函数名 = 调用.function.name
                参数 = json.loads(调用.function.arguments)
                if 函数名 == "add":
                    结果 = 计算器实例.加(参数["num1"], 参数["num2"])
                elif 函数名 == "sub":
                    结果 = 计算器实例.减(参数["num1"], 参数["num2"])
                历史.append({"role": "tool", "tool_call_id": 调用.id, "content": str(结果)})  # ③ 工具结果也塞回历史
            continue                             # 🟢懂框架：调完工具，回到 while 再问模型一次
        else:
            return 回复.content                  # 模型不再调工具 = 给最终答案
    return "⚠️ 达到最大轮次"

print(跑_agent("3加5等于多少？"))
print("总共跑了", client.第几次, "轮")
