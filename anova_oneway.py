# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 09:19:41 2018

@author: firefly
Python统计分析：[3]单因素方差分析
参考资料：https://jingyan.baidu.com/article/cdddd41c6a2f2553cb00e13b.html
"""
#1、引入相关模块
from scipy import stats
import pandas as pd
import numpy as np
from pandas import DataFrame,Series

#2、读取数据
import DaotbaseEta as DataSetapi

#只是生成值和分组，分组用功率，值用Eta_gb1
datafr = DataSetapi.fp_EtaPel

#行列转换
dataset=datafr[['STATTIMEBEGIN','PARAID','VVALUE']]
datas=dataset.groupby(['PARAID','STATTIMEBEGIN'])
datas=datas.mean().unstack('PARAID')

datas['VVALUE']['Pel']
#数据归一化，离散化
Pe=1030.0
dateready=DataFrame(columns=['Eta_gb1','Px_group'])
dateready['Px']=datas['VVALUE']['Pel']/Pe*100
dateready['Eta_gb1']=datas['VVALUE']['Eta_gb1']

#离散化
bins=[0,50,60,70,80,90,100]
group_name=['<50%','50%-60%','60%-70%','70%-80%','80%-90%','90%-100%']
dateready['Px_group']=pd.cut(dateready['Px'],bins,labels=group_name)
#准备数据集dateready

#3、数据分组
d1=dateready[dateready['Px_group']=='<50%']['Eta_gb1']
d2=dateready[dateready['Px_group']=='50%-60%']['Eta_gb1']
d3=dateready[dateready['Px_group']=='60%-70%']['Eta_gb1']
d4=dateready[dateready['Px_group']=='70%-80%']['Eta_gb1']
d5=dateready[dateready['Px_group']=='80%-90%']['Eta_gb1']
d6=dateready[dateready['Px_group']=='90%-100%']['Eta_gb1']

args=[d1,d2,d3,d4,d5,d6]

#4、首先执行levene test P<0.05.警告方差不齐
w,p=stats.levene(*args)
if p<0.05:
    print("警告：levene test 方差其次假设不成立p=%.2f" %p)
else:
    print("校验成功：levene test 方差其次假设成立p=%.2f" %p)
#p:0.358043949729694 满足方差齐次性

#4、进行方差校验
f,p=stats.f_oneway(*args)
print(f,p)
#f,p 30.085143586 1.01908302949e-05
if p<0.05:
    print("方差校验结论p=%.2f,组间存在统计学上显著差异" %p)
else:
    print("方差校验结论p=%.2f,组间存在统计学上无显著差异" %p)

#5、优化1：实现自动分组分析
#定义单因素分析函数
def anova_Pv(dateready,groupclm,value):
    '''
    dateready:用来分析的矩阵
    groupclm：分组列
    value：比对值列
    '''
    dfgroup=list(set(dateready[groupclm]))#返回分组类别个数
    args=[]
    for i in dfgroup:
        args.append(dateready[dateready[groupclm]==i][value])
    f,p=stats.f_oneway(*args)
    if p<0.05:
        print("anova_Pv:方差校验结论p=%.2f,组间存在统计学上显著差异" %p)
    else:
        print("anova_Pv:方差校验结论p=%.2f,组间存在统计学上无显著差异" %p)
    return p
anova_Pv(dateready,'Px_group','Eta_gb1')

#5、优化2：输出统计学结论
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

anova_results=anova_lm(ols('Eta_gb1~C(Px_group)',dateready).fit())

print(anova_results)


