import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
mpl.rcParams['figure.dpi']= 150
sns.set()


bla = pd.read_csv('./snelheden_1.csv')
x1 = np.array(bla['Avg_speed'])
x2 = np.array(bla['Cars_in_lane'])
y = np.arange(len(x1))/3600
fig, ax1 = plt.subplots()
ax1.plot(y, x1, color='b', label='Average speed')
ax1.set_xlabel('time (h)')
ax1.set_ylabel('Average speed (km/h)')
ax1.tick_params('y', colors='b')

ax2 = ax1.twinx()
ax2.plot(y, x2, color='r', label='Intensity')
ax2.set_ylabel('Intensity (cars on road)')
ax2.tick_params('y', colors='r')
plt.show()
