from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

# 数据
x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = np.array([2, 4, 5, 8, 9, 12, 15, 18, 19, 21])
""" numpy中reshape函数的三种常见相关用法

reshape(1,-1)转化成1行：

reshape(2,-1)转换成两行：

reshape(-1,1)转换成1列：

reshape(-1,2)转化成两列
 """
x1 = x.reshape(-1, 1)
y1 = y.reshape(-1, 1)


# 实例化分类器
regressor = LinearRegression()
result = regressor.fit(x1, y1)
print("拟合模型的系数:", result.coef_)
print("拟合模型的截距:", result.intercept_)
print("拟合模型的准确度:", result.score(x1, y1))

# 绘图
plt.scatter(x, y, c='black')
Y = x*result.coef_[0][0]+result.intercept_[0]  # 线性的拟合曲线方程
plt.plot(x, Y)
plt.title("The result Curve:")
plt.show()
