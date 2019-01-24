import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

bla = pd.read_csv('posities.csv')
x = np.array(bla['x'])*0.5/1000
y = np.array(bla['y'])
plt.figure(figsize=(30, 5))
plt.scatter(x, y)
plt.show()
