from sklearn.datasets import make_moons
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans,AgglomerativeClustering,DBSCAN

#生成半月型分布数据
X,y = make_moons(n_samples = 200,noise=0.05,random_state=2)
plt.scatter(X[:,0],X[:,1])
plt.show()
f,(ax1,ax2,ax3) = plt.subplots(3,1,figsize=(3,8),sharex=True)
#定义K均值聚类,分成2个聚类
model_km = KMeans(n_clusters=2,random_state=0)
y_kmeans = model_km.fit_predict(X) #训练并划分样本点
print(X[y_kmeans])

#绘制散点图
ax1.scatter(X[y_kmeans == 0,0],X[y_kmeans == 0,1],c='lightblue',marker='o',s=10,label='cluster1')
ax1.scatter(X[y_kmeans == 1,0],X[y_kmeans == 1,1],c='black',marker='s',s=10,label='cluster2')
ax1.set_title("K-means clustering")

#定义聚集层次聚类,分成2类
model_agg = AgglomerativeClustering(n_clusters=2,affinity='euclidean',linkage='ward')
y_agg = model_agg.fit_predict(X)
#绘制散点图
ax2.scatter(X[y_agg == 0,0],X[y_agg == 0,1],c='lightblue',marker='o',s=10,label='cluster1')
ax2.scatter(X[y_agg == 1,0],X[y_agg == 1,1],c='black',marker='s',s=10,label='cluster2')
ax2.set_title("Agglomerative clustering")

#定义DBSCAN聚类,分成两个聚类
model_db = DBSCAN(eps=0.2,min_samples=5,metric='euclidean')
y_dbscan = model_db.fit_predict(X)
#绘制散点图
ax3.scatter(X[y_dbscan == 0,0],X[y_dbscan == 0,1],c='lightblue',marker='o',s=10,label='cluster1')
ax3.scatter(X[y_dbscan == 1,0],X[y_dbscan == 1,1],c='black',marker='s',s=10,label='cluster2')
ax3.set_title("DBSCAN clustering")

plt.legend()
plt.show()