# 本机环境探针：跑通真 bge 模型前，先确认依赖齐不齐
# 用法（在你本机 v2 目录打开命令行执行）：
#   python 本机环境探针.py
# 全部 ✅ 后再跑「python 构建知识库.py」下载模型 + 构建索引。
import sys
import importlib
import os


def 检查(包名: str) -> bool:
    try:
        m = importlib.import_module(包名)
        print(f"✅ {包名:<20} 已装，版本 {getattr(m, '__version__', '?')}")
        return True
    except Exception:
        print(f"❌ {包名:<20} 缺失 -> 需要 pip install {包名}")
        return False


print("=== 一、检查 Python 依赖 ===")
齐 = True
齐 &= 检查("numpy")
齐 &= 检查("sentence_transformers")   # 这个会自动带 torch
齐 &= 检查("torch")

print("\n=== 二、检查 DeepSeek 密钥（Agent 对话要用）===")
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass
key = os.getenv("DEEPSEEK_API_KEY")
if key:
    print(f"✅ DEEPSEEK_API_KEY 已配置（长度 {len(key)}）")
else:
    print("❌ DEEPSEEK_API_KEY 未配置 -> 检查 .env 文件里有没有这行：DEEPSEEK_API_KEY=sk-...")

print("\n=== 三、结论 ===")
if 齐 and key:
    print("🎉 环境就绪！直接跑：")
    print("   pip install -r requirements.txt   # 若上面有 ❌，先装齐（torch 约 1GB，一次性）")
    print("   python 构建知识库.py               # 下载 bge 模型(~90MB)+构建索引+自测打印")
    print("   python main.py                     # 起服务，浏览器开 http://localhost:8003/")
    print("   然后问口语化问题，如『耳机坏了能退吗』『半夜有人工吗』")
else:
    print("⚠️ 上面有 ❌ 项，先处理完再继续。")
    if not 齐:
        print("   装依赖：pip install -r requirements.txt")
    if not key:
        print("   配密钥：在 .env 里写 DEEPSEEK_API_KEY=你的key")
