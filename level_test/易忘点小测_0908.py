# 易忘点专项小测 2026-09-08
# 目标：复测 weak_points.md 第 5/6/7 条（还标着 ⏳ 待复测）
# 要求：从空白把下面的 TODO 补全，跑通后把【输出】或【报错】贴给我批
# 不要提前看 易忘点小测_0908_答案.py

items = [
    {"name": "键盘", "price": 89},
    {"name": "鼠标", "price": 45},
    {"name": "显示器", "price": 699},
]

# ========== 题1：算总花费（考 第5条：sum 取数字字段，别取 name 字符串）==========
# 期望输出：总价： 833
# 坑：写成 sum(x["name"] ...) 会报错，name 是字符串 "键盘"
# TODO：算出总价，用 sum 取 "price" 字段
total =sum(r["price"]for r in items)
print("总价：", total)

# ========== 题2：打印购物清单（考 第6条：f-string 必须前缀 f）==========
# 期望每行：键盘 89 元 / 鼠标 45 元 / 显示器 699 元
# 坑：漏 f 会原样打出 {x['name']} 而不是变量值
# TODO：每个商品打印一行，注意 print(...) 前面有没有 f
for x in items:
    print(f"{x['name']} {x['price']} 元")   # ← 补全这一行

# ========== 题3：写 Cart 类（考 第7条：属性名全文件一致，建议用复数 self.items）==========
# 期望：
#   键盘 89 元
#   鼠标 45 元
#   总价： 134
# 坑：__init__ 用 self.items=[]，但 show 里写成 self.item → AttributeError
# TODO：补全下面三个方法，属性统一叫 self.items（一个叫法到底）
class Cart:
    def __init__(self):
        self.items = []          # 用复数 items
    def add(self, name, price):
        self.items.append({"name":name,"price":price})
    def total(self):
        return sum(r["price"]for r in self.items)
    def show(self):
        for r in self.items:
            print(f"{r['name']}{r['price']}")

c = Cart()
c.add("键盘", 89)
c.add("鼠标", 45)
c.show()
print("总价：", c.total())

# ========== 题4（口述，不写代码）：if __name__ == "__main__": 是什么？==========
# 用你自己的话答一句就行（第 8 条已 ✅ 掌握，这是巩固）
# 自己运行这个代码的时候 执行写在他下面的代码  被别的东西import 不执行下方代码
