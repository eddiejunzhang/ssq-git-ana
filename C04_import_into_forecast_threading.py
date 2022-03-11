#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 13:06:49 2022
C02，把一定范围的数据放入预测表中
在这个程序中还要把每一条数据的属性值计算出来保存在预测表中
C04是把C02变成多线程的
@author: zhangjun
"""

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
import threading
import constants
from lib01 import write_log

log_file='log.txt'

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

def a(attn):
    
    sumgroup1min=constants.SumGroup1Min
    sumgroup1max=constants.SumGroup1Max
    
    sum = 0
    for i in range(6):
        sum += attn[i]
    # print(sum)
    if sum >= sumgroup1min and sum <= sumgroup1max:
        return 'True'
    else:
        return 'False'

def b(attn):
    
    sumgroup2min=constants.SumGroup2Min
    sumgroup2max=constants.SumGroup2Max
    
    sum = 0
    for i in range(6):
        sum += attn[i]
    # print(sum)
    if sum >= sumgroup2min and sum <= sumgroup2max:
        return 'True'
    else:
        return 'False'
    
def c(attn):
    
    sumgroup3min=constants.SumGroup3Min
    sumgroup3max=constants.SumGroup3Max
    
    sum = 0
    for i in range(6):
        sum += attn[i]
    # print(sum)
    if sum >= sumgroup3min and sum <= sumgroup3max:
        return 'True'
    else:
        return 'False'

def d(attn):
    # r2-r1=r4-r3
    r1 = attn[0]
    r2 = attn[1]
    r3 = attn[2]
    r4 = attn[3]
    r5 = attn[4]
    r6 = attn[5]
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
            if a == b and a >=1:
                mark_minus += 1
                    
    if mark_minus > 0:
        return 'True'
    else:
        return 'False'

def e(attn):
# r1+r2=r3
    # 以下的mark是关于是否存在和值的mark
    mark = 0
    for i in range(0,4):
        a = attn[i]
        for j in range(1,5):
            b = attn[j]
            for k in range(2,6):
                c = attn[k]
                if a + b == c:
                    mark += 1
                    
    if mark > 0:
        return 'True'
    else:
        return 'False'

def f(attn):
# 包含我主观猜的号码1
    list_possilbe = constants.PossibleRedBall1
    mark = False
    for i in attn:
        for j in list_possilbe:
            if i == j:
                mark = mark or True
    if mark:
        return 'True'
    else:
        return 'False'

def g(attn):
# 包含我主观猜的号码2
    list_possilbe = constants.PossibleRedBall2
    mark = False
    for i in attn:
        for j in list_possilbe:
            if i == j:
                mark = mark or True
    if mark:
        return 'True'
    else:
        return 'False'
    
def h(attn):
# r6-r1 is in a range
    list_differencyrange = constants.DifferencyRange
    mark = False
    r1 = attn[0]
    r6 = attn[5]

    for j in list_differencyrange:
        if r6-r1 == j:
            mark = mark or True
    if mark:
        return 'True'
    else:
        return 'False'

def i(attn,df_latest_history):
    # 用这组号码，与过去100次中出的号码进行对比，如果有雷同数量为1的介手43和60之间，且有雷同数量为3的介于2和8之间，则标i 为TRUE
    semblance_list = []
    for index, row in df_latest_history.iterrows():
        count = 0
        for i in range(6):
            for ball in attn:
                if ball == row[i+1]:
                    count += 1
        semblance_list.append(count)            
    
    if semblance_list.count(1) >= 43 and semblance_list.count(1) <=60 \
        and semblance_list.count(3) >= 2 and semblance_list.count(3) <= 8:
        return 'True'
    else:
        return 'False'
    
def test_semblance_with_history(attn,previous_near,conn):
    strSQL = '''
    select id,r1,r2,r3,r4,r5,r6 
    from public.tblhistory 
    where id <= %d
    order by id desc 
    limit 100
    '''%previous_near
    df = pd.read_sql(strSQL, conn)
    # print(df)
    
    semblance_list = []
    for index, row in df.iterrows():
        count = 0
        for i in range(6):
            for ball in attn:
                if ball == row[i+1]:
                    # print(ball)
                    count += 1
        semblance_list.append(count)            
    # print(semblance_list)            
    
    # print(semblance_list.count(0))    
    # print(semblance_list.count(1)) 
    # print(semblance_list.count(2)) 
    # print(semblance_list.count(3)) 
    
    if semblance_list.count(1) >= 43 and semblance_list.count(1) <=60 \
        and semblance_list.count(3) >= 2 and semblance_list.count(3) <= 8:
        return True
    else:
        return False

def main_section(s1, s2):
    conn = link_postgresql_db()
    cur = conn.cursor()
    minT = s1
    maxT = s2
    
    strSQL = '''
    SELECT id,r1,r2,r3,r4,r5,r6 
    FROM public.tbluniversalset
    WHERE id >= %d AND id <= %d
    ORDER BY id
    '''%(minT,maxT)
    print('start to generate df.')
    df = pd.read_sql(strSQL, conn)
    # print(df)
    
    # 为i测试而准备数据集
    strSQL = '''
    select id,r1,r2,r3,r4,r5,r6 
    from public.tblhistory 
    order by id desc 
    limit 100
    '''
    df_latest_history = pd.read_sql(strSQL, conn)
    # print(df)
    
    if not df.empty:
        for index, row in df.iterrows():
            print(row['id'])
            r1 = row['r1']
            r2 = row['r2']
            r3 = row['r3']
            r4 = row['r4']
            r5 = row['r5']
            r6 = row['r6']
            attn = [r1,r2,r3,r4,r5,r6]
            # print(attn)
            # print(f(attn))
            strSQL = '''
            INSERT INTO public.tblforecast (r1,r2,r3,r4,r5,r6,
                                            a,
                                            b,
                                            c,
                                            d,
                                            e,
                                            f,
                                            g,
                                            h,
                                            i)
            values(%d,%d,%d,%d,%d,%d,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''%(r1,r2,r3,r4,r5,r6,
            a(attn),
            b(attn),
            c(attn),
            d(attn),
            e(attn),
            f(attn),
            g(attn),
            h(attn),
            i(attn,df_latest_history))
            # print(strSQL)
            cur.execute(strSQL)    

    conn.commit()
    conn.close()
    
def main():
    conn = link_postgresql_db()
    
    minT=constants.MinT
    maxT=constants.MaxT
    
    strSQL = '''
        SELECT min(id), max(id)
        FROM public.tbluniversalset
        '''
    df = pd.read_sql(strSQL, conn)
    
    if minT == 'min' or minT == 'Min':
        minT = df.iat[0,0]
    if maxT == 'max' or maxT == 'Max' or maxT > df.iat[0,1]:
        maxT = df.iat[0,1]
    
    conn.commit()
    conn.close()
    return minT, maxT

minT,maxT=main()
l = int((maxT-minT)/3)
s1 = minT
s2 = s1+l
s3 = s2+l
s4 = maxT

# 数据数据库为PG，计算机为MacMini,3线程最好
threads = []
t1 = threading.Thread(target=main_section, args=(s1,s2))
threads.append(t1)
t2 = threading.Thread(target=main_section, args=(s2,s3))
threads.append(t2)
t3 = threading.Thread(target=main_section, args=(s3,s4))
threads.append(t3)
    
if __name__ == "__main__":
    write_log(log_file, '开始计算。')
    for t in threads:
        t.setDaemon(True)
        t.start()
        
    for t in threads:
        t.join()
    
    write_log(log_file, '结束计算。')