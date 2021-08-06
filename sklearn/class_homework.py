from sklearn.datasets import load_iris  # 数据集
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score  # 进行k折交叉验证
from sklearn.tree import DecisionTreeClassifier  # 决策树分类器
# 集成算法中的装袋算法，利用BaggingClassifier类实现
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import AdaBoostClassifier  # 集成算法中的提升算法

# 导入数据集
iris = load_iris()
data = iris.data
target = iris.target

# 进行k折处理(5折交叉验证)
kfold = KFold(n_splits=5, shuffle=True, random_state=0)
# 运用决策树算法
""" dtc = DecisionTreeClassifier(
    criterion='entropy', splitter='best') """
dtc = DecisionTreeClassifier()
result = cross_val_score(dtc, data, target, cv=kfold)
print("决策树算法的平均准确率:", result.mean())

# Bagging集成算法
""" model = BaggingClassifier(base_estimator=dtc, n_estimators=100, random_state=0) """
model = BaggingClassifier(n_estimators=100, random_state=0)
result = cross_val_score(model, data, target, cv=kfold)
print("集成算法Bagging的平均准确率:", result.mean())

# AdaBoost集成算法
model = AdaBoostClassifier(n_estimators=30, random_state=0)
result = cross_val_score(model, data, target, cv=kfold)
print("集成算法AdaBoost的平均准确率:", result.mean())
