# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 15:51:48 2020
在服务器中创建一个空白表，并把历史数据CSV文件中的数据导入这个表中。
首先要在数据库中把这个表删除
表名是tblhistory
进而填写出5阶差分的值，看看规律
@author: Eddiezhang
"""
import psycopg2
import configparser

# 查找0～255的地址
def ping(ip):
    import os
    # ret =os.system('ping -c 1 -w 1 %s'%ip) #每个ip ping 1次，等待时间为1s
    ret =os.system('ping -w 1 %s'%ip) #每个ip ping 1次，等待时间为1s
    if ret:
        print('ping %s is fail'%ip)
        return(False)
    else:
        print('ping %s is ok'%ip)
        return(True)
    
def link_postgresql_db():
    config=configparser.ConfigParser()
    if ping('192.168.100.20'):
        config.read('analysis.cfg')
    else:
        config.read('analysis_oray.cfg')
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
    
def drop_table_tblhistory():
    # conn = link_postgresql_db()
    
    config=configparser.ConfigParser()
    if ping('192.168.100.20'):
        config.read('analysis.cfg')
    else:
        print('remote')
        config.read('analysis_oray.cfg')

    HOST = config['DB']['IP']
    USER = config['DB']['USER']
    DATABASE = config['DB']['DATABASE']
    PASSWORD = config['DB']['PASSWORD']
    PORT = config['DB']['PORT']
    
    conn = psycopg2.connect(database=DATABASE, user=USER, \
                            password=PASSWORD, host=HOST, port=PORT)

    cur = conn.cursor()
    strsql = "DROP TABLE tblhistory;"
    cur.execute(strsql)
    conn.commit()
    conn.close()
    
    print("Droped database successfully")

def create_table_tblhistory():
    
    # import psycopg2
    # import configparser
    
    # config=configparser.ConfigParser()
    # config.read('analysis.cfg')
    # HOST = config['DB']['IP']
    # USER = config['DB']['USER']
    # DATABASE = config['DB']['DATABASE']
    # PASSWORD = config['DB']['PASSWORD']
    # PORT = config['DB']['PORT']
    
    # conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    conn = link_postgresql_db()
    
    print("Opened database successfully")
    
    cur = conn.cursor()
    
    cur.execute('''CREATE TABLE tblhistory
           (id SERIAL PRIMARY KEY     NOT NULL,
            lottdate        TEXT   NOT NULL,
            weekday     INT,
            seqnum      TEXT   NOT NULL,
           r1           INT    NOT NULL,
           r2           INT    NOT NULL,
           r3           INT    NOT NULL,
           r4           INT    NOT NULL,
           r5           INT    NOT NULL,
           r6           INT    NOT NULL,
           b           INT    NOT NULL,
           diff5step   INT,
           plusf       INT,
           minusf      INT);''')
    print("Table created successfully")
    
    conn.commit()
    conn.close()

def import_data_into_db():
    # import psycopg2
    # import configparser
    import pandas as pd
    from datetime import datetime
    
    # config=configparser.ConfigParser()
    # config.read('analysis.cfg')
    # HOST = config['DB']['IP']
    # USER = config['DB']['USER']
    # DATABASE = config['DB']['DATABASE']
    # PASSWORD = config['DB']['PASSWORD']
    # PORT = config['DB']['PORT']
    
    # conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    conn = link_postgresql_db()
    cur = conn.cursor()
    print("Opened database successfully")
    
    filename = r"ssqhistory.csv"
    
    df = pd.read_csv(filename)
    # print(df)
    for i,r in df.iterrows():
        # print(r['Date'])
        w = datetime.strptime(r['Date'], '%Y-%m-%d')
        weekday = w.weekday()
        # print(weekday)
        r1 = r['r1']
        r2 = r['r2']
        r3 = r['r3']
        r4 = r['r4']
        r5 = r['r5']
        r6 = r['r6']
        b = r['b']
                
        e1 = r6 - 5 * r5 + 10 * r4 - 10 * r3 + 5 * r2 - r1
        
        strSQL = "INSERT INTO tblhistory \
            (lottdate, weekday, seqnum, r1, r2, r3, r4, r5, r6, b, diff5step) \
            VALUES ('%s',%d,'%s',%d,%d,%d,%d,%d,%d,%d,%d)"%(r['Date'],weekday, r['SeqNum'],r1,r2,r3,r4,r5,r6,b,e1)
        # print(strSQL)
        cur.execute(strSQL)
    conn.commit()
    conn.close()

def mark_have_plus_feature():
    import psycopg2
    import configparser
    
    config=configparser.ConfigParser()
    config.read('analysis.cfg')
    HOST = config['DB']['IP']
    USER = config['DB']['USER']
    DATABASE = config['DB']['DATABASE']
    PASSWORD = config['DB']['PASSWORD']
    PORT = config['DB']['PORT']
    
    conn = psycopg2.connect(database=DATABASE, user=USER, \
                            password=PASSWORD, host=HOST, port=PORT)
    cur = conn.cursor()
    print("Opened database successfully")
    
    strSQL = r"SELECT id, R1, R2, R3, R4, R5, R6 from tblhistory"
    cur.execute(strSQL)
    
    rows = cur.fetchall()
    for row in rows:
        
        idd = row[0]
        # r1 = row[1]
        # r2 = row[2]
        # r3 = row[3]
        # r4 = row[4]
        # r5 = row[5]
        # r6 = row[6]
        mark = 0
           
        for i in range(1,4):
            a = row[i]
            for j in range(2,5):
                b = row[j]
                for k in range(3,6):
                    c = row[k]
                    if a + b == c:
                        mark += 1
                        print(mark)
        strSQL = "UPDATE tblhistory \
SET plusf = %d \
WHERE id = %d;"%(mark, idd)
        # print(strSQL)
        cur.execute(strSQL)
    conn.commit()
    conn.close()

def mark_have_minus_feature():
    # import psycopg2
    # import configparser
    
    # config=configparser.ConfigParser()
    # config.read('analysis.cfg')
    # # config.read('analysis_oray.cfg')
    # HOST = config['DB']['IP']
    # USER = config['DB']['USER']
    # DATABASE = config['DB']['DATABASE']
    # PASSWORD = config['DB']['PASSWORD']
    # PORT = config['DB']['PORT']
    
    # conn = psycopg2.connect(database=DATABASE, user=USER, \
    #                         password=PASSWORD, host=HOST, port=PORT)
    conn = link_postgresql_db()
    cur = conn.cursor()
    print("Opened database successfully")
    
    strSQL = r"SELECT id, R1, R2, R3, R4, R5, R6 from tblhistory"
    cur.execute(strSQL)
    
    rows = cur.fetchall()
    for row in rows:
        
        idd = row[0]
        r1 = row[1]
        r2 = row[2]
        r3 = row[3]
        r4 = row[4]
        r5 = row[5]
        r6 = row[6]
        print(idd,r1,r2)
        
        mark = 0
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
                if a == b:
                    mark += 1
                    # print(mark)
        strSQL = "UPDATE tblhistory \
SET minusf = %d \
WHERE id = %d;"%(mark, idd)
        # print(strSQL)
        cur.execute(strSQL)
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    drop_table_tblhistory()
    create_table_tblhistory()
    import_data_into_db()
    # mark_have_plus_feature()
    # mark_have_minus_feature()