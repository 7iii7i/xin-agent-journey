# day2 标准库实战 cheatsheet（W2 收尾）

> 今天目标：管数据(json) / 管文件(os.path) / 管时间(datetime) 三件套 + 认 requests 为 W3 调 AI 接口铺路

## 先认三个总词
- **模块(module)**：别人写好的一盒工具，import 进来就能用
- **标准库**：Python 出厂自带的工具箱，装好 Python 就能 import，不用额外装
- **import**：把工具箱拿进当前文件用的动作（类比"从仓库把工具搬上工作台"）

## json —— 字典 ↔ 字符串（LLM 返回的就是它）
- 字典 = Python 家里的"收纳盒"；JSON = 能寄快递的"标准箱"
- `json.dumps(字典)` → 收纳盒装进快递箱，变成**字符串**（用来发给 API / 存文件）
- `json.loads(字符串)` → 把快递箱拆开，还原成**字典**（用来读 API 返回）
- `json.dump(字典, 文件)` / `json.load(文件)` → 直接读写 .json 文件
- `ensure_ascii=False` → 让中文不乱码（配 `encoding="utf-8"` 一起用）

## os / pathlib —— 管文件路径和目录
- `os.path.exists("x.txt")` → 文件在不在，返回 True/False
- `os.listdir(".")` → 列出当前目录下的东西
- `from pathlib import Path; p = Path("a") / "b.txt"` → 拼路径（**跨平台**，不用手写斜杠）

## datetime —— 管时间
- `from datetime import datetime`
- `datetime.now()` → 此刻
- `datetime.now().strftime("%Y-%m-%d %H:%M:%S")` → 格式化成可读字符串（给日志/文件名盖时间章）

## re —— 正则，按"形状"从文字里捞东西
- `import re; re.findall(r"\d+", "订单123共456")` → `['123','456']`（\d+ = "一串数字"的模具）

## requests（W3 才真用，今天先认脸）
- 发 HTTP 请求的工具箱（向网址要数据/发数据）
- `requests.get(url).json()` → 取回一个网址返回的数据，直接变字典（背后就是 json.loads）
- 下周调大模型 API：`response = requests.post(接口地址, json=请求体)` → `response.json()` 拿到模型回答

## 易混点补充（零基础常踩）

### 1. `open` 的 mode：默认是 "r"，写必须明写 "w"
- `open("x")` 或 `open("x", "r")` 都行 → 不写 mode 默认就是"只读 r"，加不加一样。
- 写文件**必须** `open("x", "w")` → 因为默认是只读，不写 "w" 就会用只读模式去写，直接报错。
- 口诀：**"r" 能省（默认），"w" 不能省（要写必须明说）。**

### 2. `ensure_ascii=False` vs `encoding="utf-8"`（两个不同环节，常一起写）
- `encoding="utf-8"` 是 **`open()` 的参数** → 管"字符↔字节"（文件怎么存）。不写在 Windows 上默认 gbk，中文可能乱码。
- `ensure_ascii=False` 是 **`json.dump` 的参数** → 管"中文要不要转成 \uXXXX 转义"（json 怎么写中文）。默认 True 会写成丑陋转义。
- 写中文 .json 文件：**两个一起写** = 存得稳 + 看得懂。
  ```python
  with open("a.json", "w", encoding="utf-8") as f:
      json.dump({"name": "楚尘"}, f, ensure_ascii=False)   # ✅ 文件里是漂亮中文
  ```
- 只写 ensure_ascii=False 但 open 没写 encoding → Windows 默认 gbk 编码中文，可能乱码/报错。
- 只写 encoding 但 ensure_ascii 用默认 True → 文件里是 `{"name": "\u695a\u5c18"}`，能存但人看不懂。

