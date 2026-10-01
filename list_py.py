# 1.os&pathlib
# 在代码中安全的读写文件、遍历文件夹、获取路径
from pathlib import Path
import os

Path.cwd() # 获取当前工作目录
Path.home() # 获取用户主目录
p.is_file() # 判断是否是文件
p.is_dir() # 判断是否是目录
p.mkdir() # 创建目录
p.glob('*.txt') # 获取目录下的所有txt文件

os.path.join() # 拼接路径
os.listdir() # 列出目录下的所有文件和目录
os.makedirs() # 创建目录
os.environ # 获取所有环境变量
os.environ.get('PATH') # 获取PATH环境变量

# 2.json
# 处理JSON格式数据(推荐系统经常需要读取配置或存储中间结果)
import json

json.loads() # 将JSON字符串转换为Python字典/列表
json.dumps() # 将Python字典/列表转换为JSON字符串
json.load() # 从文件中读取JSON数据
json.dump() # 将Python字典/列表的数据写入文件

# 3.collections
# 使用更强大的容器数据类型
from collections import defaultdict, Counter, OrderedDict, namedtuple
# defaultdict: 提供默认值的dict,若key不存在,则返回默认值
defaultdict(int) # 创建一个默认值为0的defaultdict
# Counter: 统计元素出现次数
Counter(['a', 'b', 'a', 'c']) # 创建一个统计元素出现次数的Counter
# OrderedDict: 有序的dict,保持插入顺序
OrderedDict([('a', 1), ('b', 2), ('c', 3)]) # 创建一个有序的dict
# namedtuple: 创建带字段名的元组，增强代码可读性
Person = namedtuple('Person', ['name', 'age']) # 创建一个具名元组


