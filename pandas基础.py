# pandas基础
import pandas as pd

# 一、核心数据结构

# 1.Series:带标签的一维数组
s = pd.Series([10,20,30],index=['A','B','C'])
print(s)


# 2.DataFrame:二维表格,有行索引和列名

#用字典创建DataFrame
data = {
    '姓名':['张三','李四','王五'],
    '年龄':[25,30,28],
    '城市':['北京','上海','广州']
}
df = pd.DataFrame(data)
print(df)


# 3.读写数据

# pd.read_csv()/pd.read_json()  返回一个DataFrame
#参数众多:制定分隔符sep,指定编码encoding,处理缺失值na_values
df = pd.read_csv('user_logs.csv')

# df.to_csv  将内存中的DataFrame保存为csv文件
# 通常加上index=False,避免把Pandas自动生成的行索引也存进文件里
df.to_csv('cleaned_data.csv',index=False)


# 4.查看数据
print(df.head(2)) # 看前两行
df.info() # 打印DataFrame的摘要信息:行列数,每列名称,每列非空值数量,每列数据类型
print(df.describe()) # 快速统计,计算:计数,平均值,标准差,最大/小值,四分位数




# 二、筛选与选择

data = {
    'user_id':[101,102,103,104,105],
    'age':[22,17,25,30,19],
    'gender':['M','F','F','M','F'],
    'city':['Beijing','Shanghai','Beijing','Shenzhen','Shanghai']
} # 用户信息表,4列
df = pd.DataFrame(data)

# 1.列选择
age_series = df['age'] #提取单列,返回一个一维数组Pandas Series
print(type(age_series))

subset_df = df[['user_id','age']] #提取多列,返回一个new DataFrame
print(type(subset_df))

# 2.行筛选/布尔索引
adults = df[df['age']>18] #单条件筛选
filter_df = df[(df['age']>18)&(df['gender']=='F')] #位运算符、括号

# 3.loc和iloc:精准定位
result1 = df.loc[0:2,['user_id','age']] # 取0-2行,且列名为'user_id'和'age'的数据
result2 = df.iloc[0:3,0:2] # 左闭右开

#推荐场景解析:找出"点击了商品A但没购买"的用户行为记录
#(1)找出所有点击了商品A的用户的ID集合
clicked_users = logs_df[(logs_df['action']=='click')&(logs_df['item_id']==1001)]['user_id']

#(2)找出所有购买了商品A的用户ID集合
bought_users = logs_df[(logs_df['action']=='buy')&(logs_df['item_id']==1001)]['user_id']

#(3)在'点击'的用户中剔除'购买'的用户
#.isin()判断元素是否在列表中,~表示取反
target_records = logs_df[
    (logs_df['user_id'].isin(clicked_users))&
    (~logs_df['user_id'].isin(bought_users))
]
print(target_records)



# 三、数据清洗
import numpy as np
import pandas as pd

data = {
    'user_id': [101, 102, 102, 104, 105],       # 注意：102 重复了
    'age': [22, np.nan, 25, np.nan, 19],        # 注意：有缺失值 (NaN)
    'city': ['Beijing', 'Shanghai', 'Shanghai', 'Shenzhen', None] # 注意：有重复行和缺失
}
df = pd.DataFrame(data)

# 1.缺失值处理

#查看缺失情况,返回一个和df形状一样的布尔矩阵,再求和得到每一列缺失值的数量
print(df.isnull().sum()) 
#删除含有缺失值的行
df_dropped = df.dropna()
#填充缺失值(0,均值,中位数)
df_filled_zero = df.fillna(0) #将所有缺失值替换为0

# 2.去重
# df.drop_duplicates(), 常用参数subset(根据某一列去重)
df_no_dups = df.drop.duplicates()
df_unique_users = df.drop.duplicates(subset=['user_id'],keep='first') #保留第一个出现的

