# ===== Agent 三件套 中间层（不给答案，自己写 跑_agent 的循环体）=====
# 【脚手架】下面已经备好，和基础版一模一样，不用改、不用背：
#   假客户端 client（第1次返回 tool_calls，第2次返回答案）
#   计算器 计算器实例
# 你的任务：把 跑_agent 里标 TODO 的部分写出来，凑齐三件套：
#   ① while 轮次 < 10 控制轮次
#   ② if 回复.tool_calls 判断要不要调工具
#   ③ 历史.append 把助手消息和工具结果都塞回历史
# 写完后直接跑：python 这个文件
# 正确输出应该是：
#   3 + 5 = 8
#   总共跑了 2 轮
import json



# ---- 脚手架：假客户端（不用改）----
class _函数:
    def __init__(self, name, arguments):
        self.name = name; self.arguments = arguments
class _调用:
    def __init__(self, id, function):
        self.id = id; self.function = function
class _消息:
    def __init__(self, content, tool_calls=None):
        self.content = content; self.tool_calls = tool_calls
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

# ---- 脚手架：计算器（不用改）----
class 计算器:
    def 加(self, a, b): return f"{a} + {b} = {a+b}"
    def 减(self, a, b): return f"{a} - {b} = {a-b}"
计算器实例 = 计算器()

# ===== TODO：写出 Agent 三件套（🔴死记）=====
def 跑_agent(问题: str) -> str:
    历史 = [{"role": "user", "content": 问题}]
    轮次 = 0
    # 👇 从这里往下写：while / if 回复.tool_calls / 历史.append
    # 提示：client.chat.completions.create(...) 这一行在 while 里面、if 之前
    # 写完删掉下面这行 pass
    while 轮次 < 10:
        轮次 +=1
        resp=client.chat.completions.create(model="deepseek-chat",messages=历史,tools=[],tool_choice="auto")
        回复=resp.choices[0].message
        if 回复.tool_calls:
            历史.append(回复)
            for 调用 in 回复.tool_calls:
                函数名=调用.function.name
                参数=json.loads(调用.function.arguments)
                if 函数名=="add":
                    结果=计算器实例.加(参数["num1"],参数["num2"])
                elif 函数名=="sub":
                    结果 = 计算器实例.减(参数["num1"],参数["num2"])
            历史.append({"role":"tool","tool_call_id":调用.id,"content":str(结果)})
            continue
        else:
            return 回复.content
    return "达到最大轮次"
print(跑_agent("3加5等于多少？"))
print("总共跑了", client.第几次, "轮")
