# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 13:22:19 2018

@author: firefly
"""


import warnings
import itertools
import datetime
import pandas as pd
import numpy as np
import statsmodels.api as sm   #相关模型原始数据,注意为了使用statespace等功能需要用0.8.0版本
import matplotlib.pyplot as plt
import DaotbaseEta as DataSetapi
from pandas import DataFrame,Series
warnings.filterwarnings("ignore") # specify to ignore warning messages

#plt.style.use('fivethirtyeight')
#时序图
import matplotlib.pyplot as plt
#用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei'] 
#用来正常显示负号
plt.rcParams['axes.unicode_minus'] = False 
#data.plot()
#plt.show()

#数据预处理
# The 'MS' string groups the data in buckets by start of the month
#y = y['value'].resample('MS').mean() #采样周期修改为月，统计方法为平均

datafr = DataSetapi.fp_Eta
dataset=datafr[['STATTIMEBEGIN','VVALUE']]
index = pd.DatetimeIndex(dataset['STATTIMEBEGIN'])
dataset.index = pd.DatetimeIndex(index)
y = dataset['VVALUE'].resample('D').mean() #采样周期修改为天，统计方法为平均
# The term bfill means that we use the value before filling in missing values
#y = y.fillna(y.bfill())   #空值处理方式向前填充
y = y.fillna(y.ffill())
print(y)

#y.plot(figsize=(15, 6))
y.plot()
plt.show()


'''


'''



'''
原始序列检验-平稳性和白噪音
平稳性检验方法：
    1、自相关图，观察法
    2、单位根法，P值
稳定性判断结果处理：
        稳定：进入下一步随机性校验
        不稳定：非稳定序列转稳定方法，首先差分
            对转成的新序列进行稳定性判断，方法同上
#返回值依次为adf、pvalue、usedlag、nobs、critical values、icbest、regresults、resstore
#Pdf值大于三个水平值，p值显著大于0.05，该序列为非平稳序列。
P值确认成功进入白噪声校验
'''
'''
from statsmodels.tsa.stattools import adfuller as ADF
if ADF(DataFrame(y)[u'VVALUE'])[1]<0.05:
    pvalue=ADF(DataFrame(y)[u'VVALUE'])[1]
    d=0
    print('%s阶差分,pvalue:%s' %(0,pvalue))
    print(u'差分序列的ADF检验结果为', ADF(DataFrame(y)[u'VVALUE']))

else:
    for i in range(1,9): 
        #自定义差分阶范围1，9
        y_dif = y.diff(i).dropna()
        y_dif.columns = [u'VVALUE_dif']
        pvalue=ADF(DataFrame(y_dif)[u'VVALUE'])[1]
        d=i
        if pvalue<0.05:
            #P明显小于0.05，一阶差分后序列为平稳序列
            print('%s阶差分,pvalue:%s' %(i,pvalue))
            print(u'差分序列的ADF检验结果为', ADF(DataFrame(y_dif)[u'VVALUE']))
            y=y_dif
        else:
            print('%s阶差分不能满足要求' %i)
        break;
'''
#单位跟确定
from statsmodels.tsa.stattools import adfuller as ADF
#白噪声检验
from statsmodels.stats.diagnostic import acorr_ljungbox

def checkADF_d(y_ori,diffbegin,diffend): 
    if ADF(DataFrame(y_ori)[u'VVALUE'])[1]<0.05:
        pvalue=ADF(DataFrame(y_ori)[u'VVALUE'])[1]
        y_check=y_ori
        d=0
        print('%s阶差分,pvalue:%s' %(0,pvalue))
        print(u'差分序列的ADF检验结果为', ADF(DataFrame(y)[u'VVALUE']))
    else:
        for i in range(diffbegin,diffend): 
            #自定义差分阶范围，最好1，9
            y_dif = y_ori.diff(i).dropna()
            y_dif.columns = [u'VVALUE_dif']
            pvalue=ADF(DataFrame(y_dif)[u'VVALUE'])[1]
            d=i
            if pvalue<0.05:
                #P明显小于0.05，一阶差分后序列为平稳序列
                print('%s阶差分,pvalue:%s' %(i,pvalue))
                print(u'差分序列的ADF检验结果为', ADF(DataFrame(y_dif)[u'VVALUE']))
                y_check=y_dif
                #修正后的时序图，可能是原序列或者差分序列
                y.plot() 
                plt.show()
            #返回统计量和p值
                if float(acorr_ljungbox(y, lags=1)[1])<0.05:
                    print(u'原序列的白噪声检验结果通过为：', acorr_ljungbox(y, lags=1))
                    break;
                else:
                    print(u'原序列的白噪声检验结果：当前序列无法拒绝假设，失败为：', acorr_ljungbox(y, lags=1))
                    print(u'该差分下模型没有意义', acorr_ljungbox(y, lags=1))
            #print(u'差分序列的白噪声检验结果为：', acorr_ljungbox(y_data, lags=1)) 
            #P值小于0.05，所以一阶差分后的序列为平稳非白噪声序列。，P》0.05则是白噪声，数据随机无可取价值信息
                    continue;
            else:
                print('%s阶差分不能满足要求,结束' %i)        
    return d,y_check


d,y_check=checkADF_d(y,1,9)
#自相关图
from statsmodels.graphics.tsaplots import plot_acf
plot_acf(y).show()

#偏自相关图
from statsmodels.graphics.tsaplots import plot_pacf
plot_pacf(y).show()





from statsmodels.tsa.arima_model import ARIMA
#定阶

#一般阶数不超过length/10
pmax = int(len(y)/10) 
#一般阶数不超过length/10
qmax = int(len(y)/10) 

 

#bic矩阵
bic_matrix = [] 
for p in range(pmax+1):
  tmp = []
  for q in range(qmax+1):
      #存在部分报错，所以用try来跳过报错。
    try: 
      tmp.append(ARIMA(y, (p,d,q)).fit().bic)
    except:
      tmp.append(None)
  bic_matrix.append(tmp)

#从中可以找出最小值
bic_matrix = pd.DataFrame(bic_matrix) 

#先用stack展平，然后用idxmin找出最小值位置。

p,q = bic_matrix.stack().idxmin() 
print(u'BIC最小的p值和q值为：%s、%s' %(p,q))
#BIC最小的p值和q值为：0、0,定阶完成。

#建立ARIMA(0, 1, 1)模型
arimamodel = ARIMA(y, (p,d,q)).fit() 

#作为期5天的预测，返回预测结果、标准误差、置信区间。
result=arimamodel.forecast(5)
#print(model.summary())
#p值 P>|z| 小于0.05无法拒绝原假设
#给出一份模型报告
#model.summary() 