### 3. `Path("a") / "b.txt"` 拼接路径详解
- `from pathlib import Path` → 从标准库 pathlib 把 Path 蓝图请出来。
- `Path("a")` → 造一个"路径对象"（不是字符串），代表当前目录下 a。
- `/` 在这里**不是除法**，被 pathlib 重定义为"拼路径"：`Path("a") / "b.txt"` = 把 b.txt 接到 a 后 → `a/b.txt`。
- 右边可以是字符串或另一个 Path；可连拼 `Path("a") / "b" / "c.txt"`。
- 不用手写斜杠：Windows 用 `\`、Linux/Mac 用 `/`，Path 的 `/` 自动按系统换对的斜杠，一份代码到处跑。
- `p = Path("a") / "b.txt"` → p 是路径对象外号，可接 `p.exists()` / `p.mkdir(parents=True)` / `p.read_text()`。
  ```python
  # ❌ 手写（跨平台易崩、反斜杠要转义）
  bad = "a" + "\\" + "b.txt"
  # ✅ Path（推荐）
  from pathlib import Path
  p = Path("a") / "b.txt"      # 永远正确，自动适配系统

### 4. `Path.mkdir(parents=True)` 建目录（含中间目录）
- `Path("data").mkdir()` → 建一个 data 文件夹（必须是路径对象，字符串不能调）。
- `parents=True` → 连"中间的父目录"一起建：`Path("data/log/2026").mkdir(parents=True)` 一次性建出 data/data/log/data/log/2026 三层；默认 parents=False 会因父目录不存在报错。
- 加强版里 `target = Path("data") / "记录_2026-09-09.txt"`，写文件前 `target.parent.mkdir(parents=True)` 先把父目录 data 建出来（target.parent = data）。
- `exist_ok=True` → 目录已存在也不报错（不加重复建同名目录会抛 FileExistsError）。推荐写成 `Path("data").mkdir(parents=True, exist_ok=True)` 更稳。
  ```python
  from pathlib import Path
  target = Path("data") / "记录_2026-09-09.txt"
  target.parent.mkdir(parents=True, exist_ok=True)   # 先建父目录 data
  target.write_text("记录于 ...")                      # 再写文件
  ```

### 5. 写文件完整流程（以 `Path("data")/"note.txt"` 为例，逐步）
- `p = Path("data") / "note.txt"` → p 代表**文件 note.txt**（不是文件夹 data）。
- `p.parent` → 取 p 的"父目录" = `data` 文件夹（note.txt 的上级）。
- `p.parent.mkdir(parents=True, exist_ok=True)` → 先把 data 文件夹建出来（铺路）；exist_ok=True 让已存在也不报错。
- `p.write_text("文字")` → 往 p 这个文件写一行；文件不存在自动创建，**存在则清空重写（不是追加）**。
- ⚠️ 顺序不能反：write_text 要求父目录已存在，若 data 还没建就直接写 → 报错（父目录不存在）。必须先 mkdir 再 write_text。
- 要"追加"而非覆盖：用 `p.read_text() + 新内容` 再 write_text，或 `p.open("a").write("文字")`。

### 6. `read_text()` 读文件内容（write_text 的孪生）
- `p.read_text()` → 把 p 这个文件的全部内容读成**字符串**返回（和 write_text 一对：一个写、一个读）。
- 想"打印刚写进去的内容"：`p.write_text("测试"); print(p.read_text())` → 打印 `测试`（不是路径）。
- 对照 `print(p)`：p 是路径对象，打印的是文件名 `data\hello.txt`；`p.read_text()` 才是文件里的文字。
- 呼应 json 的"两对"：`write_text`/`read_text`（文件内容）与 `dump`/`load`（json）都是"写↔读"一对。

### 7. `+` 拼接 vs `,` 分隔参数（字符串粘一段 vs 给函数列多项）
- `"记录于 " + now_str` → `+` 是字符串**拼接运算符**，把左右两段文字**粘成一段新文字**（`"记录于 2026-09-09 ..."`），结果还是一段，可传给 `write_text`。
- `"记录于 ", now_str` → `,` 是**参数分隔符**，把东西分成好几项传给函数。`write_text("记录于 ", now_str)` 等于传了**两个**参数，但 `write_text` 只收一个 → 报错 `TypeError`。
- 为什么 `print` 里逗号能用：`print("记录于", now_str)` 中 print 天生吃多个参数、自动用空格连起来显示；`write_text` 没这本事，只认一个参数。
  ```python
  print("记录于", now_str)           # ✅ print 收多参数，显示：记录于 2026-09-09 ...
  p.write_text("记录于 " + now_str)  # ✅ 一个参数（已拼好）给 write_text
  p.write_text("记录于 ", now_str)   # ❌ 两个参数，TypeError
  # 等价的 f-string 写法（更推荐）：p.write_text(f"记录于 {now_str}")
  ```
