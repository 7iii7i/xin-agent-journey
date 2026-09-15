# 只讲 self：self 就是"点号前面的那个对象"
class 笔记本:
    def __init__(self, 主人):
        self.主人 = 主人
        self.条目 = []
    def 写(self, 内容):
        self.条目.append(内容)
    def 我是谁(self):
        return self              # 把 self 原样交出来，看它到底是谁

小明的本 = 笔记本("小明")
小红的本 = 笔记本("小红")

# 关键证明：调用 小明的本.我是谁() 时，self 收到的就是 小明的本 自己
print("self 就是 小明的本 吗？", 小明的本.我是谁() is 小明的本)   # True
print("self 就是 小红的本 吗？", 小红的本.我是谁() is 小红的本)   # True

小明的本.写("A")
小红的本.写("B")
# 因为 self 指向不同对象，所以两人各记各的：
print("小明的本：", 小明的本.条目)   # ['A']
print("小红的本：", 小红的本.条目)   # ['B']
