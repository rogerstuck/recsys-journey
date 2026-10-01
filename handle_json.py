import json
from pathlib import Path
# 1.准备数据
config = {"name":AI,"VERSION":1.0}

# 2.确定保存路径:当前脚本所在目录下的config.json
config_path = Path(__file__).resolve().parent / 'config.json'

# 3.保存(写入)到文件
with open(config_path,"w",encoding="utf-8") as f: #"w"表示写入模式，"utf-8"防止中文乱码
    json.dump(config,f,ensure_ascii=False,indent=4) #ensure_ascii=False防止中文乱码，indent=4表示缩进4个空格

print(f"配置已保存到: {config_path}")

# 4.从文档读取并打印
with open(config_path,"r",encoding="utf-8") as f:
    loaded = json.load(f)

print("读取到的配置:")
print(loaded)
print(f"name = {loaded['name']}, version = {loaded['version']}")

