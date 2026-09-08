# ============================================================
# 累加器再讲一遍 · 三步走（你今晚题 1 刚学过的）
# ============================================================

print("===== 累加器 = 三个动作：开本子 → 边走边加 → 看总数 =====")

records = [
    {"name": "早饭", "amount": 12},
    {"name": "午饭", "amount": 35},
    {"name": "打车", "amount": 20},
]

# 第 1 步：在循环【外面】开一本"本子"，先写 0（清零，只这一次）
total = 0
print(f"开局：本子上 total = {total}")

# 第 2 步：进循环，每走一行，把这一行的 amount 加到本子上
for r in records:
    before = total                          # 记一下加之前是几（看清楚"累加"，不是每次从 0 起步）
    total = total + r["amount"]             # 加这一笔
    print(f"  走到 {r['name']}({r['amount']})：加之前 total = {before}，加之后 total = {total}")

# 第 3 步：循环【外面】用本子上的数字（求平均 / 打印 / 比较...）
print(f"结账：本子上的 total = {total}，平均 = {total / len(records):.2f}")
print()


print("===== sum(...) 的本质 = Python 帮你写好了累加器 =====")
# sum 内部就是：total = 0; for x in 那个东西: total = total + x
# 你只要告诉它"加什么"——r["amount"] 才是数字，self.records 是字典（不能加）
print("sum(数字列表) =", sum([12, 35, 20]))
print("sum(每条的 amount) =", sum(r["amount"] for r in records))
print("sum(整本字典) 会崩，因为字典不是数字：")
try:
    bad = sum(records)
except TypeError as e:
    print("  崩了：", e)


print()
print("===== 这就是 AccountBook.total 怎么写 =====")
class AccountBook:
    def __init__(self):
        self.records = []
    def add(self, amount, note):
        self.records.append({"amount": amount, "note": note})
    def total(self):
        # 写法 A：手写累加器（你题 1 风格，最直观）
        total = 0
        for r in self.records:
            total = total + r["amount"]
        return total
        # 写法 B：sum 帮你累加（更短，意思一样）
        # return sum(r["amount"] for r in self.records)

book = AccountBook()
book.add(12, "早饭")
book.add(35, "午饭")
book.add(20, "打车")
print("总额 =", book.total())
