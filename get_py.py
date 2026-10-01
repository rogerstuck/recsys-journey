from pathlib import Path

# 1.获取当前脚本所在目录
# __file__ 是当前脚本的路径，.resolve() 转成绝对路径，.parent 取父目录
current_dir = Path(__file__).resolve().parent

# 2.遍历该目录下所有.py文件
for py_file in current_dir.glob('*.py'):
    # 3.打印文件的绝对路径
    print(py_file.resolve())