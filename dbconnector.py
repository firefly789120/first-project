# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 14:03:10 2017

@author: firefly
数据库连接专用
"""
#mongodb连接库
from pymongo import MongoClient
#连接JDBC库
import jaydebeapi as jdbcapi



#*dbdriver,*dbdriverfile):
#def connectdb(dbcon_type,dbtype,dburl,*args): #收集参数
def connectdb(dbcon_type,dbtype,dburl,**kwds): #字典类型，参数对 
    if dbcon_type=='pymongo':
        if dbtype != 'mongodb':
            return -1
        else:
            mango_uri=dburl
            mongoconn = MongoClient(mango_uri)
        return mongoconn
    elif dbcon_type=='jdbc':
        dbdriver=kwds['dbdriver']
        dburl=dburl
        dbdriverfile=kwds['dbdriverfile']
        jdbcconn=jdbcapi.connect(dbdriver,dburl,dbdriverfile)
        return jdbcconn


'''
实际使用
#数据库操作，基于JDBC
jdbcconn=jdbcapi.connect('com.ibm.db2.jcc.DB2Driver',['jdbc:db2://10.137.225.188:50000/YCJN_RUN','administrator','1qazXSW@'],"C:/Program Files/raqsoft/common/jdbc/db2jcc.jar")
jdbcconn.close()

#mongo库操作，基于pymongo
mango_uri = 'mongodb://%s:%s' % ("10.137.225.135.", 18011)
mongoconn = MongoClient(mango_uri)  # 创建链接
db = mongoconn.ZSY_NEW  # 连接数据库
table = db.TJCXHIS_DAY  # 选择表集合
mongoconn.close()
'''

'''
测试代码
mango_uri = 'mongodb://%s:%s' % ("10.137.225.135.", 18011)        
connectdb('pymongo','mongodb',mango_uri)  

db2driver='com.ibm.db2.jcc.DB2Driver'
db2url=['jdbc:db2://10.137.225.188:50000/YCJN_RUN','administrator','1qazXSW@']
db2driverfile="C:/Program Files/raqsoft/common/jdbc/db2jcc.jar"

connectdb('jdbc','db2',db2url,dbdriver=db2driver,dbdriverfile=db2driverfile) 
''' 
