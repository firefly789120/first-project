# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 15:00:54 2017

@author: firefly
矩阵转为数据库任何数据，返回sql语句
"""


import pandas as pd
import numpy as np
import time;  # 引入time模块

'''
#tabname 数据库表名
#dataframe 即将插入数据库的表
#rownumber 即将插入数据库的行数
#strvalur 列名
'''
        
#将数据从python格式转为数据库可用格式
def getvalue(dataframe,strvalur):
    if dataframe.xs(strvalur)==None:
        return 'NULL'
    elif type(dataframe.xs(strvalur))==str:
    #    return "'"+dfrow.xs(strvalur)+"'" #'Tpy'"                   
        return "\'"+(dataframe.xs(strvalur).replace("'","''"))+"\'" #处理插入单引号问题,注意双单引号和双引号区别，此处双单
        #return (dataframe.xs(strvalur).replace("'",'"'))
    elif np.isnan(dataframe.xs(strvalur)): #处理不放呢空字符被转为nan,而None的问题
        return 'NULL'
    else:
        return dataframe.xs(strvalur)

    
    
#定义数据列对应变量-提供初始值
#将矩阵中的字段动态设置为变量，并没行的值赋值过去
#参考http://blog.csdn.net/ztf312/article/details/51122027
adict=locals()
def getvarname(dataframe,rownumber):
    for s in dataframe.columns:
        adict[s.upper()]=getvalue(dataframe.ix[rownumber],s)
    return adict

#获得插入数据表列名信息
def getcolumn(dataframe):
    insrthead="("
    for each in dataframe.columns:
        insrthead=insrthead+str(each.upper())+","      
    insrthead=insrthead[:-1]+")"
    return insrthead

#获得插入表单行值-某行
def getcolvalue(dataframe,rownumber):
    getvarname(dataframe,rownumber) #获取变量名
    valsql="("
    for each in dataframe.columns:
        valsql=valsql+str(eval(each.upper()))+","      
    valsql=valsql[:-1]+")"
    return valsql
 
#单条记录插入       
def insertone(tabname,dataframe,rownumber):
    sqlhead="INSERT INTO "+ tabname
    sqlbody=getcolumn(dataframe)
    sqlvalue="VALUES"+getcolvalue(dataframe,rownumber)
    return sqlhead+sqlbody+sqlvalue
#全部数据插入
def insertall(tabname,dataframe):
    sqlhead="INSERT INTO "+ tabname
    sqlvalue="VALUES"
    sqlbody=getcolumn(dataframe)
    for item in dataframe.index:
        sqlvalue=sqlvalue+getcolvalue(dataframe,item)+','
    return sqlhead+sqlbody+sqlvalue[:-1]

#异步插值-安装指定行插入
def insertcount(tabname,dataframe,begin,end):
    sqlhead="INSERT INTO "+ tabname
    sqlvalue="VALUES"
    sqlbody=getcolumn(dataframe)
    for item in dataframe.index[begin:end]:
        sqlvalue=sqlvalue+getcolvalue(dataframe,item)+','
    return sqlhead+sqlbody+sqlvalue[:-1]

def deleteall(tablename):
    return "delete from "+ tablename




"""
Created on Fri Jan  5 12:42:29 2018

@author: firefly
执行数据库DML语句，返回结果
"""


#进阶部分，可以不使用-20180105 


#获得当前命令执行时间，无返回，输出时间信息
def executetime(*arguments): #要求传入内的是字符串
    notice=''
    for arg in arguments:
        notice=notice+arg
    moment=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("\033[1;32;m%s\033[0m" %("时间:%s，执行命令成功：%s" %(moment,notice)))
    #print("--------------------")

#获得查询表的数据集，输出cur游标结果集    
def excuteselectall(curs,tablename): #空指针
    print("-------------select开始----------------")
    executetime("开始获取表%s记录" %tablename)
    curs.execute("select * from "+tablename)
    executetime("完成获取表%s" %tablename)
    print("-------------select结束----------------")
    return curs #返回结果集合指针
    

#删除当前表记录，无返回，输出执行信息
def excutedeleteall(curs,tablename):
    print("-------------delete开始----------------")
    executetime("开始清空表%s记录" %tablename)
    curs.execute("delete from "+ tablename)
    executetime("清空表%s记录成功" %tablename)
    print("-------------delete结束----------------")
    
#获得当前表记录数，返回整数
def executegetrows(tablename,curs):
    curs.execute("select count(*) from "+tablename)
    selcount=max(curs.fetchone())
    print("\033[1;31;m%s\033[0m" %('查询表格%s,记录数%d条' %(tablename,selcount)))
    return selcount  
#向当前表插入dataframe数据，无返回，输出执行信息    
def executeinsert(tablename,dataframe,curs):
    print("-------------insert开始----------------")
    executetime("开始向%s表进行插值" %tablename)
    count=1000
    '''
    if kwds['count'] is None: #如果提供单次执行个数，则个数为指定值
        count=1000 #默认个数为1000      
    else:
        count=kwds['count']
    '''
    #icount轮循次数   
    icount=int(np.floor(dataframe.shape[0]/count)) #单次插值个数完全轮循数
    if icount == 0:
         #剩余条数小于指定轮循执行记录插入
        curs.execute(insertcount(tablename,dataframe,0,dataframe.shape[0]))
        executegetrows(tablename,curs)
    else:
        for i in range(0,icount):
            #剩余条数大于指定轮循执行记录插入
            curs.execute(insertcount(tablename,dataframe,i*count,(i+1)*count))
            executegetrows(tablename,curs)
        #剩余条数小于指定轮循执行记录插入
        curs.execute(insertcount(tablename,dataframe,icount*count,dataframe.shape[0]))
        executegetrows(tablename,curs)
    executetime("%s表进行插值完成" %tablename)
    print("-------------insert结束----------------")
    
#校验数据同步情况-无返回，输出检查信息
def check_df_table(dframe,tablename,curs):
    curs.execute("select count(*) from "+tablename)
    print("-------------check开始----------------")
    selcount=max(curs.fetchone())
    difcount=0
    difcount=abs(dframe.shape[0]-selcount)
    if difcount == 0:
        print("\033[1;31;m%s\033[0m" %("数据同步检查：%s同步成功" %(tablename)))
    else:
        print("\033[1;31;m%s\033[0m" %("数据同步检查：%s同步失败，"
        "导入记录为%d,数据库记录为%d,失败记录数%d" %(tablename,dframe.shape[0],selcount,difcount)))
    print("-------------check结束----------------")
