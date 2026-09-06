# ===== 第 2 关：读代码 + 找 bug + 修（已修复版）=====
# 意图：从一段 JSON 文本里取出城市名并打印。
# 这段代码给的是「正常输入」，所以直接运行不会报错——
# 但两个 bug 都是潜伏 bug：一旦线上遇到异常数据就炸。
# 下面已经修好，并附 3 个测试。
import os, json

# 假设这是某次接口返回的（注意：是「字符串」，不是字典）
# 测试切换：
#   ① 正常输入   —— 保持下面这行
#   ② 缺字段     —— 改成 '{"data": {}}'
#   ③ 非法 JSON  —— 改成 '这不是json'
raw = '{"data": {"city": {"name": "玉环", "code": "331083"}}}'

# 修 BUG 2：json.loads 遇到非法文本会抛 JSONDecodeError，用 try/except 包起来
try:
    resp = json.loads(raw)
except json.JSONDecodeError:
    print("解析失败")
else:
    # 修 BUG 1：用 .get() 链安全取值，缺字段也不崩
    # 中间用 {} 而不是 None，因为下一步还要 .get()，只有字典才有 .get()
    city = resp.get("data", {}).get("city", {})
    name = city.get("name")
    if name:
        print("城市：" + name)
    else:
        print("城市：未知")
