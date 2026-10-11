# 1.模拟数据生成(用户id,物品id,时间戳)
import pandas as pd
import numpy as np

np.random.seed(42) #随机种子

# 设置模拟的用户数,物品数,交互记录数
num_users = 100
num_items = 50
num_records = 2000

data = {
    'user_id': np.random.randint(1,num_users+1,num_records),
    'item_id': np.random.randint(1,num_items+1,num_records),
    # 生成过去三十天的随机时间戳
    'timestamp': np.random.randint(1700000000,1700000000+30*24*3600,num_records)
}

df = pd.DataFrame(data)

# 去重:同一用户对同一个物品在短时间内可能点击多次,简化为只保留一次交互
df = df.drop_duplicates(subset=['user_id','item_id'])

# 按时间排序
df = df.sort_values(by='timestamp').reset_index(drop=True)

print("模拟原始数据示例:")
print(df.head())
print(f"总交互记录数:{len(df)}")


# 2.基于时间戳划分train/test
def time_based_split(df,test_ratio=0.2): # test_ratio:test/all
    # 找到分割点的时间戳
    split_index = int(len(df)*(1-test_ratio))
    split_time = df.iloc[split_index]['timestamp']

    train_df = df[df['timestamp']<split_time].copy() # 训练集:时间早于分割点
    test_df = df[df['timestamp']>=split_time].copy() # 测试集:时间晚于分割点

    return train_df,test_df

train_df,test_df = time_based_split(df,test_ratio=0.2)

print(f"\n训练集大小: {len(train_df)} (时间范围: {train_df['timestamp'].min()} ~ {train_df['timestamp'].max()})")
print(f"测试集大小: {len(test_df)} (时间范围: {test_df['timestamp'].min()} ~ {test_df['timestamp'].max()})")

# 3.生成推荐列表(模拟模型预测)
# 基线模型:热门推荐
def get_top_k_popular(train_df,k=10):

    item_counts = train_df['item_id'].value_counts() # 统计每个物品的交互次数
    top_k_items = item_counts.head(k).index.tolist() # 取出前k个物品的id

    return top_k_items

# 获取热门top10物品
top_k_items = get_top_k_popular(train_df,k=10)
print(f"\n推荐系统给所有用户推荐的 Top-10 物品: {top_k_items}")

# 4.计算精准率(Precision@K)和召回率(Recall@K)
# 精准率:推荐的物品中用户喜欢的数量/推荐总数
# 召回率:推荐物品中用户喜欢的数量/用户实际喜欢的所有物品数量
"""
二者此消彼长:
有时过度追求高精准率,导致漏掉用户喜欢的,造成召回率低
过度追求高召回率,推送了大量物品,但是精准率大幅下降
"""
def evaluate_precision_recall(test_df,top_k_items,k=10):
    # 按用户分组,获取每个用户在测试集中真实交互的物品集合
    user_true_items = test_df.groupby('user_id')['item_id'].apply(set).to_dict()

    precisions = []
    recalls = []

    # 遍历测试集中的每一个用户
    for user_id,true_items in user_true_items.items():
        # 推荐列表就是top-k热门(此处简化为所有用户推荐一样的)
        rec_items = set(top_k_items)

        # 计算命中数:推荐列表与真实交互的交集
        hits = len(rec_items.intersection(true_items))

        # 计算precision 和 recall
        precision = hits / k
        recall = hits / len(true_items)
        
        precisions.append(precision)
        recalls.append(recall)

    # 返回所有用户的平均指标
    avg_precision = np.mean(precisions)
    avg_recall = np.mean(recalls)

    return avg_precision,avg_recall

# 执行评估
avg_p, avg_r = evaluate_precision_recall(test_df, top_k_items, k=10)

print("\n========== 离线评估结果 ==========")
print(f"平均 Precision@10: {avg_p:.4f}  (推荐的东西有多大比例是用户真正喜欢的)")
print(f"平均 Recall@10:    {avg_r:.4f}  (用户真正喜欢的东西有多大比例被推出来了)")
