# week02/day2_参考答案.py —— 写完自己的再对照，别提前看
# Part A：记账本
class AccountBook:
    def __init__(self):
        self.records = []
    def add(self, amount, note):
        self.records.append({"amount": amount, "note": note})
    def total(self):
        total = 0
        for r in self.records:
            total = total + r["amount"]
        return total
    def show(self):
        for r in self.records:
            print(f"支出 {r['amount']} 元 - {r['note']}")


# Part B：待办清单
class ToDoList:
    def __init__(self):
        self.tasks = []
    def add_task(self, text):
        self.tasks.append({"text": text, "done": False})
    def finish(self, i):
        self.tasks[i]["done"] = True
    def show(self):
        for i, t in enumerate(self.tasks):
            mark = "✅" if t["done"] else "⬜"
            print(f"{i}. {mark} {t['text']}")


if __name__ == "__main__":
    book = AccountBook()
    book.add(12, "早饭"); book.add(35, "午饭"); book.add(20, "打车")
    book.show()
    print("总额：", book.total())

    print("---")
    todo = ToDoList()
    todo.add_task("背 5 个 Python 生词")
    todo.add_task("重敲记账本")
    todo.add_task("散步 20 分钟")
    todo.finish(0)
    todo.show()
