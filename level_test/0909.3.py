# 写一段程序，故意去读一个不存在的文件 missing.json，用 try/except FileNotFoundError 兜住（打印"文件不在"而不崩溃）；如果文件在，就打印内容；最后 finally 打印"处理完毕"


try:
    f=open("missing.json")
except FileNotFoundError:
    print("文件不在")
else:
    print(f.read())
finally:
    print("处理完毕")
