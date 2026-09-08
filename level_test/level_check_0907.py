# ============================================================
# 水平小测 · 2026-09-07
# 目标：看看你目前的 Python 真实水平（week01 + week02 day1 范围）
# 要求：
#   1. 每题从空白自己写出来，不要复制粘贴
#   2. 写完在终端跑：python -m uv run python level_test/level_check_0907.py
#   3. 看输出对不对，把代码 + 输出发我，我帮你批
# 覆盖：列表/字典遍历、条件判断、.get 安全取值、json.loads、class 封装
# ============================================================


# ---------- 题目 1：列表 + 字典遍历 + 条件 ----------
# 数据已给好，你只写"处理逻辑"
students = [
    {"name": "张三", "score": 85},
    {"name": "李四", "score": 59},
    {"name": "王五", "score": 92},
    {"name": "赵六", "score": 73},
]

# TODO 1：用 for 循环遍历 students
#   - 只打印"及格"(score >= 60)的学生：名字 + 分数
#   - 算所有学生的平均分，最后打印"平均分：xx.x"
# 提示：需要一个变量累加总分，循环外面再除以 len(students)
total=0
for student in students:
    score = student["score"]
    name = student["name"]
    if score >= 60:
        print(name, score)
    total= total+score
print(total/len(students))




# ---------- 题目 2：嵌套字典安全取值 ----------
import json

raw = '{"user": {"profile": {"nickname": "小明", "age": 28}}}'

# TODO 2：
#   1) 用 json.loads(raw) 把字符串变成字典
#   2) 用 .get() 链安全取出 nickname 并打印
#   3) 任意一层缺失也不能崩，打印"未知"
# 这是你前两天练过的 .get 链，自己写一遍（最后一层用默认 None + 判空）
try:
    resp=json.loads(raw)
except Exception:
    print("未知")
else:
    nickname=resp.get("user", {}).get("profile", {}).get("nickname")
    if nickname:
        print(nickname)
    else:
        print("未知")




# ---------- 题目 3：用 class 写一个小记账本（结合你会计背景）----------
# TODO 3：写一个 AccountBook 类
#   - __init__：初始化 self.records = [] 存记录
#   - add(amount, note)：往 records 加一条 {"amount": amount, "note": note}
#   - total()：返回所有记录 amount 之和（用 for 或 sum）
#   - show()：逐条打印，格式如 "支出 50 元 - 午饭"
# 然后：new 一个账本，add 三条（如 早饭12 / 午饭35 / 打车20），
#       调用 show() 和 total() 打印结果

class AccountBook :
    def __init__(self):
        self.records = []
    def add(self,amount, note):
        self.records.append({"amount": amount, "note": note})
    def  total(self):
        return sum(r["amount"] for r in self.records)
    def show(self):
        for r in self.records:
            print(f"支出{r['amount']} - {r['note']}")

book = AccountBook()
book.add(12, "早饭")
book.add(35, "午饭")
book.add(20, "打车")
book.show()
print("总额：", book.total())