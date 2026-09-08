# 练习：购物车 Cart（class 巩固 · 换场景）
# 目标：写一个购物车类，能加商品、看清单、算总额。
#
# 期望输出（跑出来应该这样）：
#   商品 苹果 × 2 = ￥10
#   商品 牛奶 × 1 = ￥8
#   商品 面包 × 3 = ￥15
#   总额： ￥33
#
# 和之前 AccountBook 的同构关系（帮你迁移）：
#   AccountBook.records  →  Cart.items        （都是空容器）
#   add(amount, note)    →  add(name, price, qty)   （往里放一条，字段变了）
#   total() 加金额        →  total() 加 price*qty    （算的方式略变）
#   show() 打印支出       →  show() 打印商品明细
#
# TODO：补全下面四个方法（别抄 AccountBook 原样，字段要换成购物车的）

class Cart:
    def __init__(self):
        self.items = []                        # 空货架

    def add(self, name, price, qty):
        # 往 self.items 加一条字典：{"name": name, "price": price, "qty": qty}
        self.items.append({"name": name, "price": price, "qty": qty})

    def total(self):
        # 算总额：把每条的 price * qty 加起来
        # 提示：和 AccountBook.total 一样用"累加器"或 sum(...)
        return sum([r["price"]*r["qty"] for r in self.items])

    def show(self):
        # 逐条打印：商品 {name} × {qty} = ￥{price*qty}
        # 提示：for 遍历 self.items，每条 r 取 r["name"] / r["qty"] / r["price"]
        for r in self.items:
            name = r["name"]
            price = r["price"]
            qty = r["qty"]
            print(f"商品{name} × {qty} = ￥{price*qty}")


# 主程序（不用改，直接跑）
cart = Cart()
cart.add("苹果", 5, 2)     # 单价 5，数量 2
cart.add("牛奶", 8, 1)
cart.add("面包", 5, 3)
cart.show()
print("总额： ￥", cart.total())
