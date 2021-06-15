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