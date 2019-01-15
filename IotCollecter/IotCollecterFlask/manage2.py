from flask import request, Flask, jsonify
from datetime import datetime, date, timedelta
import time
import pymysql, datetime
import os
import hashlib
from flask_sqlalchemy import SQLAlchemy
from flask import g
app = Flask(__name__)

@app.route("/register", methods=['POST'])
def register():
    # print("connecting")
    # print(request.form.get('username'), request.form.get('pwd'), request.form.get('gender'), request.form.get('age'), request.form.get('phone_model'), request.form.get('cpu_model'),
    # int(request.form.get('memory_size')), float(request.form.get('battery_size')), int(request.form.get('storage_size')))
    db = pymysql.connect("localhost","root","123456","iotcollecter")
    cursor = db.cursor()
    sql = "select * from user where user_name=%s"
    try:
        cursor.execute(sql, request.form.get('username'))
        results = cursor.fetchall()
        # print(results)
        db.commit()
        # print(len(results))
        # print('asd')
        if len(results) == 1:
            # print('555')
            return '2'
        else:
            # print('888')
            #sql0 = "INSERT INTO user(user_name, password, sex, birthday) VALUES (%s, %s, %s, %s)"
            sql1 = "INSERT INTO user(user_name, password, sex, birthday, phone_model, cpu_model, memory_size, battery_size, storage_size) VALUES (%s, %s, %s, %s, %s, %s ,%s, %s, %s)"
            sql2 = "create table runstatusof" + request.form.get('username') + "(id int primary key not null auto_increment, update_time datetime, CPU_ratio float, memory_ratio float, battery_ratio float, storage_ratio float);"
            sql3 = "create table locationof" + request.form.get('username') + "(id int primary key not null auto_increment, update_time datetime, longitude double, latitude double);"
            sql4 = "create table stepof" + request.form.get('username') + "(id int primary key not null auto_increment, update_time datetime, step_sum int, step_today int);"
            sql5 = "create table webof" + request.form.get('username') + "(id int primary key not null auto_increment, url varchar(100), time datetime);"
            sql6 = "create table appof" + request.form.get('username') + "(id int primary key not null auto_increment, pkgname varchar(40), foregroundtime int, launcherCount int);"
            try:
                # print('999')
                # cursor.execute(sql0, (request.form.get('username'), request.form.get('pwd'), request.form.get('gender'), dateToMysql(request.form.get('age'))))
                # print('333')
                cursor.execute(sql1, (request.form.get('username'), request.form.get('pwd'), request.form.get('gender'), dateToMysql(request.form.get('age')),request.form.get('phone_model'),
                 request.form.get('cpu_model'), request.form.get('memory_size'), request.form.get('battery_size'), request.form.get('storage_size')))
                cursor.execute(sql2)
                cursor.execute(sql3)
                cursor.execute(sql4)
                cursor.execute(sql5)
                cursor.execute(sql6)
                db.commit()
                # print ('000')
                return '1'
            except:
                db.rollback()
                return '0'
    except:
        db.rollback()
        return '0'
    db.close()

@app.route('/login', methods=['POST'])
def login():
    db = pymysql.connect("localhost","root","123456","iotcollecter" )
    cursor = db.cursor()
    sql = "select * from user where user_name=%s and password=%s"
    # print(request.form.get('username'))
    # print(request.form.get('pwd'))
    try:
        cursor.execute(sql,(request.form.get('username'),request.form.get('pwd')))
        results = cursor.fetchall()
        # print(len(results))
        if len(results)==1:
            # print('return 1')
            return '1'
        else:
            # print('return 0')
            return '0'
        db.commit()
    except:
        db.rollback()
    db.close()

@app.route('/uploadRunStatus',methods=['POST'])
def uploadRunStatus():
    # print(request.form.get('memory_ratio'))
    # print(request.form.get('user_name'))
    # print(request.form.get('storage_ratio'))
    # print(request.form.get('cpu_ratio'))
    # print(request.form.get('battery_ratio'))
    db = pymysql.connect("localhost","root","123456","iotcollecter" )
    cursor = db.cursor()
    dateMysql = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
    # print(dateMysql)
    sql1 = "select memory_size, storage_size from user where user_name = '" + request.form.get('user_name') + "'"
    try:
        cursor.execute(sql1)
        temp = cursor.fetchall();
        # print(temp)
    except:
        db.rollback()
        return'0'
    # print(temp[0][0])
    # print(temp[0][1])
    memory_ratio = 100 - float(request.form.get('memory_ratio')) / temp[0][0] /10.24
    storage_ratio = 100 - float(request.form.get('storage_ratio')) / temp[0][1] * 100
    # print(memory_ratio)
    # print(storage_ratio)
    sql = "insert into runstatusof" +  request.form.get('user_name') + "(update_time, CPU_ratio, memory_ratio, battery_ratio, storage_ratio) values ('" + dateMysql + "', '" + request.form.get('cpu_ratio') + "', '" + str(memory_ratio) + "', '" + request.form.get('battery_ratio') + "', '" + str(storage_ratio) + "')"
    #sql = "insert into runstatusof%s values (dataMysql, 1, request.form.get('memory_ratio'), 1, 1"
    try:
        # print("111")
        # print(sql)
        cursor.execute(sql)
        db.commit()
        return '3'
    except:
        db.rollback()
        return '0'
    db.close()

