# ============================================================
# class 到底是什么？—— 用你懂的"函数"来桥接
# 写法一：纯函数（不用 class，你本来就会）
# 写法二：class（同一件事，把数据和函数打包成整体）
# ============================================================

print("===== 写法一：纯函数（不用 class）=====")
def make_box():
    return {"items": []}

def add(box, thing):
    box["items"].append(thing)

def count(box):
    return len(box["items"])

b = make_box()
add(b, "苹果")
add(b, "书")
print("盒里：", b["items"], "一共", count(b), "样")


print()
print("===== 写法二：class（同一件事，打包成整体）=====")
class Box:
    def __init__(self):
        self.items = []

    def add(self, thing):
        self.items.append(thing)

    def count(self):
        return len(self.items)

b = Box()
b.add("苹果")
b.add("书")
print("盒里：", b.items, "一共", b.count(), "样")
