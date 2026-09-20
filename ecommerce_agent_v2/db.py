# ===== 数据层（db.py）Tier 2：sqlite3 → aiosqlite（全异步）=====
# 🟢 懂框架：改动很小，只是每行前面加 await，connect 换成 aiosqlite.connect。
# 为什么要异步？原来同步查库会"卡住"处理请求的线程；异步后，查库等待期间
# 事件循环可以去服务别的请求，并发量一下就上来了。
# ⚠️ 一个关键点：原来 __init__ 里直接 建表()+播种()，但 async 函数不能在 __init__ 里 await，
#    所以改成"启动时再 await 初始化()"——看 main.py 的 lifespan。
import os
import aiosqlite
from datetime import datetime
from config import 配置, 日志


# ---------- 商品库 ----------
class 商品库:
    def __init__(self, 库名=配置.DB名):
        self.库名 = 库名

    async def 初始化(self):
        async with aiosqlite.connect(self.库名) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    name        TEXT,
                    price       REAL,
                    stock       INTEGER,
                    category    TEXT,
                    description TEXT
                )
            """)
            await db.commit()
            async with db.execute("SELECT COUNT(*) FROM products") as cur:
                n = (await cur.fetchone())[0]
            if n == 0:
                await db.executemany(
                    "INSERT INTO products (name, price, stock, category, description) VALUES (?, ?, ?, ?, ?)",
                    [
                        ("无线蓝牙耳机 Pro", 199.0, 50, "耳机", "主动降噪，续航30小时"),
                        ("快充充电宝 20000mAh", 129.0, 30, "充电", "支持22.5W快充"),
                        ("机械键盘 红轴", 299.0, 12, "外设", "RGB背光，热插拔轴"),
                        ("4K显示器 27寸", 999.0, 8, "显示器", "IPS面板，99% sRGB"),
                        ("人体工学椅", 899.0, 5, "家具", "可躺，腰部支撑"),
                    ],
                )
                await db.commit()
            日志.info("商品库就绪（%d 条）", n)

    async def 搜商品(self, keyword):
        # 🔴 死记：参数名 keyword 必须 == tools.py 里 schema 的 properties key（注册表 func(**参数) 展开）
        async with aiosqlite.connect(self.库名) as db:
            async with db.execute(
                "SELECT name, price, stock, category, description FROM products WHERE name LIKE ? OR category LIKE ? OR description LIKE ?",
                (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
            ) as cur:
                行 = await cur.fetchall()
        return [{"名称": r[0], "价格": r[1], "库存": r[2], "分类": r[3], "描述": r[4]} for r in 行]

    async def 查价格(self, name):
        async with aiosqlite.connect(self.库名) as db:
            async with db.execute("SELECT price, stock FROM products WHERE name LIKE ?", (f"%{name}%",)) as cur:
                行 = await cur.fetchone()
        if 行:
            return {"名称": name, "价格": 行[0], "库存": 行[1]}
        return {"错误": "没找到该商品"}

    async def 查库存(self, name):
        async with aiosqlite.connect(self.库名) as db:
            async with db.execute("SELECT stock FROM products WHERE name LIKE ?", (f"%{name}%",)) as cur:
                行 = await cur.fetchone()
        return 行[0] if 行 else 0


# ---------- 会话库（v2 多轮记忆，同样改异步）----------
class 会话库:
    def __init__(self, 库名=配置.会话DB名):
        self.库名 = 库名

    async def 初始化(self):
        os.makedirs(os.path.dirname(self.库名) or ".", exist_ok=True)
        async with aiosqlite.connect(self.库名) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS turns (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    role       TEXT,
                    content    TEXT,
                    time       TEXT
                )
            """)
            await db.commit()

    async def 追加(self, session_id, role, content):
        async with aiosqlite.connect(self.库名) as db:
            await db.execute(
                "INSERT INTO turns (session_id, role, content, time) VALUES (?, ?, ?, ?)",
                (session_id, role, content, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            )
            await db.commit()

    async def 取历史(self, session_id, 上限=20):
        # 只取 user/assistant（工具中间结果不持久化，避免喂给模型时格式错乱）
        async with aiosqlite.connect(self.库名) as db:
            async with db.execute(
                "SELECT role, content FROM turns WHERE session_id=? AND role IN ('user','assistant') ORDER BY id ASC LIMIT ?",
                (session_id, 上限),
            ) as cur:
                行 = await cur.fetchall()
        return [{"role": r[0], "content": r[1]} for r in 行]


# 程序启动先建两个"空壳"对象；真正的建表/播种在 main.py 的 lifespan 里 await 初始化()
商品库实例 = 商品库()
会话库实例 = 会话库()
