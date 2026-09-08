# 列表常用方法（以 day2 小测的 items 为例）

items = [
    {"name": "键盘", "price": 89},
    {"name": "鼠标", "price": 45},
    {"name": "显示器", "price": 699},
]

print("=" * 40)
print("原始清单：", items)
print("=" * 40)

# ---------- 1. len() 数个数 ----------
# 英文 length = 长度。给一个列表，问"几个？"
print("\n[1] len() 数个数")
print("商品数量：", len(items))   # 3

# ---------- 2. in 判断存不存在 ----------
# in 是一个运算符（不是方法），返回 True/False
# 注意：字典 in 是"完整内容相等"，不是按某个字段查
print("\n[2] in 判断存在")
print("键盘 在不在？", {"name": "键盘", "price": 89} in items)   # True
print("键盘但 99元 在不在？", {"name": "键盘", "price": 99} in items)  # False（price 不同）

# ---------- 3. .append() 加 / .remove() 删 ----------
# .append(x) 把 x 塞到列表末尾（你已经会）
# .remove(x) 把"长得跟 x 一模一样"的那个删掉（找不到会 ValueError）
print("\n[3] .append() 加 / .remove() 删")
items.append({"name": "耳机", "price": 199})
print("加了耳机后：", len(items), "个")   # 4

items.remove({"name": "耳机", "price": 199})   # 必须传完整字典
print("删了耳机后：", len(items), "个")         # 3

# ---------- 4. sorted() 排序（需要 key=lambda 教它按啥排）----------
# lambda x: x["price"] = 给我 x，我用 x["price"] 排
# reverse=True = 反过来（从大到小）
print("\n[4] sorted() 排序")
by_price_asc = sorted(items, key=lambda x: x["price"])           # 便宜→贵
by_price_desc = sorted(items, key=lambda x: x["price"], reverse=True)  # 贵→便宜
print("便宜→贵：")
for x in by_price_asc:
    print(f"  {x['name']} {x['price']} 元")
print("贵→便宜：")
for x in by_price_desc:
    print(f"  {x['name']} {x['price']} 元")

# ---------- 5. min() / max() 找极端 ----------
# 跟 sorted 用一样的 key=lambda，但只返回一个元素
print("\n[5] min() 最便宜 / max() 最贵")
cheapest = min(items, key=lambda x: x["price"])
priciest = max(items, key=lambda x: x["price"])
print(f"最便宜：{cheapest['name']} {cheapest['price']} 元")
print(f"最贵：  {priciest['name']} {priciest['price']} 元")

# ---------- 6. 收尾：算总和（你已经会）----------
total = sum(x["price"] for x in items)
print("\n[6] 总价：", total)   # 833