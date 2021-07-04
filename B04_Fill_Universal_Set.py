#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 16:52:46 2021
B04 根据B02填写的控制表，向近似表中填写数据。
@author: zhangjun
"""

import os
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
    elif sys_id == 'Mac':
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
    elif sys_id == 'Mac':
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
    conn = psycopg2.connect(database=DATABASE, user=USER, \
                            password=PASSWORD, host=HOST, port=PORT)
    return conn

def main():
    
    config_filename = obtain_config_filename()
    config = configparser.ConfigParser()
    config.read(config_filename)
    
    HOST = config['DB']['IP']
    USER = config['DB']['USER']
    DATABASE = config['DB']['DATABASE']
    PASSWORD = config['DB']['PASSWORD']
    PORT = config['DB']['PORT']
    
    conn = psycopg2.connect(database = DATABASE, 
                            user = USER,
                            password = PASSWORD, 
                            host = HOST, 
                            port = PORT)
    print("Opened database successfully")

    cur = conn.cursor()

    strSQL = '''
    SELECT *  
    from public.tblallavailablecontrol
    '''
    # print(strSQL)
    df = pd.read_sql(strSQL,conn)    

    # print('r1 min = %s, r6 max = %s'%(r1min, r6max))
    # df = df.head(2)
    for index,row in df.iterrows():
        print(index)
        r1min = row['r1h']
        r1max = row['r1t']
        r2min = row['r2h']
        r2max = row['r2t']
        r3min = row['r3h']
        r3max = row['r3t']
        r4min = row['r4h']
        r4max = row['r4t']
        r5min = row['r5h']
        r5max = row['r5t']
        r6min = row['r6h']
        r6max = row['r6t']
        
        for i in range(int(r1min), int(r1max) + 1):
            for j in range(int(r2min), int(r2max) + 1):
                for k in range(int(r3min), int(r3max) + 1):
                    for l in range(int(r4min), int(r4max) + 1):
                        for m in range(int(r5min), int(r5max) + 1):
                            for n in range(int(r6min), int(r6max) + 1):
                                if i<j and j<k and k<l and l<m and m<n:
                                    strSQL = '''
                                    INSERT INTO tbluniversalset (R1,R2,R3,R4,R5,R6)
                                    VALUES ( %d, %d, %d, %d, %d, %d)
                                    '''%(i,j,k,l,m,n)
                                    cur.execute(strSQL)
                    print(index, 'i = ',i, 'j = ',j, 'k = ',k)
        conn.commit()
    print("Records created successfully")
    conn.close()
    
if __name__ == "__main__":
    main()