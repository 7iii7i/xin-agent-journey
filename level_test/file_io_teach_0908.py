# file_io_teach_0908.py
# 文件读写：把数据写进 .txt，下次还能读回来
# 用你题3 的老朋友 students 当数据

students = [
    {"name": "甲", "point": 80},
    {"name": "乙", "point": 95},
    {"name": "丙", "point": 60},
]

# 1) 写：把每个学生存成一行 "姓名 分数" 到 scores.txt
#    with open(...) as f:  —— 自动关文件，不用手动 f.close()
#    "w" = 写模式（write）；encoding="utf-8" 防中文乱码
with open("scores.txt", "w", encoding="utf-8") as f:
    for s in students:
        f.write(f"{s['name']} {s['point']}\n")   # \n = 每行结尾换行

print("已写入 scores.txt")

# 2) 读：把文件内容读回来，逐行打印
#    "r" = 读模式（read）；readlines() = 读成"每行一个元素"的列表
with open("scores.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("读回来的内容：")
for line in lines:
    print(line.strip())   # strip() 去掉每行末尾的换行符
