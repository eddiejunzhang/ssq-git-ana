# -*- coding: utf-8 -*-
"""
Created on Sun Jun 27 21:21:06 2021
B07 推荐几组数，去购买
@author: Eddiezhang
"""

import os
import platform
import psycopg2
import configparser
import pandas as pd
import increase_history_to_db 

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

def generate_recommemdation(qty):
    conn = link_postgresql_db()
    strSQL = '''
    SELECT id,r1,r2,r3,r4,r5,r6 FROM public.tbluniversalset
    ORDER BY RANDOM()
    LIMIT %d
    '''%qty
    print('start to generate df.')
    df = pd.read_sql(strSQL,conn)
    print('get df.')
    return df

def filter_first_sixth_diff_is(df, diff_list):
    if diff_list == None:
        diff_list = [20]
    df1 = pd.DataFrame()
    for index,row in df.iterrows():
        idnum = row['id']
        r6 = row['r6']
        r5 = row['r5']
        r4 = row['r4']
        r3 = row['r3']
        r2 = row['r2']
        r1 = row['r1']
        dif = r6 - r1
        if dif in diff_list:
            s2 = pd.Series([idnum, r1, r2, r3, r4, r5, r6],
               index=['id', 'r1', 'r2', 'r3', 'r4', 'r5','r6'])
            df1 = df1.append(s2, ignore_index=True)
    return df1

def filter_a_plus_b_is_c(df):
    # a+b = c
    df1 = pd.DataFrame()
    for index,row in df.iterrows():
        idnum = row['id']
        r6 = row['r6']
        r5 = row['r5']
        r4 = row['r4']
        r3 = row['r3']
        r2 = row['r2']
        r1 = row['r1']

        # 以下的mark是关于是否存在和值的mark
        mark = 0
        # print(idnum)
        for i in range(1,4):
            a = row[i]
            for j in range(2,5):
                b = row[j]
                for k in range(3,6):
                    c = row[k]
                    if a + b == c:
                        mark += 1
                        
        if mark > 0:
            s2 = pd.Series([idnum, r1, r2, r3, r4, r5, r6],
               index=['id', 'r1', 'r2', 'r3', 'r4', 'r5','r6'])
            df1 = df1.append(s2, ignore_index=True)
    return df1

def filter_d_minus_c_is_b_minus_a(df):
    # d-c = b-a
    df1 = pd.DataFrame()
    for index,row in df.iterrows():
        idnum = row['id']
        r6 = row['r6']
        r5 = row['r5']
        r4 = row['r4']
        r3 = row['r3']
        r2 = row['r2']
        r1 = row['r1']

        # 以下的mark是关于是否存在差相等的mark
        mark_minus = 0
        m = []
        m.append(r2-r1)
        m.append(r3-r2)
        m.append(r4-r3)
        m.append(r5-r4)
        m.append(r6-r5)
        # print(row)
        
        a = 0
        b = 0
        for i in range(len(m)-1):
            a = m[i]
            # print('a = ', a)
            for j in range(i+1,len(m)):
                b = m[j]
                # print('b = ',b)
                if a == b and a in (2,3,4):
                    mark_minus += 1
                        
        if mark_minus > 0:
            s2 = pd.Series([idnum, r1, r2, r3, r4, r5, r6],
               index=['id', 'r1', 'r2', 'r3', 'r4', 'r5','r6'])
            df1 = df1.append(s2, ignore_index=True)
    return df1

def filter_contain_history_ball(df, qty):
    df_result = pd.DataFrame()
    conn = link_postgresql_db()
    strSQL = '''
    SELECT r1,r2,r3,r4,r5,r6,b
    FROM public.tblhistory
    ORDER BY id DESC
    LIMIT %d
    '''%qty
    df1 = pd.read_sql(strSQL,conn)
    
    b1= df1.iloc[0,6]
    b2= df1.iloc[1,6]
    
    b_list = []
    b_list.append(b1)
    if b2>b1:
        b_list.append(b2-b1)
    if b1+b2<=16:
        b_list.append(b1+b2)
    if b1 *2 <=16:
        b_list.append(b1*2)
    if round(b1/2,0)>0:
        b_list.append(round(b1/2,0))
    print(b_list)
        
    filter_list = []
    for index,row in df1.iterrows():
        for item in row:
            filter_list.append(item)
    # print(filter_list)

    
    for index, row in df.iterrows():
        idnum = row['id']
        r6 = row['r6']
        r5 = row['r5']
        r4 = row['r4']
        r3 = row['r3']
        r2 = row['r2']
        r1 = row['r1']
        flag = False
        for item in row:
            if item in filter_list:
                flag = flag or True
        if flag:
            s2 = pd.Series([idnum, r1, r2, r3, r4, r5, r6],
               index=['id', 'r1', 'r2', 'r3', 'r4', 'r5','r6'])
            df_result = df_result.append(s2, ignore_index=True)            
    return df_result

def sum_is_former_one(df):
    # 中奖号码中的两个号之和，与上一期的某个号相同
    df_result = pd.DataFrame()
    conn = link_postgresql_db()
    strSQL = '''
    SELECT r1,r2,r3,r4,r5,r6
    FROM public.tblhistory
    ORDER BY id DESC
    LIMIT 1
    '''
    df1 = pd.read_sql(strSQL,conn)
    
    r_last = []
    for i in range(6):
        r_last.append(df1.iloc[0,i])
    # print(r_last)   

    for index, row in df.iterrows():
        idnum = row['id']
        r6 = row['r6']
        r5 = row['r5']
        r4 = row['r4']
        r3 = row['r3']
        r2 = row['r2']
        r1 = row['r1']
        r = []
        r.append(r1)
        r.append(r2)
        r.append(r3)
        r.append(r4)
        r.append(r5)
        r.append(r6)
        flag = False
        for i in range(5):
            for j in range(1,6):
                sum_r = r[i] + r[j]
                # print(r[i] , r[j],sum)
                for k in range(6):
                    if r_last[k] == sum_r:
                        flag = True or flag
        if flag:
            s2 = pd.Series([idnum, r1, r2, r3, r4, r5, r6],
               index=['id', 'r1', 'r2', 'r3', 'r4', 'r5','r6'])
            df_result = df_result.append(s2, ignore_index=True)            
    return df_result               

def give_me_guess(n):
    how_many = n
    df = generate_recommemdation(how_many) 
    diff = [19,20,21,22,23,24,25]
    # df = filter_first_sixth_diff_is(df, diff)
    # df = filter_a_plus_b_is_c(df)
    # df = filter_d_minus_c_is_b_minus_a(df)
    qty = 2
    # df = filter_contain_history_ball(df, qty)
    df = sum_is_former_one(df)
    
    print(df)
    return df
    
if __name__ == "__main__":
    increase_history_to_db.main()   
    n = 1                     
    give_me_guess(n)