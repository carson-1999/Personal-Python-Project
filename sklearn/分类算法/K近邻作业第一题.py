import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from sklearn import datasets
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier

iris = datasets.load_iris()
y = iris.target
iris_feature = 'sepal length','sepal width','petal lenght','petal width'
x = iris.data[:,[0,2]]
num_folds = 5
seed = 7
kfold = KFold(n_splits=num_folds,shuffle=False)
cls = KNeighborsClassifier(n_neighbors = 4)
result = cross_val_score(cls, x, y, cv=kfold)
print(result.mean())