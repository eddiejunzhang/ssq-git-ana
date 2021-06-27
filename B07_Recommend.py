# -*- coding: utf-8 -*-
"""
Created on Sun Jun 27 21:21:06 2021
B07 推荐几组数，去购买
@author: Eddiezhang
"""

import os
import psycopg2
import configparser
import pandas as pd

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

def generate_recommemdation(qty):
    pass
    conn = link_postgresql_db()
    strSQL = '''
    SELECT id,r1,r2,r3,r4,r5,r6 FROM public.tbluniversalset
    ORDER BY RAND()
    LIMIT 1
    '''
    print('start to generate df.')
    df = pd.read_sql(strSQL,conn)
    print('df is ready. ')
    print(df)
    
if __name__ == "__main__":
    how_many = 10
    generate_recommemdation(how_many) 