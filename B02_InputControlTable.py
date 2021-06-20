#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 13:44:08 2021
B02 根据历史数据，把数据填写入控制表中
@author: zhangjun
"""

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

def analysis_contol_data():
    pass
    conn = link_postgresql_db()
    cur = conn.cursor()
    
    for i in range(6):  # =6
        fix_num = i+1
        print(fix_num)
        
        for k in range(33):  # = 33
            check_num = k + 1
            a = []
            b = []
            
            for j in range(6):
                move_num = j+1

                if fix_num != move_num:
                    strSQL = '''
                    SELECT min(r%d), max(r%d) 
                    from public.tblhistory
                    where r%d = %d
                    '''%(move_num,move_num,fix_num,check_num)
                    print(strSQL)
                    df = pd.read_sql(strSQL,conn)
                    temp_a = df.iloc[0,0]
                    temp_b = df.iloc[0,1]
                    
                    if temp_a == None:
                        a.append(0)
                    else:
                        a.append(temp_a)
                        
                    if temp_b == None:
                        b.append(0)
                    else:
                        b.append(temp_b)
                        
                    # if not df.empty:
                    #     a.append(df.iloc[0,0])
                    #     b.append(df.iloc[0,1])
                    # else:
                    #     a.append(0)
                    #     b.append(0)
                else:
                    a.append(check_num)
                    b.append(check_num)                        
                    
            pass
            print(a,b)
            
            strSQL = '''
            INSERT INTO public.tblallavailablecontrol 
            (r1h, r1t,
             r2h, r2t,
             r3h, r3t,
             r4h, r4t,
             r5h, r5t,
             r6h, r6t) 
            VALUES (%d, %d,
                    %d, %d,
                    %d, %d,
                    %d, %d,
                    %d, %d,
                    %d, %d)
            '''%(a[0],b[0],
            a[1],b[1],
            a[2],b[2],
            a[3],b[3],
            a[4],b[4],
            a[5],b[5])
            cur.execute(strSQL)
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    analysis_contol_data()    
