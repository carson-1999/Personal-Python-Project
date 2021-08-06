from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from pandas import read_csv
# K近邻分类器
from sklearn.neighbors import KNeighborsClassifier

data = read_csv('pima_data.csv')
X = data.iloc[1:, 0:8]  # 样本数据特征
y = data.iloc[1:, 8]  # 样本所属分类


# 循环寻找最好的K,即35
""" for i in range(2, 60):
    # K近邻算法
    model = KNeighborsClassifier(
        n_neighbors=i, weights="distance", metric="minkowski", p=2, algorithm="auto")
    # 进行5折处理
    kfold = KFold(n_splits=5, shuffle=True, random_state=0)
    # 结合K近邻分类器获取K折交叉验证结果
    result = cross_val_score(model, X, y, cv=kfold)
    print("当K="+str(i)+"时,5折交叉验证的平均准确率:", result.mean()) """

# 循环寻找最好的折数,即5
""" for i in range(2, 60):
    # K近邻算法
    model = KNeighborsClassifier(
        n_neighbors=35, weights="distance", metric="minkowski", p=2, algorithm="auto")
    # 进行5折处理
    kfold = KFold(n_splits=i, shuffle=True, random_state=0)
    # 结合K近邻分类器获取K折交叉验证结果
    result = cross_val_score(model, X, y, cv=kfold)
    print(str(i)+"折交叉验证的平均准确率:", result.mean()) """

# K近邻算法
model = KNeighborsClassifier(
    n_neighbors=35, weights="distance", metric="minkowski", p=2, algorithm="auto")
# 进行5折处理
kfold = KFold(n_splits=5, shuffle=True, random_state=0)
# 结合K近邻分类器获取K折交叉验证结果
result = cross_val_score(model, X, y, cv=kfold)
print("在pima数据集中,当K=35时,5折交叉验证的平均准确率最高,为:", result.mean())
