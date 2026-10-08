import numpy as np

# 假设有2个用户对四个物品的评分向量(0 表示未评分)
user_a = np.array([5,3,0,1])
user_b = np.array([4,0,0,2])

# 1.余弦相似度
# cos(A, B) = (A · B) / (||A|| * ||B||)

def cosine_similarity(a,b):
    dot_product = np.dot(a,b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)
    

# 2.杰卡德相似度
# J(A, B) = |A ∩ B| / |A ∪ B|
def jaccard_similarity(a,b):
    # 将评分转为bool集合(大于0表示有交互)
    set_a = set(np.where(a>0)[0])
    set_b = set(np.where(a>0)[0])

    intersection = len(set_a & set_b) #交集大小
    union = len(set_a | set_b)  # 并集大小
    if union == 0:
        return 0.0
    return intersection / union

# 3.皮尔逊相关系数
# pearson(A, B) = cov(A, B) / (std(A) * std(B))
# 等价于:先对向量中心化(减去均值),再计算余弦相似度
def pearson_similarity(a,b):
    # 真实环境下,未评分的0会严重影响pearson和余弦的结果,所以我们只计算共同评分过的物品

    mask = (a != 0) & (b != 0)
    # a!=0生成一个bool数组,最终返回一个bool数组,标记了两人共同评分的位置

    # 若共同评分少于两个,无法计算相关性,返回0
    if np.sum(mask) < 2:
        return 0.0

    # 只取共同评分的部分进行计算
    # 把对应位置为true的元素提取出来,组成一个新数组
    a_common = a[mask]
    b_common = b[mask]

    #中心化
    a_centered = a_common - np.mean(a_common)
    b_centered = b_common - np.mean(b_common)

    return cosine_similarity(a_centered,b_centered)