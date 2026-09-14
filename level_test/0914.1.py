import sqlite3                      # 引入 sqlite3（Python 自带，不用装）

# ① 连接：没有 test.db 就新建一个
conn = sqlite3.connect("test.db")
cur = conn.cursor()                 # cur = 游标，后面靠它执行命令

# ② 建表（IF NOT EXISTS = 重复跑也不报错）
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT, age INTEGER)")

# ③ 插入两行数据
cur.execute("DELETE FROM users")
cur.execute("INSERT INTO users VALUES (1, '小明', 20)")
cur.execute("INSERT INTO users VALUES (2, '小红', 22)")
conn.commit()                       # ⚠️ 写操作必须 commit，否则不保存

# ④ 查询并取出结果
cur.execute("SELECT * FROM users") # * = 所有列
rows = cur.fetchall()               # rows 是 [(1,'小明',20), (2,'小红',22)]
for row in rows:
    print(row)                      # 逐行打印

# ⑤ 关闭
conn.close()

