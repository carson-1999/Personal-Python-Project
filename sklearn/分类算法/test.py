import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn import datasets
from sklearn.linear_model import LogisticRegression

def datashow(data,cls,cls_label):
    #生成网格采样点
    x1_min,x1_max = data[:,0].min(),data[:,0].max()
    x2_min,x2_max = data[:,1].min(),data[:,1].max()
    x1,x2 = np.mgrid[x1_min:x1_max:200j,x2_min:x2_max:200j]
    #测试点
    grid_test = np.stack((x1.flat,x2.flat),axis=1)

    #预测分类值
    grid_hat = cls.predict(grid_test)
    grid_hat = grid_hat.reshape(x1.shape)
    cm_light = mpl.colors.ListedColormap(['#FFFFFF','#D3D3D3','#708090'])
    cm_dark = mpl.colors.ListedColormap(['g','b','r'])
    marker = ['o','*','+']
    #根据预测分类值,绘制表现出分类边界
    plt.pcolormesh(x1,x2,grid_hat,cmap=cm_light)
    #绘制样本散点图
    for i in range(data.shape[0]):
        plt.scatter(data[i,0],data[i,1],c='black',s=80,marker=np.array(marker)[y[i]],cmap=cm_dark)

    #坐标轴显示设置
    plt.xlabel(iris_feature[0],fontsize=10)
    plt.ylabel(iris_feature[1],fontsize=10)
    plt.xlim(x1_min,x1_max)
    plt.ylim(x2_min,x2_max)
    plt.title('Iris Classfication by '+cls_label,fontsize=15)
    plt.grid()
    plt.show()

#加载数据集
iris = datasets.load_iris()
iris_feature='sepal length','sepal width','petal length','petal width'
#数据集中分类标签 大小(150,)
y = iris.target
#选用2个特征
x=iris.data[:,[0,2]]

#定义逻辑回归分类预测器
cls = LogisticRegression()
#根据数据集进行训练
cls.fit(x,y)
#预测并绘图显示
datashow(x,cls,'LR')

#给出特征系数,截距
print(cls.coef_,cls.intercept_)