- 记忆：**`+` 把文字粘成一段；`,` 把东西分成几项（只适合 print 这类能吃多参数的函数）。写文件别用逗号，用 `+` 或 f-string。**

### 8. f-string：`{变量}` 才能把变量"值"塞进字符串（引号里写变量名只是死字）
- `f"记录_{date_str}.txt"` → `f` 是格式化开关，引号里的 `{date_str}` 运行时被**替换成变量的值** → `记录_2026-09-09.txt`。
- `"记录_{date_str}.txt"`（没 f 前缀）→ `{date_str}` 被当普通文字原样输出，不会取值。
- **最致命的坑**：`"datetime1.txt"`（带引号）= 死文字，Python 不会去翻你那个变量盒子，文件名会变成字面的"datetime1.txt"，跟变量里存的日期毫无关系。想用变量值必须 `f"..."` + `{变量}`。
  ```python
  date_str = "2026-09-09"
  print(f"记录_{date_str}.txt")   # ✅ 记录_2026-09-09.txt（值塞进去了）
  print("记录_{date_str}.txt")    # ❌ 记录_{date_str}.txt（死字，没取值）
  ```

### 9. 变量必须先定义、后使用（Python 从上往下逐行读）
- 用到一个变量前，必须先在它上面某行 `变量名 = ...` 定义过；否则报 `NameError: name 'xxx' is not defined`。
- 错例：`p = Path("data") / f"记录_{datetime1}.txt"` 写在第 8 行，但 `datetime1 = ...` 定义在第 10 行 → 读到第 8 行时 datetime1 还不存在 → 崩。
- 修法：把"定义"整行剪切到"使用"前面，或另起一个先定义的变量（如先 `date_str = ...` 再拼文件名）。

### 10. `strftime` 格式串决定产出长相：文件名只用 `%Y-%m-%d`（无冒号）
- `%Y-%m-%d` = 年月日（`2026-09-09`），**不含冒号** → 适合做文件名。
- `%H:%M:%S` = 时分秒（`20:15:32`），**带冒号** → Windows 文件名不允许冒号，塞进去会 `OSError: Invalid argument` 报错。
- 用法分工：**文件名**用 `datetime.now().strftime("%Y-%m-%d")` 取日期；**文件内容**才用 `.strftime("%Y-%m-%d %H:%M:%S")` 取完整时间。
  ```python
  date_str  = datetime.now().strftime("%Y-%m-%d")             # 只取日期 → 给文件名（无冒号，合法）
  datetime1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    # 完整时间 → 给文件内容
  p = Path("data") / f"记录_{date_str}.txt"
  p.write_text("记录于" + datetime1)                          # 内容：记录于2026-09-09 20:15:32
  ```
- 记忆：**文件名无冒号，内容可带时间。**

### 11. `print` 直接打单个对象不用 for；for 只给"遍历多个元素"用
- `print(任何东西)` 都能直接打印：字符串、数字、列表、字典、甚至 json 字符串 `s`——print 会把这个对象**整体**显示出来，不需要 for。
- `for` 是用来"把容器里的每个元素单独处理"的（列表每个元素、字典每个键值对、字符串每个字符）。只有想"逐个取出多个东西"时才用 for。
- `s = json.dumps(字典)` → `s` 是**一个字符串（一整段文字）**，不是"多个东西"，所以 `print(s)` 一次整段打出即可，不用 for。
- 反例：逐个打印字典键值对用 `for k, v in 字典.items(): print(k, v)`；逐个打印列表元素用 `for x in 列表: print(x)`。
- 记忆：**print 是"举起来看整体"，for 是"一个个拆开处理"。dumps 的结果是整体字符串，直接 print。**
- 补充：`json.loads(s)` 读回字典后，`print(字典)` 同样**不用 for**——字典也是一个对象，print 能整体打；只有想逐个取出 key/value 处理才用 `for k, v in 字典.items(): print(k, v)`。无论字符串还是字典，print 都整体打，for 永远只为"逐个处理多个元素"。

