from sklearn.tree import DecisionTreeClassifier
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

data = pd.read_csv(r'D:\\Code\\MachingLearning\\textbook\\train.csv')
#查看数据
#print(data.head(10))

"""数据预处理阶段"""
#筛选特征
data.drop(['Cabin','Name','Ticket'],inplace=True,axis=1)
#print(data.info())

#缺失值处理,填补
data['Age'] = data['Age'].fillna(data['Age'].mean())
data = data.dropna()#默认是axis=0对有缺失值的行进行操作
#print(data.info())

#数据文字字符串替换,数字化
embarked = data['Embarked'].unique().tolist() #unique()返回去重复值后的有哪些取值的数组
data['Embarked'] = data['Embarked'].apply(lambda x:embarked.index(x)) #apply函数用索引替换字符串
   #姓名字符串转换为数字,(只有两种取值转换的)小技巧,判断布尔值再转为int类型,即数字
data.loc[:,'Sex'] = (data['Sex']=='male').astype('int') 
#或data['Sex'] = (data['Sex']=='male').astype('int')

#对数据 进行特征与标签分离的操作,标签是Survived列
   #data.columns返回数据所有的列名
x = data.iloc[:,data.columns != 'Survived'] #iloc，取出判断是True的
   #同理,取出Survived标签,利用iloc将判断True的都取出来
y = data.iloc[:,data.columns == 'Survived']

#训练集和测试集的划分,纠正数据项索引处理
Xtrain,Xtest,Ytrain,Ytest = train_test_split(x,y,test_size=0.3)
#由于是随机划分的,返回的数据的索引是混乱的,最好将索引恢复成有顺序,即对四个数据纠正索引
for i in [Xtrain,Xtest,Ytrain,Ytest]:
    i.index = range(i.shape[0])

"""模型创建和训练阶段"""
clf = DecisionTreeClassifier(random_state=20)
clf.fit(Xtrain,Ytrain)
# score = clf.score(Xtest,Ytest)
#进行交叉验证尝试
score = cross_val_score(clf,x,y,cv=10).mean()

#网格搜素:能够帮助同时调整多个参数的技术,枚举技术
  #一串参数和这些参数对应的值,即希望网格搜索的取值范围
parameters = {
    "criterion":("gini","entropy")
    ,"splitter":("best",'random')
    ,"max_depth":[*range(1,10)] #加*表示取range里面的值并形成列表
    ,"min_samples_leaf":[*range(1,25,5)]
    ,"min_impurity_decrease":[*np.linspace(0,0.5,25)]
}
#网格搜索结合了fit,score,cross_valscore等功能
GS = GridSearchCV(clf,parameters,cv=10) 
GS.fit(Xtrain,Ytrain)
#网格搜索的两个重要属性
#GS.best_params_  这个是从我们输入的参数和取值的列表中,返回最佳组合
#GS.best_score_   这个是网格搜索后模型的评判标准


