# 真实闲鱼发布第一步：等用户扫码登录，登录后探测发布表单结构
from playwright.sync_api import sync_playwright
import os, json

EDGE = r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
PROFILE = r"C:/Users/Administrator/.workbuddy/playwright_profile_real"
URL = "https://www.goofish.com/publish?spm=a21ybx.changelog.0.0.18a7672eYm7Ear"
HERE = os.path.dirname(os.path.abspath(__file__))
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"

with sync_playwright() as p:
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
    print("浏览器已弹出，请用手机闲鱼 App 扫页面上的二维码登录。")
    print("如果没看到二维码，请检查屏幕是否被其他窗口挡住。")

    logged_in = False
    for i in range(12):  # 60 秒
        page.wait_for_timeout(5000)
        txt = page.evaluate("() => document.body.innerText")
        is_login = "手机扫码安全登录" in txt
        print("[" + str(i+1) + "/12] 等待登录中... 页面含“手机扫码安全登录”=" + str(is_login))
        if "手机扫码安全登录" not in txt:
            # 进一步确认是发布表单
            if any(k in txt for k in ["标题", "价格", "描述", "宝贝", "发闲置"]):
                print(">>> 检测到已登录，发布表单出现")
                logged_in = True
                break
    if not logged_in:
        print("60 秒内未检测到登录成功，脚本退出。如已扫码但页面没刷新，请重新运行。")
        ctx.close()
        exit(0)

    page.wait_for_timeout(3000)
    page.screenshot(path=os.path.join(HERE, "probe_after_login.png"), full_page=True)
    print("已截图: probe_after_login.png")

    # 探测所有可输入元素
    fields = []
    for sel in ["input", "textarea", "div[contenteditable='true']", "div[contenteditable='']"]:
        for el in page.query_selector_all(sel):
            fields.append({
                "tag": el.evaluate("e => e.tagName"),
                "id": el.get_attribute("id"),
                "class": el.get_attribute("class"),
                "placeholder": el.get_attribute("placeholder"),
                "aria_label": el.get_attribute("aria-label"),
                "type": el.get_attribute("type"),
                "name": el.get_attribute("name"),
                "text": el.inner_text().strip()[:80],
            })
    # 探测按钮/可点击文字
    btns = []
    for el in page.query_selector_all("button, [role='button']"):
        btns.append({
            "tag": el.evaluate("e => e.tagName"),
            "class": el.get_attribute("class"),
            "text": el.inner_text().strip()[:50],
        })

    with open(os.path.join(HERE, "probe_form.json"), "w", encoding="utf-8") as f:
        json.dump({"inputs": fields, "buttons": btns}, f, ensure_ascii=False, indent=2)
    print("已保存表单结构: probe_form.json")
    print("下一步：根据这两份文件写自动填表发布脚本")
    ctx.close()
print("DONE")
