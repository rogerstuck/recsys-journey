#numpy核心用法

import numpy as np

# 一、创建数组

# 1.np.array()  
#将python原生list转换成numpy数组
list_data = [[1,2,3],[4,5,6]]
arr = np.array(list_data)
print(arr)

# 2.np.zeros()[全0]&np.ones()[全1]
#推荐系统中用途:初始化一个全0的(用户数,物品数)评分矩阵
zeros_arr = np.zeros((2,3)) # 2行3列的全0矩阵
ones_arr = np.ones((3,2))

# 3.np.arange()
#类似python的range,在Numpy中直接返回数组,可接受三个参数(起点,终点[不含],步长)
seq_arr = np.arange(0,10,2)
print(seq_arr)

# 4.np.random.rand()
# 生成指定形状的数组,元素在[0,1)间均匀分布的随机浮点数
random_arr = np.random.rand(2,2) # 2×2的随机矩阵

# 核心属性

# .shape   返回数组在每个维度上的大小
# .ndim    返回数组的维数
# .dtype   返回数组中元素的数据类型
print(arr.shape,arr.ndim,arr.dtype)

# 改变形状

# .reshape  不改变数组内数据,改变数组的形状
#推荐系统中用途:常用arr.reshape(1,-1)将一维数组转换为二维
arr = np.arange(12) 
reshaped_arr = arr.reshape(3,4) #变为3行4列的二维数组

# arr.T 矩阵转置
arr = np.array([[1,2],[3,4]])
print(arr.T)




# 二、索引与切片

arr = np.arange(20).reshape(4,5)

# 1.基本切片
sub_arr = arr[1:3,0:2] #取1-2行、0-1列

# 2.布尔索引
#推荐系统中用法:筛选/过滤数据
#单条件筛选: 把True的元素挑出来,返回一个一维数组
print(arr[arr>15])
#多条件组合筛选
#在numpy中,组合条件不能用and/or,必须用位运算符
print(arr[(arr>3)&(arr<10)])

# 3.花式索引
# 推荐系统中用法:根据用户ID列表批量提取对应的特征向量
print(arr[[0,2]]) # 提取第0、2行
print(arr[[0,1,2],[0,2,4]]) #提取(0,0)(1,2)(2,4)




# 三、向量化

arr1 = np.array([1,2,3])
arr2 = np.array([4,5,6])
arr = np.array([1,2,3])

# 元素级运算(对应位置元素的运算)
# 实际意义:对特征矩阵进行归一化操作时使用
print(arr1+arr2,arr*2)
print(np.exp(arr),np.log(arr),np.sqrt(arr),np.sin(arr)) # 分别计算e的次方、对数、开根号、三角

# 推荐场景解析:矩阵乘法
# no.dot() / @

# 用户特征矩阵:3个用户,2个特征(喜欢动作片/喜剧片程度)
U = np.array([
    [0.8,0.1],
    [0.2,0.9],
    [0.5,0.5]
])

# 电影特征向量
V = np.array([0.9,0.3])

#使用矩阵乘法预测所有用户的评分
predictions = np.dot(U,V)

print(predictions)




# 四、广播
# 运算原则:右对齐比较
# 右对齐:两个数组从最右边开始对齐
# 兼容原则:若两个维度相等/其中一个是1,则二者兼容[若一个是1，就会被复制到与另一个维度相同的大小]
# 缺失维度:若其中一个数组的维度较小,numpy会在左侧补1,然后再进行比较

A = np.ones((3,4))
B = np.array([1,2,3,4])
print(A+B) # B被拉伸为(3,4),每一行都是原来B的数据,然后对应元素相加

col = np.array([
    [1],
    [2],
    [3]
]) # (3,1)
row = np.array([10,20,30,40]) #(1,4)
print(col+row) #col、row变为(3,4)

# 推荐场景解析:计算均方误差MSE
true_ratings = np.array([
    [5,4,1,2],
    [3,5,2,2],
    [1,2,4,5]
]) #3个用户对四部电影的真实评分

pred_ratings = np.array([
    [4],
    [3],
    [3]
]) #模型对这三个用户的整体打分预测

errors = pred_ratings - true_ratings # 计算误差,广播将(3,1)直接拉伸为(3,4)
print(errors)




# 五、常用统计与线性代数

# 1.常用统计函数
arr = np.array([
    [1,2,3,4],
    [5,6,7,8],
    [9,10,11,12]
])

# 分别计算总和、平均值、最大值
print(arr.sum(),arr.mean(),arr.max()) 
#分别计算每一列、每一行的和,返回一个一维数组
print(arr.sum(axis=0),arr.sum(axis=1)) 

# 2.线性代数

# (1)np.dot()
# 若均为一维数组,计算结果为点积;若均为二维数组,则为矩阵乘法(a @ b)
a = np.array([1,2],[3,4])
b = np.array([5,6],[7,8])
print(np.dot(a,b))

# (2)np.linalg.norm() 
# 计算向量的长度/矩阵的范数,默认计算L2范数(欧几里得距离)
v = np.array([3,4])
print(np.linalg.norm(v)) # 根号下(3^2+4^2) = 5.0

#推荐场景解析:计算余弦相似度
#夹角越小,cos值越大,相似度越高
# 两个用户的特征向量
user1 = np.array([1,2,3])
user2 = np.array([4,5,6])

#计算点积、范数
dot_product = np.dot(user1,user2)
norm1 = np.linalg.norm(user1)
norm2 = np.linalg.norm(user2)

#计算余弦相似度
cos_sim = dot_product/(norm1*norm2)
print(cos_sim)


