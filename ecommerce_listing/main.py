# ===== 电商自动上架 Agent · 入口：FastAPI 把上面两块串成网页服务 =====
# 干嘛：浏览器上传 CSV → 生成文案 → 看结果 → 一键 RPA 上架到模拟发布页
# 原理：复用你之前学的 FastAPI 三件套（app + 路由 + 返回）；RPA 片段在后台同步跑
# 🔴死记：结构你认得——和之前电商/工厂项目一样的"开店+挂路由"，只是业务逻辑换了。

import os, json
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from generate_listings import 批量生成
from rpa_publisher import 批量发布

app = FastAPI()
BASE = os.path.dirname(__file__)

@app.get("/", response_class=FileResponse)
def 首页():
    return FileResponse(os.path.join(BASE, "index.html"))

@app.get("/publish-page", response_class=FileResponse)
def 发布页():
    # 你浏览器里打开这个地址，就能看到那个"模拟闲鱼发布页"
    return FileResponse(os.path.join(BASE, "publish_page.html"))

@app.post("/api/generate")
async def 生成(文件: UploadFile = File(...)):
    # 1) 收下上传的 CSV
    csv路径 = os.path.join(BASE, "_upload.csv")
    with open(csv路径, "wb") as f:
        f.write(await 文件.read())
    # 2) 批量生成文案（内部真实调 DeepSeek，产出 listings.json）
    文案列表 = 批量生成(csv路径)
    return {"数量": len(文案列表), "listings": 文案列表}

@app.post("/api/publish")
def 上架():
    # RPA 目标页：本地模拟发布页（file:// 直接喂给 Playwright）
    页面 = "file://" + os.path.join(BASE, "publish_page.html")
    结果 = 批量发布(os.path.join(BASE, "listings.json"), 页面)
    return {"结果": 结果}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
