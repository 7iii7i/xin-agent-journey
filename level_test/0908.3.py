# 写一个函数：把列表里每个数都平方，返回新列表
# 起始：nums = [1, 2, 3, 4, 5]
# 你要做：def square_numbers(nums): ...  return 新列表（每个数变成 n*n）
# 套路提示：函数里先 result=[] → for 遍历 nums → 循环内 result.append(n*n) → return result
def square_numbers(nums):
    square=[]
    for i in nums:
        square.append(i*i)
    return square
nums = [1, 2, 3, 4, 5]
print(square_numbers(nums))

students = [
    {"name": "甲", "score": 80},
    {"name": "乙", "score": 95},
    {"name": "丙", "score": 60},
    {"name": "丁", "score": 88},
]
# 你要做：用 sorted + lambda 按 score 从高到低排，逐行打印 名字 分数
# 提示：reverse=True 翻成从大到小；lambda x: x["score"]
students1=sorted(students,key=lambda x: x["score"],reverse=True)
for i in students1:
    print(i["name"],i["score"])


nums = [10, 20, 30, 40]
# ① 把每个数写进 numbers.txt（每行一个）
# ② 读回来把每行转成 int 求和
# ③ 打印总和
# 提示：写 f.write(f"{n}\n")；读回来每行是字符串，用 int(line.strip()) 转数字才能加
with open("numbers.txt","w",encoding="utf-8")as f:
    for num in nums:
        f.write(f"{num}\n")
with open("numbers.txt","r",encoding="utf-8")as f:
    lines=f.readlines()
    n = [int(line.strip()) for line in lines]
    print(sum(n))

