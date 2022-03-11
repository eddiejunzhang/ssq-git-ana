#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 21:07:21 2022
猜5个号，各不相同
@author: zhangjun
"""

import numpy as np
import random
import os
import sys
config_path_macmini = r"/Users/zhangjun/Code/_privateconfig"
if os.path.isdir(config_path_macmini): 
    config_path = config_path_macmini
    whose_pc = 'macmini'
    
sys.path.append(config_path)

import platform
import psycopg2
import configparser
import pandas as pd

def ping(ip):
    sys_id = platform.system()
    if sys_id == 'Linux':
        ret =os.system('ping -c 1 -W 1 %s'%ip) #每个ip ping 1次，等待时间为1s
    elif sys_id == 'Windows':
        ret =os.system('ping -w 1 %s'%ip) #每个ip ping 1次，等待时间为1s
    elif sys_id == 'Darwin':
        ret =os.system('ping -c 1 -W 1 %s'%ip) #每个ip ping 1次，等待时间为1s
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
        print('别识别到可用的操作系统。')
    return config_filename
    
def link_postgresql_db():
    config=configparser.ConfigParser()
    if ping('192.168.100.20'):
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
    conn = psycopg2.connect(database=DATABASE, 
                            user=USER, 
                            password=PASSWORD, 
                            host=HOST, 
                            port=PORT)
    return conn

def swap(a):
    m = random.randint(1,33)
    n = random.randint(1,33)
    a[m-1],a[n-1] = a[n-1],a[m-1]
    return a

def main():
    conn = link_postgresql_db()
    
    for k in range(1000):
        # print(k)
        a=np.linspace(1,33,33)
        
        for i in range(256):
            a=swap(a)
        # print(a)
        
        b=np.resize(a,(5,6))
        b.sort(axis=1)
        # print(b)
        # print(b[0])
        
        n = 0
        for i in range(5):
            # print(b[i])
            # print(int(b[i][0]))
            strSQL = '''
            select * from public.tblforecast t 
            where r1=%d and r2=%d and r3=%d and r4=%d and r5=%d and r6=%d
            and (a or b or c) and d and e and f and g and h
            '''%(int(b[i][0]),
            int(b[i][1]),
            int(b[i][2]),
            int(b[i][3]),
            int(b[i][4]),
            int(b[i][5]))
            df = pd.read_sql(strSQL, conn)
            if not df.empty:
                # print(df)
                n += 1
        if n > 2:
            print(n)
            print(b)
    conn.close()
            
if __name__ == "__main__":
    main()