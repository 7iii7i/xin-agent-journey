# ===== 端到端一键演示：生成文案 + RPA 自动上架 =====
# 用法：python demo.py
# 流程：① 读 sample_products.csv → 真实调 DeepSeek 生成文案
#       ② 用 Playwright 真打开 publish_page.html → 自动填表 → 点发布

import os
from generate_listings import 批量生成
from rpa_publisher import 批量发布

if __name__ == "__main__":
    print("① 批量生成闲鱼上架文案（真实调用 DeepSeek）...")
    文案列表 = 批量生成("sample_products.csv")
    for x in 文案列表:
        print("  -", x.get("原始商品"), "→", x.get("标题", x.get("错误")))

    print("\n② 运行 Playwright RPA 自动填表上架（本地模拟闲鱼发布页）...")
    页面 = "file://" + os.path.abspath("publish_page.html")
    结果 = 批量发布("listings.json", 页面)

    print("\n③ 上架结果：")
    for r in 结果:
        print("  -", r)
