# ===== 电商自动上架 Agent · 核心1：批量生成闲鱼风格上架文案 =====
# 干嘛：读 CSV（原始商品）→ 调 DeepSeek → 产出"标题/描述/卖点/建议价/类目"结构化文案
# 原理：pandas 读表 → 对每一行发起一次 LLM 调用（要求返回 JSON）→ 汇总存盘
#      这里用"单次结构化生成"，不是之前学的"Agent 三件套工具循环"——
#      因为上架文案是"直接生成内容"，不需要模型自己决定调哪个工具。
# 🟢懂框架：想清楚"什么时候用工具循环、什么时候用单次生成"是工程师的基本判断。

import os, json
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
# 🔴死记：DeepSeek 走 OpenAI 兼容协议，base_url 固定填这个
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
)

# 类目必须从这份清单里选，RPA 填表时 select_option 要对得上
类目选项 = ["手机数码", "电脑办公", "家用电器", "服饰鞋包",
         "图书音像", "运动户外", "母婴用品", "闲置其他"]

系统提示 = """你是闲鱼二手商品上架文案助手。根据用户给的商品信息，生成适合闲鱼平台的二手上架文案。
要求：
- 标题：含品类核心词+成色+性价比亮点，像个人卖家口吻，不超过30字
- 描述：口语化、像个人闲置转让，说明成色/入手价/转让原因，2-4句
- 卖点：3-5个短标签（如 九成新、自提优惠、便宜出）
- 建议价：基于入手价和成色给合理二手价（纯数字，单位元）
- 类目：必须从给定类目列表里选一个
只输出 JSON，字段：标题(str)、描述(str)、卖点(list[str])、建议价(int)、类目(str)"""

def 生成一条(名称, 成色, 原价, 入手价, 备注) -> dict:
    """把一行商品信息变成一条闲鱼风格上架文案（真实调 DeepSeek）"""
    用户消息 = (
        f"商品：{名称}\n成色：{成色}\n原价：{原价}\n入手价：{入手价}\n"
        f"备注：{备注}\n可选类目：{','.join(类目选项)}"
    )
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": 系统提示},
            {"role": "user", "content": 用户消息},
        ],
        response_format={"type": "json_object"},  # 🔴死记：让模型只回 JSON
        temperature=0.7,
    )
    return json.loads(resp.choices[0].message.content)

def 批量生成(csv路径: str, 输出="listings.json") -> list:
    """读整张表，逐行生成，结果存成 listings.json"""
    df = pd.read_csv(csv路径)
    结果 = []
    for _, row in df.iterrows():
        try:
            文案 = 生成一条(row["名称"], row["成色"], row["原价"], row["入手价"], row["备注"])
            文案["原始商品"] = row["名称"]
            结果.append(文案)
        except Exception as e:
            结果.append({"原始商品": row["名称"], "错误": str(e)})
    with open(输出, "w", encoding="utf-8") as f:
        json.dump(结果, f, ensure_ascii=False, indent=2)
    return 结果

if __name__ == "__main__":
    print("批量生成中...")
    r = 批量生成("sample_products.csv")
    for x in r:
        print(" -", x.get("原始商品"), "→", x.get("标题", x.get("错误")))
