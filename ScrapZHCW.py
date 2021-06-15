# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 22:39:26 2018
Scrap the data of SSQ lotto from www.zhcw.com
@author: Eddie
"""

from bs4 import BeautifulSoup
from chp1.advanced_link_crawler import download
import csv

MarkSeqNum='2100001' #这个变量存放最后一次取得的期号，用于判断是否是2003001这最后一期
csvfile=open('ssqhistory.csv','w',newline='')
writer=csv.writer(csvfile)
#写表头
writer.writerow(['Date','SeqNum','r1','r2','r3','r4','r5','r6','b','Revenue','1st','2nd'])

for m in range(1,136):
    # url='http://kaijiang.zhcw.com/zhcw/html/ssq/list_'+str(m)+'.html'
    url='http://kaijiang.zhcw.com/zhcw/inc/ssq/ssq_wqhg.jsp?pageNum=%d'%m # 2020-10-22改
    html=download(url)

    soup=BeautifulSoup(html,'lxml')
#    soup=BeautifulSoup(html,'html5lib')

    for i in range(2,22):
        if MarkSeqNum > '2003001':
            tr=soup.find_all('tr')[i]
#            print(tr)
            td=tr.find_all('td')
            print('Date: ' + td[0].text)
            #row这个数组是要写入csv文件的
            row=[td[0].text]
            print('SeqNum: '+ td[1].text)
            row.append(td[1].text)
            MarkSeqNum=td[1].text
        
            # 这个字段存放中奖球的号码。
            ball='' 
            for k in range(0,7):
                em=td[2].find_all('em')[k]
                ball=ball +' ' +em.text
                row.append(em.text)
            print(ball)
            
            print('Revenue: '+ td[3].text)
            row.append(td[3].text)
            strong=td[4].find('strong')
            print('First Reward: '+strong.text)
            row.append(strong.text)
    #        print('First Reward: '+td[4].text.strip())
    #        row.append(td[4].text.strip())
            print('Second Reward: '+td[5].text)
            row.append(td[5].text)
            print('')
                
            #在csv文件中写入
            writer.writerow(row)
    
csvfile.close()