@app.route('/uploadLocation',methods=['POST'])
def uploadLocation():
    # print("uploaddddddd")
    # print(request.form.get('lng'))
    # print(request.form.get('lat'))
    # print(request.form.get('user_name'))
    db = pymysql.connect("localhost","root","123456","iotcollecter" )
    cursor = db.cursor()
    date1 = datetime.datetime.now()
    sql1 = "select id,UNIX_TIMESTAMP(update_time) from locationof" +  request.form.get('user_name') + " order by id desc limit 1"
    cursor.execute(sql1)
    r1 = cursor.fetchall()
    dateMysql = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
    # print(dateMysql)
    sql = "insert into locationof" +  request.form.get('user_name') + "(update_time, longitude, latitude) values ('" + dateMysql + "', '" + request.form.get('lng') + "', '" + request.form.get('lat') + "')"
    try:
        cursor.execute(sql)
        db.commit()
        if len(r1) == 1:
            sql2 = "update locationof" + request.form.get('user_name') + " set stay_time = " + str(int(time.mktime(date1.timetuple())) - r1[0][1]) + " where id = " + str(r1[0][0])
            print(sql2)
            cursor.execute(sql2)
            db.commit()
        return '3'
    except:
        db.rollback()
        return '0'
    db.close()

@app.route('/uploadStep',methods=['POST'])
def uploadStep():
    # print(request.form.get('step_sum'))
    # print(request.form.get('step_today'))
    # print(request.form.get('user_name'))
    db = pymysql.connect("localhost","root","123456","iotcollecter" )
    cursor = db.cursor()
    dateMysql = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
    # print(dateMysql)
    today = date.today().strftime("%Y-%m-%d")
    # print(today)
    sql2 = "delete from stepof" + request.form.get('user_name') + " where update_time > '" + today + "'"
    # print(sql2)
    sql = "insert into stepof" +  request.form.get('user_name') + "(update_time, step_sum, step_today) values ('" + dateMysql + "', '" + request.form.get('step_sum') + "', '" + request.form.get('step_today') + "')"
    try:
        cursor.execute(sql2)
        db.commit()
    except:
        db.rollback()
        return '0'
    try:
        print(sql)
        cursor.execute(sql)
        db.commit()
        return '3'
    except:
        db.rollback()
        return '0'
    db.close()

@app.route('/getStepOfYesterday', methods=['POST'])
def getStepOfYesterday():
    db = pymysql.connect("localhost", "root", "123456", "iotcollecter")
    cursor = db.cursor()
    yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
    today = date.today().strftime("%Y-%m-%d")
    # print(yesterday)
    # print(today)
    sql = "select step_sum from stepof" + request.form.get('username') + " where update_time < '" + today + "'" + "order by id desc"
    try:
        print("1114444444444")
        # print(sql)
        cursor.execute(sql)
        i = cursor.fetchall();
        print(i)
        if len(i) != 0:
            print(str(i[0][0]))
            return str(i[0][0])
        else:
            return '0'
    except:
        db.rollback()
        return '0'
    db.close()

@app.route('/getLastUploadtime', methods=['POST'])
def getLastUploadtime():
    db = pymysql.connect("localhost", "root", "123456", "iotcollecter")
    cursor = db.cursor()
    today = date.today().strftime("%Y-%m-%d")
    sql = "select UNIX_TIMESTAMP(update_time) from stepof" + request.form.get('username') + " where update_time < '" + today + "'" + "order by update_time desc limit 1"
    try:
        cursor.execute(sql)
        i = cursor.fetchall();
        if len(i) == 1:
            print(str(i[0][0]))
            return str(i[0][0])
        else:
            return '0'
    except:
        db.rollback()
        return '0'
    db.close()

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



def dateToMysql(originstr):
    return originstr[0:4] + '-' + originstr[4:6] + '-' + originstr[6:8]

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)