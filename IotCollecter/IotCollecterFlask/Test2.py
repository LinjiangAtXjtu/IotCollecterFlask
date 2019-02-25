import json
import time
from datetime import datetime, date, timedelta

import pymysql
import sqlalchemy;
from flask_sqlalchemy import SQLAlchemy
from flask import request, Flask, jsonify
from flask import g

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:123456@127.0.0.1:3306/iotcollecter'
# 跟踪数据库的修改
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
userdb = SQLAlchemy(app)

class webInfoT(userdb.Model):
    __tablename__ = 'webI'
    id = userdb.Column(userdb.Integer, primary_key=True)  # primary_key会自动填充
    url = userdb.Column(userdb.String(100))
    time = userdb.Column(userdb.String(100))
@app.route('/Record_stroy',methods=['POST'])
def Record_stroy():
    userdb.drop_all()
    userdb.create_all()
    print(request.form.get("url"))
    webI= webInfoT(url=request.form.get("url"), time=request.form.get("time"))
    userdb.session.add(webI)
    userdb.session.commit()

@app.route('/get_user',methods=['POST'])
def get_user():
    g.name=request.form.get("username")
    print(request.form.get("username"))
    return request.form.get("username")

class appInfoT(userdb.Model):
     __tablename__ ='appI';
     id = userdb.Column(userdb.Integer, primary_key=True)
     username = userdb.Column(userdb.String(100))  # primary_key会自动填充
     pkgName = userdb.Column(userdb.String(100))
     foregroundtime = userdb.Column(userdb.String(100))
     launcherCount = userdb.Column(userdb.String(100))

@app.route('/app_Record_stroy',methods=['POST'])
def app_Record_stroy():
    userdb.drop_all()
    userdb.create_all()
    print(request.form.get("pkgName"))
    app=appInfoT( username=request.form.get("username"),pkgName=request.form.get("pkgName"),foregroundtime=request.form.get("foregroundtime"),launcherCount=request.form.get("launcherCount"))
    userdb.session.add(app)
    userdb.session.commit()
    return "aaa"

#
# # db = pymysql.connect("localhost","root","123456","iotcollecter" )
# # # cursor = db.cursor()
# # today = date.today().strftime("%Y-%m-%d")
# # dateMysql = datetime.now();
# # print(dateMysql)
# dateMysql = '2018-12-30 11:11:11'
# timeA = time.strptime(dateMysql, "%Y-%m-%d %H:%M:%S")
# timeStamp = int(time.mktime(timeA))
# print(int(timeStamp/3600/24))
# dateMysql = '2018-12-31 11:11:11'
# timeA = time.strptime(dateMysql, "%Y-%m-%d %H:%M:%S")
# timeStamp = int(time.mktime(timeA))
# print(int(timeStamp/3600/24))
# # sql = "select UNIX_TIMESTAMP(update_time) from stepofcjd order by id desc limit 1"
# # cursor.execute(sql)
# # i = cursor.fetchall();
# # if len(i) == 1:
# #     print(str(i[0][0]))
# # else:
# #     print('0')
# # r1 = cursor.fetchall()
# # print(" set stay_time = " + str(int(time.mktime(dateMysql.timetuple()) - r1[0][1])) + "asdasdad")
# # if len(r1) == 1:
# #     sql2 = "update locationofcjd" + " set stay_time = " + str(int(time.mktime(dateMysql.timetuple()) - r1[0][1])) + " where id = " + strr1[0][0] + ")"
# # print(sql2)1546246320