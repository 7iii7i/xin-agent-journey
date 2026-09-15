# 工具 class 演示：把"计算器（加/减）"封装成一个对象
# 这就是"封装"——调用方只看到 计算器实例.加(...) / 计算器实例.减(...)，
# 不用懂内部怎么算。和你已做的 记忆库 class 是同一套路子。

class 计算器:                              # 🔴 死记骨架：class + 名字
    def 加(self, num1, num2):             # 🔴 死记：方法首参永远是 self
        return f"{num1} + {num2} = {num1 + num2}"   # 🟢 懂框架：内部怎么算藏起来
    def 减(self, num1, num2):             # 🔴 死记
        return f"{num1} - {num2} = {num1 - num2}"    # 🟢 懂框架

# 给 DeepSeek 看的工具清单（add + sub 两个 function schema）
工具清单 = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "计算两个数字相加的和",
            "parameters": {
                "type": "object",
                "properties": {
                    "num1": {"type": "number", "description": "第一个加数"},
                    "num2": {"type": "number", "description": "第二个加数"}
                },
                "required": ["num1", "num2"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sub",
            "description": "计算两个数字相减的差",
            "parameters": {
                "type": "object",
                "properties": {
                    "num1": {"type": "number", "description": "被减数"},
                    "num2": {"type": "number", "description": "减数"}
                },
                "required": ["num1", "num2"]
            }
        }
    }
]

# 模拟 Agent：拿到"函数名 + 参数"后，调用 class 里对应的方法
def 调用工具(函数名, 参数):
    计算器实例 = 计算器()                 # 造一个计算器对象
    if 函数名 == "add":
        return 计算器实例.加(参数["num1"], 参数["num2"])   # 点号自动填 self
    elif 函数名 == "sub":
        return 计算器实例.减(参数["num1"], 参数["num2"])

if __name__ == "__main__":
    print("工具清单数量:", len(工具清单))          # 应为 2（add + sub）
    print(调用工具("add", {"num1": 23, "num2": 45}))   # 23 + 45 = 68
    print(调用工具("sub", {"num1": 100, "num2": 38}))  # 100 - 38 = 62