# 3.数据类型转换
# df['user_id'].astype(str)  强制改变某一列的数据类型
#推荐场景解析:用户ID为数字,但需要转成str和其他表合并
df['user_id'] = df['user_id'.astype](str)




# 四、分组与聚合
data = {
    'user_id': [101, 102, 101, 102, 101, 103],
    'rating': [5, 4, 3, 5, 4, 2],      # 用户对商品的评分
    'price': [100, 200, 150, 300, 50, 80] # 消费金额
}
df = pd.DataFrame(data)

# 1.基础分组聚合:groupby
# df.groupby('分组依据列名')['要计算的列名'].统计函数()
avg_rating = df.groupby('user_id')['rating'].mean() #按user_id分组,求出每个组打分的均值
print(avg_rating)

# 2.多重聚合:agg
# df.groupby('分组依据列名').agg({列1:['函数1','函数2'],'列2':'函数3'})
user_features = df.groupby('user_id').agg({
    'rating': ['mean', 'count'], 
    'price': 'sum'
}) #获得每组用户评分均值、次数，以及每组的总花费
print(user_features)

# 推荐场景解析:构建用户画像特征
# 借助groupby获得平均评分、评分次数(用户活跃度)、总消费金额(购买力)
# 进阶技巧:修改聚合后的列名

# 聚合后重命名 (将多级索引压平成单级)
final_features = df.groupby('user_id').agg(
    avg_rating=('rating', 'mean'),
    rating_count=('rating', 'count'),
    total_spend=('price', 'sum')
)
print(final_features)
# 输出列名直接变成了 avg_rating, rating_count, total_spend




# 五、合并
left_df = pd.DataFrame({
    'user_id':[101,102,103,104],
    'age':[22,25,30,19]
})
right_df = pd.DataFrame({
    'user_id':[101,102,103,105],
    'click_count':[5,10,2,8]
})

# pd.merge(left,right,on='关联键',how='合并方式')

# on='user_id' 把user_id相同的行拼接到同一行里
#若两表关联键名字不同[left-user_id,right-uid],可以使用left_on='user_id',right_on='uid'

# how='inner'交集,只保留两表中都有的'user_id'
# how='left'左表全保留,右表没有对应数据则填入缺失值
# how='outer'并集,没有对应数据填入缺失值

inner_merge = pd.merge(left_df,right_df,on='user_id',how='inner')

#推荐场景解析:多表格合并(用户特征,物品特征,行为特征)
#合并前后务必检查df.shape,确保行数符合预期




# 六、透视/应用函数/排序排名

data = {
    'user_id': [101, 101, 102, 102, 103],
    'item_id': ['A', 'B', 'A', 'C', 'B'],
    'rating': [5, 3, 4, 2, 5],
    'clicked': [1, 1, 1, 0, 1],
    'bought':  [1, 0, 0, 0, 1]
}
df = pd.DataFrame(data)

# 1.透视:构建交互矩阵
# index行名,columns列名,rating值

# 带聚合功能的透视表(数据中有重复项)
rating_matrix = df.pivot_table(index='user_id',columns='item_id',values='rating') 
# 不存在重复时
rating_matrix_strict = df.pivot(index='user_id', columns='item_id', values='rating') # index和columns禁止重复

# 2.应用函数
#推荐场景解析:生成用户标签
# df.apply(function,axis) 传入一个函数,按行(1)/列(0)应用
df['target_label'] = df.apply(lambda row: 1 if (row['clicked'] == 1 and row['bought'] == 0) else 0, axis=1)

# 3.排序与排名
# 推荐场景解析:生成top-N推荐列表  ~.head(N)
sorted_df = df.sort_values(by='rating',ascending=False) # 排序依据的列名,ascending为排序方式,默认为True(升序)
df['rank'] = df['rating'].rank(ascending=False, method='dense') #根据评分排名,降序,method='dense'表示并列时,后续名次不跳过
