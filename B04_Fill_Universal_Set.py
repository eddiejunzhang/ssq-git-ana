#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 16:52:46 2021
B04 根据B02填写的控制表，向近似表中填写数据。
@author: zhangjun
"""
import psycopg2
import configparser

def ping(ip):
    import os
    ret = os.system('ping -c -W 1 %s'%ip) #每个ip ping 1次，等待时间为1s
    if ret:
        print('ping %s is fail'%ip)
        return(False)
    else:
        print('ping %s is ok'%ip)
        return(True)


def main():
    config=configparser.ConfigParser()
    if ping('192.168.100.20'):
        config.read('/Users/zhangjun/Code/_privateconfig/analysis.cfg')
    else:
        config.read('/Users/zhangjun/Code/_privateconfig/analysis_oray.cfg')
    HOST = config['DB']['IP']
    USER = config['DB']['USER']
    DATABASE = config['DB']['DATABASE']
    PASSWORD = config['DB']['PASSWORD']
    PORT = config['DB']['PORT']
    # r1min = config['Range']['R1Min']
    # r1max = config['Range']['R1Max']
    # r2min = config['Range']['R2Min']
    # r2max = config['Range']['R2Max']
    # r3min = config['Range']['R3Min']
    # r3max = config['Range']['R3Max']
    # r4min = config['Range']['R4Min']
    # r4max = config['Range']['R4Max']
    # r5min = config['Range']['R5Min']
    # r5max = config['Range']['R5Max']
    # r6min = config['Range']['R6Min']
    # r6max = config['Range']['R6Max']
    # print('r1 min = %s, r6 max = %s'%(r1min, r6max))
          
    conn = psycopg2.connect(database = DATABASE, user = USER,\
                          password = PASSWORD, host = HOST, port = PORT)
        
    print("Opened database successfully")
    
    cur = conn.cursor()
                
    for i in range(int(r1min), int(r1max) + 1):
        for j in range(int(r2min), int(r2max) + 1):
            for k in range(int(r3min), int(r3max) + 1):
                for l in range(int(r4min), int(r4max) + 1):
                    for m in range(int(r5min), int(r5max) + 1):
                        for n in range(int(r6min), int(r6max) + 1):
                            if i<j and j<k and k<l and l<m and m<n:

                                cur.execute("INSERT INTO ？？？ (R1,R2,R3,R4,R5,R6) \
                                        VALUES ( " + str(i) +", " + str(j) + ", " + str(k) + ", " + str(l) + ", " + str(m) + ", " + str(n) + ")");
                print('i = ',i, 'j = ',j, 'k = ',k)
    conn.commit()
    print("Records created successfully")
    conn.close()
    
if __name__ == "__main__":
    main()