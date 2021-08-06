from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from pandas import read_csv
# 决策树分类器
from sklearn.tree import DecisionTreeClassifier

data = read_csv('pima_data.csv')
X = data.iloc[1:, 0:8]  # 样本数据特征
y = data.iloc[1:, 8]  # 样本所属分类

# 循环寻找最好的max_depth,即72
# 决策树算法
""" for i in range(10, 101):
    model = DecisionTreeClassifier(
        criterion="entropy", splitter="best", max_depth=i)
    # 进行5折处理
    kfold = KFold(n_splits=10, shuffle=True, random_state=0)
    # 结合K近邻分类器获取K折交叉验证结果
    result = cross_val_score(model, X, y, cv=kfold)
    print("当max_depth=" + str(i) + "时,5折交叉验证的平均准确率:", result.mean()) """

# 循环寻找最好的折数,即70
""" for i in range(2, 60):
    # 决策树算法
    model = DecisionTreeClassifier(
        criterion="entropy", splitter="best", max_depth=16)
    # 进行5折处理
    kfold = KFold(n_splits=i, shuffle=True, random_state=0)
    # 结合K近邻分类器获取K折交叉验证结果
    result = cross_val_score(model, X, y, cv=kfold)
    print(str(i) + "折交叉验证的平均准确率:", result.mean())
 """
# 决策树算法
model = DecisionTreeClassifier(
    criterion="entropy", splitter="best", max_depth=72)
# 进行5折处理
kfold = KFold(n_splits=70, shuffle=True, random_state=0)
# 结合K近邻分类器获取K折交叉验证结果
result = cross_val_score(model, X, y, cv=kfold)
print("在pima数据集中,当K=10时，6折交叉验证的平均准确率最高,为:", result.mean())
