# .get() 与 try/except 小抄

> 你做 API / 读 JSON 时天天要用。忘了就回这里查。

## 一、.get() —— 字典的「安全取值」

### 问题：直接用 `[]` 取不存在的 key 会崩

```python
user = {"name": "忻"}
print(user["age"])        # 崩：KeyError: 'age'
```

### 解法 1：.get() 缺 key 时返回 None，不崩

```python
print(user.get("age"))    # 输出：None（不报错）
```

### 解法 2：.get(key, 默认值) 缺 key 时返回你指定的值

```python
print(user.get("age", 0))        # 输出：0
print(user.get("age", "未知"))    # 输出：未知
```

### 链式取值（多层嵌套）

```python
resp = {"data": {"city": {"name": "玉环"}}}

# 硬取值（会崩如果缺任意一层）
name = resp["data"]["city"]["name"]

# 安全链式（缺任何一层都返回 None，不崩）
name = resp.get("data", {}).get("city", {}).get("name")
#                                ↑                 ↑
#        中间用 {} 当默认值，因为 {} 也有 .get() 方法
#        如果这里用 None 当默认，None.get() 会崩
```

**为什么中间要用 `{}` 而不是 `None`？**
链式调用时，上一步的返回值还要接着 `.get()`。只有「字典」才有 `.get()` 方法。如果某层缺失返回了 `None`，下一步 `None.get(...)` 会抛 `AttributeError`。所以中间层用空字典 `{}` 当兜底，保证链不断。

### 常见陷阱

```python
city = resp.get("data", {}).get("city", {})
name = city.get("name")
print("城市：" + name)        # 如果 name 是 None，这里崩：str 不能拼 None
# 修法：判断一下
if name:
    print("城市：" + name)
else:
    print("城市：未知")
```

---

## 二、try / except —— 出错也不让程序挂

### 一句话

**`try` 里放「可能崩的代码」，`except` 里放「崩了怎么办」。崩了就走 except，不崩就跳过 except。**

### 最小结构

```python
try:
    x = 1 / 0              # 这行会崩（ZeroDivisionError）
except ZeroDivisionError:
    print("出错了，但不能让程序挂")   # 崩了走这里
```

### 三个常用子句

```python
try:
    do_risky()             # 可能崩
except ValueError:
    handle_value_error()   # 崩了且是 ValueError → 走这
else:
    no_error_happened()    # 没崩 → 走这（可选）
finally:
    always_run()           # 不管崩没崩都走这（可选，常用于关文件/关连接）
```

### Tier 2 用的：捕获 JSON 解析错误

```python
import json

raw = "这不是合法 json"
try:
    data = json.loads(raw)        # 给垃圾，会抛 json.JSONDecodeError
except json.JSONDecodeError:
    print("解析失败")             # 崩了走这里，程序不挂
else:
    print("解析成功：", data)     # 没崩走这里
```

### 怎么知道该 except 哪种错误？

报错时看最后一行最下面的报错名：
- `json.loads("垃圾")` → `json.JSONDecodeError`
- `d["不存在"]` → `KeyError`
- `1 / 0` → `ZeroDivisionError`
- `int("abc")` → `ValueError`

**先用 `except Exception:` 兜底（抓所有错误），跑通后再换成具体错误名。**  production 里尽量写具体错误名，别永远用 `Exception`。

### 常见陷阱

```python
try:
    x = 1 / 0
except:                 # 不写具体错误类型
    pass                # 静默吞掉所有错误
```
❌ 这样连"键盘中断 Ctrl+C"都吞掉，调试时极难发现错误在哪。**至少写 `except Exception:`**，或更具体的名字。

---

## 三、合起来：Tier 2 的标准写法骨架

```python
import os, json

raw = '{"data": {"city": {"name": "玉环", "code": "331083"}}}'

try:
    resp = json.loads(raw)                    # BUG 2 修法：包起来
except json.JSONDecodeError:
    print("解析失败")
else:
    # BUG 1 修法：安全链式取值
    city = resp.get("data", {}).get("city", {})
    name = city.get("name")
    if name:
        print("城市：" + name)
    else:
        print("城市：未知")
```

跑 3 个测试：
- raw 正常 → 城市：玉环
- raw = '{"data": {}}' → 城市：未知（不崩）
- raw = '不是json' → 解析失败（不崩）
