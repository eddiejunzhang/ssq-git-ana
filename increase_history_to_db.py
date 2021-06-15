# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 14:06:51 2021
inrease latest records into history db.
在服务器中已经创建一个数据表，并把历史数据中未导入的数据导入这个表中。
表名是tblhistory

@author: Eddiezhang
"""

import psycopg2
import configparser
from bs4 import BeautifulSoup
from chp1.advanced_link_crawler import download
import pandas as pd

def get_ssq_record(m,df,LastGameNumber,MarkSeqNum):

    
    url='http://kaijiang.zhcw.com/zhcw/inc/ssq/ssq_wqhg.jsp?pageNum=%d'%m # 2020-10-22改
    html=download(url)

    soup=BeautifulSoup(html,'lxml')
#    soup=BeautifulSoup(html,'html5lib')

    for i in range(2,22):
        if MarkSeqNum > LastGameNumber:
            tr=soup.find_all('tr')[i]
            td=tr.find_all('td')
            row=[td[0].text]
            row.append(td[1].text)
            MarkSeqNum=td[1].text
        
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
    return df, MarkSeqNum
            
def main():
    pass
    # 取得当前数据库中，号数最大的一期期号LastGameNumber
    LastGameNumber = "2021025"
    MarkSeqNum = '2100001' #这个变量存放最后一次取得的期号，用于判断是否是2003001这最后一期
    # df用于存放待导入的数据，它开始是一个空的dataframe
    df = pd.DataFrame(columns=['Date','SeqNum','r1','r2','r3','r4','r5','r6','b','Revenue','1st','2nd'])
    
    for i in range(1,4):
        df, MarkSeqNum = get_ssq_record(i,df,LastGameNumber, MarkSeqNum)
    
    print(df)

if __name__ == "__main__":
    main()