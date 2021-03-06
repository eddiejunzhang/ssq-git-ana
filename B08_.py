#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 18:31:25 2021
B07 在B07的基础上，看看猜多少个能够中奖
@author: zhangjun
"""

from B07_Recommend import give_me_guess

def main():
    award ="040710141626"
    count = 0
    times = 1000
    n = 10000
    for j in range(times):
        df = give_me_guess(n)
        if not df.empty:
            for index,row in df.iterrows():
                idnum = row['id']
                r6 = int(row['r6'])
                r5 = int(row['r5'])
                r4 = int(row['r4'])
                r3 = int(row['r3'])
                r2 = int(row['r2'])
                r1 = int(row['r1'])
                string = "{:0>2d}{:0>2d}{:0>2d}{:0>2d}{:0>2d}{:0>2d}".format(r1,r2,r3,r4,r5,r6)
                
                count += 1
                print(j,count)
                if award == string:
                    print(count,idnum,'=======================')
                    print(string)
                    break
                
    
if __name__ == "__main__":
    main()