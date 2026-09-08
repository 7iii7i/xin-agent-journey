# 易忘点专项小测 · 参考答案（2026-09-08）
# 对应 weak_points.md 第 5/6/7/8 条
# 仅用于对照，用户写完自己的再开

items = [
    {"name": "键盘", "price": 89},
    {"name": "鼠标", "price": 45},
    {"name": "显示器", "price": 699},
]

# 题1：算总花费 —— sum 取数字字段 price（别取 name 字符串）
total = sum(x["price"] for x in items)
print("总价：", total)            # 期望 833

# 题2：打印购物清单 —— f-string 必须前缀 f
for x in items:
    print(f"{x['name']} {x['price']} 元")

# 题3：写 Cart 类 —— 属性名全文件一致（统一用复数 self.items）
class Cart:
    def __init__(self):
        self.items = []
    def add(self, name, price):
        self.items.append({"name": name, "price": price})
    def total(self):
        return sum(x["price"] for x in self.items)
    def show(self):
        for x in self.items:
            print(f"{x['name']} {x['price']} 元")

c = Cart()
c.add("键盘", 89)
c.add("鼠标", 45)
c.show()
print("总价：", c.total())
