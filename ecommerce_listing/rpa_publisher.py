# ===== 电商自动上架 Agent · 核心2：Playwright RPA 真·自动填表上架 =====
import json
# 干嘛：打开"发布页" → 把每条文案填进对应表单 → 点发布 → 等成功回执
# 原理：Playwright 驱动真实 Chromium 浏览器，用"选择器"定位页面元素并操作
# 🔴死记：这是你之前没碰过的"新骨架"——UI 自动化（RPA），和 API 调用是两码事。
# 🟢懂框架：selectors（选择器）就是"页面上这个框的身份证"，换平台只改这套映射即可。

from playwright.sync_api import sync_playwright

# ===== 适配器模式：闲鱼一套选择器，以后接淘宝只需新增一套 =====
# 🟢懂框架：把"平台差异"封在一张映射表里，主逻辑不用改——这就是简历可讲的"适配器模式"。
闲鱼选择器 = {
    "标题":   "#title",
    "描述":   "#description",
    "价格":   "#price",
    "标签":   "#tags",
    "类目":   "#category",
    "按钮":   "#publishBtn",
    "成功标志": "#result",
}

# 预留：真要接淘宝/千牛 PC 发布页，照着填一套即可，下方 发布一条() 一行不用改
淘宝选择器 = {
    "标题":   "#J_Title",        # 示意，真实页需按实际改
    "描述":   "#J_Description",
    "价格":   "#J_Price",
    "标签":   "#J_Tags",
    "类目":   "#J_Category",
    "按钮":   "#J_Publish",
    "成功标志": "#J_Result",
}

def 发布一条(数据: dict, 页面地址: str, 选择器=闲鱼选择器) -> str:
    """把一条文案自动填进发布页并提交，返回平台回执文本"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)   # 🔴死记：headless=True=无界面跑，CI/服务器通用
        page = browser.new_page()
        page.goto(页面地址)

        page.fill(选择器["标题"], 数据["标题"])
        page.fill(选择器["描述"], 数据["描述"])
        page.fill(选择器["价格"], str(数据["建议价"]))
        page.fill(选择器["标签"], "，".join(数据.get("卖点", [])))
        page.select_option(选择器["类目"], 数据["类目"])
        page.click(选择器["按钮"])

        # 等"发布成功"出现，证明 RPA 真的提交成功了（超时则抛错）
        page.wait_for_selector(f'{选择器["成功标志"]}:has-text("发布成功")', timeout=5000)
        回执 = page.text_content(选择器["成功标志"])
        browser.close()
        return 回执

def 批量发布(listings_json: str, 页面地址: str) -> list:
    """读 listings.json，逐条 RPA 上架，汇总结果"""
    with open(listings_json, encoding="utf-8") as f:
        数据 = json.load(f)
    结果 = []
    for item in 数据:
        if "错误" in item:
            结果.append({"商品": item["原始商品"], "状态": "跳过（文案生成失败）"})
            continue
        try:
            回执 = 发布一条(item, 页面地址)
            结果.append({"商品": item["原始商品"], "状态": "已上架", "回执": 回执})
        except Exception as e:
            结果.append({"商品": item["原始商品"], "状态": "失败", "错误": str(e)})
    return 结果
