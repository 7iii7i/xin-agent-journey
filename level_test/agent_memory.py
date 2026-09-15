import sqlite3

class 记忆库:
    def __init__(self, 库名=":memory:"):        # 🔴 死记骨架：class + __init__
        self.连接 = sqlite3.connect(库名)          # 连库（内存库演示；真实项目传 "agent.db" 持久化）
        self.指针 = self.连接.cursor()
        self.指针.execute("""CREATE TABLE IF NOT EXISTS 问答(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            问题 TEXT,
            回答 TEXT
        )""")                                      # 🟢 懂框架：SQLite 建表四步之一
        self.连接.commit()                         # 🟢 动结构要 commit

    def 存(self, 问题, 回答):                       # 🔴 死记骨架：方法首参 self
        self.指针.execute(
            "INSERT INTO 问答(问题, 回答) VALUES (?, ?)", (问题, 回答)  # 🟢 ? 占位防注入
        )
        self.连接.commit()                         # 🟢 动内容要 commit

    def 取历史(self):                              # 🔴 死记骨架
        self.指针.execute("SELECT 问题, 回答 FROM 问答 ORDER BY id")
        return self.指针.fetchall()               # 🟢 取数据用 fetchall()

    def 关(self):
        self.连接.close()

# ===== 主线用法：Agent 把每次对话存进记忆库 =====
库 = 记忆库()                                     # 实例化，自动建表
库.存("你是谁", "我是AI助手")
库.存("class 是啥", "一种把数据和功能打包的模板")
print("记忆库里的历史：")
for 问, 答 in 库.取历史():
    print(f"  Q: {问}  →  A: {答}")
库.关()
