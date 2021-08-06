import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

path_file = "testdata.txt"

recordMat=pd.read_csv(path_file,sep='\t')

k = 4
X = np.array(recordMat)  # 生成初始聚类数据
kmeans_model = KMeans(n_clusters=k, init='random')  # 聚类模型
#kmeans_model = KMeans(n_clusters=k, init='k-means++')  # 聚类模型
kmeans_model.fit(X)  # 训练聚类模型
# 绘制k-Means聚类结果
colors = ['r', 'g', 'b', 'c']  # 聚类颜色
markers = ['o', 's', 'D', '+']  # 聚类标志
plt.figure()
plt.axis([np.min(X[:, 0]) - 1, np.max(X[:, 0] + 1), np.min(X[:, 1]) - 1, np.max(X[:, 1]) + 1])
plt.grid(True)
print(kmeans_model.labels_)
print(kmeans_model.cluster_centers_)
for i, l in enumerate(kmeans_model.labels_):
    plt.plot(X[i][0], X[i][1], color=colors[l],marker=markers[l],ls='None')
    plt.title('K = %s' %(k))
for i in range(0,k):
    plt.plot(kmeans_model.cluster_centers_[i, 0], kmeans_model.cluster_centers_[i, 1], color='k',marker='x',ls='None')
plt.show()