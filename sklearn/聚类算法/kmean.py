from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 数据读取
data = pd.read_csv('D:/Code/MachingLearning/textbook/TESTDATA.TXT', sep='\t')

# 生成初始聚类数据
x = np.array(data)
# print(x)
# 聚类模型
kmeans_model = KMeans(n_clusters=5, init='random')
# kmeans_model = KMeans(n_clusters=k, init='k-means++')  # 聚类模型
kmeans_model.fit(x)  # 训练聚类模型
# 绘制k-Means聚类结果
colors = ['r', 'g', 'b', 'c', 'y']  # 聚类颜色
markers = ['o', 's', 'D', '+', '*']  # 聚类标志
plt.figure()
# 设置[x,x,y,y]即x坐标轴上的范围和y坐标轴上的取值范围
plt.axis([np.min(x[:, 0]) - 1, np.max(x[:, 0] + 1),
         np.min(x[:, 1]) - 1, np.max(x[:, 1]) + 1])
plt.grid(True)  # 画出网格线
# 得到每个点的簇的数字分类值
print(kmeans_model.labels_)
# 得到不同簇的中心的坐标
print(kmeans_model.cluster_centers_)
# print(kmeans_model.cluster_centers_)
# 画出每个类的每个簇图
for i, l in enumerate(kmeans_model.labels_):
    plt.plot(x[i][0], x[i][1], color=colors[l], marker=markers[l], ls='None')
    plt.title('K = %s' % (5))
# 画出标出数据库的每个簇的中心
for i in range(0, 5):
    plt.plot(kmeans_model.cluster_centers_[i, 0], kmeans_model.cluster_centers_[
             i, 1], color='k', marker='x', ls='None')
plt.show()
