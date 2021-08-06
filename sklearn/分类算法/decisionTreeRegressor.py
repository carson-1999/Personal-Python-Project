import numpy as np
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt

rng = np.random.RandomState(1) #随机种子
X = np.sort(5*rng.rand(80,1),axis=0)
y = np.sin(X).ravel() #ravel 散开,降维由(80,1)变为(80,),
#增加数据噪声
y[::5] = y[::5] + 3*(0.5-rng.rand(16))

#模型导入和数据拟合
Model1 = DecisionTreeRegressor(max_depth=2)
Model2 = DecisionTreeRegressor(max_depth=5)
Model1.fit(X,y)
Model2.fit(X,y)

#由于导入的数据需要为2维数据,需要对输入数据进行增维切片
x_test = np.arange(0.0,5.0,0.01)[:,np.newaxis]
y_1 = Model1.predict(x_test)
y_2 = Model2.predict(x_test)

#画图
plt.figure()
plt.scatter(X,y,s=20,edgecolor='black',c='darkorange',label='data')
plt.plot(x_test,y_1,color='red',label="max_depth=2",linewidth=2)
plt.plot(x_test,y_2,color='blue',label='max_depth=5',linewidth=2)
plt.xlabel('data')
plt.ylabel('target')
plt.title('The DecisionTree Regression')
plt.legend()
plt.show()