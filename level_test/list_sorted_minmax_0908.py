# sorted / min / max 拆开讲（重点：lambda 到底是什么）
# 用学生成绩当例子

students = [
    {"name": "张三", "score": 78},
    {"name": "李四", "score": 92},
    {"name": "王五", "score": 65},
    {"name": "赵六", "score": 88},
]

print("原始名单：", students)
print("=" * 55)

# ---------- 第一层：不传 key 会怎样？----------
# 字典本身没法比"谁大谁小"，Python 会按奇怪规则比，甚至报错
print("[先试] 不传 key 直接排：")
try:
    print(sorted(students))
except Exception as e:
    print("报错：", e)
print("→ 结论：排字典必须告诉 Python '按哪个字段比'")

print("=" * 55)

# ---------- 第二层：先用普通函数当 key（先别碰 lambda）----------
# key 就是一个"比大小的裁判"：给我学生 x，我返回他的 score 来比
def get_score(x):        # x 是每个学生字典
    return x["score"]    # 返回 score 当比较依据

print("[1] sorted() 排序 → 返回【一个新列表】（顺序变，但人一个不少）")
ranked = sorted(students, key=get_score, reverse=True)   # 从高到低
for s in ranked:
    print(f"  {s['name']} {s['score']}")

print("\n[2] min() 最小 → 返回【一个元素】（是整个字典，不是数字！）")
lowest = min(students, key=get_score)
print("最低分学生(整个字典)：", lowest)
print("想拿他的分数(自己用[]取)：", lowest["score"])

print("\n[3] max() 最大 → 同样返回【一个元素】")
top = max(students, key=get_score)
print("最高分学生(整个字典)：", top)
print("想拿他的分数：", top["score"])

print("=" * 55)

# ---------- 第三层：lambda = 把 get_score 压成"没名字的一行" ----------
# lambda x: x["score"]   完全等价于上面的  def get_score(x): return x["score"]
# 区别只是 lambda 没名字、写在一行里，直接塞给 key 用
print("[4] lambda 版（结果跟上面一模一样）")
print("从高到低：")
for s in sorted(students, key=lambda x: x["score"], reverse=True):
    print(f"  {s['name']} {s['score']}")
print("最高分数字：", max(students, key=lambda x: x["score"])["score"])
print("最低分数字：", min(students, key=lambda x: x["score"])["score"])