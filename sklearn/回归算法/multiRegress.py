from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

# 随机数据
x = np.array([[-8], [-7], [-7], [-7], [-4], [4], [6], [7]])
y1 = np.array([[81], [72], [62], [70], [24], [15], [41], [60]])
# 绘制数据的散点图
plt.scatter(x, y1, c='black')
# 使用二次多项式
poly = PolynomialFeatures(degree=2)
# 转换得到x的二次多项式特征（fit_transform中的x未转换成一列的话,需要用reshape(-1,1)转换）
x1 = poly.fit_transform(x)

# 使用线性回归,利用特征的二次多项式进行拟合
reg = LinearRegression(normalize=True).fit(x1, y1)
# 绘制拟合的曲线,设置x区域
xx = np.linspace(-10, 10, 200)
# 根据预测的值绘画拟合曲线
plt.plot(xx, reg.predict(poly.fit_transform(xx.reshape(-1, 1))), c='red')
# 线性回归各特征的系数
print(reg.coef_)
# 截距
print(reg.intercept_)
# 分类器准确率
print(reg.score(x1, y1))
# 显示图像
plt.show()