### 12. JSON 到底是什么（一种"大家都看得懂的纯文本数据格式"）
- JSON = JavaScript Object Notation，名字带 JavaScript 但跟它没啥关系，只是一种"用文字写数据"的通用约定格式，谁都能读。
- **本质**：JSON 就是**一段按规矩排好的字符串（纯文字）**，长得像 Python 字典 `{"name": "楚尘", "power": 99}`，但它是"写在纸上的字"，不是程序里能直接 `.keys()` 的活对象。
- **为什么需要它**：Python 字典只能活在 Python 内存里；想发给网站、存进文件、传给 Java/JS 等其他语言，就得变成 JSON 这种"通用普通话文本"。网络只传文本、不传活对象。
- **Python 字典 vs JSON 文本**：字典是"活的"（内存对象，能操作）；JSON 是"死的文字"（一串字符，要解析才能用）。`json` 模块就是"翻译机"——`dumps` 把活字典翻成 JSON 文字，`loads` 把 JSON 文字翻回活字典。
  ```python
  import json
  字典 = {"name": "楚尘"}          # 活的（内存对象）
  文字 = json.dumps(字典)          # 翻译：活 → 死（字符串 '{"name": "楚尘"}'）
  复活 = json.loads(文字)          # 翻译：死 → 活（又能 .keys() 了）
  ```
- 记忆：**字典是脑子里的想法（活），JSON 是写在纸上寄出去的字（死、纯文本、谁都懂）；json 模块是翻译员。下周调 API 模型返回的就是 JSON 文字，你得 loads 回字典才用得了。**

### 13. JSON ≠ 文件（它是"格式"，文件是"盒子"）
- **JSON 是一种数据格式（纯文本约定），文件是存储载体**——两个不同层面，JSON 不等于一个文件。
- JSON 可以**不在文件里**：它可以是内存里的一段字符串（如 `s = json.dumps(...)` 的 s，纯内存、压根没文件）、网络响应的文本、数据库字段里的文字。
- 反过来，**.json 文件只是"装 JSON 文本的盒子"**：文件本身（操作系统里的那个文件）不是 JSON，文件里"符合 JSON 格式的那些字"才是 JSON。JSON 文本塞进 .txt 文件也一样是 JSON，扩展名不影响"是不是 JSON"。
- 联系今天：题4 `s = json.dumps(...)` 的 s 就是 JSON（在内存，无文件）；题1 `json.dump(hero, f)` 是把 JSON 文本写进 hero.json 这个"盒子"。**文件是容器，JSON 是里面的内容。**

### 14. 看见题目想不起"该用啥公式"怎么办（先卡 30 秒 + 查"意图→工具"触发表）
- 现象："看解析完全能懂，但自己看到题想不起来用哪个函数"——这**不是没学会**，是"从题目到工具的提取路径"还没建起来（自动化）。解析能懂=输入通；想不出=检索/输出没练够。每次"哦对就是 json.dump"的恍然大悟都在建这条路径，只是还没自动。
- **策略 A：做题先卡 30 秒再翻答案**。别一不会就翻基础版——那 30 秒苦思正是记忆长出的时机。卡完翻答案，对比"我想到的 vs 答案用的"，差距就是该补的检索点。
- **策略 B：看完解析合上立刻自己重写一遍**（retrieval practice）。光看不算，重写才把解析变自己的。
- **策略 C：用下面"意图→工具"表当检索锚点**。看到题先判"这属于哪类动作"，再调对应工具：

| 题目说的意图 | 该想到的工具 |
|---|---|
| 字典存成文件 / 从文件读回 | `json.dump(字典, f)` / `json.load(f)` |
| 字典变字符串（不存）/ 变回来 | `json.dumps(字典)` / `json.loads(字符串)` |
| 中文别乱码 | `ensure_ascii=False` + `encoding="utf-8"` |
| 拼文件路径（跨平台） | `Path("a") / "b.txt"` |
| 建文件夹（含上级） | `p.parent.mkdir(parents=True, exist_ok=True)` |
| 写一行文字到文件 | `p.write_text("内容")` |
| 读回文件内容 | `p.read_text()` |
| 当前时间 / 文件名盖日期 | `datetime.now().strftime("%Y-%m-%d %H:%M:%S")` |
| 判断文件在不在 | `os.path.exists(路径)` |
| 文字 + 变量拼一起 | `f"..{变量}.."` 或 `"a" + 变量` |
| 多个元素逐个处理 | `for ... in ...` |

