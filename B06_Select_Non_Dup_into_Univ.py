# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 12:29:08 2021
B06 选择那些不重复的数据导入tblUniversalSet表中
@author: Eddiezhang
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

def select_and_import_data_into_univ():
    conn = link_postgresql_db()
    cur = conn.cursor()

    strSQL = '''
    select min(id) 
    from public.tbltest 
    group by dupstr 
    order by dupstr
    '''
    df = pd.read_sql(strSQL,conn)
    df = df.head(100)
    print(df)
    
    for index, row in df.iterrows():
        idnum = row['id']
        strSQL = '''
        INSERT INTO tbluniversalset (R1,R2,R3,R4,R5,R6)
        VALUES ( %d, %d, %d, %d, %d, %d)
        '''%(i,j,k,l,m,n)
        cur.execute(strSQL)

if __name__ == "__main__":
    select_and_import_data_into_univ()