# ===== RAG 评估脚本（rag_eval.py）=====
# 🟢 懂框架：离线评估 RAG 检索质量，不调 LLM 也能跑（recall / hit）。
#   指标含义：
#   - recall@候选：标准段是否被"粗排"捞回（验证粗排不漏）
#   - hit@3（无 rerank）：纯向量粗排 top-3 是否含标准段
#   - hit@3（rerank）：精排后 top-3 是否含标准段 —— 对比两者看 rerank 带来多少提升
#   - faithfulness（可选 --faith）：调 DeepSeek 判断最终回答是否基于检索资料（需 key，花钱）
#
# 用法：
#   python rag_eval.py            # 只跑离线 recall / hit 对比
#   python rag_eval.py --faith    # 额外跑忠实度评估（需 DEEPSEEK_API_KEY）
import argparse
import os

from rag import 知识库实例

# 评估集：(问题, 期望命中段里的核心短语, 领域)
# 🟢 懂框架：用"核心短语"而非写死段 index——文档合并/顺序变了也不影响判断，更稳。
评估集 = [
    ("东西寄回去行不行", "无理由退货", "电商"),
    ("半夜能不能找你们", "9:00-21:00", "电商"),
    ("买多了有便宜吗", "满199减30", "电商"),
    ("耳机质量不行能换不", "无理由退货", "电商"),
    ("螺丝还够不够用", "不锈钢螺丝 M6", "工厂"),
    ("哪些算原料", "库存分成品", "工厂"),
    ("什么时候该提醒采购补货", "安全库存阈值", "工厂"),
    ("铜线现在有多少", "铜线 2.5mm²", "工厂"),
]


def _生成回答(问题, 资料):
    """调 DeepSeek 基于检索资料生成回答（faithfulness 用）。"""
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    r = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是客服，只能根据[资料]回答，不得编造资料里没有的信息。"},
            {"role": "user", "content": f"[问题]{问题}\n[资料]{资料}"},
        ],
    )
    return r.choices[0].message.content


def _忠实度判定(问题, 资料, 回答):
    """再调一次 DeepSeek 判断回答是否基于资料。"""
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    r = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": (
                "判断下面客服回答是否完全基于[检索资料]、没有编造资料里没有的信息。\n"
                f"[问题]{问题}\n[检索资料]{资料}\n[回答]{回答}\n只回答『基于』或『编造』之一。"
            )},
        ],
    )
    return "基于" in r.choices[0].message.content


def 主(启用faith: bool = False):
    if not 知识库实例.加载():
        print("⚠️ 请先运行 python 构建知识库.py 构建索引")
        return
    print(f"知识库共 {len(知识库实例.片段列表)} 段\n")
    print(f"{'问题':<18}{'领':<4}{'hit@3(无rerank)':<16}{'hit@3(rerank)':<14}{'faith(基于)'}")
    print("-" * 70)

    命中无 = 0
    命中有 = 0
    召回数 = 0
    faith命中 = 0
    for 问题, 短语, 领域 in 评估集:
        粗排全量 = 知识库实例.检索(问题, top_k=20, 启用重排=False)  # 粗排候选（验证不漏）
        无重排 = 知识库实例.检索(问题, top_k=3, 启用重排=False)
        有重排 = 知识库实例.检索(问题, top_k=3, 启用重排=True)

        召回 = 短语 in 粗排全量
        命中无 = 命中无 + (1 if 短语 in 无重排 else 0)
        命中有 = 命中有 + (1 if 短语 in 有重排 else 0)
        召回数 = 召回数 + (1 if 召回 else 0)

        faith标记 = "-"
        if 启用faith and os.getenv("DEEPSEEK_API_KEY"):
            try:
                答 = _生成回答(问题, 有重排)
                if _忠实度判定(问题, 有重排, 答):
                    faith命中 += 1
                    faith标记 = "✅"
            except Exception as e:
                faith标记 = f"⚠️{e}"

        print(f"{问题:<16}{领域:<4}{('✅' if 召回 else '❌'):<10}"
              f"{('✅' if 短语 in 无重排 else '❌'):<16}"
              f"{('✅' if 短语 in 有重排 else '❌'):<14}{faith标记}")

    总数 = len(评估集)
    print("-" * 70)
    print(f"召回率 recall@候选 : {召回数}/{总数} = {召回数/总数:.0%}")
    print(f"hit@3 (无 rerank) : {命中无}/{总数} = {命中无/总数:.0%}")
    print(f"hit@3 (rerank)    : {命中有}/{总数} = {命中有/总数:.0%}")
    if 启用faith and os.getenv("DEEPSEEK_API_KEY"):
        print(f"faithfulness      : {faith命中}/{总数} = {faith命中/总数:.0%}")


if __name__ == "__main__":
    参数 = argparse.ArgumentParser()
    参数.add_argument("--faith", action="store_true", help="额外跑忠实度评估（需 DEEPSEEK_API_KEY）")
    选项 = 参数.parse_args()
    主(启用faith=选项.faith)
