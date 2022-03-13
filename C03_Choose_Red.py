#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 17:15:20 2022
逐一筛选红球。
@author: zhangjun
"""
import os
import sys
config_path_macmini = r"/Users/zhangjun/Code/_privateconfig"
config_path_pi4 = r"/home/pi/Python_Proj/_privateconfig"
if os.path.isdir(config_path_macmini):
    config_path = config_path_macmini
    whose_pc = 'macmini'
elif os.path.isdir(config_path_pi4):
    config_path = config_path_pi4
    whose_pc = 'mpi4'    
    
sys.path.append(config_path)

import platform
import psycopg2
import configparser
import pandas as pd
import constants
from lib01 import write_log

import random


log_file='log.txt'

def guess_red(list_guess,
              previous1round_list,
              previous2round_list):
    temp = []
    for red in list_guess:
        a = in_last_round(red,previous1round_list)
        b = last_round_neighbour(red,previous1round_list)
        c = is_lean_3(red,previous1round_list,previous2round_list)
        point = a * b * c
        if random.random() * point > 0.33:
            temp.append(red)
    print(len(temp))
    return temp

def is_lean_3(ball,previous1round_list,previous2round_list):
    # 倾斜3的分数。例如前两期中出了5和4，那么这一期中出3的可能性比较大
    point = constants.Lean3Point
    
    if ball+1 in previous1round_list and ball+2 in previous2round_list or ball-1 in previous1round_list and ball-2 in previous2round_list:
        return point
    else:
        return 1

def last_round_neighbour(ball,previous1round_list):
    # 上一期出现过的号码，相邻的号码在本期出现的可能性比较大
    point = constants.LastRoundNeighbour
    
    last_round = previous1round_list
    if ball+1 in last_round or ball-1 in last_round:
        return point
    else:
        return 1
    
def in_last_round(ball,previous1round_list):
    # 上一期出现过的号码，再次出现的可能性比较大
    point = constants.InLastRoundPoint
    
    last_round = previous1round_list
    if ball in last_round:
        return point
    else:
        return 1

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
    
def main(threshod):
    conn = link_postgresql_db()
    # 需要得到前三期的红球号数
    previous1round_list = []
    previous2round_list = []
    previous3round_list = []
    
    strSQL = '''
    SELECT id,r1,r2,r3,r4,r5,r6 
    FROM public.tblhistory
    ORDER BY id desc
    limit 3
    '''
    # print('start to generate df.')
    df = pd.read_sql(strSQL, conn)
    
    for i in range(6):
        previous1round_list.append(df.iat[0,i+1])
        previous2round_list.append(df.iat[1,i+1])
        previous3round_list.append(df.iat[2,i+1])
        
    list_guess = []
    for i in range(33):
        list_guess.append(i+1)
    while len(list_guess) > threshod:
        list_guess = guess_red(list_guess,
                               previous1round_list,
                               previous2round_list)
    print(list_guess)
    
    fp = open('Suggested_Red.txt','w')
    fp.write(
     "根据以往经验，推荐红球如下："+'\n'
     )
    for i in range(len(list_guess)-1):
        fp.write(str(list_guess[i]))
        fp.write(",")
    fp.write(str(list_guess[-1]))
        
    # text = ','.join(list_guess)
    # fp.write(text)
    
    fp.write("\n")
    fp.close()

if __name__ == "__main__":
    write_log(log_file, '开始计算。')
    # 需要几个红球作为推荐？
    threshod = 9
    main(threshod)
    write_log(log_file, '结束计算。')