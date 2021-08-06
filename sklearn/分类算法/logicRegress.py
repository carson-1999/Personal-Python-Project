from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

"""利用数据集的前3个特征,使用逻辑回归模型进行分类预测,输出结果的准确率,截距和各特征系数"""

# 数据集
data = pd.read_csv('D:/Code/MachingLearning/textbook/iris.csv')
# 提取数据集的前3个特征和标签
x = data.iloc[:, 1:4]
y = data.iloc[:, 5]

# 进行K折处理并训练模型
""" kfold = KFold(n_splits=6, random_state=0) """
model = LogisticRegression()
""" result = cross_val_score(model, x, y, cv=kfold) """
result = model.fit(x, y)
print("模型的准确率", result.score(x, y))
print("模型的截距", result.intercept_)
print("参与训练的三个特征的系数", result.coef_)
