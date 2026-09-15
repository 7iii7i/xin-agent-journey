# 真实闲鱼发布第二步：在已登录状态下，自动填表发布第一件闲置
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
import os, json, textwrap

EDGE = r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
PROFILE = r"C:/Users/Administrator/.workbuddy/playwright_profile_real"
URL = "https://www.goofish.com/publish?spm=a21ybx.changelog.0.0.18a7672eYm7Ear"
HERE = os.path.dirname(os.path.abspath(__file__))
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"


def make_image(path: str, title: str):
    """生成一张简单的占位商品图，用于上传"""
    img = Image.new("RGB", (800, 800), color=(245, 245, 245))
    draw = ImageDraw.Draw(img)
    # 标题
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except Exception:
        font = ImageFont.load_default()
    for i, line in enumerate(textwrap.wrap(title, width=18)):
        draw.text((80, 120 + i * 55), line, fill=(30, 30, 30), font=font)
    # 装饰矩形
    draw.rectangle([60, 280, 740, 520], outline=(255, 204, 0), width=4)
    draw.text((80, 300), "[AI自动上架测试图]", fill=(150, 150, 150), font=font)
    img.save(path, "JPEG", quality=85)
    print(f"已生成占位图: {path}")


def build_description(item: dict) -> str:
    lines = [item["标题"], ""]
    lines.append(item["描述"])
    lines.append("")
    lines.append("卖点：" + " | ".join(item["卖点"]))
    return "\n".join(lines)


with sync_playwright() as p:
    # 1) 生成占位图
    img_path = os.path.join(HERE, "test_bike.jpg")
    make_image(img_path, "捷安特ATX自行车")

    # 2) 读取要发布的商品文案
    with open(os.path.join(HERE, "listings.json"), "r", encoding="utf-8") as f:
        listings = json.load(f)
    item = listings[0]

    # 3) 启动已登录的浏览器
    ctx = p.chromium.launch_persistent_context(
        PROFILE,
        headless=False,
        executable_path=EDGE,
        user_agent=USER_AGENT,
        args=[
            "--no-sandbox",
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
            "--disable-dev-shm-usage",
        ],
        viewport={"width": 1280, "height": 900},
    )
    page = ctx.new_page()
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
        window.chrome = { runtime: {} };
    """)
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(4000)

    # 4) 确认在发布表单
    body = page.evaluate("() => document.body.innerText")
    if "发闲置" not in body or "宝贝描述" not in body:
        print("未检测到发布表单，可能未登录。请先用 real_publish_step1.py 登录一次。")
        page.screenshot(path=os.path.join(HERE, "step2_error.png"), full_page=True)
        ctx.close()
        exit(1)
    print(">>> 已检测到发布表单，开始填表")

    # 5) 上传宝贝图片（第一个 input[type=file]）
    file_input = page.locator('input[type="file"]').first
    file_input.set_input_files(img_path)
    print(">>> 已上传图片")
    page.wait_for_timeout(2000)

    # 6) 填宝贝描述（contenteditable div）
    desc = build_description(item)
    editor = page.locator('div[class*="editor--"]').first
    # 先聚焦，再模拟真实键盘输入（React 才能识别变化）
    editor.click()
    page.wait_for_timeout(300)
    # 用 Playwright 的 fill：新版支持 contenteditable
    try:
        editor.fill(desc)
    except Exception:
        # 兜底：逐字键盘输入
        page.keyboard.type(desc, delay=5)
    print(">>> 已填写宝贝描述")

    # 7) 填价格（第一个 placeholder=0.00 的输入框）
    price_inputs = page.locator('input[placeholder="0.00"]').all()
    if len(price_inputs) >= 1:
        price_inputs[0].fill(str(item["建议价"]))
        print(f">>> 已填价格: {item['建议价']}")
    if len(price_inputs) >= 2:
        # 原价填一个合理的数字（从描述里抓“原价1500”）
        original = 1500
        price_inputs[1].fill(str(original))
        print(f">>> 已填原价: {original}")

    page.wait_for_timeout(1500)

    # 8) 点击发布按钮
    publish_btn = page.locator('button:has-text("发布")').first
    publish_btn.click()
    print(">>> 已点击发布按钮")

    # 9) 等待结果并截图
    page.wait_for_timeout(6000)
    page.screenshot(path=os.path.join(HERE, "step2_result.png"), full_page=True)
    result_text = page.evaluate("() => document.body.innerText")
    print(">>> 结果页已保存: step2_result.png")

    # 10) 输出是否出现成功/校验提示
    for kw in ["发布成功", "已发布", "校验失败", "请填写", "请上传", "失败", "错误"]:
        if kw in result_text:
            print(f"检测到关键词: {kw}")

    ctx.close()
print("DONE")
