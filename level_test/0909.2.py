# 用 Path 拼出路径 data/记录_YYYY-MM-DD.txt（其中 YYYY-MM-DD 用 datetime.now() 取当天日期）
# 先建好父目录 data（p.parent.mkdir(parents=True, exist_ok=True)）
# 往这个文件写一行内容：记录于 <当前时间>（<当前时间> 用 datetime.now().strftime("%Y-%m-%d %H:%M:%S") 取）
# 最后用 os.path.exists(...) 判断这个文件建出来了没有，把结果打印出来
from pathlib import Path
import os
from datetime import datetime
date_str=datetime.now().strftime("%Y-%m-%d")
p=Path("data")/ f"记录_{date_str}.txt"
p.parent.mkdir(parents=True, exist_ok=True)
datetime1=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
p.write_text("记录于"+datetime1)
print(p.read_text())
print(os.path.exists(p))