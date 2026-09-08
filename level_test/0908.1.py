# 题1 — 水果清单增删查
#
# 起始数据：fruits = ["苹果", "香蕉", "橘子"]
# 你要做：① 用 append 加一个 "葡萄" ② 用 remove 删掉 "香蕉" ③ 用 len 打印数量 ④ 用 in 判断 "苹果" 在不在
# 期望输出：
# plaintext
#
# 数量： 3
# 有苹果吗： True
# ['苹果', '橘子', '葡萄']


fruits = ["苹果", "香蕉", "橘子"]
fruits.append("葡萄")
fruits.remove("香蕉")
print("数量:",len(fruits))
print("有苹果吗","苹果" in fruits)
print(fruits)

# 题2 — 商品按价格排序
#
# 起始数据：goods = [{"name":"A","price":30}, {"name":"B","price":10}, {"name":"C","price":50}]
# 你要做：用 sorted + lambda，按 price 从小到大排，逐行打印每个的 name 和 price
# 期望输出：
# plaintext
#
# B 10
# A 30
# C 50
goods = [{"name":"A","price":30}, {"name":"B","price":10}, {"name":"C","price":50}]
goods1= sorted(goods, key=lambda x: x["price"])
goods2=sorted(goods, key=lambda x: x["price"],reverse=True)
for x in goods1:
    print(f"{x['name']} {x['price']}")

for x in goods2:
    print(f"{x['name']} {x['price']}")

# 起始数据：scores = [{"name":"甲","point":80}, {"name":"乙","point":95}, {"name":"丙","point":60}]
# 你要做：用 max / min + lambda，找出最高分和最低分学生，打印他们的 name 和分数（提示：max/min 返回的是整个字典，要自己用 ["point"] 取分数）
# 期望输出：
# plaintext
#
# 最高： 乙 95
# 最低： 丙 60
scores = [{"name":"甲","point":80}, {"name":"乙","point":95}, {"name":"丙","point":60}]
higher=max(scores,key=lambda x: x["point"])
higher2=min(scores,key=lambda x: x["point"])
print(f"{higher['name']}{higher['point']}")
print(f"{higher2['name']}{higher2['point']}")