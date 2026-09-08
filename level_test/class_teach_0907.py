# ============================================================
# class 从零教学 · 用会计的"账簿"来理解
# 每一步都能单独跑，看输出
# ============================================================

print("########## 第 0 步：不用 class，你也会的普通记账 ##########")
# 一个账本 = 一个列表，每条记录是字典
records = []
records.append({"amount": 12, "note": "早饭"})
records.append({"amount": 35, "note": "午饭"})
total = sum(r["amount"] for r in records)
print("普通列表记账，总额 =", total)
print("问题：数据和操作是分开的，N 本账就混乱了 —— class 就是用来把一本账打包成整体")
print()


print("########## 第 1 步：class = 一种账簿的模板，不是账本身 ##########")
class AccountBook:
    def __init__(self):          # ① 开新账簿时自动执行
        self.records = []        # ② 给这本账簿一个空账页

# 注意：上面只是定义了模板，还没开任何一本账
book = AccountBook()             # ③ 真正开一本账（__init__ 自动跑）
print("开了一本新账，当前账页 =", book.records)   # 空的 []
print()


print("########## 第 2 步：add = 记账这个动作（方法）##########")
class AccountBook:
    def __init__(self):
        self.records = []

    def add(self, amount, note):                 # self = 这本账簿自己
        self.records.append({"amount": amount, "note": note})

book = AccountBook()
book.add(12, "早饭")          # 调用时不写 self！Python 自动把 book 塞进 self
book.add(35, "午饭")
print("记了 2 笔后，账页 =", book.records)
print("关键：self.records 是这本 book 自己的账页，换一本账就独立")
print()


print("########## 第 3 步：total = 算总额（你今晚刚会的累加器）##########")
class AccountBook:
    def __init__(self):
        self.records = []

    def add(self, amount, note):
        self.records.append({"amount": amount, "note": note})

    def total(self):
        return sum(r["amount"] for r in self.records)   # 对 self.records 求和

book = AccountBook()
book.add(12, "早饭")
book.add(35, "午饭")
book.add(20, "打车")
print("调用 book.total()，得到总额 =", book.total())
print()


print("########## 第 4 步：show = 看账（for 遍历打印）##########")
class AccountBook:
    def __init__(self):
        self.records = []

    def add(self, amount, note):
        self.records.append({"amount": amount, "note": note})

    def total(self):
        return sum(r["amount"] for r in self.records)

    def show(self):
        for r in self.records:
            print(f"支出 {r['amount']} 元 - {r['note']}")

book = AccountBook()
book.add(12, "早饭")
book.add(35, "午饭")
book.add(20, "打车")
book.show()
print("总额：", book.total())
