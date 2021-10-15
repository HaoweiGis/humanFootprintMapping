import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import pandas as pd
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
import matplotlib as mpl

from matplotlib.pyplot import MultipleLocator

# ​Generate fake data
df= pd.read_csv(r'datasets\pointdensity.csv')
x = np.array(df.iloc[:,0])
y = np.array(df.iloc[:,1])

xy = np.vstack([x,y])

z = gaussian_kde(xy)(xy)

fig, ax = plt.subplots()

csfont = {'family':'Times New Roman'}
plt.rc('font', family = 'Times New Roman')

# clist=['#1C9479','#99D98C','#D5EB92','#FFC976','#F79C65','#F26055']
clist=['#1C9479','#FFFFFF','#F26055']
newcmp = LinearSegmentedColormap.from_list('chaos',clist,256)
ax.scatter(x,y,c=z,s=50, edgecolor=['none'], cmap= newcmp, lw=0,alpha=0.5) #,clip_on=False
labels = ax.get_xticklabels() + ax.get_yticklabels()
[label.set_fontname('Times New Roman') for label in labels]

ax.set_aspect('equal', adjustable='box')  # 等轴的正方形输出

ax.spines['bottom'].set_linewidth(2);###设置底部坐标轴的粗细
ax.spines['left'].set_linewidth(2);####设置左边坐标轴的粗细
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)

z = np.polyfit(x, y, 1)
p = np.poly1d(z)
ax.plot((0, 1), (0, 1), transform=ax.transAxes, ls='--',c='#5E6063', label="1:1 line",linewidth=2)
plt.plot(x,p(x), color='#F25D54',linewidth=4,linestyle='--')

# plt.xlabel('Distance to ecological network',size = 15)
# plt.ylabel('Human footprint',size = 15)
y_major_locator=MultipleLocator(0.2)
ax.yaxis.set_major_locator(y_major_locator)
x_major_locator=MultipleLocator(0.2)  
ax.xaxis.set_major_locator(x_major_locator)

plt.xlim(0,1)
plt.ylim(0,1)

plt.yticks([0, 0.2, 0.4, 0.6, 0.8,1],
          ['0', '0.2', '0.4', '0.6', '0.8','1'])
plt.xticks([0, 0.2, 0.4, 0.6, 0.8,1],
          ['0', '0.2', '0.4', '0.6', '0.8','1'])

plt.tick_params(labelsize=20)


# plt.show()

plt.savefig('figure2-b1.jpg',dpi = 500)