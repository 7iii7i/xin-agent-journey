from encodings import utf_8

fruits = ["苹果", "香蕉", "橘子"]
# 用 with open 把每个水果写进 fruits.txt（每行一个）
# 再读回来逐行打印
with open("fruits.txt","w",encoding="utf-8")as f:
    for fruit in fruits:
        f.write(f"{fruit}\n")
with open("fruits.txt", "r", encoding="utf-8") as f:
    lines=f.readlines()
    for line in lines:
        print(line.strip())


students = [
    {"name": "甲", "point": 80},
    {"name": "乙", "point": 95},
    {"name": "丙", "point": 60},
]
# 你要做：
#
# 用 with open("students.csv", "w", encoding="utf-8") as f: 打开文件
# 先写一行表头：name,point（这就是 CSV 的"列名"）
# 用 for 循环，把每个学生写成一行：甲,80 / 乙,95 / 丙,60（逗号分隔，末尾 \n）
# 写完后自己用读的方式（"r" 模式 + readlines）把文件读回来逐行打印，验证对不对
with open("students.csv","w",encoding="utf-8")as f:
    for student in students:
        name=student["name"]
        point=student["point"]
        f.write(f"{name},{point}\n")
with open("students.csv","r",encoding="utf-8")as f:
    lines=f.readlines()
    for line in lines:
        print(line.strip())

