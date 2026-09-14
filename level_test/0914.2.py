# 建一个列表 商品列表，放 5 个商品，每个用 [名称, 价格] 表示，比如 ['键盘', 99]
# 写一个函数 插商品(名称, 价格)：负责 connect → CREATE TABLE IF NOT EXISTS products (id INTEGER, name TEXT, price INTEGER) → INSERT 一行 → commit → close
# 用 for 循环 遍历 商品列表，逐个调用 插商品，把 5 个都插进去
# 写一个函数 查全部()：connect → SELECT * FROM products → fetchall → 用 for 打印每行 → close
# （少量延伸）再写一个 查贵货()：用 SELECT * FROM products WHERE price > 50 查出价格大于 50 的，打印
# 深度判定（按你定的规则）​：
#
# SQLite 四步、函数 def/参数、列表 + for 循环 → 【必须自己写】
# WHERE 列 > 值（新语法）→ 【理解+会改】，记住格式就行
# 期望输出格式（数据你自拟，结构如此）：
#
# plaintext
#
# 全部商品：
# (1, '键盘', 99)
# (2, '鼠标', 59)
# (3, '屏幕', 699)
# (4, '耳机', 39)
# (5, '线', 9)
#
# 价格大于50的：
# (1, '键盘', 99)
# (2, '鼠标', 59)
# (3, '屏幕', 699)
import sqlite3


商品列表=[['键盘', 99],['鼠标', 59],['屏幕', 699],['耳机', 39],['线', 9]]
def 插商品(名称,价格):
    conn=sqlite3.connect("test.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER, name TEXT, price INTEGER)")
    cur.execute("INSERT INTO products VALUES (1, ?, ?)", (名称, 价格))
    conn.commit()
    conn.close()
conn = sqlite3.connect("test.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER, name TEXT, price INTEGER)")
cur.execute("DELETE FROM products")   # ← 现在在顶层，循环前只执行一次
conn.commit()
conn.close()
for 商品 in 商品列表:
    插商品(商品[0],商品[1])
def 查全部():
    conn=sqlite3.connect("test.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER, name TEXT, price INTEGER)")
    cur.execute("SELECT * FROM products")
    rows=cur.fetchall()
    for row in rows:
        print(row)
    conn.close()
def 查贵货():
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER, name TEXT, price INTEGER)")
    cur.execute("SELECT * FROM products WHERE price > 50")
    rows = cur.fetchall()
    for row in rows:
        print(row)


查全部()
查贵货()
