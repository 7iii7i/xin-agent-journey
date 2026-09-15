# 情况A：两个都必填，少传一个 → Python 报错
def 打招呼(名字, ID):
    print(f"你好 {名字}，你的ID是 {ID}")

print("=== A. 两个必填，只传1个会怎样 ===")
try:
    打招呼("小明")                 # 只传了名字，没传 ID
except TypeError as e:
    print("报错：", e)


# 情况B：给 ID 设默认值 → ID 变成"可选"
def 打招呼2(名字, ID="游客"):       # 🔴 死记写法：形参=默认值
    print(f"你好 {名字}，你的ID是 {ID}")

print("\n=== B. ID 有默认值，可不传 ===")
打招呼2("小红")                    # 不传 ID，用默认的"游客"
打招呼2("阿强", 9527)             # 传了就用传进来的 9527


# 情况C：两个都传（正常）
print("\n=== C. 两个都传 ===")
打招呼("小明", 1001)


# 易错点：默认值参数必须放"没有默认值参数"的后面
# 下面反例若真写进文件会直接 SyntaxError（Python 加载时就报错，连 try 都抓不到）：
#     def 错的(名字="匿名", ID): ...  → SyntaxError: parameter without a default follows parameter with a default
# 正确写法演示：必填在前、可选在后
print("\n=== D. 默认值参数必须放后面（正确写法） ===")
def 对的(名字, ID="游客"):        # ✅ 必填 名字 在前，可选 ID 在后
    print(f"对的写法：{名字} / {ID}")
对的("小明")                      # 可省 ID，自动用"游客"
