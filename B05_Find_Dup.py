#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 19:56:35 2021
B05 用sqlalchemy实现把Universal中的数字合并之后，导入test表中
用于排序，查找重复的行，并删除
@author: zhangjun
"""

import os
import platform
import psycopg2
import configparser

def ping(ip):
    sys_id = platform.system()
    if sys_id == 'Linux':
        ret =os.system('ping -c 1 -W 1 %s'%ip) #每个ip ping 1次，等待时间为1s
    elif sys_id == 'Windows':
        ret =os.system('ping -w 1 %s'%ip) #每个ip ping 1次，等待时间为1s
    elif sys_id == 'Darwin':
        ret =os.system('ping -c 1 -W 1 %s'%ip) #每个ip ping 1次，等待时间为1s
    else:
        print('没有识别到可用的操作系统。')
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

def drop_table_tbltest():
    # conn = link_postgresql_db()
    
    config=configparser.ConfigParser()
    # config.read('/Users/zhangjun/Code/_privateconfig/analysis.cfg')
    
    if ping('192.168.100.20'):
        config_filename = obtain_config_filename()
        config.read(config_filename)
    else:
        print('remote')
        config.read('/Users/zhangjun/Code/_privateconfig/analysis_oray.cfg')

    HOST = config['DB']['IP']
    USER = config['DB']['USER']
    DATABASE = config['DB']['DATABASE']
    PASSWORD = config['DB']['PASSWORD']
    PORT = config['DB']['PORT']
    
    conn = psycopg2.connect(database=DATABASE, user=USER, \
                            password=PASSWORD, host=HOST, port=PORT)

    cur = conn.cursor()
    strsql = "DROP TABLE tbltest;"
    cur.execute(strsql)
    conn.commit()
    conn.close()
    
    print("Droped database successfully")

def create_table_tbltest():
    
    conn = link_postgresql_db()
    
    print("Opened database successfully")
    
    cur = conn.cursor()
    
    strSQL = '''
    create table public.tbltest
	(ID int,
	dupstr char(12))
    '''
    cur.execute(strSQL)
    print("Table created successfully")
    
    conn.commit()
    conn.close()

def insert_data() :
    
    config_filename = obtain_config_filename()
    
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
        __tablename__ = 'tbluniversalset1'  # 表名
        # __abstract__ = True
        id = Column(Integer, primary_key=True)
        r1 = Column(Integer)
        r2 = Column(Integer)
        r3 = Column(Integer)
        r4 = Column(Integer)
        r5 = Column(Integer)
        r6 = Column(Integer)
    
    Base.metadata.create_all()  # 将模型映射到数据库中

# define target 
    Base_string = declarative_base(engine)  # SQLORM基类
    session_string = sessionmaker(engine)()  # 构建session对象
    
    class String(Base_string):
        __tablename__ = 'tbltest'  # 表名
        # __abstract__ = True
        id = Column(Integer, primary_key=True)
        dupstr = Column(String)
    
    Base_string.metadata.create_all() 

# select and insert   
    m, n = 1, 6476089
    item_list = session.query(Record).filter(Record.id >= m, Record.id < n).all()
    # print(item)
    for item in item_list:
        a = item.id
        b = "{:0>2d}{:0>2d}{:0>2d}{:0>2d}{:0>2d}{:0>2d}".format(item.r1, item.r2, item.r3, item.r4, item.r5, item.r6)
        print(a,b)
        string = String(id = a, dupstr = b)
        session_string.add(string)  # 添加到session
    
    # session.commit()
    session_string.commit()

    conn.close()  # 关闭连接
    
if __name__ == "__main__":
    drop_table_tbltest()    
    create_table_tbltest()
    insert_data()