# ============================================================
# class 从零教学 · 用"盒子"来理解（不用记账）
# 一个盒子能：放东西 / 数数 / 倒出来看
# ============================================================

print("########## 第 1 步：class = 一种盒子的设计图 ##########")
class Box:
    def __init__(self):
        self.items = []          # 这个盒子里的格子（一开始是空的）

# 上面只是"设计图"，还没做出盒子
b = Box()                        # 真正做出一个盒子（__init__ 自动跑）
print("做出一个盒子，里面 =", b.items)     # 空的 []
print()


print("########## 第 2 步：add = 往盒里放一样东西 ##########")
class Box:
    def __init__(self):
        self.items = []

    def add(self, thing):                  # self = 这个盒子自己
        self.items.append(thing)

b = Box()
b.add("苹果")            # 调用时不写 self！Python 自动把 b 塞进 self
b.add("书")
print("放了 2 样后，盒里 =", b.items)
print()


print("########## 第 3 步：count = 数数盒里有多少 ##########")
class Box:
    def __init__(self):
        self.items = []

    def add(self, thing):
        self.items.append(thing)

    def count(self):
        return len(self.items)             # 数格子有几样

b = Box()
b.add("苹果")
b.add("书")
b.add("钥匙")
print("调用 b.count()，盒里一共 =", b.count(), "样")
print()


print("########## 第 4 步：show = 把盒里东西倒出来看 ##########")
class Box:
    def __init__(self):
        self.items = []

    def add(self, thing):
        self.items.append(thing)

    def count(self):
        return len(self.items)

    def show(self):
        for t in self.items:
            print("盒里有：", t)

b = Box()
b.add("苹果")
b.add("书")
b.add("钥匙")
b.show()
print("一共", b.count(), "样")
