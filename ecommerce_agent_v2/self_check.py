#!/usr/bin/env python3
"""
端到端自检：启动 v2 服务 → 探测首页 → POST /ask → 验证返回 JSON。
用法（在 ecommerce_agent_v2 目录下）：
    python self_check.py
"""
import json
import subprocess
import sys
import time
import urllib.request

# 用当前解释器启动 uvicorn
PYTHON = sys.executable
HOST = "http://localhost:8003"


def main():
    print("==> 启动 v2 服务...")
    proc = subprocess.Popen(
        [PYTHON, "main.py"],
        cwd=".",
    )
    print(f"PID={proc.pid}")

    try:
        # 1) 探测首页
        for i in range(15):
            try:
                with urllib.request.urlopen(f"{HOST}/", timeout=2) as r:
                    if r.status == 200:
                        print(f"==> 首页已就绪（HTTP {r.status}）")
                        break
            except Exception as e:
                print(f"    第 {i + 1} 次探测未就绪: {e}")
                time.sleep(1)
        else:
            print("❌ 服务启动超时")
            return 1

        # 2) 模拟浏览器发一个问题
        print("==> 模拟浏览器 POST /ask ...")
        req = urllib.request.Request(
            f"{HOST}/ask",
            data=json.dumps({"session_id": "selfcheck_001", "question": "有耳机吗"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read().decode("utf-8")
            print(f"==> POST /ask 状态码: {r.status}")
            print(f"==> 响应体前 400 字:\n{body[:400]}")
            data = json.loads(body)
            assert "answer" in data, "响应 JSON 缺少 answer 字段"
            print("✅ 自检通过：服务能接收问题并返回合法 JSON")
            return 0

    except Exception as e:
        print(f"❌ 自检失败: {e}")
        return 1

    finally:
        print("==> 关闭服务...")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=3)


if __name__ == "__main__":
    sys.exit(main())
