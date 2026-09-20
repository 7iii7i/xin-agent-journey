# ===== rag.py 的「人话版」——仅供阅读对照，项目真正运行的是 rag.py =====
# 黑盒部分都标了 ⚫底层·先别管，你顺着 构建 / 加载 / 检索 三个方法读就行。
# 想跑同款自测：先 `python 构建知识库.py` 建好索引，再 `python rag_读懂版.py`。
import os
import json
import asyncio
import numpy as np
import logging

日志 = logging.getLogger("kb_demo")
_基础 = os.path.dirname(__file__)
_向量文件 = os.path.join(_基础, "data", "kb_vecs.npz")
_文本文件 = os.path.join(_基础, "data", "kb_texts.json")

# ---- 你写的业务文档：一句一段（真实项目换成你的商品/政策文档）----
原始文档 = [
    "退换货政策：商品签收后7天内，在不影响二次销售的前提下支持无理由退货，退货运费由买家承担。",
    "质保说明：电子类商品提供一年质保，非人为损坏可免费维修或换新。",
    "发货时效：现货商品当天16点前下单当日发出，预售商品以页面标注为准。",
    "蓝牙耳机X1：续航20小时，支持主动降噪，IPX4防水，售价299元。",
    "充电宝P2：容量20000mAh，支持22.5W快充，可同时充三台设备，售价129元。",
    "会员积分：每消费1元得1积分，100积分可抵1元，积分有效期12个月。",
    "优惠券使用：满199减30券不可与其他活动叠加，过期作废。",
    "客服时间：人工客服每日9:00-21:00在线，其余时段由智能客服解答。",
]

# 🟢懂框架：文档本身已经一句一段切好了（naive chunk）。
#    真实项目要做"切小段 + 留重叠"，检索更准——那是进阶，先不管。
片段 = [d for d in 原始文档 if d.strip()]


class 知识库:
    def __init__(self):
        self.片段列表 = []    # 每一段原文
        self.向量矩阵 = None  # 所有段的向量，排成一张表（几段就有几行）
        self.模型 = None

    # ===== ① 构建：第一次跑 构建知识库.py 时调用 =====
    def 构建(self):
        self.片段列表 = 片段
        # 🟢 把每段文字变成一串数字（向量）。具体怎么变的不用管，sentence_transformers 替你做。
        模型 = self._取模型()
        vecs = 模型.encode(self.片段列表, normalize_embeddings=True)
        self.向量矩阵 = np.asarray(vecs, dtype="float32")
        # 存盘：向量存 npz，原文存 json（分开存，避免 pickle 坑）
        os.makedirs(os.path.dirname(_向量文件), exist_ok=True)
        np.savez(_向量文件, 向量=self.向量矩阵)
        with open(_文本文件, "w", encoding="utf-8") as f:
            json.dump(self.片段列表, f, ensure_ascii=False, indent=2)

    # ===== ② 加载：服务启动时把向量读回内存（快，不下载模型）=====
    def 加载(self):
        if not (os.path.exists(_向量文件) and os.path.exists(_文本文件)):
            return False
        d = np.load(_向量文件)
        self.向量矩阵 = d["向量"].astype("float32")
        with open(_文本文件, encoding="utf-8") as f:
            self.片段列表 = json.load(f)
        return True

    # ===== ③ 检索：用户每次提问时调用（核心）=====
    def 检索(self, 问题, top_k=3):
        if self.向量矩阵 is None and not self.加载():
            return "（知识库尚未构建，请先运行 构建知识库.py）"
        模型 = self._取模型()
        # 🟢 用户的问题也变成向量（和构建时用的是同一个模型）
        q = np.asarray(模型.encode([问题], normalize_embeddings=True)[0], dtype="float32")
        # ⚫ 底层·先别管：这行就是"拿问题向量和每段向量比谁最像"。
        #    向量已归一化，点积(@)就等于余弦相似度；数值越大 = 越像。
        sims = self.向量矩阵 @ q
        # ⚫ 底层·先别管：从大到小排序，取最像的前 top_k 段。
        idx = np.argsort(-sims)[:top_k]
        # 🟢 把最像的几段原文拼成一段文字，返回给 LLM 当资料
        return "\n".join(f"[资料{i+1}] {self.片段列表[j]}" for i, j in enumerate(idx))

    # 注册表要的是 async 函数（调用处会 await），所以包一层。
    # ⚫ 底层·先别管：asyncio.to_thread 把同步检索丢到后台线程跑，不卡异步事件循环。
    async def 检索接口(self, query, top_k=3):
        return await asyncio.to_thread(self.检索, query, top_k)

    # ⚫ 底层·先别管：懒加载——第一次才下载模型，之后复用，省内存。
    def _取模型(self):
        if self.模型 is None:
            from sentence_transformers import SentenceTransformer
            self.模型 = SentenceTransformer("BAAI/bge-small-zh-v1.5")
        return self.模型


知识库实例 = 知识库()


# ---- 直接看检索效果（需先 python 构建知识库.py 建好索引）----
if __name__ == "__main__":
    for 问题 in ["耳机坏了能退吗", "晚上10点有人工客服吗", "满减券能和其他活动一起用吗"]:
        print("\n问题：", 问题)
        print(知识库实例.检索(问题, top_k=2))
