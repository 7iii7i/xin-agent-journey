# ===== Agent 三件套 加强版（不给答案，融合写）=====
# 【本题融合】把中间层练过的"三件套循环体" + 基础版练过的"计算器 class"
#   两个单点，从空白一起写出来，拼成一个能跑的文件。
#
# 【脚手架·不用写】假客户端 client（第1次返回 tool_calls，第2次返回答案）
#   这一段我给你备好，不用改、不用背——它只是 echo 版替身。
#
# 【你要从空白写的两块】
#   ① 计算器 class（加 / 减，和基础版一模一样）
#   ② 跑_agent 三件套（while 轮次 / if 回复.tool_calls / 历史.append）
#
# 【期望输出】（跑 python 这个文件后）：
#   3 + 5 = 8
#   总共跑了 2 轮
#
# 提示：
#   - client.chat.completions.create(...) 那行照抄脚手架给的写法即可
#   - 工具清单这里传 tools=[] 就行（echo 版不读它）
#   - 别漏 轮次 += 1、别把 content 拼成 connent
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


# ===== TODO ①：写出 计算器 class（加 / 减）=====
# 提示：class 计算器:  def 加(self, a, b): return ...   def 减(self, a, b): return ...
#       然后 计算器实例 = 计算器()
class 计算机:
    def 加(self,a,b):
        return f"{a}+{b}={a+b}"
    def 减(self,a,b):
        return f"{a}-{b}={a-b}"
计算机实例=计算机()


# ===== TODO ②：写出 跑_agent 三件套（🔴死记）=====
# 提示：历史=[{"role":"user","content":问题}]  轮次=0
#       while 轮次 < 10:  轮次 += 1
#       resp = client.chat.completions.create(...)
#       回复 = resp.choices[0].message
#       if 回复.tool_calls:  历史.append(回复)  for 调用 ... 历史.append({"role":"tool",...})  continue
#       else: return 回复.content
def 跑_agent(问题: str) -> str:
    历史=[{"role":"user","content":问题}]
    轮次=0
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
                    结果=计算机实例.加(参数["num1"],参数["num2"])
                elif 函数名=="sub":
                    结果 = 计算机实例.减(参数["num1"], 参数["num2"])
                历史.append({"role":"tool","tool_call_id":调用.id,"content":str(结果)})
                continue
        else:
            return 回复.content
    return "达到最大轮次"



# ===== 跑一下 =====
print(跑_agent("3加5等于多少？"))
print("总共跑了", client.第几次, "轮")
