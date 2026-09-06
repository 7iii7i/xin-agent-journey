# tier1_solution.py
# 这是第 1 关的「正确写法」参考版。
# 每行都加了注释说明为什么这么写、自己之前哪里可以改。
# 建议：先自己看完，再合上文件手敲一遍，把语法记到手。

# 1) 列表里放 3 个字典。每个字典就是一组"字段: 值"。
#    ⚠️ 自己写的版本：cities 行最前面有 4 个空格 + 后面跟了"3 个字典"的注释留在原地
#    → 注释留在列表外没关系，但 cities 这一行如果顶格写才不会被 Python 当成缩进错误
cities = [
    {"name": "北京", "population": 2189},
    {"name": "杭州", "population": 1237},
    {"name": "玉环", "population": 65},
]

# 2) for 循环：每次拿出一个城市叫 city。
#    ⚠️ 自己写的版本：name=city["name"] 和 population=city["population"] 是对的，
#    说明字典取值你已经会了。
for city in cities:
    # 3) 先用「f-string」拼出一行：f"..." 里的 {变量} 会被替换成值
    #    ⚠️ 自己写的版本：用的是 print(a, b, c)，会自动加空格，输出"北京 2189 万"
    #    期望输出是"北京 2189万"（数字和万之间没空格），所以必须用 f-string
    line = f"{city['name']} {city['population']}万"

    # 4) 如果人口 >= 1000，在这一行末尾追加"【大城市】"
    #    ⚠️ 自己写的版本：把 qw 做成了「元组」(city["name"], city["population"])
    #    然后试图 qw.append(...)。元组是不可变的，没有 append，会报：AttributeError: 'tuple' object has no attribute 'append'
    #    ✅ 正确做法：直接拼字符串。
    if city["population"] >= 1000:
        line = line + " 【大城市】"

    # 5) 一次打印
    #    ⚠️ 自己写的版本：qw 拼出来了但忘记用，标签永远印不出来
    print(line)