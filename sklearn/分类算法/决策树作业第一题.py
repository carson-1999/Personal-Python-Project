import matplotlib as mpl
import numpy as np
from sklearn import datasets
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier

iris = datasets.load_iris()
y = iris.target
iris_feature = 'sepal length','sepal width','petal lenght','petal width'
x = iris.data[:,[0,2]]
num_folds = 5
seed = 7
kfold = KFold(n_splits=num_folds,shuffle=False)
model = DecisionTreeClassifier(criterion = 'gini',splitter='best',max_depth=None)
result = cross_val_score(model, x, y, cv=kfold)
print(result.mean())