- 记忆：**"想不起"=路径未自动化，不是没懂；先卡再翻、看完重写、对着意图表检索，三招把路径练成自动。**

### 15. "存成 fruit.json" 这题：dump/dumps 都能，但"写盘"不能省；with open 不是唯一写法
- 任务关键词"**存成 xxx.json**" = 在磁盘上**真的生成一个文件**。分两步理解：
  - **方法A（json.dump + with open）**：`dump` 直接把字典写进"打开的文件对象 f"。
    ```python
    import json
    fruit = {"fruit": "苹果", "price": 5}
    with open("fruit.json", "w", encoding="utf-8") as f:
        json.dump(fruit, f, ensure_ascii=False)     # 一步：字典 → 文件
    ```
  - **方法B（json.dumps + Path.write_text）**：`dumps` 先把字典变成 JSON **字符串**，再用 `write_text` 把字符串写进文件。**效果等价**。
    ```python
    import json
    from pathlib import Path
    fruit = {"fruit": "苹果", "price": 5}
    s = json.dumps(fruit, ensure_ascii=False)        # 字典 → 字符串（还在内存）
    Path("fruit.json").write_text(s, encoding="utf-8")  # 字符串 → 文件
    ```
- **`json.dumps` 单独用 ❌ 造不出文件**：dumps 只给你"内存里的一段字符串"，永远不碰磁盘。光 `s = json.dumps(...)` 就不会有 fruit.json 文件——必须再把它写进文件才行。
- **`with open` 不是必须 ✅**：只要最终"写盘"了，写法不限。可替代：`Path("fruit.json").write_text(json.dumps(字典, ensure_ascii=False))`（不用 open、不用 with）。新手最稳还是 `with open + json.dump`。
- **读回同理**：想从文件读，必须"打开文件"——`json.load(f)`（with open）或 `Path(...).read_text()` + `json.loads(...)`。
- 记忆：**"存成 xxx.json" = 必须写盘；dump 一步到位，dumps 要先变字符串再写；with open 是最稳写法但不是唯一写法。**

### 16. `Path("x")` 不创建文件，`write_text` 才真正建文件并写入
- `Path("fruit.json")` = 只造一个"路径对象"（指路牌/标签），告诉 Python"我要操作这个位置的文件"。**这一步不会在磁盘上生成任何文件**——此时文件还不存在。
- `Path("fruit.json").write_text(s, encoding="utf-8")` = 真正动手：若文件不存在就**创建**它，存在则清空重写，把 s 的内容写进去。文件是在这一刻才出现的。
- 串联：`s = json.dumps(字典, ensure_ascii=False)` 这一步只是把字典变成内存里的字符串 s，**也不碰磁盘**；直到 `write_text(s)` 才落地成文件。
- 联系前面：write_text 只负责"建文件"，不负责"建它的父文件夹"。所以 `Path("data")/"note.txt"` 要先 `p.parent.mkdir(parents=True)` 把 data 文件夹建好，再 `write_text` 才不会报"父目录不存在"。
- 记忆：**Path() 是起名/指路，write_text 才动手建文件；dumps 只给字符串，不碰磁盘。**

### 17. `os.read` ≠ "读文件内容"；读文件内容用 `文件对象.read()` 或 `Path.read_text()`
- `from os import read` 导入的是 `os.read(fd, n)`：**操作系统底层函数**，第一个参数是**整数文件描述符（fd）**，第二个是读取字节数。它不是"按文件名读内容"的工具——传字符串文件名会直接报 `TypeError: read expected 2 arguments, got 1`。
- 正确"读一个文件内容"的两种写法：
  ```python
  # 写法1：文件对象的 .read() 方法（按名打开）
  with open("x.txt", encoding="utf-8") as f:
      text = f.read()          # ✅ 读内容
  # 写法2：pathlib
  from pathlib import Path
  text = Path("x.txt").read_text(encoding="utf-8")   # ✅ 读内容
  ```
- 易混点：**`open("x").read()` 的 `read` 是"文件对象的方法"**（吃 0/1 个参数，读内容）；`os.read(fd, n)` 是"模块函数"（吃 2 个参数，要 fd）。同名但完全不是一回事，想"按文件名读内容"绝不能用 `os.read`。
