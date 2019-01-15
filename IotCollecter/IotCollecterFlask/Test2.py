import json
import time
from datetime import datetime, date, timedelta

import pymysql

# db = pymysql.connect("localhost","root","123456","iotcollecter" )
# # cursor = db.cursor()
# today = date.today().strftime("%Y-%m-%d")
# dateMysql = datetime.now();
# print(dateMysql)
dateMysql = '2018-12-30 11:11:11'
timeA = time.strptime(dateMysql, "%Y-%m-%d %H:%M:%S")
timeStamp = int(time.mktime(timeA))
print(int(timeStamp/3600/24))
dateMysql = '2018-12-31 11:11:11'
timeA = time.strptime(dateMysql, "%Y-%m-%d %H:%M:%S")
timeStamp = int(time.mktime(timeA))
print(int(timeStamp/3600/24))
# sql = "select UNIX_TIMESTAMP(update_time) from stepofcjd order by id desc limit 1"
# cursor.execute(sql)
# i = cursor.fetchall();
# if len(i) == 1:
#     print(str(i[0][0]))
# else:
#     print('0')
# r1 = cursor.fetchall()
# print(" set stay_time = " + str(int(time.mktime(dateMysql.timetuple()) - r1[0][1])) + "asdasdad")
# if len(r1) == 1:
#     sql2 = "update locationofcjd" + " set stay_time = " + str(int(time.mktime(dateMysql.timetuple()) - r1[0][1])) + " where id = " + strr1[0][0] + ")"
# print(sql2)1546246320