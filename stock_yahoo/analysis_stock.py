import pandas as pd
from datetime import date
import numpy as np

dow_df = pd.read_csv('./stock_yahoo.csv')
dow_df.index = range(1, len(dow_df) + 1)

axp_df = pd.read_csv('./axp_stock.csv')
axp_df.index = range(1, len(axp_df) + 1)

mindex = []

for item in axp_df['date']:
    day = date.fromtimestamp(item)
    day = date.strftime(day, '%Y-%m-%d')
    mindex.append(day)

axp_df.index = mindex

# 删除某一列
axp_df_new = axp_df.drop(['date'], axis=1)

status = np.sign(np.diff(axp_df.close))

# 请采用倒序观看, tushare 国内金融数据平台
# 1    letv.shape
# 3    letv = ts.get_hist_data('300104', start='2017-06-06', end='2018-02-05')
# 4    type(letv)
# 5    type(letv, start='2017-06-06', end='2018-02-05')
# 6    letv.info()
# 7    letv = ts.get_hist_data('300104')
# 8    ts.get_hist_data('300104')
# 9    import tushare as ts

# pandas的dataframe连接
# 11   pd.concat([p,q], ignore_index = True)
# 12   pd.concat([p,q])
# 13   q = axp_df[:3]
# 14   p = tm_axp_df[:3]
# 15   tm_axp_df.head(1)
# 16   tm_axp_df
# 17   q.append(o)
# 18   o
# 19   o = p[:2]
# 20   p
# 21   q.append(p)
# 22   q
# 23   q = axp_df[(axp_df.index > '2017-08-10') & (axp_df.index < '2017-08-20')]
# 24   q = axp_df[axp_df.index > '2017-08-10' & axp_df.index < '2017-08-20']
# 25   q = axp_df[:2]
# 26   p[:2]
# 27   p = axp_df[::-1]
# 28   p = axp_df[:2]
# 29   p = axp_df[-1]
# 30   p = axp_df[-1:-3]
# 31   axp_df

# groupby 分组，先提取要计算的单元，然后分组，然后计算
# 32   tm_axp_df.groupby('mon').volume.sum()
# 33   tm_axp_df.groupby('mon').volume
# 34   help(pd.DataFrame.sum)
# 35   help(pd.DataFrame.sum())
# 36   tm_axp_df.groupby('mon').sum().volume
# 37   tm_axp_df.groupby('mon').sum()
# 38   tm_axp_df.groupby('mon').count().ix[:, 1]
# 39   type(tm_axp_df.groupby('mon').count())
# 40   tm_axp_df.groupby('mon').count().__type__
# 41   tm_axp_df.groupby('mon').count()
# 42   tm_axp_df.groupby('mon').groups
# 43   tm_axp_df.groupby('mon')
# 44   dir(tm_axp_df.groupby('mon'))
# 45   help(time)
# 46   tm_axp_df.mon.value_counts()
# 47   tm_axp_df.mon.count()
# 48   tm_axp_df['mon'] = mons
# 49   tm_axp_df = axp_df.copy(True)

# 这个 time.strptime 可以对字符串形式的时间格式化为对象类型，翻遍聚类时候直接通过选择比较
# 52   a.tm_mon
# 53   a.month
# 54   a = time.strptime(axp_df.index[0], '%Y-%m-%d')
# 55   time.strptime(axp_df.index[0], '%Y-%m-%d')
# 56   time.strptime(axp_df.index[0])
# 57   import time

# 筛选，pandas dataframe会根据传入的Boolean 进行选择数据，True 选择，False丢弃。
# 58   axp_df.index
# 59   len(axp_df[(axp_df.index >= '2018-01-01') & (axp_df.index < '2018-02-01')])
# 60   axp_df[(axp_df.index >= '2018-01-01') & (axp_df.index < '2018-02-01')]
# 61   axp_df[(axp_df.index >= '2018-0101') & (axp_df.index < '2018-02-01')]
# 62   axp_df[axp_df.index >= '2018-0101' & axp_df.index < '2018-02-01']
# 63   help(pd.DataFrame.sort_index)
# 64   dir(pd.DataFrame)
# 65   help(pd.DataFrame.sort_values)
# 66   type(dow_df.sort_values(by='price', ascending=False)[:3])

# 排序，根据某列的值进行排序，可选择升序降序。
# 67   dow_df.sort_values(by='price', ascending=False)[:3].company
# 68   dow_df.sort_values(by='price', ascending=False)[:3]
# 69   dow_df.sort_values(by='price', ascending=False)

# np.where 可返回Boolean dataframe
# 70   np.where(status == -1).__len()__
# 71   np.where(status == -1).size
# 72   np.where(status == -1)
# 73   status[np.where(status == -1)].size
# 74   status[np.where(status == 1)].size
# 75   status[np.where(status == 1)]
# 76   status
# np.diff 比较某对象的前一个数据与当前数据的差值，np.sign 即根据元素大小，得出1，-1,0.
# 77   status = np.sign(np.diff(axp_df.close))


# 聚类
# 1. basic version
from scipy.cluster.vq import kmeans, vq, whiten

# 成绩表，语文，数学，python，英文
list1 = [88, 74, 96, 85]
list2 = [92, 99, 95, 94]
list3 = [91, 87, 99, 95]
list4 = [78, 99, 97, 81]
list5 = [88, 78, 98, 84]
list6 = [100, 95, 100, 92] # 这是学霸，典型的。

data = np.array([list1, list2, list3, list4, list5, list6])
# 归一化
data = whiten(data)
centroids, _ = kmeans(data, 2)
result, _ = vq(data, centroids)
# result is array([0, 1, 1, 0, 0, 1])
# 说明啊，1, 2, 5 是一类，都是学霸，聚类到一起了。能否把这个画出来？多维度了？

# 2. pro version using sklearn

from sklearn.cluster import KMeans


X = np.array([list1, list2, list3, list4, list5, list6])
# X
# Out[301]:
# array([[ 88,  74,  96,  85],
#        [ 92,  99,  95,  94],
#        [ 91,  87,  99,  95],
#        [ 78,  99,  97,  81],
#        [ 88,  78,  98,  84],
#        [100,  95, 100,  92]])
k_result = KMeans(n_clusters=2).fit(X)
# k_result
# Out[303]:
# KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300,
#     n_clusters=2, n_init=10, n_jobs=1, precompute_distances='auto',
#     random_state=None, tol=0.0001, verbose=0)
pred = k_result.predict(X)
# pred
# Out[305]: array([0, 1, 1, 1, 0, 1])

KMeans(n_clusters=2).fit_predict(X)
# Out[306]: array([1, 0, 0, 0, 1, 0])

# 从以上操作可以看出，其实fit(), predict, 是可以合成一个fix_predict
# sklearn的几乎所有机器学习算法都是采用的这样的模式，先fit 然后再predict


# matplotlib

import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4, 5])
plt.title('some numbers')
plt.show()

plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro')
plt.axis([0, 6, 0, 20])
plt.show()

# 绘图
aapl_df = pd.read_csv('./AAPL_stock.csv')
aapl_df.head()

for item in aapl_df.date:
    day = date.fromtimestamp(item)
    day = date.strftime(day, '%Y-%m-%d')
    mindex.append(day)



