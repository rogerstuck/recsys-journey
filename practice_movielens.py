import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns


# 设置字体为 SimHei（黑体），解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei'] 
# 解决负号 '-' 显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False 

# 1.获取数据,检查一下数据有没有问题
ratings = pd.read_csv('ml-latest-small/ratings.csv')
movies = pd.read_csv('ml-latest-small/movies.csv')
print(ratings.head(10))
ratings.info()

# 2.评分分布分析
rating_counts = ratings['rating'].value_counts()
print("各分数出现次数:")
print(rating_counts.sort_index())

sns.countplot(data=ratings,x='rating',palette='viridis')
plt.title('评分分布分析',fontsize=14)
plt.xlabel('分数',fontsize=12)
plt.ylabel('数量',fontsize=12)
plt.show()

# 3.电影维度分析

# (1)最热门的top10电影
movie_Id = ratings['movieId'].value_counts()
print(movie_Id) # 获取评分次数最多的10部电影的ID
movies_merge = pd.merge(movies,movie_Id,on='movieId',how='inner')
print(movies_merge.columns)

top_10_movies = movies_merge.sort_values(by='count',ascending=False).head(10)

sns.barplot(
    data = top_10_movies,
    x='count',
    y='title',
    palette='viridis'
)

plt.title('评分最多的10部电影',fontsize=14)
plt.xlabel('评分次数',fontsize=12)
plt.ylabel('电影名称',fontsize=12)
plt.tight_layout()
plt.show()

# (2)电影类型分布
movies_genres = movies['genres'].str.split('|', expand=True).stack().value_counts()
print(movies_genres)

genres_top10 = movies_genres.head(10)
genres_top10.plot(kind='barh',color='coral')

plt.title('电影类型分布top10',fontsize=14)
plt.xlabel('电影数量',fontsize=12)
plt.ylabel('类型',fontsize=12)

plt.gca().invert_yaxis() #让数量最多的排最上面
plt.tight_layout()
plt.show()


# 4.用户维度分析

# (1)活跃度
users_activity = ratings['userId'].value_counts()
print(users_activity.head(10))
users_activity.info()

sns.histplot(users_activity,bins=50)

plt.title('用户活跃度分布',fontsize=14)
plt.xlabel('打分次数',fontsize=12)
plt.ylabel('用户数',fontsize=12)
plt.show()

# (2)平均分
ratings_avg = ratings.groupby('userId')['rating'].mean() # 每个用户打分的平均分
print(ratings_avg.head(10))

sns.histplot(ratings_avg,bins=50)

plt.title('用户打分情况',fontsize=14)
plt.xlabel('均分',fontsize=12)
plt.ylabel('用户数',fontsize=12)
plt.show()


# 5.进阶分析

# e.g.筛选高质量电影

#思考:电影1有51人打分均分4.9,电影2有5000人打分均分4.8,直接比较平均值不严谨,我们采用贝叶斯平均分
C = ratings['rating'].mean()
m = 50

def weighted_rating(x,m=m,C=C):
    v = x['rating_count']
    R = x['avg_rating']
    return (v/(v+m))*R+(m/(v+m))*C

movie_stats = ratings.groupby('movieId').agg(
    avg_rating=('rating','mean'),
    rating_count = ('rating','count')
).reset_index()

popular_movies = movie_stats[movie_stats['rating_count']>50]
filter_movie = popular_movies.copy()
filter_movie['weighted_score'] = filter_movie.apply(weighted_rating,axis=1)

top_weighted = filter_movie.sort_values(by='weighted_score',ascending=False).head(20)
top_weighted = top_weighted.merge(movies[['movieId', 'title']], on='movieId')

plt.figure(figsize=(10, 8))
plt.barh(top_weighted['title'], top_weighted['weighted_score'], color='orange')
plt.xlabel('加权评分')
plt.title('高质量电影 Top 20(贝叶斯加权)')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()