import pandas as pd
import warnings

import matplotlib.pyplot as plt
import numpy as np
import re
#机器学习算法库
from sklearn.ensemble import RandomForestClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV,cross_val_score,StratifiedKFold
from sklearn.metrics import confusion_matrix

#忽略警告
warnings.filterwarnings("ignore")

#导入csv训练数据和测试数据
train = pd.read_csv('D:\\Code\\MachingLearning\\textbook\\train.csv')
test = pd.read_csv('D:\\Code\\MachingLearning\\textbook\\test.csv')

#数据可视化
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
#fig = plt.figure()
#fig.set(alpha=0.2)

train["HasCabin"] = (train["Cabin"].notnull().astype('int'))
"""训练集数据预处理"""
#处理缺失值
train["Embarked"] = train["Embarked"].fillna('S')
train = train.drop(['Cabin'],axis=1)
train = train.drop(['Ticket'],axis=1)
train['Title'] = train['Name'].apply(lambda x:re.search('\w+\.',x).group()).str.replace('.','')
train['Title'] = train['Title'].replace(['Countess','Lady','Sir','Capt','Col','Don','Dr','Major','Rev','Jonkheer','Dona'],'Rare')
train['Title'] = train['Title'].replace(['Mlle','Ms'],'Miss')
train['Title'] = train['Title'].replace('Mme','Mrs')

#将title值转换为数字
title_mapping = {"Mr":1,"Miss":2,"Mrs":3,"Master":4,"Rare":5}
train['Title'] = train['Title'].map(title_mapping)
#每个title对应的年龄中位数
age_title_median = train.groupby('Title')['Age'].median()
#当前表设置title为索引
train.reset_index(inplace=True)
#当前表填充缺失值
train.Age.fillna(age_title_median,inplace=True)
#重置索引
train.reset_index(inplace=True)
bins = [0,5,12,18,24,35,60,np.inf]
labels = [1,2,3,4,5,6,7]
train['AgeGroup'] = pd.cut(train['Age'],bins,labels=labels)

#数值离散化
train['FareBand'] = pd.qcut(train['Fare'],4,labels=[1,2,3,4])
#将性别文本转换为整数值
sex_mapping = {"male":0,"female":1}
train['Sex'] = train['Sex'].map(sex_mapping)
#将登船港口文本转换为整型值
embarked_mapping = {"S":1,"C":2,"Q":3}
train["Embarked"] = train["Embarked"].map(embarked_mapping)

#特征选择,删除掉不需要用到的特征
train = train.drop(['Age'],axis=1)
train = train.drop(['Name'],axis=1)

"""对于测试集也做同样的数据预处理"""
test["Embarked"] = test["Embarked"].fillna('S')
test['HasCabin'] = (test['Cabin'].notnull().astype('int'))
test = test.drop(['Cabin'],axis=1)
test = test.drop(['Ticket'],axis=1)

test['Title'] = test['Name'].apply(lambda x:re.search('\w+\.',x).group()).str.replace('.','')
test['Title'] = test['Title'].replace(['Countess','Lady','Sir','Capt','Col','Don','Dr','Major','Rev','Jonkheer','Dona'],'Rare')
test['Title'] = test['Title'].replace(['Mlle','Ms'],'Miss')
test['Title'] = test['Title'].replace('Mme','Mrs')

test['Title'] = test['Title'].map(title_mapping)
#在当前表设置title为索引
test.reset_index(inplace=True)
#在当前表填充缺失值
test.Age.fillna(age_title_median,inplace=True)
#重置索引
test.reset_index(inplace=True)
bins = [0,5,12,18,24,35,60,np.inf]
labels = [1,2,3,4,5,6,7]
test['AgeGroup'] = pd.cut(test['Age'],bins,labels=labels)

test=test.drop(['Age'],axis=1)
test=test.drop(['Name'],axis=1)
test['Sex'] = test['Sex'].map(sex_mapping)
test['Embarked'] = test['Embarked'].map(embarked_mapping)

#填充测试集中的Fare缺失值,用同等级的均值来填充
for x in range(len(test['Fare'])):
    if pd.isnull(test['Fare'][x]):
        pclass = test['Pclass'][x]
        test['Fare'][x] = round(train[train['Pclass']==pclass]['Fare'].mean(),4)

#将测试集中的Fare离散化处理,并删除训练集和测试集中的'Fare'字段
test['FareBand'] = pd.qcut(test['Fare'],4,labels=[1,2,3,4])
test = test.drop(['Fare'],axis=1)
train = train.drop(['Fare'],axis=1)

"""模型构建和训练"""
predictors = train.drop(['Survived','PassengerId'],axis=1)
target = train['Survived']

#定义10折交叉验证,进行模型评估。设置kfold,交叉采样法拆分数据集
kfold = StratifiedKFold(n_splits=10)

#汇总不同模型算法
classifiers = []
classifiers.append(SVC(gamma='auto'))
classifiers.append(DecisionTreeClassifier())
classifiers.append(RandomForestClassifier())
classifiers.append(GaussianNB())
classifiers.append(KNeighborsClassifier())
classifiers.append(LogisticRegression())
classifiers.append(LinearDiscriminantAnalysis())
#不同机器学习交叉验证结果汇总
cv_results = []
for classifier in classifiers:
    cv_results.append(cross_val_score(classifier,predictors,target,scoring='accuracy',cv=kfold,n_jobs=-1))

#对比模型的性能
#求出模型得分的均值和标准差
cv_means = []
cv_std = []
for cv_result in cv_results:
    cv_means.append(cv_result.mean())
    cv_std.append(cv_result.std())

#汇总数据
cvResDf = pd.DataFrame({"cv_mean":cv_means,"cv_std":cv_std,'algorithm':['SVC','DecisionTreeCla','RandomForestCla','GaussianNBCla','KNN','LR','LinearDiscrimiAna']})
#print(cvResDf)

"""算法调优"""
#KNN模型
modelgsKNN = KNeighborsClassifier()
knn_param_grid = {"n_neighbors":[3,5,7,9],'weights':['uniform','distance']}
modelgsKNN = GridSearchCV(modelgsKNN,param_grid=knn_param_grid,cv=kfold,scoring='accuracy',n_jobs=-1,verbose=1)
modelgsKNN.fit(predictors,target)
#SVC模型
modelSVC = SVC(gamma='auto')
SVC_param_grid={'C':[0.5,1.5,10],'kernel':['poly','rbf']}
modelgsSVC=GridSearchCV(modelSVC,param_grid=SVC_param_grid,cv=kfold,scoring='accuracy',n_jobs=-1,verbose=1)
modelgsSVC.fit(predictors,target)
#模型得分
print("modelgsKNN模型得分为: %.3f"%modelgsKNN.best_score_)
print("modelgsSVC模型得分为: %.3f"%modelgsSVC.best_score_)
modelgsKNNtestpre_y = modelgsKNN.predict(predictors).astype(int) #测试数据模型的预测值
modelgsSVCtestpre_y = modelgsSVC.predict(predictors).astype(int)
print("KNN模型的混淆矩阵为:\n",confusion_matrix(target.astype(int).astype(str),modelgsKNNtestpre_y.astype(str)))
print("SVC模型的混淆矩阵为:\n",confusion_matrix(target.astype(int).astype(str),modelgsSVCtestpre_y.astype(str)))


"""分类结果"""
ids = test['PassengerId']
predictions = modelgsKNN.predict(test.drop('PassengerId',axis=1))
#将输出转换为dataframe并保持为csv文件
output = pd.DataFrame({'PassengerId':ids,'Survived':predictions})
output.to_csv('submission_KNN.csv',index=False)