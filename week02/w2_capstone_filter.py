import json

def 读取英雄(path):
    # with open + json.load：今天刚复习的标准写法
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def 过滤(英雄列表, 阈值):
    结果 = []
    for 英雄 in 英雄列表:
        # 链式 .get 安全取值：字段缺失返回 None，不会崩
        战力 = 英雄.get("power")
        if 战力 is None:
            continue                       # 没战力字段的跳过
        if 战力 >= 阈值:
            结果.append(英雄)
    return 结果

def 主程序():
    阈值 = 700
    # 异常处理：文件不存在 / JSON 格式错，两种都接住
    try:
        英雄列表 = 读取英雄("heroes.json")
    except FileNotFoundError:
        print("找不到 heroes.json")
        return
    except json.JSONDecodeError:
        print("heroes.json 格式不对")
        return

    达标 = 过滤(英雄列表, 阈值)
    print(f"战力 >= {阈值} 的英雄有 {len(达标)} 个：")
    for 英雄 in 达标:
        print(f"  {英雄.get('name', '无名')} - 战力 {英雄.get('power')}")

    # 写回 JSON：dump 没有 s = 写进文件对象；ensure_ascii=False 保中文
    with open("filtered.json", "w", encoding="utf-8") as f:
        json.dump(达标, f, ensure_ascii=False, indent=2)
    print("已写入 filtered.json")

# __main__ 门卫：直接运行本文件才启动；被别的文件 import 时不自作主张跑
if __name__ == "__main__":
    主程序()
