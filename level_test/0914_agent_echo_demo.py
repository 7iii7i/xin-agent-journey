# ⑤-4 Agent echo 版（教学 demo，本地可跑，不调真实 API）
# 目的：练熟 Agent 循环三件套 = while 循环 + tool_calls 判断 + 历史记录

# ---- 工具：一个最简单的加法 ----
def 加法(num1, num2):
    return num1 + num2

# ---- 历史：装所有对话消息的列表（每一轮都往里加）----
历史 = [
    {"role": "user", "content": "帮我算 3 加 5 等于多少"}
]

print("=== Agent 启动 ===")
轮次 = 0
while 轮次 < 3:                      # 真实版用 while True，这里限 3 轮做演示
    轮次 += 1
    print(f"\n--- 第 {轮次} 轮 ---")

    # ① 模拟"模型回复"（真实版这里换成调 DeepSeek）
    if 轮次 == 1:
        # 第1轮：模型说"我要调加法工具"
        回复 = {
            "content": None,
            "tool_calls": [{"name": "加法", "args": {"num1": 3, "num2": 5}}]
        }
    else:
        # 第2轮：工具结果回来，模型给出最终答案
        回复 = {
            "content": "3 加 5 等于 8。",
            "tool_calls": None
        }

    # ② 把模型回复塞进历史
    历史.append({"role": "assistant", "content": 回复["content"], "tool_calls": 回复["tool_calls"]})

    # ③ 判断：模型要不要调工具？
    if 回复["tool_calls"]:
        for 调用 in 回复["tool_calls"]:
            函数名 = 调用["name"]
            参数 = 调用["args"]
            if 函数名 == "加法":
                结果 = 加法(参数["num1"], 参数["num2"])
            历史.append({"role": "tool", "content": str(结果), "name": 函数名})
        print(f"模型请求调工具：{函数名}，参数 {参数} → 结果：{结果}")
    else:
        # 没有 tool_calls = 模型给出最终答案，结束循环
        print(f"模型最终回答：{回复['content']}")
        break

print("\n=== 完整历史（每一轮都往里加）===")
for 消息 in 历史:
    print(消息)
