# 探测真实闲鱼发布页：用系统 Edge 有头模式 + 反检测
from playwright.sync_api import sync_playwright
import os

EDGE = r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
PROFILE = r"C:/Users/Administrator/.workbuddy/playwright_profile"
URL = "https://www.goofish.com/publish?spm=a21ybx.changelog.0.0.18a7672eYm7Ear"
HERE = os.path.dirname(os.path.abspath(__file__))
# 真实 Edge on Windows 的 User-Agent
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
        viewport={"width": 1280, "height": 800},
    )
    page = ctx.new_page()
    # 隐藏 navigator.webdriver 等自动化标记
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
        window.chrome = { runtime: {} };
    """)
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(8000)
    print("当前URL:", page.url)
    print("标题:", page.title())
    page.screenshot(path=os.path.join(HERE, "probe.png"), full_page=True)
    txt = page.evaluate("() => document.body.innerText")
    for kw in ["非法访问", "登录", "扫码", "密码", "短信", "二维码", "宝贝", "标题", "价格", "描述"]:
        if kw in txt:
            print(f">>> 页面含关键词: {kw}")
    if "非法访问" in txt:
        print(">>> 仍被反爬拦截")
    ctx.close()
print("DONE")
