# ===== RAG 知识库（rag.py）=====
# 一句话：把"私有文档"切成小段 → 每段变成一串数字(向量) → 存盘；
# 用户提问时也变成向量 → 和库里所有向量比"像不像"(余弦相似度) → 取最像的 top-k 段 → 喂给 LLM。
#
# 🔴 死记骨架：这个类就三个方法——构建() / 加载() / 检索()
# 🟢 懂框架：embedding(变向量) 和 向量库(比相似) 是两件独立的事；
#    这里我们用 numpy 自己算余弦相似度，最轻量、最能看清原理。
#    生产环境会换成 chromadb / FAISS(现成的向量库)，但"检索"这件事的本质完全一样。
import os
import json
import asyncio
import logging
import numpy as np

日志 = logging.getLogger("kb")

# ---- 文档源：一小份电商业务知识（真实项目换成你的商品/政策文档）----
# 🟢 懂框架：这里文档本身已是一句一段，直接每段一块（naive chunk）。
#    真实项目要做"切小段 + 留重叠"，避免一段话太长、语义分散，检索更准。
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

片段 = [d for d in 原始文档 if d.strip()]

_基础目录 = os.path.dirname(__file__)
_向量文件 = os.path.join(_基础目录, "data", "kb_vecs.npz")
_文本文件 = os.path.join(_基础目录, "data", "kb_texts.json")


class 知识库:
    def __init__(self):
        self.片段列表 = []
        self.向量矩阵 = None  # shape: (段数, 维度)
        self.模型 = None
        self.重排模型 = None  # cross-encoder reranker，懒加载

    # 🟢 懂框架：embedding 封装成"唯一一处"。想换成某家 API 版，只改这个方法。
    def _取模型(self):
        if self.模型 is None:
            # 本地中文向量模型：BAAI/bge-small-zh-v1.5（约90MB，离线、中文效果好）
            from sentence_transformers import SentenceTransformer
            self.模型 = SentenceTransformer("BAAI/bge-small-zh-v1.5")
        return self.模型

    # 🟢 懂框架：rerank 用 cross-encoder（BAAI/bge-reranker-base，中文友好）。
    #    它把"问题+文档"拼一起现算相关性分数，比向量粗排准，但慢，所以只在粗排候选上用。
    def _取重排模型(self):
        if self.重排模型 is None:
            from sentence_transformers import CrossEncoder
            self.重排模型 = CrossEncoder("BAAI/bge-reranker-base")
        return self.重排模型

    # ① 构建：切片(已切好) → 每段变向量 → 存盘。只在第一次跑 构建知识库.py 时执行。
    # 🟢 懂框架：文档可以外部传入（如电商+工厂合并），默认用本模块原始的电商文档。
    def 构建(self, 文档=None):
        self.片段列表 = 文档 if 文档 is not None else 片段
        模型 = self._取模型()
        vecs = 模型.encode(self.片段列表, normalize_embeddings=True)  # 归一化后点积=余弦
        self.向量矩阵 = np.asarray(vecs, dtype="float32")
        os.makedirs(os.path.dirname(_向量文件), exist_ok=True)
        np.savez(_向量文件, 向量=self.向量矩阵)
        with open(_文本文件, "w", encoding="utf-8") as f:
            json.dump(self.片段列表, f, ensure_ascii=False, indent=2)
        日志.info("知识库构建完成：共 %d 段", len(self.片段列表))

    # ② 加载：服务启动时把存盘的向量读回内存（快，不下载模型）。
    def 加载(self):
        if not (os.path.exists(_向量文件) and os.path.exists(_文本文件)):
            return False
        d = np.load(_向量文件)
        self.向量矩阵 = d["向量"].astype("float32")
        with open(_文本文件, encoding="utf-8") as f:
            self.片段列表 = json.load(f)
        return True

    # ③ 检索（核心）：问题变向量 → 粗排 top-候选 → 精排 rerank → 取 top-k 最像的。
    # 🟢 懂框架：默认走 rerank 两阶段——粗排 bi-encoder（向量，快、预存）捞全保证不漏，
    #    精排 cross-encoder（reranker，准、现算）只在少数候选上重排取准。速度和精度权衡。
    def 检索(self, 问题: str, top_k: int = 3, 粗排候选: int = 20, 启用重排: bool = True):
        if self.向量矩阵 is None and not self.加载():
            return "（知识库尚未构建，请先运行 构建知识库.py）"
        模型 = self._取模型()
        q = np.asarray(模型.encode([问题], normalize_embeddings=True)[0], dtype="float32")
        # 余弦相似度：向量已归一化，所以"点积"就等于余弦相似度。越大越像。
        sims = self.向量矩阵 @ q
        候选数 = min(粗排候选, len(sims))
        粗排idx = np.argsort(-sims)[:候选数]
        if 启用重排 and 候选数 > 1:
            try:
                候选段 = [self.片段列表[j] for j in 粗排idx]
                # cross-encoder 现算：给每段打"和问题相关度"分数，越高越相关
                分数 = self._取重排模型().predict([(问题, d) for d in 候选段])
                排序 = sorted(range(候选数), key=lambda i: -float(分数[i]))
                最终idx = [粗排idx[i] for i in 排序][:top_k]
            except Exception as e:
                日志.warning("rerank 不可用，回退纯向量粗排：%s", e)
                最终idx = 粗排idx[:top_k]
        else:
            最终idx = 粗排idx[:top_k]
        return "\n".join(f"[资料{i+1}] {self.片段列表[j]}" for i, j in enumerate(最终idx))

    # 注册表要的是 async 函数（调用时会 await），所以用这一层包一下同步检索。
    # 🟢 懂框架：embedding 是 CPU 计算，用 to_thread 丢到线程里跑，不卡住异步事件循环。
    async def 检索接口(self, query: str, top_k: int = 3):
        return await asyncio.to_thread(self.检索, query, top_k)


知识库实例 = 知识库()
