import json

raw = '{"data": {"city": {"name": "玉环", "code": "331083"}}}'
resp = json.loads(raw)  # resp = 大箱子 {"data": 中箱子}

print("=== 大箱子 resp 长什么样 ===")
print(resp)
print("resp 的钥匙（最外层只有 data）:", list(resp.keys()))
print()

# 第 1 步：从大箱子里把 "data" 对应的值拿出来
step1 = resp.get("data", {})
print("=== step1 = resp.get('data', {}) 拿到的是「中箱子」===")
print(step1)
print("step1 的钥匙（只有 city）:", list(step1.keys()))
print()

# 第 2 步：在「中箱子」上再取 "city" 对应的值
step2 = step1.get("city", {})
print("=== step2 = step1.get('city', {}) 拿到的是「小箱子」===")
print(step2)
print("step2 的钥匙（只有 name / code）:", list(step2.keys()))
print()

# 正式写法（一步写完）
city = resp.get("data", {}).get("city", {})
print("=== city 最终存的东西（和 step2 完全一样）===")
print(city)
print("city 的钥匙:", list(city.keys()))
print()

print(">>> 关键证据：city 的钥匙只有 ['name', 'code']")
print(">>> 说明 city 里既没有 'data'，也没有 'city' 这一层")
print(">>> 大箱子和中箱子都已经被「剥掉」了，city 只装着最里面的小箱子")
