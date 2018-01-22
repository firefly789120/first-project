# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 13:41:42 2018

@author: Administrator
参考资料：http://blog.csdn.net/shuaishuai3409/article/details/51428106
"""

#-*- coding: utf-8 -*-
import pandas as pd
from pandas import DataFrame,Series



data1=DataFrame([[1,2],
[3,4.5],
[4,6.7],
[6,8.9],
[8,1.1],
[9,13.3],
[30,5],
[50,7],
[5,8],
[9,40],
[7,4.3],
[6,6.5],
[3,8.7],
[9,8.1],
[2,8.3],
[7,6.66],
[8,7],
[6,8],
[10,2],
[7.8,2],
[5.6,4],
[2.3,5],
[5.2,6],
[6.1,8],
[7.3,3]])
import matplotlib.pyplot as plt #导入图像库
plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
plt.figure(1, figsize=(13, 26))#可设定图像大小
#plt.figure() #建立图像
p = data1.boxplot(return_type= 'dict') #画箱线图，直接使用DataFrame的方法.代码到这为止,就已经可以显示带有异常值的箱型图了,但为了标注出异常值的数值,还需要以下代码进行标注.
#for i in range(0,4):
#标记第一个分组的异常值
x = p['fliers'][0].get_xdata() # 'flies'即为异常值的标签.[0]是用来标注第1位歌手的异常值数值,同理[i]标注第i+1位歌手的异常值.
y = p['fliers'][0].get_ydata()
y.sort() #从小到大排序

for i in range(len(x)): 
  if i>0:
    plt.annotate(y[i], xy = (x[i],y[i]), xytext=(x[i]+0.05 -0.8/(y[i]-y[i-1]),y[i]))
  else:
    plt.annotate(y[i], xy = (x[i],y[i]), xytext=(x[i]+0.08,y[i]))

plt.show() #展示箱线图
