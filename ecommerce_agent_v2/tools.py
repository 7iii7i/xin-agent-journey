# ===== 工具层（tools.py）Tier 2：注册表调用改成 async =====
# 🔴 死记骨架：工具注册表模式（和 Tier 1 完全一样，只是调用方法变成 async）
# 🟢 懂框架：因为工具内部现在要 await 数据库，所以 调用() 也要 await；
#    这是"异步传染"——一个函数异步了，调用它的整条链都得 async。
from db import 商品库实例
from rag import 知识库实例


class 工具注册表:
    def __init__(self):
        self.表 = {}  # name -> {"func": 异步函数, "schema": 给模型看的JSON}

    def 注册(self, schema, func):
        self.表[schema["function"]["name"]] = {"func": func, "schema": schema}

    def 清单(self):
        return [v["schema"] for v in self.表.values()]

    async def 调用(self, name, 参数: dict):
        # 同样只查字典执行，不再写 if；区别是加了 await
        return await self.表[name]["func"](**参数)


注册表 = 工具注册表()

# ---- 每加一个工具 = 注册一行，不用动别的代码（开闭原则）----
注册表.注册({
    "type": "function",
    "function": {
        "name": "search_product",
        "description": "按关键词搜索商品（匹配名称/分类/描述），返回商品列表",
        "parameters": {
            "type": "object",
            "properties": {"keyword": {"type": "string", "description": "搜索词，如'耳机'、'充电'"}},
            "required": ["keyword"],
        },
    },
}, 商品库实例.搜商品)

注册表.注册({
    "type": "function",
    "function": {
        "name": "get_price",
        "description": "查询指定商品的单价和库存",
        "parameters": {
            "type": "object",
            "properties": {"name": {"type": "string", "description": "商品名称（可部分匹配）"}},
            "required": ["name"],
        },
    },
}, 商品库实例.查价格)

注册表.注册({
    "type": "function",
    "function": {
        "name": "get_stock",
        "description": "查询指定商品的当前库存数量",
        "parameters": {
            "type": "object",
            "properties": {"name": {"type": "string", "description": "商品名称（可部分匹配）"}},
            "required": ["name"],
        },
    },
}, 商品库实例.查库存)

# 🆕 RAG 工具：语义检索店铺知识库（政策/规则/商品参数等私有文档）
# 🟢 懂框架：和前面三个工具套路一模一样，只是函数换成 知识库实例.检索接口（async 包了一层向量检索）
注册表.注册({
    "type": "function",
    "function": {
        "name": "kb_search",
        "description": "在店铺知识库里做语义检索，回答关于退换货、质保、发货时效、积分、优惠券、客服时间、商品参数等规则和政策的问题。用户问法口语化、关键词对不上时也能命中。",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "用户的问题，如'耳机坏了能退吗'、'晚上10点有人工客服吗'"},
                "top_k": {"type": "integer", "description": "返回最相关片段数，默认3", "default": 3},
            },
            "required": ["query"],
        },
    },
}, 知识库实例.检索接口)
