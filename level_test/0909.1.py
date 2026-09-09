# 题1'​（对应基础题1，A）：把字典 {"fruit": "苹果", "price": 5} 存成 fruit.json 再读回，打印 fruit 和 price。
# 题2'​（对应基础题2，C/D）：用 datetime 打当前时间章，并用 os.path.exists 判断 fruit.json 在不在。
# 题3'​（对应基础题3，E/F/G）：用 Path 拼 data/hello.txt，先建父目录，再写一行 "测试"。
# 题4'​（对应基础题4，B）：用 json.dumps 把字典 {"name": "楚尘", "power": 99} 变成字符串并打印（中文不乱码）。

import json

fruits={"fruit": "苹果", "price": 5}
with open("fruit.json","w",encoding="utf-8")as f:
    json.dump(fruits,f,ensure_ascii=False,indent=2)
with open("fruit.json",encoding="utf-8")as f:
    h=json.load(f)
print(h["fruit"],h["price"])

from datetime import datetime
import os
print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print(os.path.exists("fruit.json"))


from pathlib import Path
p=Path("data")/"hello.txt"
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text("测试")
print(p.read_text())

import json
s=json.dumps({"name": "楚尘", "power": 99},ensure_ascii=False)
print(s)




