# 今晚复习速记卡 · 0907

> 用途：睡前 / 明天早上花 10 分钟扫一遍，确认脑子里"画面"还在。
> 配套文件：`weak_points.md`（易忘点清单）、`week01/notes/术语表.md`（查生词）。

---

## 一、今晚战果

| 题 | 内容 | 你跑出的结果 | 状态 |
|---|---|---|---|
| 题 1 | 列表字典遍历算平均分 | `77.25` | ✅ |
| 题 2 | 嵌套字典安全取值 | `小明`（缺数据不崩，打`未知`） | ✅ |
| 题 3 | class 记账本 | 三行支出 + `总额：67` | ✅ |

**打通的 5 个概念**：`for` 循环模型、`累加器`、`try/except/else`、`class/self`、函数三件套（`def`/`return`/调用）。

---

## 二、5 个核心概念 · 速记卡

### 1. for 循环 = 复读机
- **本质**：缩进的那几行代码，对着集合每个元素**重放一遍**。列表有 4 个元素 → 重放 4 次。
- **铁律**：
  - 缩进内 = 每遍重放；缩进外 = 整程序只跑一次。
  - 每轮 `x` 只面对【一个】元素，不是整个集合。
  - 字典默认遍历**键**；要值用 `.values()`，要键值对用 `.items()`。
- **你原话痛点**："循环这个总的概念还是不懂" → 现在要能说出"缩进=模板动作，对着每个元素重放"。

### 2. 累加器 = 三个动作
- **本质**：不是新语法，是套路（开本子 → 边走边加 → 看总数）。
- **铁律**：
  - `total = 0` 写在**循环外** → 只清零一次（关键！不清零在循环里就不会每轮从 0 起步）。
  - 循环内 `total = total + 值`（或 `total += 值`）每次累加。
  - 循环外 `total / len(数据)` 算平均。
- **你原话痛点**："以为每轮都从 0 加" → 记住：加之前 total 不是 0，是上一轮的结果。

### 3. try / except / else
- **本质**：出错也不让程序挂。
- **结构**：
  ```python
  try:
      resp = json.loads(raw)        # 包"第一个可能崩的操作"
  except json.JSONDecodeError:      # 崩了怎么办（进阶：写具体错，别写 Exception）
      print("未知")
  else:
      nickname = resp.get("user",{}).get("profile",{}).get("nickname")  # 没崩才走
      if nickname:
          print(nickname)
      else:
          print("未知")
  ```
- **铁律**：不要重复 `try` 同一个 `loads`；`except` 兜底 + `else` 收正常逻辑。

### 4. class / self = 盒子模型
- **本质**：`class Box:` 是"盒子设计图"，不是盒子本身；必须 `b = Box()` 才做出一个真盒子。
- **铁律**：
  - `self` = "当前这个盒子自己"。
  - **定义时**：凡是"盒子自己的东西"都加 `self.`（`self.items`/`self.records`）。
  - **调用时**：永远不写 self（`b.add("苹果")`、`book.total()`），self 由 Python 自动塞。
  - `__init__(self)` = 开新盒子时自动跑的初始化（准备空格子）。
  - `def 方法(self, ...)` = 这个盒子能做的动作。
- **桥接**：class = 工厂函数 + 贴在它上面的函数；`self` = 那个被自动传入的 `box` 参数。

### 5. 函数三件套：def / return / 调用
- `def` = 定义（造一个函数）。
- `return` = 回传（把结果交出去给代码用，**不是打印**）。
- 调用 = 写 `名(参数)` 才真正执行；只写 `add` 是函数本身，不会跑。
- **核心坑**：`return` ≠ `print`。`return` 交出去的值，要靠外面的 `print` 才显示。

---

## 三、今晚新认的术语（速查，详情看术语表）

| 词 | 英文 | 意思 |
|---|---|---|
| `def` | define | 定义函数/方法 |
| `return` | return | 回传结果（不是打印） |
| `print()` | print | 打印到屏幕（内置函数） |
| `len()` | length | 数有几个 |
| `append` | append | 追加到列表末尾 |
| `add` | add | 添加（我们起的名字，可改） |
| `count` | count | 数 / 计数 |
| `show` | show | 展示（我们起的名字，**不是 Python 关键字**） |
| `self` | self | 自己（当前这个对象） |

**一句话**：你之前卡的全是"英文词不认识"。认全了，代码就是普通英语句子。

---

## 四、三题最终答案速查

### 题 1 · 平均分
```python
total = 0
for student in students:
    score = student["score"]
    total = total + score
print(total / len(students))     # 77.25
```

### 题 2 · 嵌套取值（防崩）
```python
import json
raw = '{"user": {"profile": {"nickname": "小明", "age": 28}}}'
try:
    resp = json.loads(raw)
except json.JSONDecodeError:
    print("未知")
else:
    nickname = resp.get("user", {}).get("profile", {}).get("nickname")
    print(nickname if nickname else "未知")
```

### 题 3 · class 记账本
```python
class AccountBook:
    def __init__(self):
        self.records = []
    def add(self, amount, note):
        self.records.append({"amount": amount, "note": note})
    def total(self):
        total = 0
        for r in self.records:
            total = total + r["amount"]
        return total
    def show(self):
        for r in self.records:
            print(f"支出 {r['amount']} 元 - {r['note']}")

book = AccountBook()
book.add(12, "早饭"); book.add(35, "午饭"); book.add(20, "打车")
book.show()
print("总额：", book.total())     # 67
```

---

## 五、自测 5 题（盖住答案想一遍）

1. `total = 0` 写在 for 循环**里面**和**外面**，结果有什么不同？为什么？
2. `for k in person:` 每轮 `k` 拿到的是整个字典，还是字典的一个键？
3. 题 2 里 `resp.get("user", {}).get("profile", {})` 中间的 `{}` 是干嘛的？
4. `class Box:` 和 `b = Box()`，哪个是"真盒子"？`self` 在调用时写不写？
5. `return a + b` 和 `print(a + b)` 的根本区别是什么？

> 答案都在上面四节里。能口述 5 题 → 今晚全掌握；哪题卡壳 → 回去翻对应那节的"铁律"。

---

## 六、下一步

- **巩固肌肉记忆**：把题 3 从空白再敲一遍（顺便把 `show` 格式补成 `支出 12 元 - 早饭` 对齐样例）。
- **别在"晕"时硬写**：脑子满就停，读成品、第二天再敲，吸收率更高。
- 需要"易忘点专项小测"复测哪块，直接说。
