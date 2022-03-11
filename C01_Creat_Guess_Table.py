#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 3 19:56:12 2022
创建推测表，Forecast
@author: zhangjun
"""

import os
import platform
import psycopg2
import configparser

def ping(ip):
    sys_id = platform.system()
    if sys_id == 'Linux':
        ret =os.system('ping -c 1 -W 1 %s'%ip) #每个ip ping 1次，等待时间为1s
    elif sys_id == 'Windows':
        ret =os.system('ping -w 1 %s'%ip) #每个ip ping 1次，等待时间为1s
    elif sys_id == 'Darwin':
        ret =os.system('ping -w 1 %s'%ip) #每个ip ping 1次，等待时间为1s
    else:
        print('别识别到可用的操作系统。')
    if ret:
        print('ping %s is fail'%ip)
        return(False)
    else:
        print('ping %s is ok'%ip)
        return(True)

def obtain_config_filename():
    sys_id = platform.system()

    if sys_id == 'Linux':
        config_filename = '/home/pi/Python_Proj/_privateconfig/analysis.cfg'
    elif sys_id == 'Windows':
        config_filename = 'D:\\Study\\PythonCoding\\_privateconfig\\analysis.cfg'
    elif sys_id == 'Darwin':
        config_filename = '/Users/zhangjun/Code/_privateconfig/analysis.cfg'
    else:
        print('没有别识到可用的操作系统。')
    print('配置文件：', config_filename)
    return config_filename

def link_postgresql_db():
    config=configparser.ConfigParser()
    # if ping('192.168.100.20'):
    if True:
        config_filename = obtain_config_filename()
        config.read(config_filename)
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

def drop_table(table_name):
    conn = link_postgresql_db()
    cur = conn.cursor()

    strsql = "DROP TABLE %s;"%table_name
    cur.execute(strsql)
    conn.commit()
    conn.close()

    print("Droped database successfully")

def create_table(table_name):

    conn = link_postgresql_db()
    print("Opened database successfully")
    cur = conn.cursor()

    strSQL = '''
    CREATE TABLE public.%s
       (ID serial,
       r1       int,
       r2       int,
       r3       int,
       r4       int,
       r5       int,
	   r6       int,
       a        bool,
       b        bool,
       c        bool,
       d        bool,
       e        bool,
       f        bool,
       g        bool,
       h        bool,
       i        bool,
       j        bool,
       k        bool,
       l        bool,
       m        bool,
       n        bool,
       o        bool,
       p        bool,
       q        bool,
       r        bool,
       s        bool,
       t        bool,
       u        bool,
       v        bool,
       w        bool,
       x        bool,
       y        bool,       
       z        bool)
    '''%table_name
    cur.execute(strSQL)
    print("Table created successfully")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    table_name = 'tblforecast'
    drop_table(table_name)
    create_table(table_name)