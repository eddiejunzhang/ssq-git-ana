#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 16:56:12 2021
创建近似表，Universal Set
@author: zhangjun
"""

import psycopg2
import configparser

def ping(ip):
    import os
    ret =os.system('ping -c 1 -W 1 %s'%ip) #每个ip ping 1次，等待时间为1s
    # ret =os.system('ping -w 1 %s'%ip) #每个ip ping 1次，等待时间为1s
    if ret:
        print('ping %s is fail'%ip)
        return(False)
    else:
        print('ping %s is ok'%ip)
        return(True)

def link_postgresql_db():
    config=configparser.ConfigParser()
    if ping('192.168.100.20'):
        config.read('/Users/zhangjun/Code/_privateconfig/analysis.cfg')
    else:
        config.read('/Users/zhangjun/Code/_privateconfig/analysis_oray.cfg')
    # config=configparser.ConfigParser()
    # config.read('analysis.cfg')
    HOST = config['DB']['IP']
    USER = config['DB']['USER']
    DATABASE = config['DB']['DATABASE']
    PASSWORD = config['DB']['PASSWORD']
    PORT = config['DB']['PORT']
    
    print(HOST)
    conn = psycopg2.connect(database=DATABASE, user=USER, \
                            password=PASSWORD, host=HOST, port=PORT)
    return conn

def drop_table_tbluniversalset():
    # conn = link_postgresql_db()
    
    config=configparser.ConfigParser()
    # config.read('/Users/zhangjun/Code/_privateconfig/analysis.cfg')
    
    if ping('192.168.100.20'):
        config.read('/Users/zhangjun/Code/_privateconfig/analysis.cfg')
    else:
        print('remote')
        config.read('/Users/zhangjun/Code/_privateconfig/analysis_oray.cfg')

    HOST = config['DB']['IP']
    USER = config['DB']['USER']
    DATABASE = config['DB']['DATABASE']
    PASSWORD = config['DB']['PASSWORD']
    PORT = config['DB']['PORT']
    
    conn = psycopg2.connect(database=DATABASE, user=USER,
                            password=PASSWORD, host=HOST, port=PORT)

    cur = conn.cursor()
    strsql = "DROP TABLE tbluniversalset;"
    cur.execute(strsql)
    conn.commit()
    conn.close()
    
    print("Droped database successfully")

def create_table_tbluniversalset():
    
    conn = link_postgresql_db()
    
    print("Opened database successfully")
    
    cur = conn.cursor()
    
    strSQL = '''
    CREATE TABLE public.tbluniversalset
       (ID serial,
       r1         int,
       r2         int,
       r3         int,
       r4        int,
       r5        int,
	r6       int)
    '''
    cur.execute(strSQL)
    print("Table created successfully")
    
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    # drop_table_tbluniversalset()    
    create_table_tbluniversalset()