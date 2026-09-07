# Day3 速查卡：while / input / append / break + 对话历史

## 1. while 循环 —— 反复执行，直到 break
```python
while True:        # 条件为 True 就一直循环（死循环）
    x = input("你: ")
    if x == "exit":
        break       # 跳出循环，程序继续往后走
    print(x)
```
- `while 条件:` 每轮先判断条件，为真才进循环体
- `break` = 立刻跳出整个循环；`continue` = 跳过本轮剩下、直接进入下一轮

## 2. input() —— 从终端读一行用户输入
```python
name = input("请输入名字：")   # 屏幕显示提示，等你敲字回车，返回字符串
```
- 返回类型永远是 **str**（字符串），即使你输入数字
- 想当数字用要转换：`int(input("年龄："))`

## 3. list.append() —— 往列表末尾加一个元素
```python
messages = []
messages.append({"role": "user", "content": "你好"})   # 加一个字典
messages.append({"role": "assistant", "content": "你好！"})  # 再加一个
# 现在 messages = [{"role":"user",...}, {"role":"assistant",...}]
```
- `append` 改变原列表本身（不返回新列表，返回 None）
- 这正是"多轮对话记忆"的实现方式：每轮把 user 和 assistant 消息都 append 进去

## 4. 对话历史 messages 是怎么回事（Agent 核心）
- 模型**本身无记忆**，每次请求都是独立的
- 所谓"记住上下文"，是你**把之前所有消息重新拼进 messages 再发一次**
- 结构：`[{"role":"system",...}, {"role":"user",...}, {"role":"assistant",...}, ...]`
  - `system`：系统设定（人设/规则），一般放最前，模型优先遵循
  - `user`：用户说的话
  - `assistant`：模型上一轮的回复
- 顺序必须 user / assistant 交替，不能乱

## 5. 今天这套 = Agent 循环的雏形
```
loop:
    读用户输入 → append 到 messages
    发请求(带上完整 messages)
    取回复 → 打印 → append 到 messages
```
以后学 LangChain / 框架，本质就是把这个循环封装起来 + 加"工具调用"。先把这 30 行手写熟，框架就是你的工具而非拐杖。

## 运行
```
cd xin-agent-journey
python -m uv run python week01/day3_interactive_chatbot.py
```
输入几句话测试它是否"记得"前面聊过的内容，输入 exit 退出。
