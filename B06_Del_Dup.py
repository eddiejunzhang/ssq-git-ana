#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 21:44:52 2021
B06 delete dup
it takes too long time.
@author: zhangjun
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

def del_data() :
    
    config_file_mac = r"/Users/zhangjun/Code/_privateconfig/analysis.cfg" 
    config_file_win10 = r"D:\Study\PythonCoding\_privateconfig\analysis.cfg" 
    if os.path.isfile(config_file_win10):
        config_filename = config_file_win10
    elif os.path.isfile(config_file_mac):
        config_filename = config_file_mac
    else:
        print('未找到配置文件.')
        
    config = configparser.ConfigParser() 
    print(config_filename)
    config.read(config_filename)
    
    HOST = config['DB']['IP']
    USERNAME = config['DB']['USER']
    DATABASE = config['DB']['DATABASE']
    PASSWORD = config['DB']['PASSWORD']
    PORT = config['DB']['PORT']
    
    # dialect + driver://username:passwor@host:port/database
    DB_URI = f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    
    from sqlalchemy import create_engine
    # from config import DB_URI
    
    engine = create_engine(DB_URI)  # 创建引擎
    conn = engine.connect()  # 连接
    result = conn.execute('SELECT 1')  # 执行SQL
    print(result.fetchone()) 
    
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import create_engine, Column, Integer, String
    from sqlalchemy.orm import sessionmaker

    Base = declarative_base(engine)  # SQLORM基类
    session = sessionmaker(engine)()  # 构建session对象
    
    class Record(Base):
        __tablename__ = 'tbluniversalset'  # 表名
        # __abstract__ = True
        id = Column(Integer, primary_key=True)
        r1 = Column(Integer)
        r2 = Column(Integer)
        r3 = Column(Integer)
        r4 = Column(Integer)
        r5 = Column(Integer)
        r6 = Column(Integer)
    
    Base.metadata.create_all()  # 将模型映射到数据库中
    
    conn1 = link_postgresql_db()
    strSQL = '''
    select id, dupstr
    from public.tbltest t 
    order by t.dupstr 
    '''
    print('start to generate df.')
    df = pd.read_sql(strSQL,conn1)
    print('df is ready. ')
    swap = ''
    count = 0
    for index,row in df.iterrows():
        idnum = row['id']
        a = row['dupstr']
        # print(r['Date'])
        if a == swap:
            print('delete one ', count, idnum)
            count += 1
            session.query(Record).filter(Record.id == idnum).delete()
        else:
            swap = a
            
    session.commt()
    conn.close()
    
if __name__ == "__main__":
    del_data()  