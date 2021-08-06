from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({'x1':np.random.chisquare(8,1000),'x2':np.random.beta(8,2,1000)*40,'x3':np.random.normal(50,3,1000)})
print(df)
x = MinMaxScaler().fit_transform(df)

y = pd.DataFrame(x)
df.plot.density(sharex=False)
y.plot.density(sharex=False)
plt.show()
