from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv('pima_data.csv',header=None)
array = data.values
X = array[:, 0:8]
Y = array[:, 8]
num_folds = 10
seed = 7
kfold = KFold(n_splits=num_folds,shuffle=False)
model = DecisionTreeClassifier(criterion = 'entropy',splitter='best',max_depth=10)
result = cross_val_score(model, X, Y, cv=kfold)
print(result.mean())