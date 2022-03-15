#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 16:53:30 2022
C06 把几个操作串起来，做成计划任务
@author: zhangjun
"""


import increase_history_to_db
import C01_Creat_Guess_Table
import C03_Choose_Red
# import C04_import_into_fcst_th_adv
import C02_import_into_forecast
import schedule
import time
import os

def compute():
    increase_history_to_db.main()

    # 重建预测表
    table_name = 'tblforecast'
    C01_Creat_Guess_Table.drop_table(table_name)
    C01_Creat_Guess_Table.create_table(table_name)

    # 推荐11个红球
    threshod = 11
    C03_Choose_Red.main(threshod)
    # 计算的结果保存在文件Suggested_Red.txt中
    # 把这个结果放入constants.py中
    filename ='Suggested_Red.txt'
    with open(filename,'r') as f:
        a = f.readline()
        a = f.readline()

    filename = 'constants.py'
    temp = 'temp'
    with open(filename, encoding='utf-8') as fr, open(temp,'w', encoding='utf-8') as fw:
        for line in fr:
            if 'PossibleRedBall1=' in line:
                new_line = 'PossibleRedBall1=%s'%a
            else:
                new_line = line
            fw.write(new_line)
    os.remove(filename)
    os.rename(temp,filename)

    # C04_import_into_fcst_th_adv.run_multi_thread()
    C02_import_into_forecast.main()

schedule.every().monday.at("00:01").do(compute)
schedule.every().wednesday.at("00:01").do(compute)
schedule.every().friday.at("00:01").do(compute)
# schedule.every().sunday.at("20:56").do(compute)

while True:
    schedule.run_pending()
    time.sleep(1)

# compute()