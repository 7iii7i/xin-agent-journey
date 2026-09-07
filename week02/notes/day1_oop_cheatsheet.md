# week02/day1 速查卡：类与对象（OOP 入门）

## 1. 为什么用「类」
之前 day1–day3 全是「过程式」：变量散着、函数独立。
「类」把**数据（属性）和操作数据的方法（函数）打包成一个对象**，方便复用和管理状态。
> 以后你学的 Agent 框架（LangChain 等）核心就是各种「类」。今天这关是地基。

## 2. class / __init__ / self

```python
class ChatBot:                    # class 定义「一类东西」的模板
    def __init__(self, model):    # 构造方法：创建对象时自动跑
        self.model = model        # self.xxx = 挂到「这个对象」上（属性）
        self.messages = []        # 每个对象有自己的 messages
```
- `self`：永远指向「当前这个对象」。方法里要访问对象自己的数据，就写 `self.xxx`
- 调用时**不用写 self**：`bot.ask("你好")` → Python 自动把 bot 作为 self 传进去

## 3. 实例方法 vs 类方法（今天先记区别）
- **实例方法**：`def ask(self, ...)` —— 操作「某个具体对象」的数据，第一个参数是 self（今天用的就是这个）
- **类方法**：`@classmethod def xxx(cls, ...)` —— 操作「整个类」，第一个参数是 cls（week02 后面会讲，先不碰）

## 4. 创建对象 + 调方法
```python
bot = ChatBot()        # 创建对象 → 自动执行 __init__
bot.ask("你好")        # 调实例方法（self 自动传入）
bot.messages           # 访问属性
```

## 5. if __name__ == "__main__"
```python
if __name__ == "__main__":
    bot = ChatBot()
    bot.chat_loop()
```
- 直接 `python day1_class_chatbot.py` 运行 → `__name__` 等于 `"__main__"` → 里面代码执行
- 被别的文件 `import day1_class_chatbot` → `__name__` 是模块名 → 里面**不执行**（不会自动弹输入）
- 作用：让一个文件「既能当脚本跑，也能当模块被 import」，不互相干扰

## 6. 和 day3 的对照（同一件事，两种写法）
| | day3（过程式） | day1（面向对象） |
|---|---|---|
| 存历史 | 全局变量 `messages = []` | 对象属性 `self.messages = []` |
| 发请求 | 函数 `call_api(messages)` | 方法 `self.ask(text)` |
| 多轮 | `while` + 全局列表 | `chat_loop` 方法 + `self.messages` |
| 好处 | 简单直接 | 状态封装在对象里，可建多个独立 bot |

## 7. 怎么跑
```
cd xin-agent-journey
python -m uv run python week02/day1_class_chatbot.py
```
连聊几句测它是否「记得」前文（self.messages 生效），输入 exit 退出。
需有效 DeepSeek key（联网）。语法已 py_compile 校验通过。
