# 函数三件套：def / return / 调用
# 本质：函数 = 一段"打包好的动作"，给材料(参数)就干活，干完用 return 交结果

# 1) 定义函数（def = 造一个函数）
def add(a, b):            # a, b 是"形参"=占位的空盒子
    return a + b          # return = 把结果交出去（不是打印！）

# 2) 调用函数（名(参数) 才执行）
result = add(3, 5)        # 3, 5 是"实参"=真正塞进去的值
print("add(3,5) =", result)        # 8

# 3) 只写函数名不执行
print("只写 add 本身：", add)       # 打出函数对象，没跑

# 4) return ≠ print 的关键区别
def add_print(a, b):
    print(a + b)          # 只打印到屏幕，没 return

r2 = add_print(3, 5)      # 屏幕打出 8
print("add_print 的返回值 r2 =", r2)   # None！因为没 return

# 5) f-string + return 组合（你熟悉的模式）
def greet(name):
    return f"你好，{name}！"

print(greet("忻"))        # 你好，忻！
