# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 14:06:51 2021
inrease latest records into history db.
在服务器中已经创建一个数据表，并把历史数据中未导入的数据导入这个表中。
表名是tblhistory

@author: Eddiezhang
"""

import os
import platform
import psycopg2
import configparser
from bs4 import BeautifulSoup
from chp1.advanced_link_crawler import download
import pandas as pd
import sqlalchemy
from datetime import datetime

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
    conn = psycopg2.connect(database=DATABASE, user=USER, \
                            password=PASSWORD, host=HOST, port=PORT)
    return conn

def get_ssq_record(m,df,LastGameNumber,MarkSeqNum):

    url='http://kaijiang.zhcw.com/zhcw/inc/ssq/ssq_wqhg.jsp?pageNum=%d'%m # 2020-10-22改
    html=download(url)

    soup=BeautifulSoup(html,'lxml')
#    soup=BeautifulSoup(html,'html5lib')
    latest_seqnumber = ''
    
    for i in range(2,22):
        if MarkSeqNum > LastGameNumber:
            tr=soup.find_all('tr')[i]
            td=tr.find_all('td')
            row=[td[0].text]
            row.append(td[1].text)
            MarkSeqNum=td[1].text

            if i == 2:
                latest_seqnumber = MarkSeqNum
        
            # 这个字段存放中奖球的号码。
            for k in range(0,7):
                em=td[2].find_all('em')[k]
                row.append(em.text)
            
            # print('Revenue: '+ td[3].text)
            row.append(td[3].text)
            strong=td[4].find('strong')
            # print('First Reward: '+strong.text)
            row.append(strong.text)
            # print('Second Reward: '+td[5].text)
            row.append(td[5].text)
            # print('')
    
            # print(row)
            if MarkSeqNum > LastGameNumber:
                new=pd.DataFrame({'Date':row[0],
                      'SeqNum':row[1],
                      'r1':row[2],
                      'r2':row[3],
                      'r3':row[4],
                      'r4':row[5],
                      'r5':row[6],
                      'r6':row[7],
                      'b':row[8],
                      'Revenue':row[9],
                      '1st':row[10],
                     '2nd':row[11]},
                    index=[1])
                df=df.append(new,ignore_index=True) 
    return df, MarkSeqNum, latest_seqnumber

def insert_data_into_db(df):
    
    config_filename = obtain_config_filename()
        
    config = configparser.ConfigParser() 
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
        __tablename__ = 'tblhistory'  # 表名
        id = Column(Integer, primary_key=True, autoincrement=True)
        lottdate = Column(String(50))
        weekday = Column(Integer)
        seqnum = Column(String(50))
        r1 = Column(Integer)
        r2 = Column(Integer)
        r3 = Column(Integer)
        r4 = Column(Integer)
        r5 = Column(Integer)
        r6 = Column(Integer)
        b = Column(Integer)
        diff5step = Column(Integer)
        plusf = Column(Integer)
        minusf = Column(Integer)
    
    Base.metadata.create_all()  # 将模型映射到数据库中

    # session.add_all([
    #     Record(lottdate='2021/1/1', seqnum='16', r1=3, r2=4, r3=5, r4=6, r5=7, r6=8, b=16),
    #     Record(lottdate='2021/1/2', seqnum='17', r1=4, r2=5, r3=5, r4=6, r5=7, r6=8, b=16)
    #     ])
    
    for index, row in df.iterrows():
        value_date = row['Date']
        value_seq = row['SeqNum']
        value_r1 = row['r1']
        value_r2 = row['r2']
        value_r3 = row['r3']
        value_r4 = row['r4']
        value_r5 = row['r5']
        value_r6 = row['r6']
        value_b = row['b']
        value_revenue = row['Revenue']
        value_1st = row['1st']
        value_2nd = row['2nd']
        
        w = datetime.strptime(value_date, '%Y-%m-%d')
        value_weekday = w.weekday()
        
        history_record = Record(lottdate=value_date, 
                                weekday=value_weekday,
                                seqnum=value_seq, 
                                r1=value_r1, 
                                r2=value_r2, 
                                r3=value_r3, 
                                r4=value_r4, 
                                r5=value_r5, 
                                r6=value_r6, 
                                b=value_b)  # 创建一个student对象
        session.add(history_record)  # 添加到session
    
    session.commit()

    conn.close()  # 关闭连接
    
def main():
    pass
    # 取得当前数据库中，号数最大的一期期号LastGameNumber
    with open('latest_recorded.txt', 'r') as f:
        LastGameNumber = f.read()
    # LastGameNumber = "2021077"
    MarkSeqNum = '2100001' #这个变量存放最后一次取得的期号，用于判断是否是2003001这最后一期
    # df用于存放待导入的数据，它开始是一个空的dataframe
    df = pd.DataFrame(columns=['Date','SeqNum','r1','r2','r3','r4','r5','r6','b','Revenue','1st','2nd'])
    
    latest = ''
    for i in range(1,4):
        df, MarkSeqNum, latest_seqnumber = get_ssq_record(i,df,LastGameNumber, MarkSeqNum)
        latest = max(latest_seqnumber,latest)
    
    df = df.sort_values(by='SeqNum',axis=0, ascending=True)
    
    print(df)
    print('The last game is: ',latest )
    
    with open('latest_recorded.txt', 'w') as f:
        f.write(latest)

    insert_data_into_db(df)

if __name__ == "__main__":
    main()