# week02/day2：复现练习 —— 把 class 钉进肌肉记忆
# 用法：打开本文件，把下面两个「空白区」从零敲出来，跑 python week02/day2_复现练习.py 验收
# 写不出就先读 day2_参考答案.py，读懂再回来从空白敲（别照抄，手敲才长记性）
# 新概念只有 1 个：if __name__ == "__main__" （见文件最底部说明）

# ============================================================
# Part A：从空白重敲「记账本 AccountBook」
# 要求：
#   1. class AccountBook:  造盒子设计图
#   2. __init__(self):     准备 self.records = []  （空列表放账单）
#   3. add(self, amount, note):  往 records 追加 {"amount": amount, "note": note}
#   4. total(self):        累加器算出总额，用 return 交出去（不是 print）
#   5. show(self):         逐条打印 "支出 12 元 - 早饭" 这种格式
#   6. 底部创建 book，加三笔（早饭12 / 午饭35 / 打车20），show() 再打印总额
# 提示：show 的格式串用  f"支出 {r['amount']} 元 - {r['note']}"
# ============================================================
class AccountBook:
      def __init__(self):
       self.records = []
      def add(self, amount, note):
          self.records.append({"amount": amount, "note": note})
      def  total(self):
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





# ============================================================
# Part B：换场景写「待办清单 ToDoList」（昨晚购物车是第二个场景，这是第三个）
# 要求：
#   1. class ToDoList:  __init__ 准备 self.tasks = []
#   2. add_task(self, text):  加一条待办，存 {"text": text, "done": False}
#   3. finish(self, i):       把第 i 条标记 done = True（i 从 0 数起）
#   4. show(self):            逐条打印，做完了显示 ✅，没做显示 ⬜
#   5. 底部加三条待办，finish(0) 标记第一条完成，show() 看效果
# 提示：show 里用  for i, t in enumerate(self.tasks):  再用 if t["done"] 判断
# ============================================================
class ToDoList:
    def __init__(self):
        self.task = []
    def  add_task(self, text):
        self.task.append({"text": text, "done": False})
    def finish(self, i):
        self.task[i]["done"] = True
    def show(self):
        for i, t in enumerate(self.task):
            if t["done"]:
               print(f"✅ {t['text']}")
            else:
                print(f"⬜ {t['text']}")
t = ToDoList()
t.add_task("写日报")
t.add_task("学 Python")
t.add_task("运动 30 分钟")
t.finish(0) # 把"写日报"标完成
t.show()






# ============================================================
# 今日唯一新课：if __name__ == "__main__"
#   - 这行写在文件最底部，意思是「本文件被你直接用 python 跑时，才执行它下面缩进的那段」
#   - 如果本文件被别的文件 import（当工具箱用），这段不执行，不会自动弹输入/跑代码
#   - 你现在直接跑本文件，所以下面这段会执行：创建 book 跑 show 等
# 写法固定，照抄即可：
# if __name__ == "__main__":
#     book = AccountBook()
#     book.add(12, "早饭"); book.add(35, "午饭"); book.add(20, "打车")
#     book.show()
#     print("总额：", book.total())
# ============================================================
